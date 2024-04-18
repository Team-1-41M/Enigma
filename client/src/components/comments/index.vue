<script setup lang="ts">
import { useCommentsStore } from './store';
const store = useCommentsStore()

onMounted(() => {
    store.fetchCommentsAsync();
})
</script>

<template>
<div class="comments-wrapper">
    <CommentsItem 
        v-for="item in store.comments"
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