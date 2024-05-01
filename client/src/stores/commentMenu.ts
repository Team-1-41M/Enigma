import { defineStore } from 'pinia'
import { createCommentAsync } from '~/actions/comments';
import type { CommentCreateRequest } from '~/types/comment';

export const useCommentMenuStore = defineStore('commentMenu', () => {
  const showMenu = ref(false);
  const elementId = ref(null as null | string);
  const comment = ref<string>('');
  const xCoord = ref(null as null | number);
  const yCoord = ref(null as null | number);

  const openMenu = (e: string, x: number, y: number) => {
    showMenu.value = true;
    elementId.value = e;
    xCoord.value = x;
    yCoord.value = y;
  }

  const closeMenu = () => {
    showMenu.value = false;
    comment.value = '';
    elementId.value = null;
  }

  const saveCommentAsync = async (parentId?: string, commentText?: string) => {
    const projectStore = useCurrentProjectStore(); 

    const commentModel: CommentCreateRequest = {
      component_id: elementId.value as unknown as number,
      component_name: projectStore.elements.find(e => e.id === elementId.value)!.name,
      text: commentText ? commentText : comment.value,
      parent_id: parentId as unknown as number ?? null
    }

    await createCommentAsync(projectStore.projectID!, commentModel)

    closeMenu();
  }

  return {
    showMenu,
    elementId,
    comment,
    xCoord,
    yCoord,
    openMenu,
    closeMenu,
    saveCommentAsync
  }
})
