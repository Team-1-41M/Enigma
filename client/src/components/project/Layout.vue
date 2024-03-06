<script setup lang="ts">
import { useProjectContextMenuStore } from '~/stores/projectContextMenu';
import type { Project } from '~/types/project';
import { useDeleteConfirmationModalStore } from './deleteConfirmationModal/deleteConfirmationModalStore';

interface Props {
    list: Project[],
}
const props = defineProps<Props>();

const contextMenuStore = useProjectContextMenuStore();
const deleteModalStore = useDeleteConfirmationModalStore();

const handleDeletion = (project: Project) => {
    deleteModalStore.openModal(project)
}
</script>

<template>
    <div class="layout-wrapper">
        <ProjectAddButton></ProjectAddButton>
        <ProjectItem v-for="project in list" :project="project"/>
    </div>
    <ProjectContextMenu
        @delete="handleDeletion"/>
    <ProjectDeleteConfirmationModal/>
</template>

<style scoped>
.layout-wrapper {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    width: 100%;
    height: 100%;
    padding: 40px;
    background-color: var(--primary);
}
</style>