export type Comment = {
    id: number,
    project_id: number,
    component_id: string,
    component_name: string,
    user_id: string,
    created_at: string,
    updated_at: string,
    text: string,
    parent_id: number | null
}

export type CommentCreateRequest = {
    component_id: number,
    component_name: string,
    text: string,
    parent_id?: number,
}