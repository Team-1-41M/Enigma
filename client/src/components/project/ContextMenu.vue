<script setup lang="ts">
import { useProjectContextMenuStore } from '~/stores/projectContextMenu';
import type { Project } from '~/types/project';

const store = useProjectContextMenuStore();

const emit = defineEmits<{
  'delete': [ project: Project ],
  'create': [ project: Project ],
  'edit': [ project: Project ],
}>();

const topValue = computed(() => {
  return `${store.yCoord}px`;
})

const leftValue = computed(() => {
  return `${store.xCoord}px`;
})

const handleDeletion = () => {
  emit('delete', store.project!); //TODO: Модалка с подтверждением наверное 
  store.closeMenu();
}

const handleEdit = () => {
  emit('edit', store.project!); //TODO: Точно модалка
  store.closeMenu();
}
</script>

<template>
  <Teleport to="body">
    <div 
      class="Project-item-menu-wrapper"
      v-if="store.showMenu">
        <ContextMenu
          :close-handler="store.closeMenu">
          <ContextMenuOption
            :text="'Переименовать'"
            @click="handleEdit"
            ></ContextMenuOption>
          <ContextMenuOption
            :text="'Удалить'"
            @click="handleDeletion"
            ></ContextMenuOption>
        </ContextMenu>
    </div>
  </Teleport>
</template>

<style scoped>
.Project-item-menu-wrapper {
  width: 20vw;
  position: absolute;
  top: v-bind(topValue);
  left: v-bind(leftValue);
  border-radius: 7px;
}
</style>