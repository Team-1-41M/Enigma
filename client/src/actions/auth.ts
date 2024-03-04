import type { AxiosResponse } from "axios";

export const signUp = async (data: { name: string, password: string, email: string }): Promise<AxiosResponse<void, any>> => { // TODO proper error type
    const { $api } = useNuxtApp();

    return await $api.post('/api/v1/auth/sign-up', data);
}

export const signIn = async (data: { name: string, password: string }): Promise<AxiosResponse<void, any>> => { // TODO proper error type
    const { $api } = useNuxtApp();

    return await $api.post('/api/v1/auth/sign-in', data);
}

export const signOut = async (): Promise<AxiosResponse<void, any>> => { // TODO proper error type
    const { $api } = useNuxtApp();

    return await $api.post('/api/v1/auth/sign-out');
}