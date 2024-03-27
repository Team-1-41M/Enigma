<script setup lang="ts">
import { EditMode } from '~/types/editMode';
import { ElementType, type Background, type BlockElement, type TextElement, type AnyElement } from '~/types/elements';

const store = useCurrentProjectStore();

const CONTROLS = [
    [0, 0, -1, -1],
    [0, 0.5, -1, 0],
    [0, 1, -1, 1],
    [0.5, 1, 0, 1],
    [1, 1, 1, 1],
    [1, 0.5, 1, 0],
    [1, 0, 1, -1],
    [0.5, 0, 0, -1],
] as [number, number, -1 | 0 | 1, -1 | 0 | 1][];

const CONTROL_RADIUS = 10;

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

const camera = reactive({
    pos: [0, 0] as Point,
    zoom: 1,
});

function mouseToWorld(
    [x, y]: Point,
): Point {
    let { pos: [hx, hy], zoom: hz } = camera;
    return [
        (x + hx) / hz,
        (y + hy) / hz,
    ];
}

function worldToMouse(
    [x, y]: Point,
): Point {
    let { pos: [hx, hy], zoom: hz } = camera;
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
    let point = mouseToWorld(mousePos);
    return (elements ?? store.elements)
        // FIXME find foremost
        .find(el => inside(point, elementBox(el)));
}

