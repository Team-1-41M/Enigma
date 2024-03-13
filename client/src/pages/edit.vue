<script setup lang="ts">
const store = useCurrentProjectStore();;


await store.createBlockElement(el => {
    el.x = 100;
    el.y = 100;
    el.width = 100;
    el.height = 100;
    el.background = '#0077ff';
});
await store.createTextElement(el => {
    el.x = 100;
    el.y = 100;
    el.content = 'Hello, World!';
});

const canvas = ref();

onMounted(draw);

function colorToColor(color: Color): string {
    if (typeof(color) === 'string')
        return color;
    return `rgb(${color.r}, ${color.g}, ${color.b})`;
}

function drawText(ctx: CanvasRenderingContext2D, element: TextElement) {
    ctx.font = `${element.fontStyle} ${element.fontSize}pt ${element.fontFamily}`;
    ctx.fillStyle = colorToColor(element.color);
    ctx.fillText(element.content, element.x, element.y);
}

function drawBlock(ctx: CanvasRenderingContext2D, element: BlockElement) {
    ctx.fillStyle = colorToColor(element.background);
    ctx.fillRect(element.x, element.y, element.width, element.height);
    // TODO arcs for border-radius
    // TODO borders
}

function drawBlockControls(ctx: CanvasRenderingContext2D, element: BlockElement) {
    ctx.strokeStyle = '#C63E3E';
    ctx.lineWidth = 7;
    ctx.strokeRect(element.x, element.y, element.width, element.height);

    let radius;

    for (let [ptx, pty, cx, cy] of CONTROLS) {
        ctx.lineWidth = 2;
        ctx.fillStyle = isControlClicked(cx, cy) ? '#FFF' : '#D9D9D9';
        radius = isControlClicked(cx, cy) ? 10 : 7;
        let x = element.x + ptx * element.width  + cx * (cy === 0 ? 5 : 2.5);
        let y = element.y + pty * element.height + cy * (cx === 0 ? 5 : 2.5);
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
    }
}

function draw() {
    const ctx: CanvasRenderingContext2D = canvas.value.getContext('2d');
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    ctx.save();
    ctx.translate(-store.cameraX, -store.cameraY);
    store.elements.forEach(element => {
        // TODO zoom
        // TODO do not draw outside of camera
        if (element.type === 'text')
            drawText(ctx, element);
        else
            drawBlock(ctx, element);
    });

    store.elements.forEach(element => {
        if (store.selectedElement !== element.id)
            return;
        if (element.type === 'text')
            return; // TODO (?)
        else
            drawBlockControls(ctx, element);
    })

    ctx.restore();

    // oops! your laptop battery is dead
    requestAnimationFrame(draw);
}

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
    let element = store.elements
        .find(element => {
            if (element.type === 'text')
                return false;
            // FIXME consider camera
            return -store.cameraX + element.x - 10 <= event.clientX && event.clientX <= -store.cameraX + element.x + element.width + 10
                && -store.cameraY + element.y - 10 <= event.clientY && event.clientY <= -store.cameraY + element.y + element.height + 10;
        });

    if (element != null) {
        element = element as BlockElement;
        store.selectedElement = element.id;

        for (let [ptx, pty, cx, cy] of CONTROLS) {
            let x = ptx * element.width + element.x - store.cameraX;
            let y = pty * element.height + element.y - store.cameraY;
            if (x - 10 <= event.clientX && event.clientX <= x + 10
                && y - 10 <= event.clientY && event.clientY <= y + 10) {
                click = {
                    x: event.clientX,
                    y: event.clientY,
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
            x: event.clientX,
            y: event.clientY,
            draggedEnough: false,
            clicked: {
                clickType: 'element',
                x: element.x,
                y: element.y,
            }
        }
        return;
    }

    store.selectedElement = null;
    click = {
        x: event.clientX,
        y: event.clientY,
        draggedEnough: true,
        clicked: {
            clickType: 'camera',
            cameraX: store.cameraX,
            cameraY: store.cameraY,
        }
    }
}

function mouseMove(event: MouseEvent) {
    if (click == null)
        return;
    let dx = event.clientX - click.x;
    let dy = event.clientY - click.y;
    click.draggedEnough
        ||= Math.abs(dx) > 5
        || Math.abs(dy) > 5;
    if (!click.draggedEnough)
        return;
    if (click.clicked.clickType === 'element') {
        let element = store.elements.find(element => element.id === store.selectedElement)!;
        element.x = click.clicked.x + dx;
        element.y = click.clicked.y + dy;
        store.updateElement(element, 'x');
        store.updateElement(element, 'y');
        console.log('dragging element', element);
    } else if (click.clicked.clickType === 'camera') {
        store.cameraX = click.clicked.cameraX - dx;
        store.cameraY = click.clicked.cameraY - dy;
        console.log('dragging camera', store.cameraX, store.cameraY);
    } else if (click.clicked.clickType === 'blockControl') {
        let element = store.elements.find(element => element.id === store.selectedElement)! as BlockElement;
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

function mouseUp() {
    // TODO if (!click.draggedEnough) open text options
    click = null;
}
</script>

<template>
    <canvas ref="canvas" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" />
</template>

<style scoped>
</style>