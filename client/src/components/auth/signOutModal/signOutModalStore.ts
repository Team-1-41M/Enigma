import { defineStore } from 'pinia'

export const useSignOutModalStore = defineStore('signOutModal', () => {
  const isVisible = ref(false);

  const openModal = () => {
    isVisible.value = true;
  }

  const closeModal = () => {
    isVisible.value = false;
  }

  return {
    isVisible,
    openModal,
    closeModal,
  }
})

