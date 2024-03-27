<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { TextElement } from '~/types/elements';


const props = defineProps<{
    element: TextElement
}>()
</script>

<template>
    <div class="text-item-wrapper">
        <Icon icon="fluent:text-t-16-filled"/>
        <label>element.name</label>
    </div>

</template>

<style scoped>
.text-item-wrapper {
    width: 100%
}

svg {
    color: var(--text)
}
</style>