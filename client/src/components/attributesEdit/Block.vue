<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { BlockElement } from '~/types/elements';

const store = useCurrentProjectStore();

const elementColor = computed(() => {
    return (store.selectedElements.at(0)! as BlockElement).background
})
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
        <div class="horisontal-block">
            <Icon icon="healthicons:w"/>
            <input type="number" v-model="(store.selectedElements.at(0)! as BlockElement).width" @blur="store.updateElement(store.selectedElements.at(0)!, 'width')">
        </div>
        <div class="horisontal-block">
            <Icon icon="healthicons:h"/>
            <input type="number" v-model="(store.selectedElements.at(0)! as BlockElement).height" @blur="store.updateElement(store.selectedElements.at(0)!, 'height')">
        </div>
        <div class="horisontal-block">
            <!--NOTE: Нет угла наклона-->
            <Icon icon="tabler:border-corner-rounded"></Icon>
            <input type="number" v-model="(store.selectedElements.at(0)! as BlockElement).borderRadius" @blur="store.updateElement(store.selectedElements.at(0)!, 'borderRadius')">
        </div>
    </div>
       
    <div class="background-color-wrapper">
        <h3>Заполнение</h3>
        <div class="horisontal-block">
            <div class="picked-color"/>
            <input type="text" v-model="(store.selectedElements.at(0)! as BlockElement).background" @blur="store.updateElement(store.selectedElements.at(0)!, 'background')">
        </div>
        
    </div>

    <!-- <div class="borders-wrapper">
        <h3>Границы</h3>
        <Icon icon="ic:round-plus"></Icon>

        <div class="horisontal-block" style="gap:6px">
            <div class="picked-color"/>
            <input type="text" v-model="(store.selectedElements.at(0)! as BlockElement).borders" @blur="store.updateElement(store.selectedElements.at(0)!, 'borderRadius')">
        
        </div>
    </div> -->

    

</template>

<style scoped>
.coordinates-wrapper {
    height: fit-content;
    display: grid;
    padding: 20px;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
    grid-template-areas:
        ". ."
        ". ."
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