function mouseOverBlockControl(
    mousePos: Point,
    element?: BlockElement,
): { element: BlockElement, cx: -1 | 0 | 1, cy: -1 | 0 | 1 } | undefined {
    let [mx, my] = mouseToWorld(mousePos);

    for (const el of element === undefined ? store.elements : [element]) {
        if (el.type !== ElementType.Block) continue;

        for (let [ptx, pty, cx, cy] of CONTROLS) {
            let x = el.x + ptx * el.width;
            let y = el.y + pty * el.height;
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
    return x1 < x2 + w2
        && x1 + w1 > x2
        && y1 < y2 + h2
        && y1 + h1 > y2;
}

function inside(
    [px, py]: Point,
    { x, y, w, h }: Box,
): boolean {
    return x <= px && px <= x + w
        && y <= py && py <= y + h;
}

function elementBox(element: AnyElement): Box {
    let width, height;

    switch (element.type) {
        case ElementType.Text:
            let measure = canvas.value!.getContext('2d')!.measureText(element.content);
            width = measure.width;
            height = measure.actualBoundingBoxAscent + measure.actualBoundingBoxDescent; // FIXME check if it supports multiline
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

function drawText(ctx: CanvasRenderingContext2D, element: TextElement) {
    ctx.font =
        `${element.fontFamily} ` +
        `${element.fontSize}pt ` +
        `${element.italic ? "italic" : ""} ` +
        `${element.fontWeight}`;
    ctx.fillStyle = colorToColor(element.color);
    ctx.fillText(element.content, element.x, element.y);
}

function drawBlock(ctx: CanvasRenderingContext2D, element: BlockElement) {
    ctx.fillStyle = colorToColor(element.background);
    ctx.fillRect(element.x, element.y, element.width, element.height);
    // TODO arcs for border-radius
    // TODO borders

    if (store.selectedElements.find(e => e.id === element.id))
        drawSelectionBox(ctx, elementBox(element));
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
    });
}

function drawSelectionBox(
    ctx: CanvasRenderingContext2D,
    box: Box,
    alpha?: true,
) {
    if (box.w === 0 || box.h === 0) return;

    const SELECTION_BOX_LINE_WIDTH = 7;

    if (alpha) {
        ctx.fillStyle = '#C63E3E' + (alpha ? '33' : '');
        ctx.fillRect(
            box.x + SELECTION_BOX_LINE_WIDTH / 2,
            box.y + SELECTION_BOX_LINE_WIDTH / 2,
            box.w - SELECTION_BOX_LINE_WIDTH,
            box.h - SELECTION_BOX_LINE_WIDTH,
        );
    }

    ctx.strokeStyle = '#C63E3E' + (alpha ? '77' : '');
    ctx.lineWidth = SELECTION_BOX_LINE_WIDTH;
    ctx.strokeRect(box.x, box.y, box.w, box.h);
}

function drawBlockControls(ctx: CanvasRenderingContext2D) {
    if (store.selectedElements.length !== 1) return;

    let element = store.selectedElements[0];
    if (element.type !== ElementType.Block) return;

    drawSelectionBox(ctx, elementBox(element));

    for (let [ptx, pty, cx, cy] of CONTROLS) {
        ctx.lineWidth = 2;
        ctx.fillStyle = isControlClicked(cx, cy) ? '#FFF' : '#D9D9D9';
        let radius = isControlClicked(cx, cy) ? 10 : 7;
        let x = element.x + ptx * element.width + cx * (cy === 0 ? 5 : 2.5);
        let y = element.y + pty * element.height + cy * (cx === 0 ? 5 : 2.5);
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
    }
}
function draw() {
    const ctx = canvas.value!.getContext('2d')!;
    ctx.canvas.width = ctx.canvas.parentElement!.clientWidth;
    ctx.canvas.height = ctx.canvas.parentElement!.clientHeight;
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    ctx.save();

    let { pos: [hx, hy], zoom: hz } = camera;
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
// Controlling
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
} as const;
type ClickType = typeof ClickType[keyof typeof ClickType];

type BaseClick = {
    clickType: ClickType,
};

type AnyClick = CameraClick | ElementsMoveClick | BlockControlClick | BlockDrawClick | SelectClick;

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

let click = undefined as undefined | ClickInfo<AnyClick>;

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
        const mousePos = [event.offsetX, event.offsetY] as Point;

        checkControls: if (store.selectedElements.length === 1) {
            const selected = store.selectedElements[0];
            if (selected.type !== ElementType.Block) break checkControls;

            const control = mouseOverBlockControl(mousePos, selected);
            if (control === undefined) break checkControls;
            const {
                element: { x, y, width, height },
                cx, cy,
            } = control;

            return {
                clickType: ClickType.BlockControl,
                x, y,
                w: width,
                h: height,
                cx, cy,
            } as BlockControlClick;
        }

        moveElements: {
            const found = mouseOverElement(mousePos);
            if (found === undefined) break moveElements;

            if (!store.selectedElements.find(e => e.id === found.id))
                store.selectedElements = [found];

            return {
                clickType: ClickType.ElementsMove,
                elementsPosBeforeClick: store.selectedElements.map(({ x, y }) => [x, y]),
            } as ElementsMoveClick;
        }

        return {
            clickType: ClickType.Select,
        } as SelectClick;
    },

    [EditMode.Block]: (event: MouseEvent) => ({
        clickType: ClickType.BlockDraw,
        x: event.offsetX,
        y: event.offsetY,
    } as BlockDrawClick),

    [EditMode.Text]: (event: MouseEvent) => {
        // TODO
        return Actions[EditMode.Camera](event);
    },

    [EditMode.Camera]: (_event: MouseEvent) => ({
        clickType: ClickType.Camera,
        cameraBeforeClick: [...camera.pos],
    } as CameraClick),
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

    click = {
        start: [event.offsetX, event.offsetY],
        end: [event.offsetX, event.offsetY],
        draggedEnough: false,
        returnToMode,
        clicked: Actions[store.currentMode](event),
    };
}

// Updaters (mouse move)

