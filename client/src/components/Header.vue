<script setup lang="ts">

</script>

<template>
    <header>
        <img src="~/assets/icons/logo.svg" 
            @click="navigateTo('/projects')"/>
        <h1>Enigma</h1>
        <div class="spacer" />
        <UserDisplay 
            @click="navigateTo('/sign-in')"/>
    </header>
</template>

<style scoped>
header {
    display: flex;
    align-items: center;
    box-sizing: border-box;
    height: 75px;
    padding: 20px 32px;
    background-color: var(--primary);
    border-bottom: 2px solid var(--secondary)
}

.spacer {
    flex-grow: 1;
}

h1 {
    font-weight: 400;
    font-style: italic;
    font-size: 24px;
    margin-left: 6px;
}

</style>