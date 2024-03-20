<script setup lang="ts">
import type { Project } from '~/types/project';
const socketStore = useProjectWebSocketStore();

const handleClick = () => {
    socketStore.sendMessage(stringa.value)
}

const stringa = ref<string>('');
</script>

<template>
    <div class="edit-widget-wrapper">
        <div>{{ socketStore.elements }}</div>
        <input 
            type="text"
            v-model="stringa">
        <button 
            @click='handleClick'>
            Отправить
        </button>
    </div>
    
</template>

<style scoped>

</style>