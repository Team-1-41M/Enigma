<script setup lang="ts">

</script>

<template>
    <header>
        <img src="~/assets/icons/logo.svg" alt="Discover Nuxt 3" />
        <h1>Enigma</h1>
    </header>
</template>

<style scoped>
header {
    display: flex;
    align-items: center;
    box-sizing: border-box;
    height: 7vh;
    padding-left: 1vw;
    background-color: var(--primary);
    border-bottom: 2px solid var(--secondary)
}

h1 {
    font-weight: 400;
    font-style: italic;
    font-size: 24px;
    margin-left: 6px;
}

</style>