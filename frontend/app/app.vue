<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-indigo-700 text-white shadow">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div>
            <h1 class="text-xl font-bold leading-tight">Shop OOP Management System</h1>
            <p class="text-xs text-indigo-200">Vue.js + Nuxt.js demo covering all 4 OOP principles</p>
          </div>
        </div>
        <nav class="flex gap-2 text-sm">
          <NuxtLink to="/" class="px-3 py-2 rounded hover:bg-indigo-600" active-class="bg-indigo-800">สินค้า</NuxtLink>
          <NuxtLink to="/customers" class="px-3 py-2 rounded hover:bg-indigo-600" active-class="bg-indigo-800">ลูกค้า</NuxtLink>
          <NuxtLink to="/about" class="px-3 py-2 rounded hover:bg-indigo-600" active-class="bg-indigo-800">หลัก OOP</NuxtLink>
        </nav>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-6 py-8">
      <NuxtPage />
    </main>
  </div>
</template>
