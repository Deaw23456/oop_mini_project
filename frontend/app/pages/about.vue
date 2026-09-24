<template>
  <div class="space-y-8">
    <div>
      <h2 class="text-2xl font-bold text-gray-800">หลักการ OOP ทั้ง 4 ข้อ</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="card in cards" :key="card.title"
        class="bg-white rounded-xl shadow p-6 border-t-4"
        :style="{ borderColor: card.color }">
        <h3 class="text-lg font-bold text-gray-800 mb-2">{{ card.title }}</h3>
        <p class="text-gray-600 text-sm leading-relaxed">{{ card.desc }}</p>
        <pre class="mt-4 bg-gray-50 border rounded-lg p-3 text-xs text-gray-700 overflow-x-auto">{{ card.code }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const cards = [
  {
    title: 'Encapsulation (การห่อหุ้มข้อมูล)',
    color: '#6366f1',
    desc: 'ซ่อนข้อมูลภายในด้วย private fields และเข้าถึงผ่าน getters/setters ที่ควบคุมค่าได้',
    code: `class Customer:\n    def __init__(self, name, balance):\n        self._name = name\n        self._balance = balance\n\n    @property\n    def balance(self):\n        return self._balance`,
  },
  {
    title: 'Inheritance (การสืบทอด)',
    color: '#ec4899',
    desc: 'คลาสย่อยสืบทอดคุณสมบัติจากคลาสแม่ Product และเพิ่มรายละเอียดเฉพาะของตัวเอง',
    code: `class Product(ABC):\n    ...\n\nclass Electronics(Product):\n    ...\n\nclass Clothing(Product):\n    ...`,
  },
  {
    title: 'Polymorphism (การมีหลายรูปแบบ)',
    color: '#10b981',
    desc: 'เมธอดเดียวกัน calculate_price() ทำงานต่างกันตามชนิดของสินค้า',
    code: `for p in products:\n    # เรียกแบบเดียวกัน แต่ผลต่างกัน\n    print(p.calculate_price())\n# iPhone  >>> 32100.00 (VAT)\n# T-Shirt >>> 475.00 (discount)\n# Milk    >>> 50.00  (full)`,
  },
  {
    title: 'Abstraction (การซ่อนรายละเอียด)',
    color: '#f59e0b',
    desc: 'ใช้ abstract class (Product) และ interface (Paymentable) กำหนดโครงสร้าง โดยไม่ต้องรู้รายละเอียดภายใน',
    code: `class Paymentable(ABC):\n    @abstractmethod\n    def pay(self, amount): ...\n\nclass CashPayment(Paymentable):\n    def pay(self, amount):\n        return f"Paid {amount} cash"`,
  },
]
</script>
