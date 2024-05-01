<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { useCommentsStore } from './store';

const props = defineProps<{
  parentId: number,
}>();

const comment = defineModel<string>('comment');

const emit = defineEmits(['close']);

const store = useCommentMenuStore();
const commentsStore = useCommentsStore();

const projectStore = useCurrentProjectStore();

const handleSave = async () => {
  await store.saveCommentAsync(props.parentId, comment.value);
  await commentsStore.fetchCommentsAsync();
  emit('close');
}
</script>

<template>
  <div v-if="projectStore.selectedElements.length === 1">
    <div class="create-menu-wrapper">
      <Icon class="comment" icon="iconamoon:comment-fill"/>
      <input type="text" v-model="comment" ref="commentInput" placeholder="Введите комментарий">
      <Icon class="send" icon="ph:arrow-circle-up-fill" @click="handleSave"/>
    </div>
    <div v-if="store.comment.length > 0">
      <div class="horisontal">
        <Icon class="send" icon="ph:at-light"/>
        <Icon class="send" icon="circum:image-on"/>
      </div>
    </div>
  </div>
  

</template>

<style scoped>
.comment-menu-wrapper {
  height: fit-content;
  background-color: var(--primary-light);
  border-radius: 8px;
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
  color: var(--text);
  border: none;
  outline: none;
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