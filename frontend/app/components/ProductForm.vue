<template>
  <form @submit.prevent="handleSubmit" class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <input
      v-model="form.name"
      required
      placeholder="ชื่อสินค้า"
      class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
    />
    <input
      v-model.number="form.price"
      required
      type="number"
      min="0"
      placeholder="ราคา"
      class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
    />
    <input
      v-model.number="form.quantity"
      required
      type="number"
      min="0"
      placeholder="จำนวน"
      class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
    />
    <select
      v-model="form.category"
      class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
    >
      <option value="electronics">Electronics (VAT 7%)</option>
      <option value="clothing">Clothing (ลด 5%)</option>
      <option value="food">Food (ราคาเต็ม)</option>
    </select>
    <input
      v-if="form.category === 'electronics'"
      v-model="form.brand"
      placeholder="แบรนด์"
      class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
    />
    <input
      v-if="form.category === 'clothing'"
      v-model="form.size"
      placeholder="ไซส์ (เช่น S, M, L)"
      class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
    />
    <input
      v-if="form.category === 'food'"
      v-model="form.expiry_date"
      placeholder="วันหมดอายุ (เช่น 2026-12-31)"
      class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
    />
    <button
      type="submit"
      class="bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition md:col-span-3"
    >
      บันทึกสินค้า
    </button>
  </form>
</template>

<script setup lang="ts">
import type { ProductPayload } from '~/composables/useShop'

const emit = defineEmits<{
  (e: 'submitted', payload: ProductPayload): void
}>()

const form = reactive({
  name: '',
  price: 0,
  quantity: 0,
  category: 'electronics' as ProductPayload['category'],
  brand: '',
  size: 'M',
  expiry_date: '',
})

function handleSubmit() {
  emit('submitted', { ...form })
  form.name = ''
  form.price = 0
  form.quantity = 0
  form.brand = ''
  form.size = 'M'
  form.expiry_date = ''
}
</script>
