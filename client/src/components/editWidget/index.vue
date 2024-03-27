<script setup lang="ts">
import { EditMode } from '~/types/editMode';
import { ElementType, type Background, type BlockElement, type TextElement, type AnyElement, TextAlignment } from '~/types/elements';

const store = useCurrentProjectStore();

const CONTROLS: [number, number, -1 | 0 | 1, -1 | 0 | 1][] = [
    [0, 0, -1, -1],
    [0, 0.5, -1, 0],
    [0, 1, -1, 1],
    [0.5, 1, 0, 1],
    [1, 1, 1, 1],
    [1, 0.5, 1, 0],
    [1, 0, 1, -1],
    [0.5, 0, 0, -1],
];

const CONTROL_RADIUS = 5;

function isControlClicked(cx: -1 | 0 | 1, cy: -1 | 0 | 1): boolean {
    return click?.clicked.clickType === 'blockControl'
        && click.clicked.cx === cx
        && click.clicked.cy === cy;
}

//
// Coordinate magic
//

type Point = [number, number];
type Box = {
    x: number,
    y: number,
    w: number,
    h: number,
};

type Camera = {
    pos: Point,
    zoom: number,
};
const camera = reactive<Camera>({
    pos: [0, 0],
    zoom: 1,
});

function mousePos(event: MouseEvent): Point {
    const { pageX, pageY } = event;
    const { x, y } = canvas.value!.getBoundingClientRect();
    return [pageX - x, pageY - y];
}

function mouseToWorld(
    [x, y]: Point,
): Point {
    const { pos: [hx, hy], zoom: hz } = camera;
    return [
        (x + hx) / hz,
        (y + hy) / hz,
    ];
}

function worldToMouse(
    [x, y]: Point,
): Point {
    const { pos: [hx, hy], zoom: hz } = camera;
    return [
        x * hz - hx,
        y * hz - hy,
    ];
}

function twoPointsToBox(
    [x1, y1]: Point,
    [x2, y2]: Point,
): Box {
    return {
        x: Math.min(x1, x2),
        y: Math.min(y1, y2),
        w: Math.abs(x2 - x1),
        h: Math.abs(y2 - y1),
    };
}

function mouseOverElement(
    mousePos: Point,
    elements?: AnyElement[],
): AnyElement | undefined {
    const point = mouseToWorld(mousePos);
    return (elements ?? store.elements)
        // FIXME find foremost
        .find(el => inside(point, elementBox(el)));
}

function mouseOverBlockControl(
    mousePos: Point,
    element?: BlockElement,
): { element: BlockElement, cx: -1 | 0 | 1, cy: -1 | 0 | 1 } | undefined {
    const [mx, my] = mouseToWorld(mousePos);

    for (const el of element === undefined ? store.elements : [element]) {
        if (el.type !== ElementType.Block) continue;

        for (const [ptx, pty, cx, cy] of CONTROLS) {
            const x = el.x + ptx * el.width + cx * (cy === 0 ? 8 : 6);
            const y = el.y + pty * el.height + cy * (cx === 0 ? 8 : 6);
            if (Math.sqrt((x - mx) ** 2 + (y - my) ** 2) <= CONTROL_RADIUS * camera.zoom)
                return { element: el, cx, cy };
        }
    }

    return undefined;
}

function boxesIntersect(
    { x: x1, y: y1, w: w1, h: h1 }: Box,
    { x: x2, y: y2, w: w2, h: h2 }: Box,
): boolean {
    // TODO check
    return x1 <= x2 + w2
        && x1 + w1 >= x2
        && y1 <= y2 + h2
        && y1 + h1 >= y2;
}

function inside(
    [px, py]: Point,
    { x, y, w, h }: Box,
): boolean {
    return x <= px && px <= x + w
        && y <= py && py <= y + h;
}

function textWidth(ctx: CanvasRenderingContext2D, text: string, scale?: true): number {
    let max = 0;
    for (const line of text.split(/\r\n|\r|\n/g)) {
        const metrics = ctx.measureText(line);
        max = Math.max(max, metrics.width) * (scale ? camera.zoom : 1);
    }
    return max;
}

