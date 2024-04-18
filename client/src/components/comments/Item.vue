<script setup lang="ts">
const props = defineProps<{
    //TODO: Тип для коммента
    comment: any
}>()
</script>

<template>
<div class="comment-wrapper">
    <p>{{comment.componentName}}</p>
</div>    
</template>

<style scoped>
.comments-wrapper {
    width: 100%;
    height: 100%;
    background-color: var(--primary);
}
</style>