<script setup lang="ts">
import type { Comment } from '~/types/comment';
import { Icon } from '@iconify/vue';
import TimeAgo from 'javascript-time-ago';
import ru from 'javascript-time-ago/locale/ru';

const props = defineProps<{
    comment: Comment
}>();

TimeAgo.addDefaultLocale(ru);
const timeAgo = new TimeAgo('ru-RU');


</script>

<template>
<div class="comment-wrapper">
    <Icon class='user-icon' icon="ic:baseline-account-circle"/>
    <p>{{comment.componentName}}</p>
    <div class="horisontal-box">
        <p class="author-name">{{comment.authorName}}</p>
        <p class="time-text">{{ timeAgo.format(new Date(comment.createdAt)) }}</p>
    </div>
    <p class="comment-text">
        {{ comment.text }}
    </p>
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
</style>