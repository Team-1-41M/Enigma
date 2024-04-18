import { defineStore } from 'pinia'
import { getProjectCommentsAsync } from '~/actions/comments';
import type { Comment } from '~/types/comment';

export const useCommentsStore = defineStore('commentsStore', () => {
  //TODO: Тип для коммента
  const comments = ref<Comment[]>([]);

  const fetchCommentsAsync = async () => {
    comments.value = await getProjectCommentsAsync();
  }

  const createCommentAsync = async () => {

  }

  return {
    comments,
    fetchCommentsAsync,
    createCommentAsync
  }
})