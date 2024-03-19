<script setup lang="ts">
import type { Project } from '~/types/project';

const socketStore = useProjectWebSocketStore();

</script>

<template>
    <div class="components-tree-wrapper">
        <p>{{socketStore.elements}}</p>
    </div>
</template>

<style scoped>
.components-tree-wrapper {
    width: 100%;
    height: 100%;
    background-color: var(--primary);
}
</style>