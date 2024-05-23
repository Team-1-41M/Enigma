<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { ElementType, type AnyElement, type Shadow } from "~/types/elements";

const store = useCurrentProjectStore();

const selectedBlockElement = computed(() => {
    const currentElement = store.selectedElements.length === 1 && store.selectedElements[0];
    if (!currentElement || currentElement.type != ElementType.Block) return;
    return currentElement;
});

const elementShadowColor = computed(() => {
    const currentElement = selectedBlockElement.value;
    if (currentElement === undefined || currentElement.shadow === undefined) return "#ffffff";
    return currentElement.shadow.color;
});

const toggleShadow = () => {
    let block = store.selectedElements[0];
    if (block === undefined || block.type !== ElementType.Block) return;

    if (block.shadow !== undefined) block.shadow = undefined;
    else {
        block.shadow = {
            color: "#000000",
            offsetX: 0,
            offsetY: 0,
            blur: 0,
            spread: 0,
        };
    }
    store.updateElement(block, "shadow");
};

let selectedElementsPrevHack = ref([] as AnyElement[]);
store.$subscribe((_, store) => {
    if (store.selectedElements === selectedElementsPrevHack.value) return;
    checkClearShadow(selectedElementsPrevHack.value[0]);
    selectedElementsPrevHack.value = store.selectedElements;
});

const isInvalidShadowProperty = (prop?: any) => {
    return prop === undefined || prop === null || prop === "";
};

const validateShadow = (shadow?: Shadow) => {
    if (
        shadow === undefined ||
        isInvalidShadowProperty(shadow.blur) ||
        isInvalidShadowProperty(shadow.color) ||
        isInvalidShadowProperty(shadow.offsetX) ||
        isInvalidShadowProperty(shadow.offsetY) ||
        isInvalidShadowProperty(shadow.spread)
    )
        return undefined;
    return shadow;
};

const checkClearShadow = (block?: AnyElement) => {
    block ||= store.selectedElements[0];
    if (block === undefined || block.type !== ElementType.Block) return;

    let shadow = block.shadow;
    if (shadow === undefined) return;

    if (validateShadow(shadow)) return;

    block.shadow = undefined;
    store.updateElement(block, "shadow");
    return false;
};
</script>

<template>
    <div v-if="selectedBlockElement !== undefined">
        <summary @click="toggleShadow()">
            <h3>Тень</h3>
            <Icon
                :icon="
                    selectedBlockElement.shadow == undefined ? 'ic:round-plus' : 'ic:round-minus'
                "
            />
        </summary>

        <div v-if="selectedBlockElement.shadow">
            <div class="horizontal-block">
                <div class="horizontal-block hoverable">
                    <div class="picked-color" />
                    <input
                        v-if="selectedBlockElement.shadow"
                        type="text"
                        v-model="selectedBlockElement.shadow.color"
                        @blur="
                            checkClearShadow() ||
                                store.updateElement(selectedBlockElement!, 'shadow')
                        "
                    />
                </div>
            </div>
            <div class="horizontal-block">
                <div class="horizontal-block hoverable">
                    <Icon icon="healthicons:x" />
                    <input
                        type="number"
                        v-model="selectedBlockElement.shadow.offsetX"
                        @blur="
                            checkClearShadow() ||
                                (selectedBlockElement !== undefined &&
                                    store.updateElement(selectedBlockElement!, 'shadow'))
                        "
                    />
                </div>
                <div class="horizontal-block hoverable">
                    <Icon icon="healthicons:y" />
                    <input
                        type="number"
                        v-model="selectedBlockElement.shadow.offsetY"
                        @blur="
                            checkClearShadow() ||
                                (selectedBlockElement !== undefined &&
                                    store.updateElement(selectedBlockElement!, 'shadow'))
                        "
                    />
                </div>
            </div>
            <div class="horizontal-block">
                <div class="horizontal-block hoverable">
                    <Icon icon="mdi:blur" />
                    <input
                        type="number"
                        v-model="selectedBlockElement.shadow.blur"
                        @blur="
                            checkClearShadow() ||
                                (selectedBlockElement !== undefined &&
                                    store.updateElement(selectedBlockElement!, 'shadow'))
                        "
                    />
                </div>
                <div class="horizontal-block hoverable">
                    <Icon icon="gis:offset" />
                    <input
                        type="number"
                        v-model="selectedBlockElement.shadow.spread"
                        @blur="
                            checkClearShadow() ||
                                (selectedBlockElement !== undefined &&
                                    store.updateElement(selectedBlockElement!, 'shadow'))
                        "
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.root {
    display: flex;
    flex-direction: column;
}

summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    color: var(--text);
}

summary h3 {
    margin: 0;
}

input {
    width: 85px;
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
    background-color: #c63e3e5e;
    outline: none;
}

input[type="number"] {
    appearance: textfield;
    -moz-appearance: textfield;
}

.horizontal-block {
    display: flex;
    gap: 4px;
    width: fit-content;
}

.hoverable:hover {
    border: 1px solid #c63e3e5e;
}

.hoverable {
    border: 1px solid transparent;
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

h3 {
    font-weight: 300;
}
</style>
