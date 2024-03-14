import { defineStore } from 'pinia'
import { type Project } from '~/types/project';

export const useCreateModalStore = defineStore('createModal', () => {
  const isVisible = ref(false);
  const newTitle = ref('');

  const openModal = () => {
    isVisible.value = true;
    newTitle.value = '';
  }

  const closeModal = () => {
    isVisible.value = false;
    newTitle.value = '';
  }

  return {
    isVisible,
    newTitle,
    openModal,
    closeModal,
  }
})

