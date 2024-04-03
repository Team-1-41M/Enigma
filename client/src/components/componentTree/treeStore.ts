import { defineStore } from 'pinia'
import type { AnyElement } from '~/types/elements'

export const useTreeStore = defineStore('tree', () => {
  const draggedElement = ref<AnyElement | null>(null);

  const projectStore = useCurrentProjectStore();

  const handleDrop = (newParentId: string | undefined, index: number) => {
    draggedElement.value!.parent = newParentId;
    projectStore.updateElement(draggedElement.value!, 'parent');
    draggedElement.value = null;
  }

  return {
    draggedElement,
    handleDrop
  }
})