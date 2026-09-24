<template>
  <div class="space-y-8">
    <div>
      <h2 class="text-2xl font-bold text-gray-800">ลูกค้า และ รถเข็น (Encapsulation)</h2>
      <p class="text-gray-500 text-sm">ข้อมูล private ถูกเข้าถึงผ่าน method/property (getter) และจ่ายเงินผ่าน interface ต่าง ๆ (Polymorphism)</p>
    </div>

    <ErrorBanner :message="error" />

    <!-- Create customer -->
    <div class="bg-white rounded-xl shadow p-6">
      <h3 class="text-lg font-bold text-gray-800 mb-4">สร้างลูกค้า</h3>
      <form @submit.prevent="handleCreate" class="flex gap-3 flex-wrap">
        <input v-model="newCust.name" required placeholder="ชื่อลูกค้า"
          class="input" />
        <input v-model.number="newCust.balance" required type="number" min="0" placeholder="ยอดเงิน"
          class="input w-40" />
        <button type="submit" class="btn btn-emerald">เพิ่มลูกค้า</button>
      </form>
    </div>

    <!-- Customer list -->
    <div v-if="customers.length" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div v-for="c in customers" :key="c.name" class="bg-white rounded-xl shadow p-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-bold text-gray-800">{{ c.name }}</h3>
          <span class="text-sm text-gray-600">ยอดคงเหลือ: <b class="text-emerald-600">{{ fmt(c.balance) }} บาท</b></span>
        </div>

        <!-- Cart items -->
        <div class="mt-4">
          <p class="text-sm text-gray-500">
            มูลค่ารถเข็น: <b class="text-indigo-600">{{ fmt(c.cart_total) }} บาท</b>
          </p>
          <ul v-if="c.cart_items.length" class="mt-2 divide-y divide-gray-100">
            <li v-for="item in c.cart_items" :key="item.name"
              class="flex items-center justify-between gap-3 py-2 text-sm">
              <div class="min-w-0">
                <div class="flex items-center gap-2">
                  <CategoryBadge :category="item.category" />
                  <span class="font-medium text-gray-800">{{ item.name }}</span>
                </div>
                <span class="text-xs text-gray-500">
                  {{ fmt(item.price) }} บาท / ชิ้น
                </span>
              </div>
              <div class="flex shrink-0 items-center gap-2">
                <span class="text-xs text-gray-500">
                  {{ fmt(item.price * item.quantity) }} บาท
                </span>
                <div class="flex items-center rounded-lg border border-gray-200">
                  <button
                    type="button"
                    @click="handleDecreaseFromCart(c.name, item.name)"
                    :disabled="loading || item.quantity <= 1"
                    class="quantity-button"
                    aria-label="ลดจำนวนสินค้า"
                  >
                    −
                  </button>
                  <span class="w-7 text-center text-sm font-semibold text-gray-700">
                    {{ item.quantity }}
                  </span>
                  <button
                    type="button"
                    @click="handleIncreaseFromCart(c.name, item.name)"
                    :disabled="loading || productStock(item.name) <= 0"
                    class="quantity-button"
                    aria-label="เพิ่มจำนวนสินค้า"
                  >
                    +
                  </button>
                </div>
                <button
                  type="button"
                  @click="handleRemoveAllFromCart(c.name, item.name, item.quantity)"
                  :disabled="loading"
                  class="text-red-500 hover:text-red-700 text-xs font-medium"
                >
                  ลบทั้งหมด
                </button>
              </div>
            </li>
          </ul>
          <p v-else class="mt-2 text-xs text-gray-400">รถเข็นว่างอยู่</p>
        </div>

        <!-- Add product to cart -->
        <div class="mt-4">
          <label class="text-xs text-gray-500 font-medium">เลือกสินค้าไปที่รถเข็น</label>
          <div class="flex gap-2 mt-1">
            <select v-model="byProduct[c.name]" class="input flex-1">
              <option value="" disabled>-- เลือกสินค้า --</option>
              <option v-for="p in availableProducts(c.name)" :key="p.name" :value="p.name">
                {{ p.name }} ({{ fmt(p.calculated_price) }} บาท)
              </option>
            </select>
            <button @click="handleAddToCart(c.name)"
              :disabled="!byProduct[c.name] || !availableProducts(c.name).length"
              class="btn btn-indigo">🛒 เพิ่ม 1 ชิ้น</button>
          </div>
        </div>

        <!-- Checkout -->
        <div class="mt-4">
          <label class="text-xs text-gray-500 font-medium">ชำระเงินผ่าน</label>
          <div class="flex gap-2 mt-1">
            <select v-model="byPayment[c.name]" class="input flex-1">
              <option value="cash">Cash (เงินสด)</option>
              <option value="card">Credit Card (+3%)</option>
              <option value="promptpay">PromptPay</option>
            </select>
            <button
              @click="handleCheckout(c.name)"
              :disabled="c.cart_total <= 0"
              class="btn btn-emerald">💳 Checkout</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="bg-white rounded-xl shadow p-8 text-center text-gray-500">
      ยังไม่มีลูกค้า — สร้างลูกค้าขึ้นมาก่อนเพื่อทดสอบรถเข็นและชำระเงิน
    </div>
  </div>
