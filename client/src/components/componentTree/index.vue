<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { ElementType,type BlockElement, type TextElement, type AnyElement } from '~/types/elements';
import { Icon } from '@iconify/vue';
import { ElementType,type BlockElement, type TextElement, type AnyElement } from '~/types/elements';
import type { Project } from '~/types/project';
import { useTreeStore } from './treeStore';

const props = defineProps<{
    tree: AnyElement[],
    parentId?: string
}>();
import { useTreeStore } from './treeStore';

const props = defineProps<{
    tree: AnyElement[],
    parentId?: string
}>();

const socketStore = useCurrentProjectStore();
const treeStore = useTreeStore();

const draggedItemId = ref<string>('')

const handleDragStart = (element: AnyElement | null) => {
    treeStore.draggedElement = element
}

const handleSelect = (element: AnyElement) => {
    socketStore.selectedElements = [element]
}

const handleReorder = (newParentId: string | undefined, newIndex: number) => {
    console.log(newIndex)
    treeStore.handleDrop(newParentId, newIndex);
}
</script>

<template>
    <div class="components-tree-wrapper">
        <div v-for="(element, index) in tree" style="width: 100%">
            <ComponentTreeItem
                v-if="element.parent === props.parentId && element.type == ElementType.Text"
                :tree-item="element"
                :dragged-item-id="treeStore.draggedElement ?? ''"
                :index="index"
                :parentId="element.parent"
                :children-count="0"
                :selected="socketStore.selectedElements.some(e => element.id === e.id)"
                @dragged="handleDragStart"
                @select="handleSelect"
                @reorder="handleReorder"
                @drop="null">
                    <template #title>
                        <ComponentTreeTextItem :element="element"></ComponentTreeTextItem>
                    </template>
            </ComponentTreeItem>
            <ComponentTreeItem
                v-if="element.parent === props.parentId && element.type == ElementType.Block"
                :tree-item="element"
                :dragged-item-id="treeStore.draggedElement ?? ''"
                :index="index"
                :parentId="element.parent"
                :children-count="0"
                :selected="socketStore.selectedElements.some(e => element.id === e.id)"
                @dragged="handleDragStart"
                @select="handleSelect"
                @reorder="handleReorder">
                    <template #title>
                        <Icon icon="radix-icons:frame"/>
                        {{ element.name }}
                    </template>
                    <template #children>
                        <ComponentTree :tree="socketStore.elements.filter((e) => e.parent == element.id)" :parent-id="element.id"/>
                    </template>
            </ComponentTreeItem>
        </div>
    </div>
</template>

<style scoped>
.components-tree-wrapper {
    height: 100%;
    background-color: var(--primary);
    color: var(--text)
    color: var(--text)
}
</style>