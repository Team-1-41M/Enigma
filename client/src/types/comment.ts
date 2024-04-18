export type Comment = {
    id: number,
    componentId: number,
    componentName: string,
    authorName: string,
    createdAt: string,
    text: string,
    parentId: number | null
}