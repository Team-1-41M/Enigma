<script setup lang="ts">
import { useCommentsStore } from './store';
const store = useCommentsStore();
const projectsStore = useCurrentProjectStore();

onMounted(async () => {
    
})

await store.fetchCommentsAsync();
</script>

<template>
<div class="comments-wrapper">
    <CommentsItem 
        v-if="projectsStore.selectedElements.length === 0"
        v-for="item in store.comments.filter(c => c.parent_id === null)"
        :comment="item"/>
    <CommentsItem
        v-else
        v-for="item in store.comments.filter(c => c.component_id == projectsStore.selectedElements[0].id && c.parent_id === null)"
        :comment="item"/>
</div>    
</template>

<style scoped>
.comments-wrapper {
    width: 100%;
    height: 100%;
    background-color: var(--primary);
}
</style>