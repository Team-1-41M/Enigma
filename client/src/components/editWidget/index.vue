<script setup lang="ts">
import { EditMode } from '~/types/editMode';
import { ElementType, type Background, type BlockElement, type TextElement } from '~/types/elements';

const store = useCurrentProjectStore();

//
// Coordinate magic
//

const camera = reactive({
    x: 0,
    y: 0,
    zoom: 1,
});

function mouseToWorld(x: number, y: number): number[] {
    return [
        (x - camera.x) * camera.zoom,
        (y - camera.y) * camera.zoom,
    ];
}

function worldToMouse(x: number, y: number): number[] {
    return [
        x / camera.zoom + camera.x,
        y / camera.zoom + camera.y,
    ];
}

function twoPointsToBox(point1: number[], point2: number[]) {
    return {
        x: Math.min(point1[0], point2[0]),
        y: Math.min(point1[1], point2[1]),
        w: Math.abs(point1[0] - point2[0]),
        h: Math.abs(point1[1] - point2[1]),
    };
}

//
// Drawing
//

const canvas = ref();

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
}

function drawBlockSelection(
    ctx: CanvasRenderingContext2D,
    element: { x: number, y: number, width: number, height: number },
    alpha?: `#${string}`,
) {
    ctx.strokeStyle = '#C63E3E' + (alpha || '');
    ctx.lineWidth = 7;
    ctx.strokeRect(element.x, element.y, element.width, element.height);
}

function drawBlockControls(ctx: CanvasRenderingContext2D, element: BlockElement) {
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
    const ctx: CanvasRenderingContext2D = canvas.value.getContext('2d');
    ctx.canvas.width = ctx.canvas.parentElement!.clientWidth;
    ctx.canvas.height = ctx.canvas.parentElement!.clientHeight;
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    ctx.save();
    ctx.translate(-camera.x, -camera.y);
    ctx.scale(camera.zoom, camera.zoom);
    store.elements.forEach(element => {
        // TODO do not draw outside of camera
        switch (element.type) {
            case ElementType.Block:
                drawBlock(ctx, element);
                break;
            case ElementType.Text:
                drawText(ctx, element);
                break;
        }
    });

    store.elements.forEach(element => {
        if (!store.selectedElements.includes(element.id))
            return;

        switch (element.type) {
            case ElementType.Block:
                drawBlockSelection(ctx, element);
                if (store.selectedElements.length === 1)
                    drawBlockControls(ctx, element);
                break;
            case ElementType.Text:
                // TODO (?)
                break;
        }
    });

    // TODO proper tool drawing map/switch
    if (click?.clicked.clickType === 'blockDraw') {
        let { x, y, w: width, h: height } = twoPointsToBox(
            [click.x, click.y],
            [click.clicked.x, click.clicked.y],
        );
        drawBlockSelection(ctx, { x, y, width, height });
    }

    ctx.restore();

    // oops! your laptop battery is dead
    requestAnimationFrame(draw);
}

//
// Controlling
//

let click = null as null | {
    x: number;
    y: number;
    draggedEnough: boolean;
    clicked: {
        clickType: 'camera',
        cameraX: number,
        cameraY: number,
    } | {
        clickType: 'element',
        x: number,
        y: number,
    } | {
        clickType: 'blockControl',
        x: number,
        y: number,
        w: number,
        h: number,
        cx: -1 | 0 | 1,
        cy: -1 | 0 | 1,
    } | {
        clickType: 'blockDraw',
        x: number,
        y: number,
    };
};

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

function isControlClicked(cx: -1 | 0 | 1, cy: -1 | 0 | 1): boolean {
    return click?.clicked.clickType === 'blockControl'
        && click.clicked.cx === cx
        && click.clicked.cy === cy;
}

