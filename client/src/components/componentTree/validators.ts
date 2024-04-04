import type { AnyElement } from "~/types/elements"
import { useTreeStore } from "./treeStore";

export const isValidReorder = (element: AnyElement, parentId: string | undefined) => {
  if (!parentId) {
    return true;
  }
  const { elements } = useCurrentProjectStore();
  const parent = elements.find((e) => e.id === parentId);
  if (!parent)
    throw new Error();
  if (parent.type === 'text' || element.id === parentId)
    return false;
  return !checkIfNewParentNodeIsChild(element, parentId);
}

const checkIfNewParentNodeIsChild = (newChildAnyElement: AnyElement, newParentId: string) => {
  const { elements } = useCurrentProjectStore();
  let parent = elements.find((e) => e.id === newParentId)!;
 
  while (parent.parent) {
    if (parent.id == newChildAnyElement.id)
      return true
    parent = elements.find((e) => e.id === parent.parent)!;
  } 
  return false;
}

export const isValidDropOnTopOrBottom = (draggindId: string, targetId: string | undefined): boolean => {
  if (!targetId)
    return true;
  if (draggindId === targetId)
    return false;

  const { draggedElement } = useTreeStore();
  if (!draggedElement)
    throw new Error();

  return !checkIfNewParentNodeIsChild(draggedElement, targetId!);
};

export const isValidDropOnTarget = (targetId: string | undefined): boolean => {
  if (!targetId)
    return true;

  const { draggedElement } = useTreeStore();
  if (!draggedElement)
    throw new Error();

  const { elements } = useCurrentProjectStore();
  const targetAnyElement = elements.find((e) => e.id === targetId);
  if (!targetAnyElement)
    throw new Error();
  if (targetAnyElement.type == 'text')
    return false;

  return !checkIfNewParentNodeIsChild(draggedElement, targetId!);
};