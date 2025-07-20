<script setup>
defineProps({
  title: String,
})
</script>

<template>
  <div class="screen">
    <h3 class="screen-title">{{ title }}</h3>
    <div class="screen-content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.screen {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: 0.3s ease;
}
.screen-title {
  margin-bottom: 0.8rem;
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--cl-tertiary);
}
.screen-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
