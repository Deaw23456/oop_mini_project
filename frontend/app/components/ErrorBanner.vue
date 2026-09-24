<template>
  <div v-if="message" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded">
    ⚠️ {{ message }}
  </div>
</template>

<script setup lang="ts">
defineProps<{ message: string }>()
</script>