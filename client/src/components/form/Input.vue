<script setup lang="ts">
defineProps<{
    name: string;
    type: 'text' | 'password' | 'email';
}>();
</script>

<template>
    <div>
        <span>
            <slot />
        </span>
        <input :name="name" :type="type" />
    </div>
</template>

<style scoped>
div {
    --colors: #aaa;
    width: 100%;
    margin-bottom: 2em;
}

span {
    color: var(--colors);
    font-size: 12px;
}

input {
    width: 100%;
    border: none;
    border-bottom: 1px solid var(--colors);
    padding: 10px;
    font-size: inherit;
    font-family: inherit;
    height: 2em;
}
</style>