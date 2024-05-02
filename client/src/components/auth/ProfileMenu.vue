<script setup lang="ts">
import { useProfileMenuStore } from '~/stores/profileMenu';

const store = useProfileMenuStore();
const userStore = useUserStore();

const emit = defineEmits<{
    'signOut': [],
}>();

const handleSignOut = () => {
    emit('signOut');
    store.closeMenu();
}
</script>

<template>
    <div class="Project-item-menu-wrapper" v-if="store.showMenu">
        <ContextMenu :close-handler="store.closeMenu">
            <div class="user">
                <div class="avatar">
                    <span>{{ userStore.user?.name?.charAt(0) }}</span>
                </div>
                <span class="name">{{ userStore.user?.name }}</span>
                <span class="email">{{ userStore.user?.email }}</span>
            </div>
            <ContextMenuOption :text="'Выйти'" @click="handleSignOut"></ContextMenuOption>
        </ContextMenu>
    </div>
</template>

<style scoped>
.user {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px 20px;
    border-radius: 10px;
    background-color: #1E0825;
    color: var(--text);
    cursor: pointer;
    z-index: 10000000000000000
}

.name {
    font-weight: 500;
    margin-bottom: 5px;
}

.email {
    color: #ADADAD;
    font-size: 0.8em;
}

.avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-bottom: 10px;
    width: 1.5em;
    height: 1.5em;
    font-size: 1.5em;
    border-radius: 10em;
    background-color: var(--accent);
    border: 1px solid #CBCFD5;
}

.Project-item-menu-wrapper {
    width: 20vw;
    position: absolute;
    top: 59px;
    right: 32px;
    border-radius: 7px;
    z-index: 1;
}
</style>