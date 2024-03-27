<script setup lang="ts">
const socketStore = useCurrentProjectStore();
</script>

<template>
    <div class="attribute-wrapper">
        <AttributesEditBlock
            v-if="socketStore.selectedElements.length === 1 && 
                  socketStore.selectedElements.at(0)!.type === 'block'"/>
        <AttributesEditText
            v-if="socketStore.selectedElements.length === 1 && 
                  socketStore.selectedElements.at(0)!.type === 'text'"/>
    </div>
    
</template>

<style scoped>
.attribute-wrapper {
    width: 100%;
    height: 100%;
    background-color: var(--primary);
}
</style>