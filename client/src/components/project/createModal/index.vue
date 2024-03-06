<script setup lang="ts">
import { useCreateModalStore } from './createModalStore';

const store = useProjectStore() //
const modalStore = useCreateModalStore();

const handleConfirmation = async () => {
  await store.createProject(modalStore.newTitle);
  modalStore.closeModal();
}

const handleCancellation = () => {
  modalStore.closeModal();
}
</script>

<template>
  <ModalBase
    :is-visible="modalStore.isVisible">
    <div class="project-rename-modal-wrapper">
      <h2 class="modal-header">
        Название проекта
      </h2>
      <p class="modal-text">
        <input type="text" v-model="modalStore.newTitle" />  
      </p>
      <div class="modal-button-container">
        <button @click="handleConfirmation">
          Создать
        </button>
        <button @click="handleCancellation">
          Отмена
        </button>
      </div>
    </div>
  </ModalBase>
</template>

<style scoped>
.project-rename-modal-wrapper {
  background-color: var(--modal-background);
  padding: 25px 50px;
  width: 444px;
  border-radius: 7px;
  display: flex;
  flex-direction: column;
}

.modal-button-container {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

button {
  border-radius: 10px;
  border: none;
  padding: 5px 20px;
  font: inherit;
  cursor: pointer;
}

button:first-of-type {
  color: var(--text);
  background-color: var(--accent);
}

button:first-of-type:hover {
  filter: brightness(140%);
}

button:nth-of-type(2) {
  color: var(--text);
  background-color: transparent;
  border: 1px solid var(--text);
  box-sizing: border-box;
}

button:nth-of-type(2):hover {
  background-color: rgba(255, 255, 255, 0.2);
}

input {
  width: calc(100% - 30px);
  border-radius: 10px;
  border: none;
  background-color: #DEDBDB;
  padding: 5px 15px;
  font: inherit;
}

h2 {
  margin: 0;
  font-weight: inherit;
}
</style>