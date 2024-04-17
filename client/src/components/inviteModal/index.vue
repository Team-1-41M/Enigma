<script setup lang="ts">
import { Icon } from '@iconify/vue/dist/iconify.js';
import { useInviteModalStore } from './inviteModalStore';

const modalStore = useInviteModalStore();

const mode = ref<'edit' | 'read'>('edit');

const handleConfirmation = async () => {
  modalStore.setShareLinkToClipBoardAsync(mode.value);
}

const handleClosing = () => {
  modalStore.closeModal();
}

const handleEmailSend = () => {
  //TODO: В далеком будущем
}
</script>

<template>
  <ModalBase
    :is-visible="modalStore.isVisible">
    <div class="project-invite-modal-wrapper">
      <div class="modal-row">
        <h2 class="modal-header">
          Поделиться проектом
        </h2>
        <Icon 
          class="close-icon"
          @click="handleClosing"
          icon="mdi:close"/>
      </div>
      
      <div class="modal-row">
        <input type="text" v-model="modalStore.email" placeholder="Email"/>  
        <button @click="handleEmailSend">
          Пригласить
        </button>
      </div >
      <div class="modal-row">
        <Icon class="network-icon" icon="zondicons:network"/>
        <label>Любой, у кого есть ссылка</label>
        <select v-model="mode">
          <option value="read">Может просмотреть</option>
          <option value="edit">Может редактировать</option>
        </select>
      </div >
        
      <div class="get-link" @click="handleConfirmation">
        <Icon icon="teenyicons:link-solid"/>
        Копировать ссылку
      </div>
    </div>
  </ModalBase>
</template>

<style scoped>
.close-icon {
  height: 40px;
  width: 40px;  
}

select {
  background-color: transparent;
  color: var(--text);
  outline: #DF4848;
}

.network-icon {
  color: var(--text)
}

option {
  background-color: var(--primary-darker);
  color: var(--text)
}

.project-invite-modal-wrapper {
  background-color: var(--primary);
  padding: 25px 50px;
  border-radius: 7px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-row {
  display: flex;
  gap: 8px;
  justify-content: space-between;
  align-items: center;
  color: var(--text)
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

h2 {
  margin: 0;
  font-weight: inherit;
}

input {
  height: 43px;
  background-color: transparent;
  border: none;
  color: var(--text);
  font-family: Inter;
  font-size: 16px;
  font-weight: 400;
  line-height: 19.36px;
  letter-spacing: -0.04em;
  text-align: left;
  border: 1px solid transparent;
}

input:focus {
  border: 1px solid var(--accent);
}

.get-link {
  color: #DF4848;
  cursor: pointer;
}

.get-link:hover {
  color: hsl(0, 70%, 70%);
  cursor: pointer;
}
</style>