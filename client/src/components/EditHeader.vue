<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { Project } from '~/types/project';
import { EditMode } from '~/types/editMode';
import ProfileMenu from './auth/ProfileMenu.vue';
import { useSignOutModalStore } from './auth/signOutModal/signOutModalStore';
import { useInviteModalStore } from './inviteModal/inviteModalStore'

const profileMenuStore = useProfileMenuStore();
const signOutModalStore = useSignOutModalStore();

const handleDisplayClick = (event: MouseEvent) => {
    profileMenuStore.openMenu();
}

const handleSignOut = () => {
    signOutModalStore.openModal()
}
const store = useCurrentProjectStore();
const route = useRoute();

const projectID = route.params.id as any;
const projectsStore = useProjectStore();

await projectsStore.fetchProjects();
const projectTitle = ref<string>(projectsStore.projectList.find(e => e.id == projectID)?.title ?? '')

const inviteModal = useInviteModalStore();

const openInviteModal = () => {
    inviteModal.openModal();
}

</script>

<template>
<header>
    <div class="logo">
        <img 
            src="~/assets/icons/logo.svg" 
            style="margin-left: 20px;"
            @click="navigateTo('/projects')"/>
        <h1>Enigma</h1>
    </div>
    <div class="mode-switcher">
        <Icon icon="carbon:move"
            :class="{'selected': store.currentMode === EditMode.Move}"
            @click="store.currentMode = EditMode.Move"/>
        <Icon 
            icon="radix-icons:frame"
            :class="{'selected': store.currentMode === EditMode.Block}"
            @click="store.currentMode = EditMode.Block"/>
        <!--NOTE: Нужно будет выпадающий селект ебануть (кастомный на дивах, встроенному хуй стили в лучшем браузере на земле хром пропишешь спасибо гугл)-->
        <!-- <Icon icon="ic:outline-square"
            :class="{'selected': store.currentMode === EditMode.Square}"
            @click="store.currentMode = EditMode.Square"/> -->
        <Icon icon="fluent:text-t-16-filled" 
            :class="{'selected': store.currentMode === EditMode.Text}"
            @click="store.currentMode = EditMode.Text"/>
        <Icon icon="la:hand-paper-solid"
            :class="{'selected': store.currentMode === EditMode.Camera}"
            @click="store.currentMode = EditMode.Camera"/>
    </div>
    <h2>
        {{ projectTitle }}
    </h2>
    <div class="share-button"
        @click="openInviteModal">
        Поделиться
    </div>
    <div class="user-display-container">
        <UserDisplay @click="handleDisplayClick" />
        <ProfileMenu
            @sign-out="handleSignOut" />
        <AuthSignOutModal />
    </div>
    <InviteModal/>
</header>

</template>

<style scoped>
header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    height: 75px;
    background-color: var(--primary);
    border-bottom: 2px solid var(--secondary)
}

h1 {
    font-weight: 400;
    font-style: italic;
    font-size: 24px;
    margin-left: 6px;
}

h2 {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);  
    font-family: Inter;
    font-size: 24px;
    font-style: italic;
    font-weight: 400;
    line-height: 29px;
    letter-spacing: -0.04em;
    text-align: left;
}

.share-button {
    background-color: var(--accent);
    color: var(--text);
    cursor: pointer;
    border-radius: 4px;
}

.logo {
    display: flex;
    flex: 0.3
}

.user-display-container {
    
    flex: 0.3;
}

.user-display {
    padding-right: 32px;
}

.mode-switcher {
    flex: 1
}

.mode-switcher svg {
    height: 75px;
    width: 40px;
    color: var(--text)
}

.mode-switcher svg:hover {
    transform: scale(1.1);
    background-color: var(--primary-darker);
}   

.selected {
    /*TODO*/
    border: 2px solid white
}
</style>