import { defineStore } from 'pinia'
import { getProjectCommentsAsync } from '~/actions/comments';
import type { Comment } from '~/types/comment';

export const useCommentsStore = defineStore('commentsStore', () => {
  const comments = ref<Comment[]>([]);

  const fetchCommentsAsync = async () => {
    const { projectID } = useCurrentProjectStore();
    console.log(await getProjectCommentsAsync(projectID!))
    comments.value = await getProjectCommentsAsync(projectID!);
    console.log(comments.value)
  }

  const createCommentAsync = async () => {

  }

  return {
    comments,
    fetchCommentsAsync,
    createCommentAsync
  }
})