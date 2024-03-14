import { defineStore } from 'pinia'
import { type Project } from '~/types/project';

export const useRenameModalStore = defineStore('renameModal', () => {
  const isVisible = ref(false);
  const selectedProject = ref(null as null | Project);
  const newTitle = ref('');

  const openModal = (project: Project) => {
    isVisible.value = true;
    selectedProject.value = project;
    newTitle.value = project.title ?? '';
  }

  const closeModal = () => {
    isVisible.value = false;
    selectedProject.value = null;
    newTitle.value = '';
  }

  return {
    isVisible,
    selectedProject,
    newTitle,
    openModal,
    closeModal,
  }
})

