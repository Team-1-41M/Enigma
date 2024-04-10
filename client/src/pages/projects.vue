<script setup lang="ts">
import { useProjectStore } from '../stores/projects';

const userStore = useUserStore();
await userStore.fetchUser();
if (!userStore.user) navigateTo('/sign-in');
userStore.$subscribe((_, userStore) => {
    if (!userStore.user) navigateTo('/sign-in');
});

const store = useProjectStore();

store.fetchProjects();
</script>

<template>
    <Header/>
    <ProjectLayout
        :list="store.projectList"/>
</template>

<style>

</style>