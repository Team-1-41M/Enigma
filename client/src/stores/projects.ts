import { defineStore } from 'pinia';
import { getProjectsAsync } from '~/actions/projects';
import type { Project } from '~/types/project';

export const useProjectStore = defineStore('projects', {
  state: () => ({
    projectList: [] as Project[],
  }),
  actions: {
    async fetchProjects() {
      this.projectList = await getProjectsAsync();
    },
    
  }
})