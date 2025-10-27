<template>
  <div class="flex min-h-screen bg-gray-900 text-white relative">
    <!-- Cart Icon -->
    <div v-if="showCartIcon" class="absolute top-4 right-6">
      <button class="relative" @click="goToProfile">
        <span class="text-3xl">🛒</span>
        <span
          v-if="cart.length"
          class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full"
        >
          {{ cart.reduce((sum, item) => sum + item.quantity, 0) }}
        </span>
      </button>
    </div>

    <!-- Main Content -->
    <main class="flex-1 p-8">
      <!-- Products Tab -->
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
            <p class="text-sm text-gray-400 mt-1">
              Seller: {{ product.seller.username }} | Shop:
              {{ product.seller.shop_name || "N/A" }}
            </p>
          </div>
        </div>

        <p v-else class="text-gray-400 mt-16 text-center">
          🔍 No products found.
        </p>
      </div>

      <!-- Orders Tab -->
      <div v-if="activeTab === 'orders'">
        <h2 class="text-xl font-bold mb-4">📦 Orders</h2>
        <p class="text-gray-400">ยังไม่มีคำสั่งซื้อ</p>
      </div>

      <!-- Profile Tab / My Cart -->
      <div v-if="activeTab === 'profile'">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">👤 Profile & My Cart</h2>
          <!-- ปุ่มกลับไปดูสินค้า -->
          <button
            class="bg-indigo-600 hover:bg-indigo-700 px-3 py-1 rounded-lg font-semibold text-white"
            @click="
              activeTab = 'products';
              showCartIcon = true;
            "
          >
            ← Back to Products
          </button>
        </div>

        <div v-if="cart.length" class="space-y-4">
          <div
            v-for="(item, index) in cart"
            :key="index"
            class="bg-gray-800 p-4 rounded-lg flex justify-between items-center shadow-inner"
          >
            <div class="flex items-center space-x-3">
              <img
                :src="item.image_url || defaultImage"
                class="w-16 h-16 object-cover rounded"
              />
              <div>
                <p class="font-semibold">{{ item.name }}</p>
                <p class="text-sm text-gray-400">Qty: {{ item.quantity }}</p>
              </div>
            </div>
            <span class="font-semibold text-pink-400"
              >฿{{ (item.price * item.quantity).toFixed(2) }}</span
            >
          </div>
          <p class="text-right font-bold mt-2">
            Total: ฿{{
              cart
                .reduce((sum, item) => sum + item.price * item.quantity, 0)
                .toFixed(2)
            }}
          </p>
        </div>
        <p v-else class="text-gray-400 text-center mt-4">Your cart is empty</p>
      </div>
    </main>

    <!-- Product Modal -->
    <div
      v-if="selectedProduct"
      class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-60"
      @click.self="closeProduct"
    >
      <div
        class="bg-gray-900 rounded-2xl shadow-2xl w-[90%] max-w-5xl relative flex flex-col md:flex-row overflow-hidden"
      >
        <!-- ปุ่มปิด -->
        <button
          class="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl"
          @click="closeProduct"
        >
          ✕
        </button>

        <!-- ส่วนรูปสินค้า -->
        <div class="w-full md:w-1/2 flex flex-col items-center bg-gray-800 p-6">
          <img
            :src="selectedProduct.image_url || defaultImage"
            alt="Product"
            class="w-full h-96 object-contain rounded-lg bg-gray-700"
          />

          <div class="flex gap-2 mt-4">
            <img
              v-for="(img, i) in [selectedProduct.image_url]"
              :key="i"
              :src="selectedProduct.image_url || defaultImage"
              class="w-20 h-20 rounded-lg object-cover cursor-pointer border border-gray-600 hover:border-pink-400"
            />
          </div>
        </div>

        <!-- ส่วนรายละเอียดสินค้า -->
        <div class="flex-1 p-6 text-white flex flex-col justify-between">
          <div>
            <h2 class="text-3xl font-bold mb-2">{{ selectedProduct.name }}</h2>
            <p class="text-gray-300 mb-4">{{ selectedProduct.description }}</p>

            <div class="flex items-center gap-3 mb-4">
              <span class="text-yellow-400 text-xl">★★★★★</span>
              <span class="text-gray-400 text-sm">4.9 (3.2k รีวิว)</span>
            </div>

            <p class="text-4xl text-pink-400 font-extrabold mb-6">
              ฿{{ selectedProduct.price }}
            </p>
          </div>

          <div class="flex gap-4">
            <button
              class="bg-pink-600 hover:bg-white text-white  hover:text-black font-bold py-3 px-8 rounded-lg flex-1"
              @click="addToCart(selectedProduct)"
            >
              🛒 เพิ่มลงตะกร้า
            </button>
            <NuxtLink
              to="/payment"
              class="flex-1 flex items-center justify-center bg-green-600 hover:bg-white text-white hover:text-black  font-bold py-3 px-8 rounded-lg"
            >
              💰 ซื้อเลย
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";

// -----------------------------
// State
// -----------------------------
const activeTab = ref("products");
const defaultImage = "/default-item.jpg";
const allProducts = ref([]);
const selectedProduct = ref(null);
const showCartIcon = ref(true);

// 🛒 Cart state + localStorage
const cart = ref(JSON.parse(localStorage.getItem("cart") || "[]"));

// Sync cart กับ localStorage
watch(
  cart,
  (newVal) => {
    localStorage.setItem("cart", JSON.stringify(newVal));
  },
  { deep: true }
);

// -----------------------------
// Fetch products จาก API
// -----------------------------
const fetchProducts = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/products");
    allProducts.value = res.data.map((p) => ({
      id: p.id || p._id,
      name: p.name,
      description: p.description,
      price: parseFloat(p.price),
      image_url: p.image_url
        ? `http://localhost:5000${p.image_url}`
        : defaultImage,
      seller: p.seller || { username: "Unknown", shop_name: "" },
    }));
  } catch (err) {
    console.error("Failed to fetch products:", err);
  }
};

// -----------------------------
// Modal control
// -----------------------------
const openProduct = (product) => {
  selectedProduct.value = product;
};

const closeProduct = () => {
  selectedProduct.value = null;
};

// -----------------------------
// Cart functions
// -----------------------------
const addToCart = (product) => {
  const existing = cart.value.find((item) => item.id === product.id);
  if (existing) {
    existing.quantity = (existing.quantity || 1) + 1;
  } else {
    cart.value.push({ ...product, quantity: 1 });
  }
  closeProduct();
};

// ---------------
// Show cart
// ---------------
function goToProfile() {
  activeTab.value = "profile";
  showCartIcon.value = false; // ซ่อนปุ่ม
}

function goBack() {
  activeTab.value = "home";
  showCartIcon.value = true; // แสดงปุ่ม
}

// -----------------------------
// Lifecycle
// -----------------------------
onMounted(() => {
  fetchProducts();
});
</script>
