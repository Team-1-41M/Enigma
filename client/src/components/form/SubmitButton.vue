<script setup lang="ts">
</script>

<template>
    <button type="submit">
        <slot />
    </button>
</template>

<style scoped>
button {
    font-family: inherit;
    font-weight: 400;
    color: var(--text);
    border: none;
    display: block;
    float: right;
    width: 172px;
    background-color: var(--auth-primary);
    border-radius: 50px;
    height: 50px;
}
</style>