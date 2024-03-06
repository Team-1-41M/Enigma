<script setup lang="ts">
import { useDeleteConfirmationModalStore } from './deleteConfirmationModalStore';

const store = useProjectStore() //
const modalStore = useDeleteConfirmationModalStore();

const handleConfirmation = async () => {
  await store.deleteProject(modalStore.selectedProject!.id);
  modalStore.closeModal();
}

const handleCancellation = () => {
  modalStore.closeModal();
}
</script>

<template>
  <ModalBase
    :is-visible="modalStore.isVisible">
    <div class="project-delete-modal-wrapper">
      <h2 class="modal-header">
        Удаление проекта
      </h2>
      <p class="modal-text">Вы собираетесь удалить проект {{ modalStore.selectedProject!.title }}</p>
      <div class="modal-button-container">
        <button @click="handleConfirmation">
          Удалить
        </button>
        <button @click="handleCancellation">
          Отмена
        </button>
      </div>
    </div>
  </ModalBase>
</template>

<style scoped>
.project-delete-modal-wrapper {
  background-color: var(--modal-background);
  padding: 1%;
  width: 444px;
  border-radius: 7px;
  display: flex;
  flex-direction: column;
  gap: $gap;
}

h2 {
  margin-top: 0
}
</style>