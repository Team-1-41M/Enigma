import { defineStore } from 'pinia'

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref([] as Array<{
    id: string,
    text: string,
    type: string,
    duration: number
  }>);

  /**
   * Creates toast notification in bottom right corner of the screen. It will dissapear automatically.
   * If it doesn't appear, make sure you've added <Notifications/> to the page 
   * @param notificationText Self explanatory
   * @param notificationDuration Time until the notification dissapears in seconds. 5 seconds by default
   * @param notificationType 'error' - red one, bad. 'success' - green one, good.
   */
  const addNotification = (notificationText: string, notificationType: 'error' | 'success', notificationDuration=5) => {
    notifications.value.push({
      id: Math.random().toString(16),
      text: notificationText,
      type: notificationType,
      duration: notificationDuration,
    })
  }

  const removeNotification = (id: string) => {
    notifications.value = notifications.value.filter(n => n.id !== id);
  }

  return {
    notifications,
    addNotification,
    removeNotification
  }
})