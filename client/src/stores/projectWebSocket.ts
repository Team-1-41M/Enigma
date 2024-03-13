import { defineStore } from 'pinia'
import type { Project } from '~/types/project'

export const useProjectWebSocketStore = defineStore('projectWebsocket', () => {
  const currentProject = ref<Project | null>(null);

  const elements = ref<string>('') //TODO: Прямо в проекте должно храниться

  const socket = ref<WebSocket | null>(null)

  const loadProject = (id: string) => {
    socket.value = new WebSocket('ws://localhost:8000/api/v1/projects/1/content');

    socket.value.onopen = (event) => {
      console.log("WebSocket connection opened:", event);

    };
    
    socket.value.onmessage =  (event) => {
      console.log("WebSocket message received:", event);
      console.log()
      elements.value = event.data
    };
  }

  const sendMessage = (message: string) => {
    socket.value!.send(message);
  }

  
  return {
    currentProject,
    elements,
    loadProject,
    sendMessage
  }
})

