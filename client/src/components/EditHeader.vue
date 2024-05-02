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
            <img src="~/assets/icons/logo.svg" style="margin-left: 20px;" @click="navigateTo('/projects')" />
            <h1>Enigma</h1>
        </div>
        <div class="mode-switcher">
            <span :class="{ 'selected': store.currentMode === EditMode.Move }"
                @click="store.currentMode = EditMode.Move">
                <Icon icon="carbon:move" />
            </span>
            <span :class="{ 'selected': store.currentMode === EditMode.Block }"
                @click="store.currentMode = EditMode.Block">
                <Icon icon="radix-icons:frame" />
            </span>
            <span :class="{ 'selected': store.currentMode === EditMode.Text }"
                @click="store.currentMode = EditMode.Text">
                <Icon icon="fluent:text-t-16-filled" />
            </span>
            <span :class="{ 'selected': store.currentMode === EditMode.Camera }"
                @click="store.currentMode = EditMode.Camera">
                <Icon icon="la:hand-paper-solid" />
            </span>
            <span :class="{ 'selected': store.currentMode === EditMode.Comments }"
                @click="store.currentMode = EditMode.Comments">
                <Icon icon="iconamoon:comment-light" />
            </span>
        </div>
        <h2>
            {{ projectTitle }}
        </h2>
        <div class="share-button" @click="openInviteModal">
            Поделиться
        </div>
        <div class="user-display-container">
            <div>
                <UserDisplay @click="handleDisplayClick" />
                <ProfileMenu @sign-out="handleSignOut" />
                <AuthSignOutModal />
            </div>
        </div>
        <InviteModal />
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
    padding: 5px 7px;
}

.logo {
    width: 275px;
    display: flex;
}

.user-display-container {
    width: 275px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.user-display {
    padding-right: 32px;
}

.mode-switcher {
    flex: 1;
}

.mode-switcher span {
    display: inline-flex;
    height: 75px;
    width: 50px;
    align-items: center;
    justify-content: center;
}

.mode-switcher svg {
    color: var(--text);
    height: 45px;
    width: 45px;
}

.mode-switcher span:hover {
    transform: scale(1.1);
    filter: brightness(1.2);
}

.mode-switcher span:not(.selected):hover {
    background-color: var(--primary-darker);
}

.selected {
    background-color: var(--accent);
}
</style>