<script setup>
defineProps({
  modelValue: String,
  options: Array,
  label: {
    type: String,
    default: ''
  }
})
const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="select-lang">
    <label v-if="label" class="select-label">{{ label }}</label>
    <select
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    >
      <option v-for="option in options" :key="option.code" :value="option.code">
        {{ option.name }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.select-lang {
  display: flex;
  flex-direction: column;
}
.select-label {
  margin-bottom: 0.4rem;
  font-weight: 500;
  color: var(--cl-tertiary);
  font-size: 0.9rem;
}
select {
  padding: 0.6rem 1rem;
  border-radius: 12px;
  border: 1px solid var(--cl-gray-300);
  background-color: white;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  font-size: 1rem;
  cursor: pointer;
  transition: 0.3s;
}
select:focus {
  outline: 2px solid var(--cl-primary);
}
</style>
