<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { TextElement } from '~/types/elements';


const props = defineProps<{
    element: TextElement
}>()
</script>

<template>
        <Icon icon="fluent:text-t-16-filled"/>
        <p class="summary-text">{{ props.element.name }}</p>

</template>

<style scoped>
.text-item-wrapper {
    display: flex;
    width: 100%
}

svg {
    color: var(--text)
}

.summary-text {
    margin: 4px 0px;
    color: var(--text);
  }
</style>