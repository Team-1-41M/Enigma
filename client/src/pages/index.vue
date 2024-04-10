<script setup lang="ts">
const userStore = useUserStore();
await userStore.fetchUser();
if (!userStore.user) navigateTo('/sign-in');
else navigateTo('/projects');
userStore.$subscribe((_, userStore) => {
    if (!userStore.user) navigateTo('/sign-in');
    else navigateTo('/projects');
});
</script>

<template>
</template>

<style>

</style>