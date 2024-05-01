<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { useCommentsStore } from './store';

const store = useCommentMenuStore();
const commentsStore = useCommentsStore();

const topValue = computed(() => {
  return `${store.yCoord}px`;
})

const leftValue = computed(() => {
  return `${store.xCoord}px`;
})

const handleCancellation = () => {
  store.closeMenu();
}

const handleSave = async () => {
  if (store.comment.length > 0) {
    await store.saveCommentAsync();
  }
  store.closeMenu();
  await commentsStore.fetchCommentsAsync();
}

const commentInput = ref<HTMLInputElement>();

const onMenuOpen = () => {
  (commentInput.value as HTMLInputElement).focus()
}
</script>

<template>
  <Teleport to="body">
    <div 
      class="comment-menu-wrapper"
      v-if="store.showMenu">
        <ContextMenu
          :close-handler="store.closeMenu"
          :open-handler="onMenuOpen">
          <div>
            <div class="create-menu-wrapper">
              <Icon class="comment" icon="iconamoon:comment-fill"/>
              <input type="text" v-model="store.comment" ref="commentInput" @blur="store.closeMenu" placeholder="Введите комментарий">
              <Icon class="send" icon="ph:arrow-circle-up-fill" @click.stop="handleSave"/>
            </div>
            <div v-if="store.comment.length > 0">
              <div class="horisontal">
                <Icon class="send" icon="ph:at-light"/>
                <Icon class="send" icon="circum:image-on"/>
              </div>
            </div>
          </div>
        </ContextMenu>
    </div>
  </Teleport>
</template>

<style scoped>
.comment-menu-wrapper {
  height: fit-content;
  background-color: var(--primary-light);
  border-radius: 8px;
  position: absolute;
  top: v-bind(topValue);
  left: v-bind(leftValue);
  border-radius: 7px;
}

.comment {
  height: 40px;
  width: 40px;
  margin: 4px;
  color: var(--accent);
}

.send {
  height: 31px;
  width: 31px;
  margin-right: 8px;
  color: var(--text);
  align-self: center;
}

.send:hover {
  transition: all 200ms;
  color: var(--accent)
}

input {
  height: 45px;
  background-color: transparent;
  color: var(--text)
}

input:focus {
  border: none;
  outline: none;
}

.create-menu-wrapper {
  display: flex;
}

::placeholder {
  color: var(--text);
  opacity: 0.7;
}
</style>