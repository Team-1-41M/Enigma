<script setup lang="ts">
import type { Project } from '~/types/project';

const socketStore = useProjectWebSocketStore();
  
</script>

<template>
    <div class="attribute-wrapper">
        <p>Attr</p>
    </div>
    
</template>

<style scoped>
.attribute-wrapper {
    width: 100%;
    height: 100%;
    background-color: var(--primary);
}
</style>