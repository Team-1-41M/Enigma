import { defineStore } from 'pinia';
import { 
  getProjectsAsync,
  createProjectAsync,
  deleteProjectAsync
} from '~/actions/projects';
import type { Project } from '~/types/project';

export const useProjectStore = defineStore('projects', {
  state: () => ({
    projectList: [] as Project[],
  }),
  actions: {
    async fetchProjects() {
      this.projectList = await getProjectsAsync();
    },
    async createProject(title: string) {
      await createProjectAsync(title);
      await this.fetchProjects();
    },
    async deleteProject(id: number) {
      await deleteProjectAsync(id);
      await this.fetchProjects();
    }
  }
})