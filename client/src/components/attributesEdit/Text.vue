<script setup lang="ts">import { Icon } from '@iconify/vue';
import type { BlockElement } from '~/types/elements';

const store = useCurrentProjectStore();
</script>

<template>
    <div class="coordinates-wrapper">
        <div class="horisontal-block">
            <Icon icon="healthicons:y"/>
            <input type="number" v-model="store.selectedElements.at(0)!.x" @blur="store.updateElement(store.selectedElements.at(0)!, 'x')">
        </div>
        <div class="horisontal-block">
            <Icon icon="healthicons:x"/>
            <input type="number" v-model="store.selectedElements.at(0)!.y" @blur="store.updateElement(store.selectedElements.at(0)!, 'y')">
        </div>
    </div>


</template>

<style scoped>
.coordinates-wrapper {
    height: fit-content;
    display: grid;
    padding: 20px;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr;
    grid-template-areas:
        ". .";
    border-bottom: 1px solid var(--text);
}

.background-color-wrapper {
    padding: 0px 20px;
}

input {
    width: 82px;
    background-color: transparent;
    border: none;
    color: var(--text);
    font-family: Inter;
    font-size: 16px;
    font-weight: 400;
    line-height: 19.36px;
    letter-spacing: -0.04em;
    text-align: left;
    border: 1px solid transparent;
}

input:focus {
    background-color: #C63E3E5E;
    outline: none;
}

input[type=number] {
    appearance: textfield;
    -moz-appearance: textfield;
}

.horisontal-block {
    display: flex;
    gap: 4px;
    width: fit-content
}

.horisontal-block:hover {
    border: 1px solid #C63E3E5E
}

svg {
    color: var(--text);
    height: 25px;
    width: 25px;
}

.picked-color {
    height: 20px;
    width: 20px;
    background-color: v-bind(elementColor);
}
</style>