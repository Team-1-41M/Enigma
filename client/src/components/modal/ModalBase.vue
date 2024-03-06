<script setup lang="ts">
interface Props {
  isVisible: boolean
}
const props = defineProps<Props>();
</script>

<template>
    <Teleport to="body">
      <div :class="isVisible ? 'modal-background-active' : 'modal-background-inactive'">
        <Transition name="modal"> 
          <slot v-if="props.isVisible"/>
        </Transition>
      </div>
    </Teleport>
</template>

<style scoped>
.modal-enter-active {
  animation: bounce-in 0.3s;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.modal-background-active {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  position: absolute;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-background-inactive {
  display: none;
}
</style>