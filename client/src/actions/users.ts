import type { AxiosResponse } from "axios";
import type { User } from "~/types/user";

export const me = async (): Promise<AxiosResponse<User, any>> => { // TODO proper error type
    const { $api } = useNuxtApp();

    return await $api.post('/api/v1/auth/me'); // TODO /users/
}