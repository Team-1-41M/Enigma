<script setup lang="ts">
import { Icon } from '@iconify/vue';

const handleClick = () => {
    //TODO: Создание проекта, переход к нему через navigateTo
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
    width: 14em;
    height: 20em;
    text-align: center;
    border-radius: 4px;  
    background-color: var(--primary);
}

.project-add-button-wrapper:hover {
    background-color: var(--primary-light);
    cursor: pointer;
}

.alert-icon {
    display: block;
    margin: auto;
    position: relative;
    top: 50%;
    color: var(--text);
    -ms-transform: translateY(-50%);
    transform: translateY(-50%);
    font-size: 60px;
}
</style>