<script setup lang="ts">
import type { Project } from '~/types/project';

interface Props {
    list: Project[],
}
const props = defineProps<Props>();
</script>

<template>
    <div class="layout-wrapper">
        <ProjectAddButton></ProjectAddButton>
        <ProjectItem v-for="project in list" :project="project"/>
    </div>
</template>

<style scoped>
.layout-wrapper {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    width: 100%;
}
</style>