<script setup lang="ts">
import type { Comment } from '~/types/comment';
import { Icon } from '@iconify/vue';
import TimeAgo from 'javascript-time-ago';
import { useCommentsStore } from './store';

const props = defineProps<{
    comment: Comment
}>();

const store = useCommentsStore();

const timeAgo = new TimeAgo('ru-RU');

const commentsOpened = ref(false);

const commentText = ref<string>('');
</script>

<template>
<div class="comment-wrapper" @click="commentsOpened = true">
    <Icon class='user-icon' icon="ic:baseline-account-circle"/>
    <p>{{comment.component_name}}</p>
    <div class="horisontal-box">
        <p class="author-name">{{comment.user_id}}</p>
        <p class="time-text">{{ timeAgo.format(new Date(comment.created_at)) }}</p>
    </div>
    <p class="comment-text">
        {{ comment.text }}
    </p>
    <div class="children" v-for="child in store.comments.filter(c => c.parent_id === comment.id)">
        <Icon class='user-icon' icon="ic:baseline-account-circle"/>
        <p>{{child.component_name}}</p>
        <div class="horisontal-box">
            <p class="author-name">{{child.user_id}}</p>
            <p class="time-text">{{ timeAgo.format(new Date(child.created_at)) }}</p>
        </div>
        <p class="comment-text">
            {{ child.text }}
        </p>
    </div>
    <CommentsForm v-if="commentsOpened" :parentId="comment.id" @close="commentsOpened = false" v-model:comment='commentText'/>

</div>    
</template>

<style scoped>
.comment-wrapper {
    background-color: var(--primary);
    border-bottom: 2px solid var(--background);
    margin: 8px;
}

p {
    margin: 0;
    padding: 0
}

.horisontal-box {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.time-text {
    color: #dedbdbbd;
    font-family: Inter;
    font-size: 13px;
    font-weight: 400;
    line-height: 15.73px;
    text-align: left;
}


.user-icon {
    height: 33px;
    width: 33px;
    color: var(--text)
}

.children {
    margin-left: 15px;
}
</style>