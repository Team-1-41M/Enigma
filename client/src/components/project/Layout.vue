<script setup lang="ts">
import { useProjectContextMenuStore } from '~/stores/projectContextMenu';
import type { Project } from '~/types/project';
import { useCreateModalStore } from './createModal/createModalStore';
import { useRenameModalStore } from './renameModal/renameModalStore';
import { useDeleteConfirmationModalStore } from './deleteConfirmationModal/deleteConfirmationModalStore';

interface Props {
    list: Project[],
}
const props = defineProps<Props>();

const contextMenuStore = useProjectContextMenuStore();
const createModalStore = useCreateModalStore();
const renameModalStore = useRenameModalStore();
const deleteModalStore = useDeleteConfirmationModalStore();

const handleCreate = () => {
    createModalStore.openModal()
}

const handleRename = (project: Project) => {
    renameModalStore.openModal(project)
}

const handleDeletion = (project: Project) => {
    deleteModalStore.openModal(project)
}
</script>

<template>
    <div class="layout-wrapper">
        <ProjectAddButton @create="handleCreate" />
        <ProjectItem v-for="project in list" :project="project"/>
    </div>
    <ProjectContextMenu
        @rename="handleRename"
        @delete="handleDeletion"/>
    <ProjectCreateModal/>
    <ProjectRenameModal/>
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