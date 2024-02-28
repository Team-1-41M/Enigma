<script setup lang="ts">
interface Props {
  text: string,
}
const props = defineProps<Props>()
</script>

<template>
  <li>
    {{ props.text }}
  </li>

</template>

<style scoped>
li {
  color: var(--text);
  border-bottom: 1px solid #DEDBDB;
  width: 90%;
  padding: 5%;
  margin: 0;
  font-family: Inter;
  font-size: 15px;
  font-weight: 400;
  line-height: 18px;
  letter-spacing: 0em;
  text-align: left;
}

li:first-child {
  border-radius: 9px 9px 0 0;
}

li:last-child {
  border-bottom: none;
  border-radius: 0 0 9px 9px;
}

li:hover {
  cursor: pointer;
  background-color: #34203a;
}
</style>