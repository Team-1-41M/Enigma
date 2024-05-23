import axios, { type AxiosInstance } from "axios";

export default defineNuxtPlugin(() => {
	let api: AxiosInstance = axios.create({
		withCredentials: true,
		baseURL: `/api`
	});

	return {
		provide: {
			axios,
			api: api
		}
	};
});
