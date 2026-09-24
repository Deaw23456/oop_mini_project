<template>
  <div class="space-y-8">
    <section>
      <h2 class="text-2xl font-bold text-gray-800">รายการสินค้า (Inventory)</h2>
      <p class="text-gray-500 text-sm">
        แสดง Polymorphism — แต่ละชนิดคำนวณราคาไม่เหมือนกัน (VAT / ส่วนลด / ราคาเต็ม)
      </p>
    </section>

    <ErrorBanner :message="error" />

    <section v-if="loading && products.length === 0" class="text-gray-500">
      กำลังโหลดสินค้า...
    </section>

    <section v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProductCard
        v-for="p in products"
        :key="p.name"
        :product="p"
        :can-add-to-cart="customers.length > 0"
        @add-to-cart="handleAddToCart"
        @remove="handleRemove"
      />
    </section>

    <section class="bg-white rounded-xl shadow p-6">
      <h3 class="text-lg font-bold text-gray-800 mb-4">เพิ่มสินค้าใหม่</h3>
      <ProductForm @submitted="handleAddProduct" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { useShop, type ProductPayload } from '~/composables/useShop'

const {
  products,
  customers,
  loading,
  error,
  fetchProducts,
  fetchCustomers,
  addProduct,
  removeProduct,
  addToCart,
} = useShop()

const selectedCustomer = ref('')

onMounted(async () => {
  await Promise.all([fetchProducts(), fetchCustomers()])
  if (customers.value.length) {
    selectedCustomer.value = customers.value[0].name
  }
})

async function handleAddProduct(payload: ProductPayload) {
  await addProduct(payload)
}

function handleAddToCart(productName: string) {
  if (selectedCustomer.value) {
    addToCart(selectedCustomer.value, productName)
  }
}

function handleRemove(productName: string) {
  removeProduct(productName)
}
</script>