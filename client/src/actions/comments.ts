import type { Comment } from "~/types/comment"

export const getProjectCommentsAsync = async (): Promise<Comment[]> => {
    return [{
        id: 11,
        componentId: '1',
        componentName: 'Блок 1',
        authorName: 'Login',
        createdAt: '2024-04-17T20:32:04.314Z',
        text: 'Текст комментария',
        parentId: null
    }]
}