type Updater<C extends AnyClick> = (click: ClickInfo<C>) => void;
const Updaters: { [C in ClickType]?: Updater<Extract<AnyClick, { clickType: C }>> } = {
    [ClickType.Camera]: click => {
        let {
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
            let { start, end, clicked: { elementsPosBeforeClick } } = click;
            let [sx, sy] = mouseToWorld(start);
            let [ex, ey] = mouseToWorld(end);
            element.x = Math.round(elementsPosBeforeClick[i][0] + (ex - sx));
            element.y = Math.round(elementsPosBeforeClick[i][1] + (ey - sy));
            store.updateElement(element, 'x', 'y');
        });
    },

    [ClickType.BlockControl]: click => {
        let element = store.selectedElements[0];
        if (element.type !== ElementType.Block) return;

        let { start, end } = click;
        let [sx, sy] = mouseToWorld(start);
        let [ex, ey] = mouseToWorld(end);
        let dx = ex - sx;
        let dy = ey - sy;
        let { x, y, w, h, cx, cy } = click.clicked;

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
        let selectionBox = twoPointsToBox(mouseToWorld(click.start), mouseToWorld(click.end));
        store.selectedElements = store.elements
            .filter(element => boxesIntersect(selectionBox, elementBox(element)));
    }
}

function mouseMove(event: MouseEvent) {
    if (click == null) return;

    // check if moved enough; some actions may interpret this as an auxiliary completer upon release
    // (e.g. selecting a block)
    let [sx, sy] = click.start;
    let { offsetX: mx, offsetY: my } = event;
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
        let { start, end } = click;

        let { x, y, w, h } = twoPointsToBox(mouseToWorld(start), mouseToWorld(end));
        x = Math.round(x);
        y = Math.round(y);
        w = Math.round(w);
        h = Math.round(h);
        if (w < 1 || h < 1) return;

        store.addBlock(el => {
            el.x = x;
            el.y = y;
            el.width = w;
            el.height = h;
        });
    },

    [ClickType.Select]: click => {
        if (click.draggedEnough) return;
        const found = mouseOverElement(mouseToWorld(click.end));
        store.selectedElements = found !== undefined ? [found] : [];
    }
};

function mouseUp() {
    if (click === undefined) return;

    let completer = Completers[click.clicked.clickType];
    if (completer !== undefined) completer(click as any);

    if (click.returnToMode !== undefined)
        store.currentMode = click.returnToMode;

    click = undefined;
}

// Renderers

type Renderer<C extends AnyClick> = (ctx: CanvasRenderingContext2D, click: ClickInfo<C>) => void;
const Renderers: { [C in ClickType]?: Renderer<Extract<AnyClick, { clickType: C }>> } = {
    [ClickType.BlockDraw]: (ctx, click) => {
        drawSelectionBox(ctx, twoPointsToBox(mouseToWorld(click.start), mouseToWorld(click.end)), true);
    },

    [ClickType.Select]: (ctx, click) => {
        drawSelectionBox(ctx, twoPointsToBox(mouseToWorld(click.start), mouseToWorld(click.end)), true);
    },
};

function drawClicks(ctx: CanvasRenderingContext2D) {
    if (click === undefined) return;

    let renderer = Renderers[click.clicked.clickType];
    if (renderer !== undefined) renderer(ctx, click as any);
}

// Wheel

function wheel(event: WheelEvent) {
    event.preventDefault();
    if (click !== undefined) return; // FIXME figma does not have this limitation

    // worldMouse(mousePos, cameraBefore, zoomBefore) = worldMouse(mousePos, cameraAfter, zoomAfter)
    // (mousePos + cameraBefore) / zoomBefore = (mousePos + cameraAfter) / zoomAfter
    // cameraAfter = (mousePos + cameraBefore) * zoomAfter / zoomBefore - mousePos
    const [mx, my] = [event.offsetX, event.offsetY];
    const zoomBefore = camera.zoom;
    camera.zoom = Math.min(2, Math.max(0.5, camera.zoom - event.deltaY / 1000));
    camera.pos = [
        (mx + camera.pos[0]) * camera.zoom / zoomBefore - mx,
        (my + camera.pos[1]) * camera.zoom / zoomBefore - my,
    ];
}
</script>

<template>
    <!-- FIXME these events should be on window (otherwise causes bugs when dragging elements or camera outside window, releasing mouse, and moving back in) -->
    <div style="height: 99%">
        <canvas ref="canvas" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" @wheel="wheel" />
    </div>
</template>