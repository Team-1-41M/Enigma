<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { AnyElement } from '~/types/elements';

interface HoverableHTMLElement extends HTMLElement {
  hovered: boolean
}

interface Props {
  treeItem: AnyElement,
  index: number,
  parentId: string | undefined,
  childrenCount: number,
  selected: boolean,
  isExpanded?: boolean,
//   isValidDropOnTopOrBottom: (draggindId: string, targetId: string | null) => boolean,
// 	isValidDropOnTarget: (targetId: string | null) => boolean,
}
const props = defineProps<Props>();
const emit = defineEmits<{
  'update:isExpanded': [value: boolean],
  'reorder': [ newParent: string | undefined, newIndex: number ],
  'select': [ item: AnyElement ],
  'dragged': [ item: AnyElement | null ]
}>()

const isDraggedOver = ref(false);
const topTargetRef = ref<HoverableHTMLElement>();
const bottomTargetRef = ref<HoverableHTMLElement>();
const itemRef = ref<HoverableHTMLElement>();
const details = ref<HTMLDetailsElement>();

const isExpanded = computed({
  get() {
    return props.isExpanded
  },
  set(value) {
    emit("update:isExpanded", value)
  }
});

const handleToggle = (event: any) => {
  if (event === undefined) { // to show children on drop
    details.value!.open = true;
  }
  emit('select', props.treeItem);
}

const preventDragEvents = (event: DragEvent) => {
	event.stopPropagation();
	event.preventDefault();
};

const handleDragStart = (event: DragEvent) => {
  event.stopPropagation();
  emit('dragged', props.treeItem);
};

const handleDragEnter = (event: DragEvent, targetRef: HoverableHTMLElement) => {
	preventDragEvents(event);

  // if (props.draggedItemId === props.treeItemId)
  //   return;

	const targetId = targetRef === itemRef.value
		? props.treeItem.id
		: props.parentId;

	// if (!props.isValidDropOnTopOrBottom(props.draggedItemId!, targetId))
	// 	return;

  isDraggedOver.value = true;

//   if (props.isValidDropOnTarget(targetId))
//     targetRef.hovered = true;
};

const handleDragLeave = (event: DragEvent, targetRef: HoverableHTMLElement) => {
	preventDragEvents(event);

  targetRef!.hovered = false;

  isDraggedOver.value = false;  
};

const handleDragOver = (event: DragEvent, targetId: string | undefined) => {
	preventDragEvents(event);

  isDraggedOver.value = true;
};

const handleDrop = (event: DragEvent, targetRef: HoverableHTMLElement, newParent: string | undefined, newIndex: number) => {
	preventDragEvents(event);
	targetRef.hovered = false;
	isDraggedOver.value = false;

//   if (!props.isValidDropOnTopOrBottom(props.draggedItemId, newParent) || !props.isValidDropOnTarget(newParent))
// 		return;

  handleToggle(undefined);

  emit('reorder', newParent, newIndex);
  emit('dragged', null);
};

const handleDragEnd = (event: DragEvent) => {
	preventDragEvents(event);
  emit('dragged', null);
	isDraggedOver.value = false;
};
</script>

<template>
	<div 
		ref="itemRef"
		draggable="true"
		:class="{ 'dragged-over': isDraggedOver }"
		@dragstart="handleDragStart($event)"
		@dragend="handleDragEnd($event)">
      <div
        ref="topTargetRef"
        class="drop-target-area"
        :class="{ 'hovered-drop-target-area': topTargetRef?.hovered && isDraggedOver }"
        @dragenter="handleDragEnter($event, topTargetRef!)"
        @dragleave="handleDragLeave($event, topTargetRef!)"
        @dragover="handleDragOver($event, props.parentId)"
        @drop="handleDrop($event, topTargetRef!, parentId, index)">
      </div>
      <details
        ref="details" 
        @toggle="handleToggle"  
        @drop="handleToggle"
        :open="false"
        >
          <summary
            :class="[ { 'hovered-summary': itemRef?.hovered && isDraggedOver }, { 'selected-details': selected} ]"
            @dragenter="handleDragEnter($event, itemRef!)"
            @dragleave="handleDragLeave($event, itemRef!)"
            @dragover="handleDragOver($event, props.treeItem.id)"
            @drop="handleDrop($event, itemRef!, treeItem.id, childrenCount)">
              <Icon
                :class="{ 'disabled-pointer-events': isDraggedOver }"
                class="menu-arrow-icon"
                icon="majesticons:chevron-right" />
              <div :class="{ 'disabled-pointer-events': isDraggedOver } " class="tree-item">
                <slot name="title" />
              </div>
          </summary>
          <div class="children-container">
            <slot name="children" />
          </div>
      </details>
      <div
        ref="bottomTargetRef"
        class="drop-target-area"
        :class="{ 'hovered-drop-target-area': bottomTargetRef?.hovered && isDraggedOver }"
        @dragenter="handleDragEnter($event, bottomTargetRef!)"
        @dragleave="handleDragLeave($event, bottomTargetRef!)"
        @dragover="handleDragOver($event, props.parentId)"
        @drop="handleDrop($event, bottomTargetRef!, parentId, index + 1)">
      </div>
	</div>
</template>

<style scoped>
.drop-target-area {
	height: 0px;
	transition: all 100ms ease-out;
    border-radius: 8px;
}
.dragged-over > .drop-target-area {
  height: 1em;
}

.hovered-summary {
	background: var(--primary-light);
	border: 2px dotted var(--primary-light);
}
.hovered-drop-target-area {
	height: 2em !important;
	background: var(--primary-light);
	border: 2px dotted var(--primary-light);
}
details summary {
	color: var(--text);
	list-style: none;
	display: flex;
	cursor: pointer;
	transition: background-color 100ms ease-out;
	user-select: none;
	position: relative;
	padding: 0.5em 0;
	gap: 0.5em;
    border-radius: 8px;
    width: 100%; 
}
summary:hover {
  background-color: var(--primary-light);
}
.selected-details {
  background-color: var(--accent);
}

summary[class="selected-details"]:hover {
  background-color: var(--accent-light);
}

details[open] summary ~ * {
  animation: open 2s ease-in-out;
}
.children-container {
  margin-left: 1em;
}
.menu-arrow-icon {
  width: 1em;
  height: 1em;
	transition: all 100ms ease-out;
	align-self: center;
}
details[open] > summary .menu-arrow-icon {
  transform: rotate(90deg);
}
.disabled-pointer-events {
	pointer-events: none;
}

.tree-item {
    width: 100%;
    display: flex; 
    align-items: center;
    gap: 8px;
}
</style> 