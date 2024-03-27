<script setup lang="ts">
import EditHeader from '~/components/EditHeader.vue';

const route = useRoute();

const projectID = route.params.id as any;

const socketStore = useCurrentProjectStore();
socketStore.projectID = projectID;

await socketStore.socket; // FIXME show "Connecting..." modal (or toast, or anything else)
</script>

<template>
    <div class="project-page-wrapper">
        <EditHeader class="header" />
        <ComponentTree :tree="socketStore.elements" />
        <EditWidget />
        <AttributesEdit />
    </div>
</template>

<style scoped>
.project-page-wrapper {
    height: 100%;
    display: grid;
    grid-template-columns: 0.3fr 1fr 0.3fr;
    grid-template-rows: 0.06fr 1fr;
    grid-template-areas:
        "header header header"
        ". . .";
}

.header {
    grid-area: header;
    height: auto
}
</style>