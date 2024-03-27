import { defineStore } from 'pinia';
import { EditMode } from '~/types/editMode';
import { generateElementID, type AnyElement, type BaseElement, type BlockElement, type ElementID, type TextElement, ElementType, createBlockElement, createTextElement } from '~/types/elements';
import type { Project, ProjectID } from '~/types/project';
import { SocketCommand, type AnySocketMessage, type CreateSocketMessage, type UpdateSocketMessage, type DeleteSocketMessage } from '~/types/socket';

const referencePromise = <T>() => {
    // https://stackoverflow.com/questions/63205154/is-it-possible-to-resolve-a-promise-by-user-action-or-manually-managed-triggers
    let resolve = undefined as undefined | ((value: T) => void);
    const promise = new Promise<T>(r => { resolve = r });

    return {
        done: (value: T) => resolve!(value),
        promise,
    };
};

const timeout = (ms: number) => {
    return new Promise(resolve => setTimeout(resolve, ms));
};

const shallowEqual = (object1: { [key: string]: any }, object2: { [key: string]: any }) => {
    const keys1 = Object.keys(object1);
    const keys2 = Object.keys(object2);
    if (keys1.length !== keys2.length) return false;
    for (const key of keys1)
        if (object1[key] !== object2[key]) return false;
    return true;
}

type WebSocketExtended = WebSocket & { sendBuffered: (updateMessage: UpdateSocketMessage) => void };

