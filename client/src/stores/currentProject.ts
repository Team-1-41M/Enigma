import { defineStore } from 'pinia';

export type ElementID = string; // TODO UUID

export type BorderRadius = number | {
    topLeft: number,
    topRight: number,
    bottomRight: number,
    bottomLeft: number,
};

export type ColorRGB = {
    r: number,
    g: number,
    b: number,
};

// i wanted #${Hex}${Hex}${Hex}${Hex}${Hex}${Hex} but language server gave up
export type ColorHEX = `#${string}`;

export type Color = ColorRGB | ColorHEX; // TODO ColorHSV, ColorRGBA, etc

export type Background = Color;

export type Border = {
    color: Color,
    width: number,
    style: 'solid' | 'dashed' | 'dotted',
};

export type Borders = 'none' | Border | {
    top: Border,
    right: Border,
    bottom: Border,
    left: Border,
};

export type BlockElement = {
    id: ElementID,
    type: 'block',
    x: number,
    y: number,
    width: number,
    height: number,
    borderRadius: BorderRadius,
    background: Background,
    borders: Borders,
    // TODO shadow
};

export function createBlockElement(edit?: (el: BlockElement) => void) {
    let el = {
        id: '',
        type: 'block',
        x: 0,
        y: 0,
        width: 100,
        height: 100,
        borderRadius: 0,
        background: '#ffffff',
        borders: 'none',
    } as BlockElement;
    if (edit) edit(el);
    return el;
}

export type TextElement = {
    id: ElementID,
    type: 'text',
    x: number,
    y: number,
    fontSize: number,
    fontFamily: 'Roboto', // TODO
    fontWeight: 'normal', // TODO
    fontStyle: 'normal', // TODO
    color: Color,
    content: string,
};

export function createTextElement(edit?: (el: TextElement) => void) {
    let el = {
        id: '',
        type: 'text',
        x: 0,
        y: 0,
        fontSize: 12,
        fontFamily: 'Roboto',
        fontWeight: 'normal',
        fontStyle: 'normal',
        color: '#000000',
        content: '',
    } as TextElement;
    if (edit) edit(el);
    return el;
}

export type ProjectElement = BlockElement | TextElement;

export const useCurrentProjectStore = defineStore('currentProject', {
    state: () => ({
        elements: [] as ProjectElement[],
        cameraX: 0,
        cameraY: 0,
        // TODO zoom
        selectedElement: null as null | ElementID,
    }),
    actions: {
        async createBlockElement(edit?: (el: BlockElement) => void): Promise<BlockElement> {
            const el = createBlockElement(edit);
            el.id = this.$state.elements.length.toString();
            await this.addBlock(el);
            return el;
        },
        async createTextElement(edit?: (el: TextElement) => void): Promise<TextElement> {
            const el = createTextElement(edit);
            el.id = this.$state.elements.length.toString();
            await this.addText(el);
            return el;
        },
        async addBlock(el: BlockElement) {
            this.elements.push(el);
            // TODO send `Create {id: el.id, type: 'block'}`
        },
        async addText(el: TextElement) {
            this.elements.push(el);
            // TODO send `Create {id: el.id, type: 'text'}`
        },
        async removeElement<E extends ProjectElement>(el: E) {
            this.elements = this.elements.filter(e => e.id !== el.id);
            // TODO send `Delete {id}`
        },
        async updateElement<E extends ProjectElement>(el: E, changedAttribute: keyof E) {
            this.elements = this.elements.map(e => e.id === el.id ? { ...e, [changedAttribute]: el[changedAttribute] } : e);
            // TODO send `Update {id: el.id, [changedAttribute]: el[changedAttribute]}`
        }
    }
})