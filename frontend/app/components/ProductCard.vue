<template>
  <article class="bg-white rounded-xl shadow p-6 flex flex-col justify-between">
    <div>
      <div class="flex items-start justify-between">
        <span class="text-lg font-semibold text-gray-800">{{ product.name }}</span>
        <CategoryBadge :category="product.category" />
      </div>
      <p class="text-xs text-gray-400 mt-1">ราคาตั้ง: {{ fmt(product.price) }} บาท</p>
      <p class="mt-3 text-2xl font-bold text-indigo-600">{{ fmt(product.calculated_price) }}</p>
      <p class="text-sm text-gray-500">บาท / ชิ้น</p>
      <p class="mt-2 text-sm" :class="product.quantity > 0 ? 'text-green-600' : 'text-red-600'">
        คงเหลือ: {{ product.quantity }} ชิ้น
      </p>
    </div>

    <div class="mt-4 flex gap-2">
      <button
        v-if="canAddToCart"
        @click="$emit('add-to-cart', product.name)"
        :disabled="product.quantity <= 0"
        class="flex-1 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white text-sm font-medium py-2 rounded-lg transition"
      >
        หยิบใส่รถเข็น
      </button>
      <button
        @click="$emit('remove', product.name)"
        class="bg-red-50 hover:bg-red-100 text-red-600 text-sm font-medium px-3 py-2 rounded-lg transition"
      >
        ลบ
      </button>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { Product } from '~/composables/useShop'

defineProps<{
  product: Product
  canAddToCart: boolean
}>()

defineEmits<{
  (e: 'add-to-cart', name: string): void
  (e: 'remove', name: string): void
}>()

const fmt = new Intl.NumberFormat('th-TH').format
</script>