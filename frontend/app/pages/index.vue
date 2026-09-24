<template>
  <div class="space-y-8">
    <section>
      <h2 class="text-2xl font-bold text-gray-800">รายการสินค้า</h2>
      <p class="text-gray-500 text-sm">
        แสดง Polymorphism — แต่ละชนิดคำนวณราคาไม่เหมือนกัน (VAT / ส่วนลด / ราคาเต็ม)
      </p>
    </section>

    <ErrorBanner :message="error" />

    <section v-if="customers.length" class="bg-white rounded-xl shadow p-4">
      <div class="flex flex-col gap-2 sm:flex-row sm:items-center">
        <label for="index-customer" class="text-sm font-medium text-gray-700">
          เพิ่มสินค้าให้ลูกค้า:
        </label>
        <select
          id="index-customer"
          v-model="selectedCustomer"
          class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none sm:w-64"
        >
          <option v-for="customer in customers" :key="customer.name" :value="customer.name">
            {{ customer.name }}
          </option>
        </select>
      </div>
    </section>
    <p v-else-if="!loading" class="text-sm text-gray-500">
      ยังไม่มีลูกค้า — สร้างลูกค้าในหน้า <NuxtLink to="/customers" class="text-indigo-600 underline">ลูกค้า</NuxtLink> ก่อนเพิ่มสินค้าเข้ารถเข็น
    </p>

    <section v-if="loading && products.length === 0" class="text-gray-500">
      กำลังโหลดสินค้า...
    </section>

    <section v-else-if="products.length === 0" class="bg-white rounded-xl shadow p-6 text-center text-gray-500">
      ยังไม่มีสินค้าในร้าน
    </section>

    <section v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProductCard
        v-for="p in products"
        :key="p.name"
        :product="p"
        :can-add-to-cart="!!selectedCustomer"
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
  selectedCustomer.value = customers.value[0]?.name ?? ''
})

watch(customers, (customerList) => {
  if (!customerList.some(customer => customer.name === selectedCustomer.value)) {
    selectedCustomer.value = customerList[0]?.name ?? ''
  }
})

async function handleAddProduct(payload: ProductPayload) {
  await addProduct(payload)
}

async function handleAddToCart(productName: string) {
  if (selectedCustomer.value) {
    await addToCart(selectedCustomer.value, productName)
  }
}

async function handleRemove(productName: string) {
  await removeProduct(productName)
}
</script>