</template>

<script setup lang="ts">
import { useShop } from '~/composables/useShop'

const {
  customers,
  products,
  error,
  loading,
  fetchCustomers,
  fetchProducts,
  createCustomer,
  addToCart,
  removeFromCart,
  checkout,
} = useShop()

const newCust = reactive({ name: '', balance: 0 })
const byProduct = reactive<Record<string, string>>({})
const byPayment = reactive<Record<string, string>>({})

const fmt = new Intl.NumberFormat('th-TH').format

onMounted(async () => {
  await Promise.all([fetchCustomers(), fetchProducts()])
})

/** Products with stock left for the initial add control. */
function availableProducts(customerName: string) {
  const customer = customers.value.find(c => c.name === customerName)
  const inCart = customer ? new Set(customer.cart_items.map(i => i.name)) : new Set()
  return products.value.filter(p => p.quantity > 0 && !inCart.has(p.name))
}

function productStock(productName: string) {
  return products.value.find(p => p.name === productName)?.quantity ?? 0
}

async function handleCreate() {
  const ok = await createCustomer({ ...newCust })
  if (ok) {
    newCust.name = ''
    newCust.balance = 0
  }
}

async function handleAddToCart(customerName: string) {
  const productName = byProduct[customerName]
  if (productName) {
    await addToCart(customerName, productName)
    byProduct[customerName] = ''
  }
}

async function handleIncreaseFromCart(customerName: string, productName: string) {
  if (productStock(productName) > 0) {
    await addToCart(customerName, productName, 1)
  }
}

async function handleDecreaseFromCart(customerName: string, productName: string) {
  await removeFromCart(customerName, productName, 1)
}

async function handleRemoveAllFromCart(
  customerName: string,
  productName: string,
  quantity: number,
) {
  await removeFromCart(customerName, productName, quantity)
}

async function handleCheckout(customerName: string) {
  const payment = byPayment[customerName] || 'cash'
  await checkout(customerName, payment)
}
</script>

<style scoped>
.input {
  @apply border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none;
}
.quantity-button {
  @apply w-7 h-8 text-gray-600 hover:bg-gray-100 disabled:text-gray-300 disabled:hover:bg-transparent;
}
.btn {
  @apply text-white text-sm px-4 py-2 rounded-lg transition disabled:bg-gray-300;
}
.btn-indigo {
  @apply bg-indigo-600 hover:bg-indigo-700;
}
.btn-emerald {
  @apply bg-emerald-600 hover:bg-emerald-700;
}
</style>