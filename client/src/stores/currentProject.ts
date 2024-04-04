import { defineStore } from 'pinia';
import { EditMode } from '~/types/editMode';
import { generateElementID, type AnyElement, type BaseElement, type BlockElement, type ElementID, type TextElement, ElementType, createBlockElement, createTextElement } from '~/types/elements';
import type { Project, ProjectID } from '~/types/project';
import { SocketCommand, type AnySocketMessage, type CreateSocketMessage, type UpdateSocketMessage, type DeleteSocketMessage, type PutAfterMessage } from '~/types/socket';

const referencePromise = <T>() => {
    // https://stackoverflow.com/questions/63205154/is-it-possible-to-resolve-a-promise-by-user-action-or-manually-managed-triggers
    let resolve: undefined | ((value: T) => void) = undefined;
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

    function loadProject(projectID: ProjectID) {
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
                    let element: { [key: string]: any } = {};

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
                        element[key] = value === null ? undefined : value;
                    }

                    elements.value.push(element as any);
                }
                return;
            }

            const commandPos = message.indexOf('{');

            const command = message.slice(0, commandPos).trim() as SocketCommand;
            const data = JSON.parse(message.slice(commandPos)) as AnySocketMessage;
            data.command = command;
            // FIXME check if successful parse

            const id = data.id; // FIXME check if there is data.id

            const updateItem = (element: { [key: string]: any }) => {
                for (const [key, value] of Object.entries(data)) {
                    // FIXME i smell security problems here
                    element[key] = value === null ? undefined : value;
                }
            };

            // this block does not cause new messages (which would be pain)
            let el = undefined;
            switch (data.command) {
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
                case SocketCommand.PutAfter:
                    putAfter(id, data.after);
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
    async function sendSocketMessage<T extends AnySocketMessage>(message: T) {
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

    function generateName(type: ElementType): string {
        return `${type === ElementType.Block ? 'Блок' : 'Текст'} ` + // TODO i18n?
            `${elements.value.filter(e => e.type === type).length + 1}`;
    }

    function findElement<E extends BaseElement>(id: ElementID, type?: E['type']): E | undefined {
        return elements.value.find(e => e.id === id && (type === undefined || e.type === type)) as E;
    }

    async function addBlock(edit?: (el: BlockElement) => void): Promise<BlockElement> {
        const el = createBlockElement(generateElementID(), generateName(ElementType.Block));
        const def: BlockElement = { ...el };
        if (edit !== undefined) edit(el);
        elements.value.push(el);

        await sendSocketMessage<CreateSocketMessage>({
            command: SocketCommand.Create,
            id: el.id,
            type: ElementType.Block,
            name: el.name,
        });

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
        const def: TextElement = { ...el };
        if (edit !== undefined) edit(el);
        elements.value.push(el);

        await sendSocketMessage<CreateSocketMessage>({
            command: SocketCommand.Create,
            id: el.id,
            type: ElementType.Text,
            name: el.name,
        });

        if (edit !== undefined) {
            await updateElement(
                el,
                ...([...Object.keys(def), ...Object.keys(el)] as (keyof TextElement)[])
                    .filter((value, index, array) => array.indexOf(value) === index)
                    .filter(key => el[key] !== def[key])
            );
        }

        return el;
    };

    function remove(id: ElementID) {
        elements.value = elements.value.filter(e => e.id !== id);
        for (const childToRemove of elements.value.filter(e => e.parent === id))
            remove(childToRemove.id);
    }

    async function removeElement(id: ElementID) {
        const pre = elements.value;
        remove(id);
        if (pre.length === elements.value.length) return;

        await sendSocketMessage<DeleteSocketMessage>({
            command: SocketCommand.Delete,
            id,
        });

        // Backend will cascade the deletion and send the delete messages for children
    };

    async function updateElement<E extends AnyElement>(
        el: E,
        ...changedAttribute: (keyof E)[]
    ) {
        const changes = Object.fromEntries(changedAttribute.map(a => [a, el[a] === undefined ? null : el[a]]));
        for (const e of elements.value)
            if (e.id === el.id)
                for (const [key, value] of Object.entries(changes)) {
                    const obj = e as any;
                    if (value === null) delete obj[key];
                    else obj[key] = value;
                }

        await sendSocketMessage<UpdateSocketMessage>({
            command: SocketCommand.Update,
            id: el.id,
            ...changes,
        });
    };

    function putAfter(id: ElementID, after?: ElementID) {
        const foundIndex = elements.value.findIndex(e => e.id === id);
        if (foundIndex < 0) return;
        const found = elements.value[foundIndex];
        const temp = elements.value.toSpliced(foundIndex, 1);

        let newIndex = 0;
        if (after !== undefined) {
            const afterIndex = temp.findIndex(e => e.id === after);
            if (afterIndex < 0) return;
            newIndex = afterIndex + 1;
        }
        temp.splice(newIndex, 0, found);
        elements.value = temp;
    }

    async function putElementAfter(id: ElementID, after?: ElementID) {
        putAfter(id, after);

        await sendSocketMessage<PutAfterMessage>({
            command: SocketCommand.PutAfter,
            id,
            after,
        });
    }

    function globalPosition(element: AnyElement): [number, number] {
        const { x, y } = element;

        const parent = elements.value.find(e => e.id === element.parent);
        if (parent === undefined) return [x, y];

        const [px, py] = globalPosition(parent);
        return [x + px, y + py];
    }

    function localPosition([globalX, globalY]: [number, number], parent: AnyElement): [number, number] {
        const [px, py] = globalPosition(parent);
        return [globalX - px, globalY - py];
    }

    function detachFromParent(id: ElementID, parentToDetach: ElementID) {
        const found = findElement(id);
        if (found === undefined) return;
        const parentToDetachEl = findElement(parentToDetach);
        if (parentToDetachEl === undefined) return;

        if (found.parent === parentToDetach)
            makeChild(found.id, parentToDetachEl.parent);
        else if (found.parent !== undefined)
            detachFromParent(found.parent, parentToDetach);
    }

    async function makeChild(id: ElementID, newParent?: ElementID) {
        const found = elements.value.find(e => e.id === id);
        if (found === undefined || found.parent === newParent) return;

        const foundParent = elements.value.find(e => e.id === newParent);
        if (newParent !== undefined && foundParent === undefined) return;

        if (newParent !== undefined)
            detachFromParent(newParent, id);

        let oldPos = globalPosition(found);
        let [newX, newY] = foundParent === undefined ? oldPos : localPosition(oldPos, foundParent);
        found.parent = newParent;
        found.x = newX;
        found.y = newY;
        await updateElement(found, "parent", "x", "y");
    }

    type TreeItem = { id: ElementID, children: TreeItem[] }; // do I need to export this?

    function tree(root?: ElementID): TreeItem[] {
        // FIXME recursive == rip performance (O(N^2)?)
        return elements.value
            .filter(e => e.parent === root)
            .map(e => ({ id: e.id, children: tree(e.id) }));
    }

    function traversedTree(root?: ElementID, accum?: ElementID[]): ElementID[] {
        if (accum === undefined) accum = [];
        elements.value
            .filter(e => e.parent === root)
            .forEach(e => {
                accum!.push(e.id);
                traversedTree(e.id, accum);
            });
        return accum;
    }

    (window as any).elements = elements;
    (window as any).traversedTree = traversedTree;

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
        putElementAfter,
        globalPosition,
        localPosition,
        makeChild,
        tree,
        traversedTree,
        sendSocketMessage,
    };
});