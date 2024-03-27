export const signUp = async (data: { name: string, password: string, email: string }): Promise<void> => { // TODO proper error type
    const { $api } = useNuxtApp();

    return (await $api.post('auth/sign-up', data)).data;
}

export const signIn = async (data: { name: string, password: string }): Promise<void> => { // TODO proper error type
    const { $api } = useNuxtApp();
    
    const response = $api.post('auth/sign-in', data);

    return (await $api.post('auth/sign-in', data)).data;
}

export const signOut = async (): Promise<void> => { // TODO proper error type
    const { $api } = useNuxtApp();

    return (await $api.post('auth/sign-out')).data;
}