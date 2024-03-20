export const signUp = async (data: { name: string, password: string, email: string }): Promise<void> => { // TODO proper error type
    const { $api } = useNuxtApp();

    return (await $api.post('/api/v1/auth/sign-up', data)).data;
}

export const signIn = async (data: { name: string, password: string }): Promise<void> => { // TODO proper error type
    const { $api } = useNuxtApp();

    const response = $api.post('/api/v1/auth/sign-in', data);

    console.log(response)

    return (await $api.post('/api/v1/auth/sign-in', data)).data;
}

export const signOut = async (): Promise<void> => { // TODO proper error type
    const { $api } = useNuxtApp();

    return (await $api.post('/api/v1/auth/sign-out')).data;
}