function elementBox(element: AnyElement): Box {
    let width, height;

    switch (element.type) {
        case ElementType.Text:
            let ctx = canvas.value!.getContext('2d')!;
            setFont(ctx, element);
            width = textWidth(ctx, element.content);
            const metrics = ctx.measureText(element.content);
            height
                = (metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent)
                * ((element.content.match(/\r\n|\r|\n/g) || '').length + 1)
            break;
        case ElementType.Block:
            width = element.width;
            height = element.height;
            break;
    };

    return {
        x: element.x,
        y: element.y,
        w: width,
        h: height,
    };
}

//
// Drawing
//

const canvas = ref<HTMLCanvasElement>();

onMounted(draw);

function colorToColor(color: Background): string {
    if (typeof (color) === 'object' && 'r' in color && 'g' in color && 'b' in color)
        return `rgb(${color.r}, ${color.g}, ${color.b})`;
    return color;
}

function setFont(hasFont: { font: string }, text: TextElement, scale?: true) {
    hasFont.font =
        `${text.italic ? "italic" : ""} ` +
        `${text.fontWeight ?? ""}` +
        (scale ? `calc(${text.fontSize}pt * ${camera.zoom})` : `${text.fontSize}pt`) + ` ` +
        `${text.fontFamily}`;
}

function drawText(ctx: CanvasRenderingContext2D, element: TextElement) {
    if (element.content === "" || currentlyEditingText.value?.id === element.id) return;

    ctx.fillStyle = colorToColor(element.color);

    setFont(ctx, element);
    const metrics = ctx.measureText(element.content);
    const w = textWidth(ctx, element.content);
    const lineHeight = metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent;

    let x = element.x;
    switch (element.alignment) {
        case TextAlignment.Center:
            x -= w / 2;
            break;
        case TextAlignment.Left:
            break;
        case TextAlignment.Right:
            x -= w;
            break;
    }
    for (const [i, line] of element.content.split(/\r\n|\r|\n/g).entries())
        ctx.fillText(line, x, element.y + lineHeight * (1 + i) - metrics.fontBoundingBoxDescent);
}

function drawBlock(ctx: CanvasRenderingContext2D, element: BlockElement) {
    ctx.fillStyle = colorToColor(element.background);
    ctx.fillRect(element.x, element.y, element.width, element.height);
    // TODO arcs for border-radius
    // TODO borders
}

function drawElements(ctx: CanvasRenderingContext2D) {
    store.elements.forEach(element => {
        // TODO do not draw outside of camera
        // TODO use parent's position
        switch (element.type) {
            case ElementType.Block:
                drawBlock(ctx, element);
                break;
            case ElementType.Text:
                drawText(ctx, element);
                break;
        }

        if (store.selectedElements.find(e => e.id === element.id))
            drawSelectionBox(ctx, elementBox(element));
    });
}

function drawSelectionBox(
    ctx: CanvasRenderingContext2D,
    box: Box,
    alpha?: true,
) {
    const SELECTION_BOX_LINE_WIDTH = 7;

    if (alpha) {
        ctx.fillStyle = '#C63E3E' + (alpha ? '33' : '');
        ctx.fillRect(box.x, box.y, box.w, box.h);
    }

    ctx.strokeStyle = '#C63E3E' + (alpha ? '77' : '');
    ctx.lineWidth = SELECTION_BOX_LINE_WIDTH;
    ctx.strokeRect(
        box.x - SELECTION_BOX_LINE_WIDTH / 2,
        box.y - SELECTION_BOX_LINE_WIDTH / 2,
        box.w + SELECTION_BOX_LINE_WIDTH,
        box.h + SELECTION_BOX_LINE_WIDTH,
    );
}

function drawBlockControls(ctx: CanvasRenderingContext2D) {
    if (store.selectedElements.length !== 1) return;

    const element = store.selectedElements[0];
    if (element.type !== ElementType.Block) return;

    drawSelectionBox(ctx, elementBox(element));

    for (const [ptx, pty, cx, cy] of CONTROLS) {
        ctx.lineWidth = 2;
        ctx.fillStyle = isControlClicked(cx, cy) ? '#FFF' : '#D9D9D9';
        const radius = isControlClicked(cx, cy) ? 10 : 7;
        const x = element.x + ptx * element.width + cx * (cy === 0 ? 8 : 6);
        const y = element.y + pty * element.height + cy * (cx === 0 ? 8 : 6);
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
    }
}

