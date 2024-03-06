import { defineStore } from 'pinia'
import { type Project } from '~/types/project';

export const useDeleteConfirmationModalStore = defineStore('deleteConfirmationModal', () => {
  const isVisible = ref(false);
  const selectedProject = ref(null as null | Project);

  const openModal = (project?: Project) => {
    isVisible.value = true;
    selectedProject.value = project ?? null;
  }

  const closeModal = () => {
    isVisible.value = false;
    selectedProject.value = null;
  }

  return {
    isVisible,
    selectedProject,
    openModal,
    closeModal,
  }
})

