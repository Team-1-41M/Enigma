<script setup lang="ts">
import { ref } from 'vue';
import { Icon } from '@iconify/vue/dist/iconify.js';
import type { AnyElement, BlockElement } from '~/types/elements';

interface Props {
  element: BlockElement;
  isExpanded?: boolean;
}
const props = defineProps<Props>();
const emits = defineEmits<{
  'update:isExpanded': [value: boolean],
  'select': [ element: AnyElement ],
  'openMenu': [ element: AnyElement, x: number, y: number ],
  'reorder': [ newParent: string | undefined, newIndex: number ],
  'setDraggingElement': [ element: AnyElement | null ],
}>()
const store = useCurrentProjectStore();

const details = ref<HTMLDetailsElement>()

const isExpanded = computed({
  get() {
    return props.isExpanded
  },
  set(value) {
    emits("update:isExpanded", value)
  }
});

const handleReorder = (newParent: string | undefined, newIndex: number) => {
  emits('reorder', newParent, newIndex);
}

const handleRightClick = (e: MouseEvent, element: AnyElement) => {
  e.stopImmediatePropagation()
  emits('openMenu', element, e.clientX, e.clientY);
}

const handleMenuOpening = (element: AnyElement, x: number, y: number) => {
  emits('openMenu', element, x, y);
}

const handleSelection = (element: AnyElement) => {
  emits('select', element)
}

const handleDragStart = (element: AnyElement | null) => {
  emits('setDraggingElement', element);
}
</script>

<template>
  <ComponentTreeItem
    :tree-item="element"
    :index="0" 
    :parent-id="element.parent" 
    :children-count="0"
    :selected="store.selectedElements.some(e => element.id === e.id)"
    @dragged="handleDragStart"
    @reorder="handleReorder"
    @select="handleSelection"
    >
      <template #title>
        <div class="category-item-wrapper">
          <Icon 
            icon="radix-icons:frame"/>
          <p class="summary-text">{{ props.element.name }}</p>
        </div>
      </template>
      <template #children>
        <div
            v-for="child in store.elements.filter(e => {e.parent == props.element.id})">
            <BlockItem
                v-if="child.type == 'block'"
                :key="child.id"
                :element="child"
                @select="handleSelection"
                @reorder="handleReorder" 
                @contextmenu.prevent="handleRightClick($event, child)"
                @openMenu="handleMenuOpening"
                @set-dragging-category="handleDragStart"/>
            <ComponentTreeTextItem
                v-else
                :element="child"/>
        </div>
        
      </template>
  </ComponentTreeItem>
</template>

<style scoped lang="scss">
.category-item-wrapper {
  display: flex;
  height: fit-content;
  align-items: center;
  gap: $gap;
}

.summary-text {
  margin: 4px 0px;
  font-size: $medium;
  color: var(--text-950);
}

.lock-icon {
  width: 1.2em;
  height: 1.2em;
}
</style>