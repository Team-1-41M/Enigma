<script setup lang="ts">
import { useProjectContextMenuStore } from '~/stores/projectContextMenu';
import type { Project } from '~/types/project';

interface Props {
    project: Project,
}
const props = defineProps<Props>();

const contextMenuStore = useProjectContextMenuStore();

const handleProjectClick = () => {
  navigateTo(`project/${props.project.id}`)
}

const handleRightClick = (event: MouseEvent) => {
  contextMenuStore.openMenu(props.project, event.clientX, event.clientY);
}
</script>

<template>
  <div class="project-wrapper"
  @contextmenu.prevent="handleRightClick">
    <div class="project-border" 
      @click="handleProjectClick"
      >
      <div class="cover-image"></div>
      <label class="project-name"> {{ project.title }} </label>
      <label class="project-last-updated">Изменено 0 д. назад</label>
      <!--
        TODO:Считать время для строчки сверху (сейчас мне лень)
        NOTE: Что-нибудь такое для обложек
        <img class="cover-image" 
        :src="`${config.public.baseUrl}/uploads/images/`" /> 
        -->
    </div> 
  </div>
</template>

<style scoped>
.project-wrapper {
  width: 19em;
  height: 14em;
  position: relative;
  background-color: #2F0D3B;
  border-radius: 9px;
}

.project-border {
  border: 1px solid transparent;
  border-radius: 9px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.project-border:hover {
  border: 1px solid var(--accent);
  cursor: pointer;
}

.project-wrapper:hover {
  cursor: pointer;
}

.cover-image {
  width: 93%;
  height: 70%;
  margin-top: 6px;
  border-radius: 7px;
  align-self: center;
  background-color: gray;
}

.delete-project-button {
  position: absolute;
  z-index: 10;
  bottom: 4px;
  right: 4px;

}

label {
  font-style: italic;
  font-weight: 400;
  letter-spacing: 0em;
  text-align: left;
  padding-top: 10px;
  padding-left: 3.5%;
}

.project-name {
  font-size: 15px;
  line-height: 18px;
}

.project-last-updated{ 
  font-size: 12px;
  line-height: 15px;
}
</style>