function mouseDown(event: MouseEvent) {
    // TODO rewrite to a tool map/switch
    if (store.currentMode === EditMode.Block) {
        click = {
            x: event.offsetX,
            y: event.offsetY,
            draggedEnough: false, // proper startClick or something
            clicked: {
                clickType: 'blockDraw',
                x: event.offsetX,
                y: event.offsetY,
            }
        };
        return;
    }

    let element = store.elements
        .find(element => {
            if (element.type === 'text')
                return false;
            // FIXME consider camera
            return -camera.x + element.x - 10 <= event.offsetX && event.offsetX <= -camera.x + element.x + element.width + 10
                && -camera.y + element.y - 10 <= event.offsetY && event.offsetY <= -camera.y + element.y + element.height + 10;
        });

    if (element != null) {
        element = element as BlockElement;
        store.selectedElements = [element.id];

        for (let [ptx, pty, cx, cy] of CONTROLS) {
            let x = ptx * element.width + element.x - camera.x;
            let y = pty * element.height + element.y - camera.y;
            if (x - 10 <= event.offsetX && event.offsetX <= x + 10
                && y - 10 <= event.offsetY && event.offsetY <= y + 10) {
                click = {
                    x: event.offsetX,
                    y: event.offsetY,
                    draggedEnough: false,
                    clicked: {
                        clickType: 'blockControl',
                        x: element.x,
                        y: element.y,
                        w: element.width,
                        h: element.height,
                        cx,
                        cy,
                    }
                }
                return;
            }
        }

        click = {
            x: event.offsetX,
            y: event.offsetY,
            draggedEnough: false,
            clicked: {
                clickType: 'element',
                x: element.x,
                y: element.y,
            }
        }
        return;
    }

    store.selectedElements = [];
    click = {
        x: event.offsetX,
        y: event.offsetY,
        draggedEnough: true,
        clicked: {
            clickType: 'camera',
            cameraX: camera.x,
            cameraY: camera.y,
        }
    }
}

function mouseMove(event: MouseEvent) {
    if (click == null)
        return;

    // TODO
    if (click.clicked.clickType === 'blockDraw') {
        click.clicked.x = event.offsetX;
        click.clicked.y = event.offsetY;
    }

    let dx = event.offsetX - click.x;
    let dy = event.offsetY - click.y;
    click.draggedEnough
        ||= Math.abs(dx) > 5
        || Math.abs(dy) > 5;
    if (!click.draggedEnough)
        return;
    if (click.clicked.clickType === 'element') {
        let element = store.elements.find(element => store.selectedElements.includes(element.id))!;
        element.x = click.clicked.x + dx;
        element.y = click.clicked.y + dy;
        store.updateElement(element, 'x');
        store.updateElement(element, 'y');
        console.log('dragging element', element);
    } else if (click.clicked.clickType === 'camera') {
        camera.x = click.clicked.cameraX - dx;
        camera.y = click.clicked.cameraY - dy;
        console.log('dragging camera', camera.x, camera.y);
    } else if (click.clicked.clickType === 'blockControl') {
        let element = store.elements.find(element => store.selectedElements.includes(element.id))! as BlockElement;
        if (click.clicked.cx === -1) {
            element.x = Math.min(click.clicked.x + dx, click.clicked.x + click.clicked.w - 1);
            element.width = Math.max(1, click.clicked.w - dx);
        } else if (click.clicked.cx === 1) {
            element.width = Math.max(1, click.clicked.w + dx);
        }

        if (click.clicked.cy === -1) {
            element.y = Math.min(click.clicked.y + dy, click.clicked.y + click.clicked.h - 1);
            element.height = Math.max(1, click.clicked.h - dy);
        } else if (click.clicked.cy === 1) {
            element.height = Math.max(1, click.clicked.h + dy);
        }

        store.updateElement(element, 'x');
        store.updateElement(element, 'y');
        store.updateElement(element, 'width');
        store.updateElement(element, 'height');

        console.log('dragging block control', click.clicked.cx, click.clicked.cy);
    }
}

async function mouseUp() {
    if (click?.clicked.clickType === 'blockDraw') {
        let { x, y, w, h } = twoPointsToBox(
            [click.x, click.y],
            [click.clicked.x, click.clicked.y],
        );
        if (w >= 1 && h >= 1) {
            let el = await store.addBlock(el => {
                el.x = x;
                el.y = y;
                el.width = w;
                el.height = h;
            });
            store.updateElement(el, 'x', 'y', 'width', 'height');
        }
    }

    // TODO if (!click.draggedEnough) open text options
    click = null;
}
</script>

<template>
    <canvas ref="canvas" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" />
</template>