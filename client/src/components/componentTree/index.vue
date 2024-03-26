<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { ElementType,type BlockElement, type TextElement, type AnyElement } from '~/types/elements';
import type { Project } from '~/types/project';

const socketStore = useCurrentProjectStore();

const draggedItemId = ref<string>('')

</script>

<template>
    <div class="components-tree-wrapper">
        <div v-for="(element, index) in socketStore.elements" style="width: 100%">
            <ComponentTreeTextItem
                v-if="element.type == ElementType.Text"
                :element="element"/>
            <ComponentTreeItem
                v-if="element.type == ElementType.Block"
                :tree-item-id="element.id"
                :dragged-item-id="draggedItemId"
                :index="index"
                :parentId="element.parent"
                :children-count="0"
                :selected="socketStore.selectedElements.some(e => element.id === e.id)">
                    <template #title>
                        <Icon icon="radix-icons:frame"/>
                        {{ element.name }}
                    </template>
            </ComponentTreeItem>
        </div>
    </div>
</template>

<style scoped>
.components-tree-wrapper {
    width: 100%;
    height: 100%;
    background-color: var(--primary);
    color: var(--text)
}
</style>