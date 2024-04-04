import { defineStore } from 'pinia'
import type { Project } from '~/types/project';

export const useProfileMenuStore = defineStore('profileMenu', () => {
  const showMenu = ref(false);

  const openMenu = () => {
    showMenu.value = true;
  }

  const closeMenu = () => {
    showMenu.value = false;
  }

  return {
    showMenu,
    openMenu,
    closeMenu
  }
})
