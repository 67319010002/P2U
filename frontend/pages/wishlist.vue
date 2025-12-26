<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />
    
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-white flex items-center gap-2">
            ❤️ รายการโปรด
          </h1>
          <p class="text-dark-400 mt-1">{{ wishlist.length }} รายการ</p>
        </div>
      </div>

      <!-- Wishlist Grid -->
      <div v-if="wishlist.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="product in wishlist" 
          :key="product.id" 
          class="card overflow-hidden group"
        >
          <div class="relative aspect-square">
            <img :src="product.image_url || '/placeholder.png'" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
            <button 
              @click="removeFromWishlist(product)"
              class="absolute top-3 right-3 w-10 h-10 rounded-full bg-dark-900/80 backdrop-blur text-red-500 flex items-center justify-center hover:bg-red-500 hover:text-white transition-colors"
            >
              ❤️
            </button>
          </div>
          <div class="p-4">
            <h3 class="font-medium text-white truncate">{{ product.name }}</h3>
            <p class="text-dark-400 text-sm mt-1">{{ product.seller?.shop_name || product.seller?.username }}</p>
            <div class="flex items-center justify-between mt-3">
              <p class="text-xl font-bold text-green-400">฿{{ product.price.toLocaleString() }}</p>
              <button 
                @click="addToCart(product)"
                class="btn-primary text-sm py-2 px-4"
              >
                🛒 เพิ่มลงตะกร้า
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="card p-12 text-center">
        <div class="w-20 h-20 rounded-full bg-dark-700 mx-auto mb-4 flex items-center justify-center text-4xl">
          ❤️
        </div>
        <h3 class="text-lg font-semibold text-white mb-2">ยังไม่มีรายการโปรด</h3>
        <p class="text-dark-400 mb-6">กดปุ่มหัวใจบนสินค้าเพื่อเพิ่มในรายการโปรด</p>
        <NuxtLink to="/dashboard" class="btn-primary">
          🛒 เลือกซื้อสินค้า
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const wishlist = ref([]);
const baseUrl = 'http://localhost:5000';

async function fetchWishlist() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get(`${baseUrl}/api/wishlist`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    wishlist.value = res.data.wishlist || [];
  } catch (err) {
    console.error('Failed to fetch wishlist:', err);
  }
}

async function removeFromWishlist(product) {
  const token = localStorage.getItem('token');
  try {
    await axios.delete(`${baseUrl}/api/wishlist/${product.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    wishlist.value = wishlist.value.filter(p => p.id !== product.id);
  } catch (err) {
    console.error('Failed to remove from wishlist:', err);
  }
}

async function addToCart(product) {
  // This should integrate with existing cart logic
  alert(`เพิ่ม ${product.name} ลงตะกร้าแล้ว!`);
}

onMounted(fetchWishlist);
</script>
