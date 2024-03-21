<script setup lang="ts" generic="I extends { [key: string]: string }, S, E">
import type { AxiosResponse } from "axios";
import SubmitButton from "~/components/form/SubmitButton.vue";

const props = withDefaults(
    defineProps<{
        submit: (data: I) => Promise<S>;
        success: (result: S) => void;
        parseError?: (error: E) => string | void;
    }>(),
    {
        parseError: (_: any) => handleError(_),
    },
);

const slots = defineSlots<{
    default(): any;
    submitText(): any;
}>();

const formElement = ref<HTMLFormElement | null>(null);

async function submitFunction(e: Event) {
    e.preventDefault();

    const form = formElement.value;
    if (form == null) return;

    let i: { [key: string]: string } = {};
    for (let element of form.getElementsByTagName("input")) {
        i[element.name] = element.value;
    }

    props
        .submit(i as I)
        .then(s => props.success(s))
        .catch(e => props.parseError(e as E));
}
</script>

<script lang="ts">
const handleError = (_: any): void => {
    const notificationStore = useNotificationsStore();
    notificationStore.addNotification("Произошла неизвестная ошибка", 'error');
}
</script>

<template>
    <form ref="formElement" @submit="submitFunction">
        <slot />
        <SubmitButton>
            <slot name="submitText">Отправить</slot>
        </SubmitButton>
    </form>
</template>

<style scoped>
span {
    color: red;
    /* TODO */
}
</style>