<script setup lang="ts">
import { useProjectStore } from '../stores/projects';

const store = useProjectStore();

store.projectList = [{
    id: 1,
    name: 'first'
}]

store.fetchProjects();
</script>

<template>
    <ProjectLayout
        :list="store.projectList"/>
</template>

<style>

</style>