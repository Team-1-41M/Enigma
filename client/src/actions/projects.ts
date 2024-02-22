import type { Project } from "~/types/project";

export const getProjectsAsync = async () => {
    const { $api } = useNuxtApp();

    const response = await $api.get<Project[]>('/api/v1/projects');
    return response.data;
}