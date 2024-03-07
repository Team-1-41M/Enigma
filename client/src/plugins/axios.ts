import axios, { type AxiosInstance } from "axios";

export default defineNuxtPlugin((nuxtApp) => {
	
	const config = useRuntimeConfig();
	
	let api: AxiosInstance = axios.create({
		withCredentials: true,
		baseURL: config.public.baseUrl
	});

	return {
		provide: {
			api: api
		}
	};
});
