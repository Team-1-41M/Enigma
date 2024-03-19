export type Frame = {
    id: number,
    name: string,
    X: number,
    Y: number,
    height: number,
    width: number,
    children: (TextElement | ContainerElement | ImageElement)[]
}

export type BaseElement = {
    id: number,
    name: string,
    X: number,
    Y: number,
    height: number,
    width: number,
}

export type TextElement = {
    fontWeight: string,
    alignment: ('center' | 'middle' | 'right')
}&BaseElement

export type ContainerElement = {
    borderRadius: number,
    children: (TextElement | ContainerElement | ImageElement)[]
}&BaseElement

export type ImageElement = {
    borderRadius: number,
    url: string
}&BaseElement