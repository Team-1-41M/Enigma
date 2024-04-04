<script setup lang="ts">
import { useUserStore } from '~/stores/user';

const userStore = useUserStore();

userStore.fetchUser();
</script>

<template>
    <div class="parent">
        <div>
            <span>{{ userStore.user?.name?.charAt(0) }}</span>
        </div>
        <span>{{ userStore.user?.name }}</span>
    </div>
</template>

<style scoped>
.parent {
    display: flex;
    align-items: center;
    padding: 10px 20px;
    border-radius: 10px;
    background-color: #1E0825;
    color: var(--text);
    cursor: pointer;
}

.parent > div {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-right: 10px;
    width: 1.5em;
    height: 1.5em;
    border-radius: 10em;
    background-color: var(--accent);
    border: 1px solid #CBCFD5;
}

.parent > div > span {
    position: absolute;
}
</style>