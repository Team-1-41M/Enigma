<script setup lang="ts">
import { Icon } from "@iconify/vue";
import {
    BorderStyle,
    ElementType,
    type AnyElement,
    type Border,
    type MultiBorders,
} from "~/types/elements";

const store = useCurrentProjectStore();

const selectedBlockElement = computed(() => {
    const currentElement = store.selectedElements.length === 1 && store.selectedElements[0];
    if (!currentElement || currentElement.type != ElementType.Block) return;
    return currentElement;
});

const elementBorderColor = computed(() => {
    const currentElement = selectedBlockElement.value;
    if (
        currentElement === undefined ||
        currentElement.borders === undefined ||
        !("color" in currentElement.borders)
    )
        return "#000000";
    return currentElement.borders.color;
});

const elementBorderTopColor = computed(() => {
    const currentElement = selectedBlockElement.value;
    if (
        currentElement === undefined ||
        currentElement.borders === undefined ||
        !("top" in currentElement.borders) ||
        currentElement.borders.top === undefined
    )
        return "#000000";
    return currentElement.borders.top.color;
});

const elementBorderRightColor = computed(() => {
    const currentElement = selectedBlockElement.value;
    if (
        currentElement === undefined ||
        currentElement.borders === undefined ||
        !("right" in currentElement.borders) ||
        currentElement.borders.right === undefined
    )
        return "#000000";
    return currentElement.borders.right.color;
});

const elementBorderBottomColor = computed(() => {
    const currentElement = selectedBlockElement.value;
    if (
        currentElement === undefined ||
        currentElement.borders === undefined ||
        !("bottom" in currentElement.borders) ||
        currentElement.borders.bottom === undefined
    )
        return "#000000";
    return currentElement.borders.bottom.color;
});

const elementBorderLeftColor = computed(() => {
    const currentElement = selectedBlockElement.value;
    if (
        currentElement === undefined ||
        currentElement.borders === undefined ||
        !("left" in currentElement.borders) ||
        currentElement.borders.left === undefined
    )
        return "#000000";
    return currentElement.borders.left.color;
});

let selectedElementsPrevHack = ref([] as AnyElement[]);
store.$subscribe((_, store) => {
    if (store.selectedElements === selectedElementsPrevHack.value) return;
    checkClearSingleBorder(selectedElementsPrevHack.value[0]);
    checkClearMultiBorder(selectedElementsPrevHack.value[0]);
    selectedElementsPrevHack.value = store.selectedElements;
});

const isInvalidBorderProperty = (prop?: any) => {
    return prop === undefined || prop === null || prop === "";
};

const validateBorder = (border?: Border) => {
    if (
        border === undefined ||
        isInvalidBorderProperty(border.width) ||
        isInvalidBorderProperty(border.color) ||
        isInvalidBorderProperty(border.style)
    )
        return undefined;
    return border;
};

const checkClearSingleBorder = (block?: AnyElement) => {
    block ||= store.selectedElements[0];
    if (block === undefined || block.type !== ElementType.Block) return;

    let border = block.borders;
    if (border === undefined || !("color" in border)) return;

    if (validateBorder(border)) return;

    block.borders = undefined;
    store.updateElement(block, "borders");
    return false;
};

const checkClearMultiBorder = (block?: AnyElement) => {
    block ||= store.selectedElements[0];
    if (block === undefined || block.type !== ElementType.Block) return;

    let borders = block.borders;
    if (borders === undefined || "color" in borders) return;

    let top = validateBorder(borders.top);
    let right = validateBorder(borders.right);
    let bottom = validateBorder(borders.bottom);
    let left = validateBorder(borders.left);
    if (top || right || bottom || left) {
        borders.top = top;
        borders.right = right;
        borders.bottom = bottom;
        borders.left = left;
        store.updateElement(block, "borders");
        return;
    }

    block.borders = undefined;
    store.updateElement(block, "borders");
    return false;
};

const toggleBorders = () => {
    let block = store.selectedElements[0];
    if (block === undefined || block.type !== ElementType.Block) return;

    if (block.borders !== undefined) block.borders = undefined;
    else {
        block.borders = {
            color: "#000000",
            width: 1,
            style: BorderStyle.Solid,
        };
    }
    store.updateElement(block, "borders");
};

const toggleMultiBorder = (border: keyof MultiBorders) => {
    let block = store.selectedElements[0];
    if (block === undefined || block.type !== ElementType.Block) return;

    let borders = block.borders;
    if (borders === undefined || "color" in borders) return;

    if (borders[border] !== undefined) borders[border] = undefined;
    else {
        borders[border] = {
            color: "#000000",
            width: 1,
            style: BorderStyle.Solid,
        };
    }
    store.updateElement(block, "borders");
};

