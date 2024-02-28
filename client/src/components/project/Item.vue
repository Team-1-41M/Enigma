<script setup lang="ts">
import type { Project } from '~/types/project';

interface Props {
    project: Project,
}
const props = defineProps<Props>();

const handleProjectClick = () => {
  //TODO: NavigateTo по айдишнику
}

const handleDeletion = () => {
  //TODO: Удаление
}
</script>

<template>
    <div class="project-wrapper">
    <div class="project-border" @click="handleProjectClick">
      <p> {{ project.name }} </p>
      <div class="cover-image"></div>
      <!--NOTE: Что-нибудь такое для обложек 
        <img class="cover-image" 
        :src="`${config.public.baseUrl}/uploads/images/`" /> 
        -->
    </div> 
  </div>
</template>

<style>
.project-wrapper {
  width: 14em;
  height: 20em;
  position: relative;
}

.project-border {
  border: 2px solid white;
  border-radius: 10px;
  height: 100%;
}

.project-wrapper:hover {
  cursor: pointer;
}

.cover-image {
  width: 100%;
  height: 70%;
  background-color: gray;
}

.delete-project-button {
  position: absolute;
  z-index: 10;
  bottom: 4px;
  right: 4px;

}
</style>