function draw() {
    const ctx = canvas.value!.getContext('2d')!;
    ctx.canvas.width = ctx.canvas.parentElement!.offsetWidth;
    ctx.canvas.height = ctx.canvas.parentElement!.offsetHeight - 5; // FIXME
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    ctx.save();

    const { pos: [hx, hy], zoom: hz } = camera;
    ctx.translate(-hx, -hy);
    ctx.scale(hz, hz);
    drawElements(ctx);
    drawBlockControls(ctx);
    drawClicks(ctx);
    ctx.restore();

    // oops! your laptop battery is dead
    requestAnimationFrame(draw);
}

//
// Text editing
//

const currentlyEditingText = ref<TextElement>();

// TODO move to store so that it can be set by the GUI
// TODO make all properties have custom defaults
// TODO make defaults obvious
let lastTextAlignment: TextAlignment = TextAlignment.Left;
let lastFontSize = 12;

const textEditor = ref<HTMLTextAreaElement>();

watch([currentlyEditingText, camera], () => updateTextEditor());

watch(currentlyEditingText, currentlyEditingText => {
    if (currentlyEditingText === undefined) return;
    setTimeout(() => textEditor.value!.focus(), 0);
});

function updateTextEditor() {
    const area = textEditor.value!;

    const text = currentlyEditingText.value;
    if (text === undefined) {
        area.style.display = 'none';
        return;
    }
    area.style.display = 'initial';

    area.style.textAlign = text.alignment;
    setFont(area.style, text, true);

    const [left, top] = worldToMouse([text.x, text.y]);
    area.style.left = `${left}px`;
    area.style.top = `${top}px`;

    const ctx = canvas.value!.getContext('2d')!;
    setFont(ctx, text);
    const metrics = ctx.measureText(text.content);
    const width = textWidth(ctx, text.content, true);
    const lineHeight = (metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent) * camera.zoom;
    const height = lineHeight * ((text.content.match(/\r\n|\r|\n/g) || '').length + 1);

    area.style.width = `${width}px`;
    area.style.height = `${height}px`;
    area.style.lineHeight = `${lineHeight}px`;
    area.scrollTop = 0;
}

function updateText(e: Event) {
    const text = currentlyEditingText.value;
    if (text === undefined) return;

    text.content = (e.target as HTMLInputElement).value;
    store.updateElement(text, "content");

    updateTextEditor();
}

async function finishTextEdit() {
    const text = currentlyEditingText.value;
    if (text === undefined) return;
    if (!/\S/g.test(text.content)) await store.removeElement(text.id);
    currentlyEditingText.value = undefined;
}

watch(store, () => {
    const text = currentlyEditingText.value;
    if (text === undefined) return;
    if (!store.selectedElements.some(el => el.id === text.id))
        finishTextEdit();
});

//
// Clicking
//

const ClickType = {
    /**
     * Нажатие перемещает камеру.
     */
    Camera: 'camera',

    /**
     * Нажатие перемещает элемент.
     */
    ElementsMove: 'elementsMove',

    /**
     * Нажатие перемещает контроль блока (угол или сторона, для расширения).
     */
    BlockControl: 'blockControl',

    /**
     * Нажатие рисует блок.
     */
    BlockDraw: 'blockDraw',

    /**
     * Нажатие выбирает элементы.
     */
    Select: 'select',

    /**
     * Нажатие выбирает куда поместить текст.
     */
    PlacingText: 'placingText',
} as const;
type ClickType = typeof ClickType[keyof typeof ClickType];

type BaseClick = {
    clickType: ClickType,
};

type AnyClick = CameraClick | ElementsMoveClick | BlockControlClick | BlockDrawClick | SelectClick | PlacingTextClick;

type CameraClick = BaseClick & {
    clickType: typeof ClickType.Camera,
    cameraBeforeClick: Point,
};

