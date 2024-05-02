<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { ElementType, type AnyElement, type BlockElement } from "~/types/elements";

const store = useCurrentProjectStore();

const selectedBlockElement = computed(() => {
    const currentElement = store.selectedElements.length === 1 && store.selectedElements[0];
    if (!currentElement || currentElement.type != ElementType.Block) return;
    return currentElement;
});

const isInvalidBlockProperty = (prop?: any) => {
    return prop === undefined || prop === null || prop === "";
};

const defaultProperty = <Prop extends keyof BlockElement>(
    el: BlockElement,
    prop: Prop,
    def: BlockElement[Prop],
    additionalValidation?: (prop: BlockElement[Prop]) => boolean
) => {
    if (
        !isInvalidBlockProperty(el[prop]) &&
        (additionalValidation === undefined || additionalValidation(el[prop]))
    )
        return;

    el[prop] = def;
    store.updateElement(el, prop);
};

const defaultUnsetValues = (currentElement?: AnyElement) => {
    currentElement ||= selectedBlockElement.value;
    if (currentElement === undefined || currentElement.type !== ElementType.Block) return true;

    defaultProperty(currentElement, "background", "#ffffff");
    defaultProperty(currentElement, "x", 0);
    defaultProperty(currentElement, "y", 0);
    defaultProperty(currentElement, "width", 1, (w) => w >= 1);
    defaultProperty(currentElement, "height", 1, (h) => h >= 1);
    defaultProperty(currentElement, "borderRadius", 0);
    return true;
};

let selectedElementsPrevHack = ref([] as AnyElement[]);
store.$subscribe((_, store) => {
    if (store.selectedElements === selectedElementsPrevHack.value) return;
    defaultUnsetValues(selectedElementsPrevHack.value[0]);
    selectedElementsPrevHack.value = store.selectedElements;
});

const elementColor = computed(() => {
    const currentElement = selectedBlockElement.value;
    if (currentElement === undefined || currentElement.background === undefined) return "#ffffff";
    return currentElement.background;
});
</script>

<template>
    <div class="block-edit-wrapper" v-if="selectedBlockElement">
        <div class="coordinates-wrapper">
            <div class="horizontal-block">
                <Icon icon="healthicons:x" />
                <input
                    type="number"
                    v-model="selectedBlockElement.x"
                    @blur="
                        defaultUnsetValues(selectedBlockElement) &&
                            selectedBlockElement !== undefined &&
                            store.updateElement(selectedBlockElement, 'x')
                    "
                />
            </div>
            <div class="horizontal-block">
                <Icon icon="healthicons:y" />
                <input
                    type="number"
                    v-model="selectedBlockElement.y"
                    @blur="
                        defaultUnsetValues(selectedBlockElement) &&
                            selectedBlockElement !== undefined &&
                            store.updateElement(selectedBlockElement, 'y')
                    "
                />
            </div>
            <div class="horizontal-block">
                <Icon icon="healthicons:w" />
                <input
                    type="number"
                    v-model="(selectedBlockElement as BlockElement).width"
                    @blur="
                        defaultUnsetValues(selectedBlockElement) &&
                            selectedBlockElement !== undefined &&
                            store.updateElement(selectedBlockElement, 'width')
                    "
                />
            </div>
            <div class="horizontal-block">
                <Icon icon="healthicons:h" />
                <input
                    type="number"
                    v-model="(selectedBlockElement as BlockElement).height"
                    @blur="
                        defaultUnsetValues(selectedBlockElement) &&
                            selectedBlockElement !== undefined &&
                            store.updateElement(selectedBlockElement, 'height')
                    "
                />
            </div>
            <div class="horizontal-block">
                <!--NOTE: Нет угла наклона-->
                <Icon icon="tabler:border-corner-rounded"></Icon>
                <input
                    type="number"
                    v-model="(selectedBlockElement as BlockElement).borderRadius"
                    @blur="
                        defaultUnsetValues(selectedBlockElement) &&
                            selectedBlockElement !== undefined &&
                            store.updateElement(selectedBlockElement, 'borderRadius')
                    "
                />
            </div>
        </div>

        <div class="background-color-wrapper">
            <h3>Заполнение</h3>
            <div class="horizontal-block">
                <div class="picked-color" />
                <input
                    type="text"
                    v-model="(selectedBlockElement as BlockElement).background"
                    @blur="
                        defaultUnsetValues(selectedBlockElement) &&
                            selectedBlockElement !== undefined &&
                            store.updateElement(selectedBlockElement, 'background')
                    "
                />
            </div>
        </div>

        <AttributesEditBorder />
        <AttributesEditShadows />
    </div>
</template>

<style scoped>
.block-edit-wrapper {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.block-edit-wrapper > * {
    width: calc(100% - 30px);
    padding: 15px;
    border-bottom: 1px solid var(--text);
}

.coordinates-wrapper {
    height: fit-content;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
    grid-template-areas:
        ". ."
        ". ."
        ". .";
}

.background-color-wrapper h3 {
    margin-top: 0px;
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
    background-color: v-bind(elementColor);
}

h3 {
    font-weight: 300;
}
</style>
