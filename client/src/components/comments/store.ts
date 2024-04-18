import { defineStore } from 'pinia'
import { getProjectCommentsAsync } from '~/actions/comments';

export const useCommentsStore = defineStore('commentsStore', () => {
  //TODO: Тип для коммента
  const comments = ref<any[]>([]);

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