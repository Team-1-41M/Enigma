import type { Project } from "~/types/project";

export const getProjectsAsync = async () => {
    const { $api } = useNuxtApp();

    const response = await $api.get('/api/v1/projects');
    return (response.data as any).data as Project[];
}