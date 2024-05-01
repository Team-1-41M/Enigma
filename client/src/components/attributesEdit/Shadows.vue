<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { BlockElement, Border, Borders } from '~/types/elements';

const store = useCurrentProjectStore();

const elementShadowColor = computed(() => {
    return (store.selectedElements.at(0)! as BlockElement).shadow?.color ?? '#000000' 
})

const initialiseShadows = () => {
    (store.selectedElements.at(0)! as BlockElement).shadow = {
        color: '#000000',
        offsetX: 0,
        offsetY: 0,
        blur: 0,
        spread: 0
    }
}

if (!(store.selectedElements.at(0)! as BlockElement).shadow) {
    initialiseShadows();
}
</script>

<template>
    <details>
        <summary>
            <h3>Тени</h3>
            <Icon icon="ic:round-plus"></Icon>
        </summary>
        <!--One border-->
        <div>
            <div class="horisontal-block">
                <div class="horisontal-block hoverable">
                    <div class="picked-color"/>
                    <input
                        v-if="(store.selectedElements.at(0)! as BlockElement).shadow"
                        type="text"
                        v-model="(store.selectedElements.at(0)! as BlockElement).shadow!.color"
                        @blur="store.updateElement(store.selectedElements.at(0)!, 'shadow')"/>
                </div>
            </div>
            <div class="horisontal-block">
                <div class="horisontal-block hoverable">
                    <Icon icon="healthicons:x"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).shadow!.offsetX" @blur="store.updateElement(store.selectedElements.at(0)!, 'shadow')"/>
                </div>
                <div class="horisontal-block hoverable">
                    <Icon icon="healthicons:y"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).shadow!.offsetY" @blur="store.updateElement(store.selectedElements.at(0)!, 'shadow')"/>
                </div>
            </div>
            <div class="horisontal-block">
                <div class="horisontal-block hoverable">
                    <Icon icon="mdi:blur"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).shadow!.blur" @blur="store.updateElement(store.selectedElements.at(0)!, 'shadow')"/>
                </div>
                <div class="horisontal-block hoverable">
                    <Icon icon="gis:offset"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).shadow!.spread" @blur="store.updateElement(store.selectedElements.at(0)!, 'shadow')"/>
                </div>
            </div>
            
        </div>
    </details>
    

</template>

<style scoped>
summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    color: var(--text)
}

summary h3 {
    margin: 0;
}


input {
    width: 100%;    
    max-width: 82px;
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

.hoverable:hover {
    border: 1px solid #C63E3E5E
}

.hoverable {
    border: 1px solid transparent
}

svg {
    color: var(--text);
    height: 25px;
    width: 25px;
}

.picked-color {
    height: 20px;
    width: 20px;
    background-color: v-bind(elementShadowColor);
}
</style>