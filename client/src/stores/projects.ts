import { defineStore } from "pinia";
import {
    getProjectsAsync,
    createProjectAsync,
    deleteProjectAsync,
    renameProjectAsync,
} from "~/actions/projects";
import { ProjectCreateError, type Project } from "~/types/project";

export const useProjectStore = defineStore("projects", () => {
    const projectList = ref([] as Project[]);
    const notifications = useNotificationsStore();

    async function fetchProjects() {
        projectList.value = await getProjectsAsync();
    }

    async function createProject(title: string) {
        const result = await createProjectAsync(title);
        if (typeof result === "string") {
            notifications.notifyError(result, [
                ProjectCreateError.ProjectLimit,
                "Один пользователь может создать только 3 проекта",
            ]);
            return;
        }
        await fetchProjects();
    }

    async function deleteProject(id: number) {
        await deleteProjectAsync(id);
        await fetchProjects();
    }

    async function renameProject(id: number, title: string) {
        await renameProjectAsync(id, title);
        await fetchProjects();
    }

    return {
        projectList,
        fetchProjects,
        createProject,
        deleteProject,
        renameProject,
    };
});
