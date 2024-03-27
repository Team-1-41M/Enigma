<script setup lang="ts">
import  { useNotificationsStore } from '~/stores/notifications';

interface Props {
    notification: {
        id: string,
        text: string,
        type: string,
        duration: number
    }
}
const props = defineProps<Props>();
const store = useNotificationsStore();

setTimeout(() => {
    store.removeNotification(props.notification.id)
}, props.notification.duration * 1000);

const duration = computed(() => {
  return `${props.notification.duration}s`;
})

</script>

<template>
  <li 
    class="notification-container"
    :class="notification.type"
    @click="store.removeNotification(notification.id)">
      <h3>{{notification.text}}</h3>
      <div class="loader-line">
      </div>
  </li>

</template>

<style scoped>
.success {
  background-color: var(--success);
}

.success > .loader-line {
  background-color: var(--success-lighter);
}

.error {
  background-color: var(--error);
}

.error > .loader-line {
  background-color: var(--error-lighter);
}

.notification-container {
  list-style: none;
  margin: 0 0 1rem;
  padding-left: 1rem;
  border-radius: 8px;
  position: relative;
  color: white;
}

h3 {
  margin-top: $gap;
  font-size: $medium;
  display: inline-block;
}

.loader-line {
  width: 100%;
  height: 0.25em;
  position: absolute;
  float: left;
  bottom: 0;
  border-radius: 0 8px 8px 8px;
  animation: progressAnimation linear forwards;
  animation-duration: v-bind(duration);
}

@keyframes progressAnimation {
  from { width: 100% }
  to   { width: 1% }
}
</style>