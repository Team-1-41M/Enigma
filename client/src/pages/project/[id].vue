<script setup lang="ts">
import EditHeader from '~/components/EditHeader.vue';
import { useProjectWebSocketStore } from '~/stores/projectWebSocket';

const route = useRoute();

const projectId = route.params.id as string;

const socketStore = useProjectWebSocketStore();

socketStore.loadProject(projectId); 
</script>

<template>
    <div class="project-page-wrapper">
        <EditHeader
            class="header"/>
        <ComponentTree/>
        <EditWidget/>
        <AttributesEdit/>
    </div>
</template>

<style scoped>
.project-page-wrapper {
    height: 100%;
    display: grid; 
    grid-template-columns: 0.3fr 1fr 0.3fr; 
    grid-template-rows: 0.06fr 0.94fr; 
    grid-template-areas: 
        "header header header"
        ". . ."; 
}
.header { 
    grid-area: header; 
    height: auto
}
</style>