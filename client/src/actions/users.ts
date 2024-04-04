import type { User } from "~/types/user";

export const me = async (): Promise<User | undefined> => {
    const { $api } = useNuxtApp();
 
    try {
        return (await $api.get('users/me')).data;
    } catch (e) {
        return undefined;
    }
}