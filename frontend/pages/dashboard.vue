<template>
  <div class="bg-gray-900 text-white min-h-screen px-4 py-6">
    <!-- Header -->
    <header class="flex justify-between items-center mb-8">
      <h1 class="text-2xl font-bold">🛒 SecondHand Market</h1>
      <div class="flex items-center space-x-4">
        <input
          v-model="search"
          @input="debouncedSearch"
          type="text"
          placeholder="Search products..."
          class="px-3 py-1.5 rounded bg-gray-800 border border-gray-700 focus:outline-none"
        />
        <button class="btn-black" @click="goToCart">🛍 Cart ({{ cart.length }})</button>
      </div>
    </header>

    <!-- Product Grid -->
    <div v-if="filteredProducts.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="bg-gray-800 rounded-lg overflow-hidden shadow-md p-4 relative note-hover-effect"
      >
        <img
          :src="product.image || defaultImage"
          alt="product"
          class="w-full h-48 object-cover rounded mb-3"
        />
        <h2 class="text-lg font-semibold">{{ product.title }}</h2>
        <p class="text-sm text-gray-400 truncate">{{ product.description }}</p>
        <p class="mt-2 font-bold text-indigo-400">฿{{ product.price }}</p>
        <button
          class="mt-3 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded transition"
          @click="addToCart(product)"
        >
          Add to Cart
        </button>
      </div>
    </div>

    <p v-else class="text-center text-gray-500 mt-16">🔍 No products found.</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const defaultImage = '/default-item.jpg' // ใส่ภาพ fallback ถ้าไม่มีภาพสินค้า
const search = ref('')
const timeout = ref(null)

const allProducts = ref([
  {
    id: 1,
    title: 'Used iPhone 12',
    description: 'Secondhand in great condition',
    price: 14500,
    image: 'https://via.placeholder.com/300x200',
  },
  {
    id: 2,
    title: 'Office Chair - Like New',
    description: 'Comfortable and adjustable',
    price: 900,
    image: 'https://via.placeholder.com/300x200',
  },
  {
    id: 3,
    title: 'Gaming Laptop',
    description: 'High spec, perfect for games and work',
    price: 20000,
    image: 'https://via.placeholder.com/300x200',
  },
])

const cart = ref([])

const filteredProducts = computed(() => {
  const q = search.value.toLowerCase().trim()
  return q
    ? allProducts.value.filter((p) =>
        p.title.toLowerCase().includes(q) || p.description.toLowerCase().includes(q)
      )
    : allProducts.value
})

const debouncedSearch = () => {
  clearTimeout(timeout.value)
  timeout.value = setTimeout(() => {
    // trigger computed
  }, 300)
}

const addToCart = (product) => {
  cart.value.push(product)
}

const goToCart = () => {
  alert('Go to cart page (to be implemented)')
}
</script>

<style scoped>
.btn-black {
  background-color: #000;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: 1px solid transparent;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.btn-black:hover {
  background-color: #222;
  color: #a3a3a3;
  border-color: #555;
}
</style>