const goToSingleBorderMode = () => {
    let block = store.selectedElements[0];
    if (block === undefined || block.type !== ElementType.Block) return;

    let initialBorders = block.borders;
    if (initialBorders === undefined || "color" in initialBorders) return;

    let border =
        validateBorder(initialBorders.top) ||
        validateBorder(initialBorders.right) ||
        validateBorder(initialBorders.bottom) ||
        validateBorder(initialBorders.left);
    block.borders = border && { ...border };
    store.updateElement(block, "borders");
};

const goToMultiBordersMode = () => {
    let block = store.selectedElements[0];
    if (block === undefined || block.type !== ElementType.Block) return;

    let initialBorders = block.borders;
    if (initialBorders === undefined || !("color" in initialBorders)) return;

    block.borders = {
        top: { ...initialBorders },
        bottom: { ...initialBorders },
        left: { ...initialBorders },
        right: { ...initialBorders },
    };
    store.updateElement(block, "borders");
};
</script>

<template>
    <div v-if="selectedBlockElement !== undefined">
        <summary class="border" @click="toggleBorders()">
            <h3>Границы</h3>
            <Icon
                :icon="
                    selectedBlockElement.borders === undefined ? 'ic:round-plus' : 'ic:round-minus'
                "
            />
        </summary>

        <!-- One Border Mode -->
        <div
            class="border"
            v-if="selectedBlockElement.borders && 'color' in selectedBlockElement.borders"
        >
            <div class="horizontal-block">
                <div class="horizontal-block hoverable">
                    <div class="picked-border-color" />
                    <input
                        type="text"
                        v-model="selectedBlockElement.borders.color"
                        @blur="
                            checkClearSingleBorder() ||
                                (selectedBlockElement !== undefined &&
                                    store.updateElement(selectedBlockElement, 'borders'))
                        "
                    />
                </div>
                <div class="horizontal-block hoverable">
                    <Icon icon="fluent:line-thickness-20-regular" />
                    <input
                        type="number"
                        v-model="selectedBlockElement.borders.width"
                        @blur="
                            checkClearSingleBorder() ||
                                (selectedBlockElement !== undefined &&
                                    store.updateElement(selectedBlockElement, 'borders'))
                        "
                    />
                </div>
            </div>
            <div class="horizontal-block border">
                <select v-model="selectedBlockElement.borders.style">
                    <option :value="'solid'">Прямая</option>
                    <option :value="'dashed'">Линиями</option>
                    <option :value="'dotted'">Точками</option>
                </select>
            </div>
            <Icon icon="tabler:dots" @click="goToMultiBordersMode" />
        </div>

        <!-- All Borders Mode-->
        <div
            v-else-if="selectedBlockElement?.borders && !('color' in selectedBlockElement.borders)"
        >
            <div class="horizontal-block">
                <Icon icon="tabler:dots" @click="goToSingleBorderMode" />
            </div>

            <summary @click="toggleMultiBorder('top')">
                <label>Верхняя</label>
                <Icon
                    :icon="
                        selectedBlockElement.borders.top === undefined
                            ? 'ic:round-plus'
                            : 'ic:round-minus'
                    "
                />
            </summary>
            <div class="border" v-if="selectedBlockElement.borders.top !== undefined">
                <div class="horizontal-block">
                    <div class="horizontal-block hoverable">
                        <div class="picked-border-color top" />
                        <input
                            type="text"
                            v-model="selectedBlockElement.borders.top.color"
                            @blur="
                                checkClearMultiBorder() ||
                                    (selectedBlockElement !== undefined &&
                                        store.updateElement(selectedBlockElement, 'borders'))
                            "
                        />
                    </div>

                    <div class="horizontal-block hoverable">
                        <Icon icon="fluent:line-thickness-20-regular" />
                        <input
                            type="number"
                            v-model="selectedBlockElement.borders.top.width"
                            @blur="
                                checkClearMultiBorder() ||
                                    (selectedBlockElement !== undefined &&
                                        store.updateElement(selectedBlockElement, 'borders'))
                            "
                        />
                    </div>
                </div>
                <div class="horizontal-block">
                    <select v-model="selectedBlockElement.borders.top.style">
                        <option :value="'solid'">Прямая</option>
                        <option :value="'dashed'">Линиями</option>
                        <option :value="'dotted'">Точками</option>
                    </select>
                </div>
            </div>

            <summary @click="toggleMultiBorder('right')">
                <label>Правая</label>
                <Icon
                    :icon="
                        selectedBlockElement.borders.right === undefined
                            ? 'ic:round-plus'
                            : 'ic:round-minus'
                    "
                />
            </summary>
            <div class="border" v-if="selectedBlockElement.borders.right !== undefined">
                <div class="horizontal-block">
                    <div class="horizontal-block hoverable">
                        <div class="picked-border-color right" />
                        <input
                            type="text"
                            v-model="selectedBlockElement.borders.right.color"
                            @blur="
                                checkClearMultiBorder() ||
                                    (selectedBlockElement !== undefined &&
                                        store.updateElement(selectedBlockElement, 'borders'))
                            "
                        />
                    </div>

                    <div class="horizontal-block hoverable">
                        <Icon icon="fluent:line-thickness-20-regular" />
                        <input
                            type="number"
                            v-model="selectedBlockElement.borders.right.width"
                            @blur="
                                checkClearMultiBorder() ||
                                    (selectedBlockElement !== undefined &&
                                        store.updateElement(selectedBlockElement, 'borders'))
                            "
                        />
                    </div>
                </div>
                <div class="horizontal-block">
                    <select v-model="selectedBlockElement.borders.right.style">
                        <option :value="'solid'">Прямая</option>
                        <option :value="'dashed'">Линиями</option>
                        <option :value="'dotted'">Точками</option>
                    </select>
                </div>
            </div>

            <summary @click="toggleMultiBorder('bottom')">
                <label>Нижняя</label>
                <Icon
                    :icon="
                        selectedBlockElement.borders.bottom === undefined
                            ? 'ic:round-plus'
                            : 'ic:round-minus'
                    "
                />
            </summary>
            <div class="border" v-if="selectedBlockElement.borders.bottom !== undefined">
                <div class="horizontal-block">
                    <div class="horizontal-block hoverable">
                        <div class="picked-border-color bottom" />
                        <input
                            type="text"
                            v-model="selectedBlockElement.borders.bottom.color"
                            @blur="
                                checkClearMultiBorder() ||
                                    (selectedBlockElement !== undefined &&
                                        store.updateElement(selectedBlockElement, 'borders'))
                            "
                        />
                    </div>

                    <div class="horizontal-block hoverable">
                        <Icon icon="fluent:line-thickness-20-regular" />
                        <input
                            type="number"
                            v-model="selectedBlockElement.borders.bottom.width"
                            @blur="
                                checkClearMultiBorder() ||
                                    (selectedBlockElement !== undefined &&
                                        store.updateElement(selectedBlockElement, 'borders'))
                            "
                        />
                    </div>
                </div>
                <div class="horizontal-block">
                    <select v-model="selectedBlockElement.borders.bottom.style">
                        <option :value="'solid'">Прямая</option>
                        <option :value="'dashed'">Линиями</option>
                        <option :value="'dotted'">Точками</option>
                    </select>
                </div>
            </div>

            <summary @click="toggleMultiBorder('left')">
                <label>Левая</label>
                <Icon
                    :icon="
                        selectedBlockElement.borders.left === undefined
                            ? 'ic:round-plus'
                            : 'ic:round-minus'
                    "
                />
            </summary>
            <div class="border" v-if="selectedBlockElement.borders.left !== undefined">
                <div class="horizontal-block">
                    <div class="horizontal-block hoverable">
                        <div class="picked-border-color left" />
                        <input
                            type="text"
                            v-model="selectedBlockElement.borders.left.color"
                            @blur="
                                checkClearMultiBorder() ||
                                    (selectedBlockElement !== undefined &&
                                        store.updateElement(selectedBlockElement, 'borders'))
                            "
                        />
                    </div>

                    <div class="horizontal-block hoverable">
                        <Icon icon="fluent:line-thickness-20-regular" />
                        <input
                            type="number"
                            v-model="selectedBlockElement.borders.left.width"
                            @blur="
                                checkClearMultiBorder() ||
                                    (selectedBlockElement !== undefined &&
                                        store.updateElement(selectedBlockElement, 'borders'))
                            "
                        />
                    </div>
                </div>
                <div class="horizontal-block">
                    <select v-model="selectedBlockElement.borders.left.style">
                        <option :value="'solid'">Прямая</option>
                        <option :value="'dashed'">Линиями</option>
                        <option :value="'dotted'">Точками</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: var(--text);
    cursor: pointer;
}

summary h3 {
    margin: 0;
}

select {
    background-color: transparent;
    color: var(--text);
    font: inherit;
    border: none;
    outline: none;
}

option {
    background-color: var(--primary-darker);
    color: var(--text);
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
    flex-wrap: wrap;
    gap: 4px;
    width: fit-content;
}

.border {
    margin-bottom: 10px;
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

h3 {
    font-weight: 300;
}
</style>
