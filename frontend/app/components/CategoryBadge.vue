<template>
  <span :class="badgeClass" class="text-xs font-semibold px-2 py-1 rounded-full">
    {{ label }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{ category: string }>()

const badgeMap: Record<string, { label: string; cls: string }> = {
  Electronics: { label: 'Electronics', cls: 'bg-blue-100 text-blue-700' },
  Clothing: { label: 'Clothing', cls: 'bg-pink-100 text-pink-700' },
  Food: { label: 'Food', cls: 'bg-green-100 text-green-700' },
}

const badge = computed(() => badgeMap[props.category] || { label: props.category, cls: 'bg-gray-100 text-gray-700' })
const label = badge.value.label
const badgeClass = badge.value.cls
</script>
