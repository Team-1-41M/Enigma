<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { BlockElement, Border, Borders } from '~/types/elements';

const store = useCurrentProjectStore();

const elementBorderColor = computed(() => {
    return (store.selectedElements.at(0)! as BlockElement).borders?.color ?? '#ffffff' 
})

const elementBorderTopColor = computed(() => {
    return ((store.selectedElements.at(0)! as BlockElement).borders as Borders).top?.color ?? '#ffffff' 
})

const elementBorderRightColor = computed(() => {
    return ((store.selectedElements.at(0)! as BlockElement).borders as Borders).right?.color ?? '#ffffff' 
})

const elementBorderBottomColor = computed(() => {
    return ((store.selectedElements.at(0)! as BlockElement).borders as Borders).bottom?.color ?? '#ffffff' 
})

const elementBorderLeftColor = computed(() => {
    return ((store.selectedElements.at(0)! as BlockElement).borders as Borders).left?.color ?? '#ffffff' 
})

const oneBorderMode = ref(true);

const initialiseBorders = () => {
    (store.selectedElements.at(0)! as BlockElement).borders = {
        color: '#ffffff',
        width: 1,
        style: 'solid'
    }
}

if (!(store.selectedElements.at(0)! as BlockElement).borders) {
    initialiseBorders();
} else if ((store.selectedElements.at(0)! as BlockElement).borders!.right) {
    oneBorderMode.value = false;
}

const goToMultipleBordersMode = () => {
    oneBorderMode.value = false;
    let initialBorders = (store.selectedElements.at(0)! as BlockElement).borders as Border;
    (store.selectedElements.at(0)! as BlockElement).borders! = {
        top: {...initialBorders},
        bottom: {...initialBorders},
        left: {...initialBorders},
        right: {...initialBorders}
    };

}
</script>

<template>
    <details>
        <summary>
            <h3>Границы</h3>
            <Icon icon="ic:round-plus"></Icon>
        </summary>
        <!--One border-->
        <div v-if="oneBorderMode">
            <div class="horisontal-block">
                <div class="horisontal-block hoverable">
                    <div class="picked-border-color"/>
                    <input
                        v-if="(store.selectedElements.at(0)! as BlockElement).borders"
                        type="text"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.color"
                        @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                    <input
                        v-else
                        type="text"
                        v-model="((store.selectedElements.at(0)! as BlockElement).borders as Border).color"/>
                </div>
    
                <div class="horisontal-block hoverable">
                    <Icon icon="fluent:line-thickness-20-regular"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.width" @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
                <Icon icon="ic:round-plus"/>
            </div>
            <div class="horisontal-block" >
                <select v-model="(store.selectedElements.at(0)! as BlockElement).borders!.style">
                    <option :value="'solid'">Прямая</option>
                    <option :value="'dashed'">Линиями</option>
                    <option :value="'dotted'">Точками</option>
                </select>
                <Icon
                    icon="tabler:dots"
                    @click="goToMultipleBordersMode"/>
            </div>
        </div>
        <!--All borders-->
        <div v-else>
            <label>Top:</label>
            <div class="horisontal-block">
                
                <div class="horisontal-block hoverable">
                    <div class="picked-border-color top"/>
                    <input
                        type="text"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.top.color"
                        @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
    
                <div class="horisontal-block hoverable">
                    <Icon icon="fluent:line-thickness-20-regular"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.top.width" @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
                <Icon icon="ic:round-plus"/>
            </div>
            <div class="horisontal-block" >
                <select v-model="(store.selectedElements.at(0)! as BlockElement).borders!.top.style">
                    <option :value="'solid'">Прямая</option>
                    <option :value="'dashed'">Линиями</option>
                    <option :value="'dotted'">Точками</option>
                </select>
            </div>
            <label>Right:</label>
            <div class="horisontal-block">
                <div class="horisontal-block hoverable">
                    <div class="picked-border-color right"/>
                    <input
                        type="text"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.right.color"
                        @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
    
                <div class="horisontal-block hoverable">
                    <Icon icon="fluent:line-thickness-20-regular"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.right.width" @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
                <Icon icon="ic:round-plus"/>
            </div>
            <div class="horisontal-block" >
                <select v-model="(store.selectedElements.at(0)! as BlockElement).borders!.right.style">
                    <option :value="'solid'">Прямая</option>
                    <option :value="'dashed'">Линиями</option>
                    <option :value="'dotted'">Точками</option>
                </select>
            </div>
            <label>Bottom:</label>
            <div class="horisontal-block">
                <div class="horisontal-block hoverable">
                    <div class="picked-border-color bottom"/>
                    <input
                        type="text"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.bottom.color"
                        @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
    
                <div class="horisontal-block hoverable">
                    <Icon icon="fluent:line-thickness-20-regular"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.bottom.width" @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
                <Icon icon="ic:round-plus"/>
            </div>
            <div class="horisontal-block" >
                <select v-model="(store.selectedElements.at(0)! as BlockElement).borders!.bottom.style">
                    <option :value="'solid'">Прямая</option>
                    <option :value="'dashed'">Линиями</option>
                    <option :value="'dotted'">Точками</option>
                </select>
            </div>
            <label>Left:</label>
            <div class="horisontal-block">
                <div class="horisontal-block hoverable">
                    <div class="picked-border-color left"/>
                    <input
                        type="text"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.left.color"
                        @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
    
                <div class="horisontal-block hoverable">
                    <Icon icon="fluent:line-thickness-20-regular"/>
                    <input 
                        type="number"
                        v-model="(store.selectedElements.at(0)! as BlockElement).borders.left.width" @blur="store.updateElement(store.selectedElements.at(0)!, 'borders')"/>
                </div>
                <Icon icon="ic:round-plus"/>
            </div>
            <div class="horisontal-block" >
                <select v-model="(store.selectedElements.at(0)! as BlockElement).borders!.left.style">
                    <option :value="'solid'">Прямая</option>
                    <option :value="'dashed'">Линиями</option>
                    <option :value="'dotted'">Точками</option>
                </select>
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
    background-color: v-bind(elementColor);
}

.picked-border-color {
    height: 20px;
    width: 20px;
    background-color: v-bind(elementBorderColor);
}

.top {
    background-color: v-bind(elementBorderTopColor);
}

.right {
    background-color: v-bind(elementBorderRightColor);
}

.bottom {
    background-color: v-bind(elementBorderBottomColor);
}

.left {
    background-color: v-bind(elementBorderLeftColor);
}
</style>