<script setup lang="ts">
import { useProjectStore } from '../stores/projects';

const store = useProjectStore();

store.fetchProjects();
</script>

<template>
    <Header/>
    <ProjectLayout
        :list="store.projectList"/>
</template>

<style>

</style>