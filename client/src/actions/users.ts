import type { User } from "~/types/user";

export const me = async (): Promise<User> => { // TODO proper error type
    const { $api } = useNuxtApp();
 
    return (await $api.get('/api/v1/auth/me')).data; // TODO /users/
}