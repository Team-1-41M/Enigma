<script setup lang="ts">
import { Icon } from '@iconify/vue';

const projectStore = useProjectStore();

const handleClick = () => {
    //TODO: Открытие модалки тут
    projectStore.createProject('test');
}

</script>

<template>
    <div class="project-add-button-wrapper"
    @click="handleClick">
        <Icon 
            class="alert-icon"
            icon="majesticons:file-plus">
        </Icon>
    </div>
</template>

<style scoped>
.project-add-button-wrapper {
    width: 19em;
    height: 14em;
    text-align: center;
    border: 1px solid transparent;
    border-radius: 9px;  
    background-color: #492149;
}

.project-add-button-wrapper:hover {
    border: 1px solid var(--accent);
    cursor: pointer;
}

.alert-icon {
    display: block;
    margin: auto;
    position: relative;
    top: 50%;
    color: var(--accent);
    -ms-transform: translateY(-50%);
    transform: translateY(-50%);
    font-size: 60px;
}
</style>