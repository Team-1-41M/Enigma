<script setup lang="ts">
import  { useNotificationsStore } from '~/stores/notifications';

const store = useNotificationsStore();
</script>

<template>
  <TransitionGroup name="list" tag="ul" class="notification-list-container">
    <NotificationsItem 
      v-for="notification in store.notifications"
      :notification="notification"
      :key="notification.id"/>
  </TransitionGroup>
</template>

<style scoped>
.notification-list-container {
  position: fixed;
  right: 10px;
  bottom: 10px;
  margin-bottom: 0;
  width: 35em;
  z-index: 1001;
}

.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-active {
  position: absolute;
}
</style>