import { defineStore } from 'pinia';
import { me } from "~/actions/users";
import type { User } from "~/types/user";
import * as auth from "~/actions/auth";

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null as null | User
    }),
    actions: {
        async fetchUser() {
            this.user = await me() || null;
        },
        async signOut() {
            await auth.signOut();
            this.user = null;
        }
    }
})