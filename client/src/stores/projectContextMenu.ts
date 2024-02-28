import { defineStore } from 'pinia'
import type { Project } from '~/types/project';

export const useProjectContextMenuStore = defineStore('projectContextMenu', () => {
  const showMenu = ref(false);
  const project = ref(null as null | Project);
  const xCoord = ref(null as null | number);
  const yCoord = ref(null as null | number);

  const openMenu = (p: Project, x: number, y: number) => {
    showMenu.value = true;
    project.value = p;
    xCoord.value = x + 10;
    yCoord.value = y + 6;
  }

  const closeMenu = () => {
    showMenu.value = false;
    project.value = null;
  }

  return {
    showMenu,
    project,
    xCoord,
    yCoord,
    openMenu,
    closeMenu
  }
})
