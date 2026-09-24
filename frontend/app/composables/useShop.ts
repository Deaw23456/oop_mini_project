export interface Product {
  name: string
  price: number
  quantity: number
  category: string
  calculated_price: number
}

export interface CartItem {
  name: string
  price: number
  category: string
  quantity: number
}

export interface Customer {
  name: string
  balance: number
  cart_total: number
  cart_items: CartItem[]
}

export interface ProductPayload {
  name: string
  price: number
  quantity: number
  category: 'electronics' | 'clothing' | 'food'
  brand?: string
  size?: string
  expiry_date?: string
}

export interface CustomerPayload {
  name: string
  balance: number
}

type PaymentMethod = 'cash' | 'card' | 'promptpay'

/**
 * Shared API access for the shop system.
 */
export const useShop = () => {
  const { public: { apiBase } } = useRuntimeConfig()

  const products = ref<Product[]>([])
  const customers = ref<Customer[]>([])
  const loading = ref(false)
  const error = ref('')

  function setError(e: unknown) {
    error.value = (e as any)?.data?.detail || (e as any)?.message || 'Unknown error'
  }

  async function run<T>(operation: () => Promise<T>): Promise<T | null> {
    loading.value = true
    error.value = ''
    try {
      return await operation()
    } catch (e) {
      setError(e)
      return null
    } finally {
      loading.value = false
    }
  }

  async function fetchProducts() {
    products.value = (await run(() => $fetch<Product[]>(`${apiBase}/products`))) ?? products.value
  }

  async function fetchCustomers() {
    customers.value = (await run(() => $fetch<Customer[]>(`${apiBase}/customers`))) ?? customers.value
  }

  async function createCustomer(payload: CustomerPayload) {
    const result = await run(() => $fetch<{ message: string }>(`${apiBase}/customers`, { method: 'POST', body: payload }))
    await fetchCustomers()
    return result?.message ?? ''
  }

  async function addProduct(payload: ProductPayload) {
    const result = await run(() => $fetch<{ message: string }>(`${apiBase}/products`, { method: 'POST', body: payload }))
    await fetchProducts()
    return result?.message ?? ''
  }

  async function removeProduct(name: string) {
    const result = await run(() => $fetch<{ message: string }>(`${apiBase}/products/${name}`, { method: 'DELETE' }))
    await fetchProducts()
    return result?.message ?? ''
  }

  async function addToCart(customerName: string, productName: string, quantity = 1) {
    const result = await run(() =>
      $fetch<{ message: string }>(`${apiBase}/cart/add`, {
        method: 'POST',
        body: {
          customer_name: customerName,
          product_name: productName,
          quantity,
        },
      }),
    )
    await Promise.all([fetchCustomers(), fetchProducts()])
    return result?.message ?? ''
  }

  async function removeFromCart(
    customerName: string,
    productName: string,
    quantity = 1,
  ) {
    const result = await run(() =>
      $fetch<{ message: string }>(`${apiBase}/cart/remove`, {
        method: 'POST',
        body: {
          customer_name: customerName,
          product_name: productName,
          quantity,
        },
      }),
    )
    await Promise.all([fetchCustomers(), fetchProducts()])
    return result?.message ?? ''
  }

  async function checkout(customerName: string, payment: PaymentMethod) {
    const result = await run(() =>
      $fetch<{ message: string }>(`${apiBase}/cart/checkout`, {
        method: 'POST',
        body: { customer_name: customerName, payment },
      }),
    )
    await Promise.all([fetchCustomers(), fetchProducts()])
    return result?.message ?? ''
  }

  return {
    products,
    customers,
    loading,
    error,
    fetchProducts,
    fetchCustomers,
    createCustomer,
    addProduct,
    removeProduct,
    addToCart,
    removeFromCart,
    checkout,
  }
}