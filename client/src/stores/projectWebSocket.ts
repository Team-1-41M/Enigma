import { defineStore } from 'pinia'
import type { Project } from '~/types/project'
import { EditMode } from '~/types/editMode';
import type { 
  Frame,
  TextElement,
  ContainerElement,
  ImageElement
} from '~/types/elements';

export const useProjectWebSocketStore = defineStore('projectWebsocket', () => {
  const currentProject = ref<Project | null>(null);


  const elements = ref<Frame>({
    id: 1,
    name: 'TestName',
    X: 0,
    Y: 0,
    height: 400,
    width: 800,
    children: [
      {
        id: 2,
        name: 'Топбар',
        X: 0,
        Y: 0,
        height: 50,
        width: 800,
        borderRadius: 0,
        children: [
          {
            id: 3,
            name: 'Топбар',
            X: 0,
            Y: 0,
            height: 50,
            width: 800,
            fontWeight: '100',
            alignment: 'center'
          },
          {
            id: 4,
            name: 'Kvadratique',
            X: 50,
            Y: 50,
            height: 50,
            width: 50,
            borderRadius: 5,
            children: [
            ]
          }
        ]
      }
    ]
  }) //TODO: Прямо в проекте должно храниться

  const currentMode = ref<EditMode>(EditMode.Move);

  const socket = ref<WebSocket | null>(null)

  const loadProject = (id: string) => {
    socket.value = new WebSocket('ws://localhost:8000/api/v1/projects/1/content');

    socket.value.onopen = (event) => {
      console.log("WebSocket connection opened:", event);

    };
    
    socket.value.onmessage =  (event) => {
      console.log("WebSocket message received:", event);
      console.log()
      
      //elements.value = event.data
    };
  }

  const sendMessage = (message: string) => {
    socket.value!.send(message);
  }

  
  return {
    currentProject,
    elements,
    currentMode,
    loadProject,
    sendMessage
  }
})

