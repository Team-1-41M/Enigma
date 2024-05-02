import type { Project } from "~/types/project";

export const getProjectsAsync = async () => {
    const { $api } = useNuxtApp();

    try {
        const response = await $api.get('users/me/projects');
        return (response.data as any).data as Project[];
    } catch (e) {
        return [];
    }
}

export const getProjectByIdAsync = async (projectId: string) => {
    const { $api } = useNuxtApp();

    const response = await $api.get(`projects/${projectId}`);
    return (response.data as any).data as Project;
}

export const createProjectAsync = async (title: string) : Promise<Project | undefined> => { 
    const { $api } = useNuxtApp();

    try {
        const response = await $api.post<Project>('projects', { title });
        return response.data;
    } catch (e) {
        return undefined;
    }
}

export const deleteProjectAsync = async (id: number) => {
    const { $api } = useNuxtApp();

    const response = await $api.delete(`projects/${id}`);
    return response;
}

export const renameProjectAsync = async (id: number, title: string) => {
    const { $api } = useNuxtApp();

    const response = await $api.put(`projects/${id}`, { title });
    return response;
}

export const getProjectShareLinkAsync = async (id: number, mode: "read" | "edit") => {
    const { $api } = useNuxtApp();

    const response = await $api.post(`projects/${id}/link`, {
        credential: mode
    })
    return response;
}