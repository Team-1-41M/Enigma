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
        Удалить проект
      </h2>
      <p class="modal-text">Вы собираетесь удалить проект {{ modalStore.selectedProject!.title }}</p>
      <div class="modal-button-container">
        <button class="modal-confirm-button" @click="handleConfirmation">
          Удалить
        </button>
        <button class="modal-reject-button" @click="handleCancellation">
          Отмена
        </button>
      </div>
    </div>
  </ModalBase>
</template>

<style scoped>
.project-delete-modal-wrapper {
  background-color: var(--modal-background);
  padding: 25px 50px;
  width: 444px;
  border-radius: 7px;
  display: flex;
  flex-direction: column;
}

.modal-button-container {
  margin-left: auto;
  display: flex;
  gap: 7px;
}

button {
  border-radius: 7px;
  padding: 5px 20px;
  cursor: pointer;
  font: inherit;
  color: var(--text);
}

.modal-confirm-button {
  background-color: var(--accent);
  border: none;
}

.modal-confirm-button:hover {
  filter: brightness(140%);
}

.modal-reject-button {
  background-color: transparent;
  border: 1px solid var(--text); 
}

.modal-reject-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

p, h2 {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
}

h2 {
  margin: 0;
  font-weight: inherit;
  size: 20px;
  line-height: 24px;
}
</style>