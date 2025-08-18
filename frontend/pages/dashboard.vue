<template>
  <div class="flex min-h-screen bg-gray-900 text-white relative">
    <!-- Cart Icon -->
    <div class="absolute top-4 right-6">
      <button class="relative">
        <!-- ไอคอนรถเข็น -->
        <span class="text-3xl">🛒</span>
        <!-- ตัวเลขจำนวนสินค้า -->
        <span
          v-if="cart.length"
          class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full"
        >
          {{ cart.length }}
        </span>
      </button>
    </div>

    <!-- Main Content -->
    <main class="flex-1 p-8">
      <!-- Products -->
      <div v-if="activeTab === 'products'">
        <h2 class="text-xl font-bold mb-4">🛒 Products</h2>
        <div
          v-if="allProducts.length"
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6"
        >
          <div
            v-for="product in allProducts"
            :key="product.id"
            class="bg-gray-800 rounded-lg shadow-md p-4 cursor-pointer hover:bg-gray-700 transition"
            @click="openProduct(product)"
          >
            <img
              :src="product.image_url || defaultImage"
              class="w-full h-40 object-cover rounded mb-3"
            />
            <h3 class="font-semibold">{{ product.name }}</h3>
            <p class="text-sm text-gray-400">{{ product.description }}</p>
            <p class="mt-2 font-bold text-indigo-400">฿{{ product.price }}</p>
            <!-- แสดงชื่อร้านและผู้ขาย -->
            <p class="text-sm text-gray-400 mt-1">
              Seller: {{ product.seller.username }} | Shop: {{ product.seller.shop_name || 'N/A' }}
            </p>
          </div>
        </div>
        <p v-else class="text-gray-400 mt-16 text-center">🔍 No products found.</p>
      </div>

      <!-- Orders -->
      <div v-if="activeTab === 'orders'">
        <h2 class="text-xl font-bold mb-4">📦 Orders</h2>
        <p class="text-gray-400">ยังไม่มีคำสั่งซื้อ</p>
      </div>

      <!-- Profile -->
      <div v-if="activeTab === 'profile'">
        <h2 class="text-xl font-bold mb-4">👤 Profile</h2>
        <p class="text-gray-400">ข้อมูลผู้ใช้จะแสดงตรงนี้</p>
      </div>
    </main>

    <!-- Modal -->
    <div
      v-if="selectedProduct"
      class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50"
      @click.self="closeProduct"
    >
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-lg relative">
        <!-- ปุ่มปิด -->
        <button
          class="absolute top-2 right-2 text-gray-400 hover:text-white"
          @click="closeProduct"
        >
          ✖
        </button>

        <img
          :src="selectedProduct.image_url || defaultImage"
          class="w-full h-60 object-cover rounded mb-4"
        />
        <h2 class="text-2xl font-bold mb-2">{{ selectedProduct.name }}</h2>
        <p class="text-gray-300 mb-2">{{ selectedProduct.description }}</p>
        <p class="text-lg font-bold text-indigo-400 mb-3">฿{{ selectedProduct.price }}</p>
        <p class="text-sm text-gray-400">
          Seller: {{ selectedProduct.seller.username }} | Shop: {{ selectedProduct.seller.shop_name || 'N/A' }}
        </p>

        <!-- ปุ่มเพิ่มลงตะกร้า -->
        <button
          class="mt-4 bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg font-semibold"
          @click="addToCart(selectedProduct)"
        >
          🛒 Add to Cart
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const activeTab = ref("products");
const defaultImage = "/default-item.jpg";
const allProducts = ref([]);
const selectedProduct = ref(null);
const cart = ref([]); // 🛒 state ของตะกร้า

// ดึงสินค้าทุกตัวจาก public API
const fetchProducts = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/products");
    // แปลงข้อมูลให้ตรงกับ property ที่ใช้ใน template
    allProducts.value = res.data.map(p => ({
      id: p.id || p._id,
      name: p.name,
      description: p.description,
      price: p.price,
      image_url: p.image_url || defaultImage,
      seller: p.seller || { username: "Unknown", shop_name: "" } // fallback ถ้าไม่มี seller
    }));
  } catch (err) {
    console.error("Failed to fetch products:", err);
  }
};

// เปิดป๊อปอัพ
const openProduct = (product) => {
  selectedProduct.value = product;
};

// ปิดป๊อปอัพ
const closeProduct = () => {
  selectedProduct.value = null;
};

// เพิ่มสินค้าในตะกร้า
const addToCart = (product) => {
  cart.value.push(product);
  closeProduct();
};
onMounted(() => {
  fetchProducts();
});
</script>
