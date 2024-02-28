<script setup lang="ts">
interface Props {
  closeHandler: () => void;
}
const props = defineProps<Props>();

const dropdown = ref(null)

onMounted(() => {
  (dropdown.value! as HTMLUListElement).focus()
})
</script>

<template>
    <ul 
      class="dropdown-options-list"
      tabindex="1"
      ref="dropdown"
      @blur="closeHandler">
      <slot/>
    </ul>
</template>

<style scoped>
.dropdown-options-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  border-radius: 7px;
  background-color: #1E0825;
}

.dropdown-options-list:focus {
  border: none;
}
</style>