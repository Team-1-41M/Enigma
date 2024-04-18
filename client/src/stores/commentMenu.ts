import { defineStore } from 'pinia'

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

  return {
    showMenu,
    elementId,
    comment,
    xCoord,
    yCoord,
    openMenu,
    closeMenu
  }
})
