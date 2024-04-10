import { defineStore } from 'pinia'
import type { AnyElement } from '~/types/elements'
import { isValidReorder } from './validators';

export const useTreeStore = defineStore('tree', () => {
  const draggedElement = ref<AnyElement | null>(null);

  const projectStore = useCurrentProjectStore();

  const handleDrop = async (newParentId: string | undefined, index: number) => {
    if (!isValidReorder(draggedElement.value!, newParentId!))
      return;
    draggedElement.value!.parent = newParentId;
    projectStore.updateElement(draggedElement.value!, 'parent');

    if (index !== 0) {    
      const parentChildrenList = projectStore.elements.filter((e) => e.parent === newParentId)
      await projectStore.putElementAfter(draggedElement.value!.id, parentChildrenList[index - 1].id);
    } else {
      await projectStore.putElementAfter(draggedElement.value!.id);
    }
    draggedElement.value = null;
  }

  return {
    draggedElement,
    handleDrop
  }
})