type ElementsMoveClick = BaseClick & {
    clickType: typeof ClickType.ElementsMove,
    elementsPosBeforeClick: Point[],
};

type BlockControlClick = BaseClick & {
    clickType: typeof ClickType.BlockControl,
    x: number,
    y: number,
    w: number,
    h: number,
    cx: -1 | 0 | 1,
    cy: -1 | 0 | 1,
};

type BlockDrawClick = BaseClick & {
    clickType: typeof ClickType.BlockDraw,
};

type SelectClick = BaseClick & {
    clickType: typeof ClickType.Select,
};

type PlacingTextClick = BaseClick & {
    clickType: typeof ClickType.PlacingText,
};

let click: undefined | ClickInfo<AnyClick> = undefined;

type ClickInfo<C extends AnyClick> = {
    /**
     * Точка в которой произошел клик, в координатах холста (mouse).
     */
    start: Point;

    /**
     * Точка, в которой в новейший момент находится мышь, в координатах холста (mouse).
     */
    end: Point;

    /**
     * Достаточно ли преодолено дистанции после нажатия? Описывает либо клик, либо перетаскивание.
     */
    draggedEnough: boolean;

    /**
     * Режим, который будет установлен при завершении нажатия.
     */
    returnToMode?: EditMode;

    /**
     * Дополнительные данные о клике.
     */
    clicked: C,
};

// Actions (mouse down)

const Actions = {
    [EditMode.Move]: (event: MouseEvent) => {
        const mp: Point = mousePos(event);

        checkControls: if (store.selectedElements.length === 1) {
            const selected = store.selectedElements[0];
            if (selected.type !== ElementType.Block) break checkControls;

            const control = mouseOverBlockControl(mp, selected);
            if (control === undefined) break checkControls;
            const {
                element: { x, y, width, height },
                cx, cy,
            } = control;

            const result: BlockControlClick = {
                clickType: ClickType.BlockControl,
                x, y,
                w: width,
                h: height,
                cx, cy,
            };
            return result;
        }

        moveElements: {
            const found = mouseOverElement(mp);
            if (found === undefined) break moveElements;

            if (!store.selectedElements.find(e => e.id === found.id))
                store.selectedElements = [found];

            const result: ElementsMoveClick = {
                clickType: ClickType.ElementsMove,
                elementsPosBeforeClick: store.selectedElements.map(({ x, y }) => [x, y]),
            };
            return result;
        }

        const result: SelectClick = {
            clickType: ClickType.Select,
        };
        return result;
    },

    [EditMode.Block]: (_event: MouseEvent): BlockDrawClick => ({
        clickType: ClickType.BlockDraw,
    }),

    [EditMode.Text]: (_event: MouseEvent): PlacingTextClick => ({
        clickType: ClickType.PlacingText,
    }),

    [EditMode.Camera]: (_event: MouseEvent): CameraClick => ({
        clickType: ClickType.Camera,
        cameraBeforeClick: [...camera.pos],
    }),
} as const;

function mouseDown(event: MouseEvent) {
    event.preventDefault();
    if (click !== undefined) return;

    let returnToMode = undefined;

    const MIDDLE_BUTTON = 1;
    if (event.button === MIDDLE_BUTTON) {
        returnToMode = store.currentMode;
        store.currentMode = EditMode.Camera;
    }

    finishTextEdit();

    const mousePos: Point = [event.offsetX, event.offsetY];
    click = {
        start: [...mousePos],
        end: [...mousePos],
        draggedEnough: false,
        returnToMode,
        clicked: Actions[store.currentMode](event),
    };
}

// Updaters (mouse move)

