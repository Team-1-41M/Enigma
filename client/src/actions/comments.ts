import type { Comment, CommentCreateRequest } from "~/types/comment"

export const getProjectCommentsAsync = async (projectId: number): Promise<Comment[]> => {
    const { $api } = useNuxtApp();

    const response = await $api.get(`projects/projects/${projectId}/comments`);
    return response.data as Comment[];
}

export const createCommentAsync = async (projectId: number, comment: CommentCreateRequest): Promise<void> => {
    const { $api } = useNuxtApp();

    await $api.post(`projects/projects/${projectId}/comments`, comment);
    return ;
}