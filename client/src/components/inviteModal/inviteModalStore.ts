import { defineStore } from 'pinia'
import { getProjectShareLinkAsync } from '~/actions/projects';
import { type Project } from '~/types/project';

export const useInviteModalStore = defineStore('inviteModal', () => {
  const isVisible = ref(false);
  const email = ref('');

  const setShareLinkToClipBoardAsync = async (mode: 'edit' | 'read') => {
    const { projectID } = useCurrentProjectStore();
    const { addNotification } = useNotificationsStore();
    if (!projectID) {
      addNotification('Не найден id проекта', 'error');
    } else {
      const link = (window.location.href.split('/').slice(0, -1).concat((await getProjectShareLinkAsync(projectID, mode)).data.token).join('/'));
      navigator.clipboard.writeText(link)

      addNotification('Скопировано в буфер обмена', 'success', 3);
    }
  }

  const openModal = () => {
    isVisible.value = true;
  }

  const closeModal = () => {
    isVisible.value = false;
  }

  return {
    isVisible,
    email,
    setShareLinkToClipBoardAsync,
    openModal,
    closeModal,
  }
})

