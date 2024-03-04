<script setup lang="ts">
const slots = defineSlots<{ [key: string]: () => any }>();
const variants = Object.keys(slots);
const variantCount = variants.length;

defineProps<{
    tabSelect: (variant: string, index: number) => void;
    selected: number;
}>();
</script>

<template>
    <div class="parent">
        <div v-for="(variant, index) in variants" :onclick="() => tabSelect(variant, index)" :selected="selected == index">
            <slot :name="variant" />
        </div>
    </div>
</template>

<style scoped>
.parent {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.parent::before {
    content: '';
    position: absolute;
    left: calc(50% + v-bind((selected * 172 - variantCount * 172 / 2) + 'px'));
    transition: left 250ms;
    background-color: var(--auth-primary);

    border-radius: 50px;
    width: 172px;
    height: 50px;
    z-index: -1;
}

.parent div {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;

    width: 172px;
    height: 50px;
}

.parent div[selected='true'] {
    color: var(--text);
}
</style>