export const useCurrentProjectStore = defineStore('currentProject', () => {
    const projectID = ref<ProjectID | null>(null);
    const elements = ref<AnyElement[]>([]);
    const selectedElements = ref<AnyElement[]>([]);
    const currentMode = ref<EditMode>(EditMode.Move);

    //
    // Sockets
    //

    const { done: initialDone, promise: socketPromise } = referencePromise<WebSocketExtended>();
    const socketDone = ref(initialDone);
    const socket = ref(socketPromise);

    const loadProject = (projectID: ProjectID) => {
        // https://stackoverflow.com/questions/10406930/how-to-construct-a-websocket-uri-relative-to-the-page-uri
        const newSocket = new WebSocket(
            `${(window.location.protocol === "https:") ? "wss://" : "ws://"}` +
            `${window.location.host}` +
            `/ws/projects/${projectID}/content`
        ) as WebSocketExtended;

        const updatesBuffer: UpdateSocketMessage[] = [];
        const syncBuffer: { [key: string]: any }[] = [];

        const interval = setInterval(
            () => {
                if (newSocket.readyState === WebSocket.OPEN) {
                    for (const message of updatesBuffer) {
                        const command = message.command;
                        delete (message as any).command;
                        // first of all, save my ram,
                        // second of all, that's too much latency (100ms * 100 = 10 seconds)
                        if (syncBuffer.length < 100) syncBuffer.push(message);
                        newSocket.send(`${command} ${JSON.stringify(message)}`);
                    }
                    updatesBuffer.length = 0;
                }
            },
            100,
        );

        newSocket.sendBuffered = (updateMessage: UpdateSocketMessage) => {
            let foundAny = false;
            for (const message of updatesBuffer)
                if (message.id === updateMessage.id) {
                    for (const [key, value] of Object.entries(updateMessage))
                        message[key] = value;
                    foundAny = true;
                    break;
                }
            if (!foundAny) updatesBuffer.push(updateMessage);
        };

        newSocket.onopen = async () => {
            const currentSocket = await Promise.race([
                socket.value,
                Promise.resolve(null),
            ]);

            if (currentSocket !== null && currentSocket !== newSocket) {
                newSocket.close();
                return;
            }

            socketDone.value(newSocket);
        };

        newSocket.onmessage = async event => {
            const currentSocket = await Promise.race([
                socket.value,
                Promise.resolve(null),
            ]);

            if (currentSocket !== newSocket) return;

            const message = event.data as string;

            // first connect message
            if (message.startsWith('[')) {
                elements.value = [];
                for (const el of JSON.parse(message)) {
                    let element = {} as { [key: string]: any };

                    switch (el.type) {
                        case ElementType.Block:
                            element = createBlockElement(el.id, el.name);
                            break;
                        case ElementType.Text:
                            element = createTextElement(el.id, el.name);
                            break;
                    }

                    for (const [key, value] of Object.entries(el)) {
                        // FIXME i smell security problems here
                        element[key] = value;
                    }

                    elements.value.push(element as any);
                }
                return;
            }

            const commandPos = message.indexOf('{');

            const command = message.slice(0, commandPos).trim();
            const data = JSON.parse(message.slice(commandPos));
            // FIXME check if successful parse

            const id = data.id; // FIXME check if there is data.id

            const updateItem = (element: { [key: string]: any }) => {
                for (const [key, value] of Object.entries(data)) {
                    // FIXME i smell security problems here
                    element[key] = value;
                }
            };

            // this block does not cause new messages (which would be pain)
            let el = undefined;
            switch (command) {
                case SocketCommand.Create:
                    if (elements.value.find(e => e.id === id)) return;
                    switch (data.type) {
                        case ElementType.Block:
                            el = createBlockElement(id, data.name);
                            break;
                        case ElementType.Text:
                            el = createTextElement(id, data.name);
                            break;
                    }
                    if (el === undefined) return;
                    elements.value.push(el);
                    updateItem(el);
                    break;
                case SocketCommand.Update:
                    if (syncBuffer.length > 0)
                        if (shallowEqual(syncBuffer[0], data)) {
                            // matching buffer,
                            // remove first element from the buffer and do not do any local changes
                            syncBuffer.shift();
                            return;
                        } else if (syncBuffer[0].id === id && Object.keys(syncBuffer[0]).some(key => key in data))
                            // not matching buffer,
                            // someone else changed what's buffered or the changes order is different,
                            // drop buffer and accept changes
                            syncBuffer.length = 0;

                    el = findElement(id);
                    if (el === undefined) return;
                    updateItem(el);

                    el = selectedElements.value.find(e => e.id === id);
                    updateItem(el as any);

                    break;
                case SocketCommand.Delete:
                    elements.value = elements.value.filter(e => e.id !== id);
                    selectedElements.value = selectedElements.value.filter(e => e.id !== id);
                    break;
            }
        };

        newSocket.onclose = async event => {
            clearInterval(interval);

            if (event.wasClean && event.code === 1000) return;

            await timeout(1000);

            const currentSocket = await Promise.race([
                socket.value,
                Promise.resolve(null),
            ]);

            if (currentSocket !== newSocket) return;

            const { done, promise } = referencePromise<WebSocketExtended>();
            socketDone.value = done;
            socket.value = promise;

            loadProject(projectID);
        }
    };

    /**
     * Send a command message to the socket.
     * 
     * Will `await` for a successful connection to occur before sending.
     * 
     * @param message Message to send.
     */
    async function sendSocketMessage(message: AnySocketMessage) {
        const connected = await socket.value;
        if (message.command === SocketCommand.Update) {
            connected.sendBuffered(message);
            return;
        }

        const command = message.command;
        delete (message as any).command;
        connected.send(`${command} ${JSON.stringify(message)}`);
    };

    watch(projectID, async projectID => {
        const currentSocket = await Promise.race([
            socket.value,
            Promise.resolve(null),
        ]);

        if (currentSocket !== null) {
            currentSocket.close();

            const { done, promise } = referencePromise<WebSocketExtended>();
            socketDone.value = done;
            socket.value = promise;
        }

        if (projectID !== null)
            loadProject(projectID);
    });

    //
    // Project
    //

    watch(projectID, projectID => {
        if (projectID !== null) return;

        elements.value = [];
        selectedElements.value = [];
        currentMode.value = EditMode.Move;
    });

    const generateName = (type: ElementType): string =>
        `${type === ElementType.Block ? 'Блок' : 'Текст'} ` + // TODO i18n?
        `${elements.value.filter(e => e.type === type).length + 1}`;

    const findElement = <E extends BaseElement>(id: ElementID, type?: E['type']): E | undefined =>
        elements.value.find(e => e.id === id && (type === undefined || e.type === type)) as E;

    async function addBlock(edit?: (el: BlockElement) => void): Promise<BlockElement> {
        const el = createBlockElement(generateElementID(), generateName(ElementType.Block));
        const def = { ...el } as BlockElement;
        if (edit !== undefined) edit(el);
        elements.value.push(el);

        await sendSocketMessage({
            command: SocketCommand.Create,
            id: el.id,
            type: ElementType.Block,
            name: el.name,
        } as CreateSocketMessage);

        if (edit !== undefined) {
            await updateElement(
                el,
                ...([...Object.keys(def), ...Object.keys(el)] as (keyof BlockElement)[])
                    .filter((value, index, array) => array.indexOf(value) === index)
                    .filter(key => el[key] !== def[key])
            );
        }

        return el;
    };

    async function addText(edit?: (el: TextElement) => void): Promise<TextElement> {
        const el = createTextElement(generateElementID(), generateName(ElementType.Text));
        if (edit !== undefined) edit(el);
        elements.value.push(el);

        await sendSocketMessage({
            command: SocketCommand.Create,
            id: el.id,
            type: ElementType.Text,
            name: el.name,
        } as CreateSocketMessage);

        return el;
    };

    async function removeElement(id: ElementID) {
        const pre = elements.value;
        elements.value = elements.value.filter(e => e.id !== id);
        if (pre.length === elements.value.length) return;

        await sendSocketMessage({
            command: SocketCommand.Delete,
            id,
        } as DeleteSocketMessage);

        // Backend will cascade the deletion and send the delete messages for children
    };

    const updateElement = async <E extends AnyElement>(
        el: E,
        ...changedAttribute: (keyof E)[]
    ) => {
        const changes = Object.fromEntries(changedAttribute.map(a => [a, el[a]]));
        elements.value = elements.value.map(e => e.id === el.id ? { ...e, ...changes } : e);

        await sendSocketMessage({
            command: SocketCommand.Update,
            id: el.id,
            ...changes,
        } as UpdateSocketMessage);
    };

    // const elements = ref<AnyElement[]>({
    //   id: '1',
    //   name: 'TestName',
    //   X: 0,
    //   Y: 0,
    //   height: 400,
    //   width: 800,
    //   children: [
    //     {
    //       id: '2',
    //       name: 'Топбар',
    //       X: 0,
    //       Y: 0,
    //       height: 50,
    //       width: 800,
    //       borderRadius: 0,
    //       children: [
    //         {
    //           id: '3',
    //           name: 'Топбар',
    //           X: 0,
    //           Y: 0,
    //           height: 50,
    //           width: 800,
    //           fontWeight: '100',
    //           alignment: 'center'
    //         },
    //         {
    //           id: '4',
    //           name: 'Kvadratique',
    //           X: 50,
    //           Y: 50,
    //           height: 50,
    //           width: 50,
    //           borderRadius: 5,
    //           children: [
    //           ]
    //         }
    //       ]
    //     }
    //   ]
    // })

    return {
        socket,
        projectID,
        elements,
        selectedElements,
        currentMode,
        findElement,
        addBlock,
        addText,
        removeElement,
        updateElement,
        sendSocketMessage,
    };
});