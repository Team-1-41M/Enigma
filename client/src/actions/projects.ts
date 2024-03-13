import type { Project } from "~/types/project";

export const getProjectsAsync = async () => {
    const { $api } = useNuxtApp();

    const response = await $api.get('/api/v1/users/me/projects');
    return (response.data as any).data as Project[];
}

export const getProjectByIdAsync = async (projectId: string) => {
    const { $api } = useNuxtApp();

    const response = await $api.get(`/api/v1/projects/${projectId}`);
    return (response.data as any).data as Project;
}

export const createProjectAsync = async (title: string) : Promise<Project> => { 
    const { $api } = useNuxtApp();

    const response = await $api.post<Project>('/api/v1/projects', { title });
    return response.data;
}

export const deleteProjectAsync = async (id: number) => {
    const { $api } = useNuxtApp();

    const response = await $api.delete(`/api/v1/projects/${id}`);
    return response;
}

export const renameProjectAsync = async (id: number, title: string) => {
    const { $api } = useNuxtApp();

    const response = await $api.put(`/api/v1/projects/${id}`, { title });
    return response;
}