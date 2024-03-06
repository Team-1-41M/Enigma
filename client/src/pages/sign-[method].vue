<script setup lang="ts">
import Input from '~/components/form/Input.vue';
import TabToggle from '~/components/auth/TabToggle.vue';
import { signIn, signUp } from '~/actions/auth';

definePageMeta({
    key: "auth",
    validate: route => route.params.method == 'in' || route.params.method == 'up',
});

const route = useRoute();

const variant = computed(() => route.params.method as 'in' | 'up');
const variantIndex = computed(() => ['in', 'up'].indexOf(variant.value));

const router = useRouter();
function tabSelect(variant: string) {
    router.push({ path: '/sign-' + variant })
}

function successfulSignIn() {
    // TODO toast
    console.log("signed in successfully")
    router.push({ path: '/' })
}

function successfulSignUp() {
    // TODO toast
    console.log("signed up successfully")
    router.push({ path: '/sign-in' })
}
</script>

<template>
    <div class="bgOverlay">
        <div class="window">
            <TabToggle :tabSelect="tabSelect" :selected="variantIndex">
                <template #in>Войти</template>
                <template #up>Регистрация</template>
            </TabToggle>
            <h1>
                Добро пожаловать в
                <span class="title">Enigma</span>
            </h1>
            <template v-if="variant == 'in'">
                <Form :submit="signIn" :success="successfulSignIn">
                    <Input name="name" type='text'>Логин или Email</Input>
                    <Input name="password" type='password'>Пароль</Input>
                    <template #submitText>ОК</template>
                </Form>
            </template>
            <template v-if="variant == 'up'">
                <Form :submit="signUp" :success="successfulSignUp">
                    <Input name="name" type='text'>Логин</Input>
                    <Input name="email" type='email'>Email</Input>
                    <Input name="password" type='password'>Пароль</Input>
                    <template #submitText>ОК</template>
                </Form>
            </template>
        </div>
    </div>
</template>

<style scoped>
.bgOverlay::before {
    content: '';
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;

    background-image: url('~/assets/images/keyboard.png');
    background-size: cover;
    filter: blur(15px) brightness(40%);
}

.bgOverlay {
    background-color: #000;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}

.window {
    box-shadow: -20px 20px 50px 0px #0000008C;
    background-color: #fff;
    padding: 120px;
    width: 400px;
    border-radius: 10px;
    z-index: 1;
}

h1 {
    color: #000;
    font-size: 36px;
}

.title {
    display: block;
    color: var(--auth-primary);
    font-style: italic;
    font-size: 48px;
}
</style>