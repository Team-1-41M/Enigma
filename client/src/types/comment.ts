export type Comment = {
    id: number,
    componentId: string,
    componentName: string,
    authorName: string,
    createdAt: string,
    text: string,
    parentId: number | null
}