type Updater<C extends AnyClick> = (click: ClickInfo<C>) => void;
const Updaters: { [C in ClickType]?: Updater<Extract<AnyClick, { clickType: C }>> } = {
    [ClickType.Camera]: click => {
        const {
            start: [sx, sy],
            end: [ex, ey],
            clicked: { cameraBeforeClick: [hx, hy] },
        } = click;
        camera.pos = [
            // `cam - ...` because camera movement is opposite to its coords
            hx - (ex - sx),
            hy - (ey - sy),
        ];
    },

    [ClickType.ElementsMove]: click => {
        store.selectedElements.forEach((element, i) => {
            const { start, end, clicked: { elementsPosBeforeClick } } = click;
            const [sx, sy] = mouseToWorld(start);
            const [ex, ey] = mouseToWorld(end);
            element.x = Math.round(elementsPosBeforeClick[i][0] + (ex - sx));
            element.y = Math.round(elementsPosBeforeClick[i][1] + (ey - sy));
            store.updateElement(element, 'x', 'y');
        });
    },

    [ClickType.BlockControl]: click => {
        const element = store.selectedElements[0];
        if (element.type !== ElementType.Block) return;

        const { start, end } = click;
        const [sx, sy] = mouseToWorld(start);
        const [ex, ey] = mouseToWorld(end);
        const dx = ex - sx;
        const dy = ey - sy;
        const { x, y, w, h, cx, cy } = click.clicked;

        if (cx === -1) {
            element.x = Math.min(Math.round(x + dx), Math.round(x + w - 1));
            element.width = Math.max(1, Math.round(w - dx));
        } else if (cx === 1) {
            element.width = Math.max(1, Math.round(w + dx));
        }

        if (cy === -1) {
            element.y = Math.min(Math.round(y + dy), Math.round(y + h - 1));
            element.height = Math.max(1, Math.round(h - dy));
        } else if (cy === 1) {
            element.height = Math.max(1, Math.round(h + dy));
        }

        store.updateElement(element, 'x', 'y', 'width', 'height');
    },

    [ClickType.Select]: click => {
        const selectionBox = twoPointsToBox(mouseToWorld(click.start), mouseToWorld(click.end));
        store.selectedElements = store.elements
            .filter(element => boxesIntersect(selectionBox, elementBox(element)));
    }
}

function mouseMove(event: MouseEvent) {
    if (click == null) return;

    // check if moved enough; some actions may interpret this as an auxiliary completer upon release
    // (e.g. selecting a block)
    const [sx, sy] = click.start;
    const [mx, my] = mousePos(event);
    click.draggedEnough
        ||= Math.abs(mx - sx) > 5
        || Math.abs(my - sy) > 5;
    if (!click.draggedEnough) return;

    click.end = [mx, my];

    const updater = Updaters[click.clicked.clickType];
    if (updater !== undefined) updater(click as any);
}

// Completers (mouse up)

type Completer<C extends AnyClick> = (click: ClickInfo<C>) => void;
const Completers: { [C in ClickType]?: Completer<Extract<AnyClick, { clickType: C }>> } = {
    [ClickType.BlockDraw]: click => {
        const { start, end } = click;

        let { x, y, w, h } = twoPointsToBox(mouseToWorld(start), mouseToWorld(end));

        w = Math.round(w);
        h = Math.round(h);
        if (w < 1 || h < 1) return;

        store.addBlock(el => {
            el.x = Math.round(x);
            el.y = Math.round(y);
            el.width = w;
            el.height = h;
        });
    },

    [ClickType.ElementsMove]: click => {
        if (click.draggedEnough) return;
        const found = mouseOverElement(click.end);
        store.selectedElements = found !== undefined ? [found] : [];
    },

    [ClickType.Select]: click => {
        if (click.draggedEnough) return;
        const found = mouseOverElement(click.end);
        store.selectedElements = found !== undefined ? [found] : [];
    },

    [ClickType.PlacingText]: async click => {
        const [x, y] = mouseToWorld(click.end);
        let text = await store.addText(el => {
            el.x = Math.round(x);
            el.y = Math.round(y);
            el.alignment = lastTextAlignment;
            el.fontSize = lastFontSize;
        });
        store.selectedElements = [text];
        currentlyEditingText.value = text;
    }
};

function mouseUp() {
    if (click === undefined) return;

    const completer = Completers[click.clicked.clickType];
    if (completer !== undefined) completer(click as any);

    if (click.returnToMode !== undefined)
        store.currentMode = click.returnToMode;

    click = undefined;
}

// Renderers

