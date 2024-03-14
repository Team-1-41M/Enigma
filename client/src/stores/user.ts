import { defineStore } from 'pinia';
import { me } from "~/actions/users";
import type { User } from "~/types/user";

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null as null | User
    }),
    actions: {
        async fetchUser() {
            this.user = await me();
        }
    }
})