type Renderer<C extends AnyClick> = (ctx: CanvasRenderingContext2D, click: ClickInfo<C>) => void;
const Renderers: { [C in ClickType]?: Renderer<Extract<AnyClick, { clickType: C }>> } = {
    [ClickType.BlockDraw]: (ctx, click) => {
        // FIXME draw styled block instead, or add block element at click and resize actual created block
        drawSelectionBox(ctx, twoPointsToBox(mouseToWorld(click.start), mouseToWorld(click.end)), true);
    },

    [ClickType.Select]: (ctx, click) => {
        if (!click.draggedEnough) return;
        drawSelectionBox(ctx, twoPointsToBox(mouseToWorld(click.start), mouseToWorld(click.end)), true);
    },

    [ClickType.PlacingText]: (ctx, click) => {
        const [x, y] = mouseToWorld(click.end);
        const box = {
            x, y,
            w: lastFontSize / 1.5,
            h: lastFontSize,
        };
        switch (lastTextAlignment) {
            case TextAlignment.Center:
                box.x -= box.w / 2;
                break;
            case TextAlignment.Left:
                break;
            case TextAlignment.Right:
                box.x -= box.w;
                break;
        }
        drawSelectionBox(ctx, box, true);
    }
};

function drawClicks(ctx: CanvasRenderingContext2D) {
    if (click === undefined) return;

    const renderer = Renderers[click.clicked.clickType];
    if (renderer !== undefined) renderer(ctx, click as any);
}

// Other

function doubleClick(event: MouseEvent) {
    if (store.currentMode !== EditMode.Move
        || store.selectedElements.length != 1) return;

    // enter editing mode if clicked on selected text
    const found = mouseOverElement(mousePos(event));
    if (found !== undefined
        && found.type === ElementType.Text

        && found.id == store.selectedElements[0].id) {
        currentlyEditingText.value = found;
        return;
    }
}

function keyEnter(event: KeyboardEvent) {
    if (event.key !== "Enter"
        || click !== undefined
        || store.selectedElements.length !== 1
        || store.selectedElements[0].type !== ElementType.Text) return;

    currentlyEditingText.value = store.selectedElements[0];
}

function keyDelete(event: KeyboardEvent) {
    if (event.key !== "Delete") return;

    for (const element of [...store.selectedElements])
        store.removeElement(element.id);
}

window.addEventListener('mousemove', mouseMove);
window.addEventListener('mouseup', mouseUp);
window.addEventListener('keyup', keyEnter);
window.addEventListener('keyup', keyDelete);

onUnmounted(() => {
    window.removeEventListener('mousemove', mouseMove);
    window.removeEventListener('mouseup', mouseUp);
    window.removeEventListener('keyup', keyEnter);
    window.removeEventListener('keyup', keyDelete);
});

// Wheel

function wheel(event: WheelEvent) {
    event.preventDefault();
    if (click !== undefined) return; // FIXME figma does not have this limitation

    // worldMouse(mousePos, cameraBefore, zoomBefore) = worldMouse(mousePos, cameraAfter, zoomAfter)
    // (mousePos + cameraBefore) / zoomBefore = (mousePos + cameraAfter) / zoomAfter
    // cameraAfter = (mousePos + cameraBefore) * zoomAfter / zoomBefore - mousePos
    const [mx, my] = mousePos(event);
    const zoomBefore = camera.zoom;
    camera.zoom = Math.min(2, Math.max(0.5, camera.zoom - event.deltaY / 1000));
    camera.pos = [
        (mx + camera.pos[0]) * camera.zoom / zoomBefore - mx,
        (my + camera.pos[1]) * camera.zoom / zoomBefore - my,
    ];
}
</script>

<template>
    <div>
        <textarea ref="textEditor" :value="currentlyEditingText?.content" @input="updateText" @blur="finishTextEdit"
            @keydown.esc="finishTextEdit" style="display: none" />
        <canvas ref="canvas" @mousedown="mouseDown" @dblclick="doubleClick" @wheel="wheel" />
    </div>
</template>

<style scoped>
div {
    position: relative;
}

textarea {
    position: absolute;
    resize: none;
    padding: 0;
    border: none;
    outline: none;
    background-color: transparent;
    overflow: hidden;
}
</style>