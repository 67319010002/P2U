<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-6">
    <div class="max-w-5xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8 pt-5">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-pink-400 to-purple-500 bg-clip-text text-transparent mb-2">
          การชำระเงิน
        </h1>
        <p class="text-gray-400">ตรวจสอบและยืนยันการสั่งซื้อของคุณ</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Products List -->
        <div class="lg:col-span-2 space-y-4">
          <div class="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-pink-400" viewBox="0 0 24 24">
                <path fill="currentColor" d="M7 22q-.825 0-1.412-.587T5 20t.588-1.412T7 18t1.413.588T9 20t-.587 1.413T7 22m10 0q-.825 0-1.412-.587T15 20t.588-1.412T17 18t1.413.588T19 20t-.587 1.413T17 22M6.15 6l2.4 5h7l2.75-5zM5.2 4h14.75q.575 0 .875.513t.025 1.037l-3.55 6.4q-.275.5-.737.775T15.55 13H8.1L7 15h12v2H7q-1.125 0-1.7-.987t-.05-1.963L6.6 11.6L3 4H1V2h3.25z"/>
              </svg>
              สินค้าในตะกร้า ({{ cartItems.length }})
            </h2>

            <!-- Products -->
            <div v-if="cartItems.length > 0" class="space-y-3">
              <div
                v-for="(item, index) in cartItems"
                :key="index"
                class="bg-gray-700/30 rounded-lg p-4 flex items-center gap-4 hover:bg-gray-700/50 transition border border-gray-600"
              >
                <div class="w-20 h-20 bg-gray-600 rounded-lg overflow-hidden flex-shrink-0">
                  <img
                    :src="getImageUrl(item.image_url)"
                    :alt="item.name"
                    class="w-full h-full object-cover"
                    @error="onImgError($event)"
                  />
                </div>
                <div class="flex-1">
                  <h3 class="font-semibold text-lg mb-1">{{ item.name }}</h3>
                  <div class="flex items-center gap-4 text-sm text-gray-400">
                    <span class="flex items-center gap-1">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.77-.45-2.34-.94-2.34-1.67 0-.84.79-1.43 2.1-1.43 1.38 0 1.9.66 1.94 1.64h1.71c-.05-1.34-.87-2.57-2.49-2.97V5H10.9v1.69c-1.51.32-2.72 1.3-2.72 2.81 0 1.79 1.49 2.69 3.66 3.21 1.95.46 2.34 1.15 2.34 1.87 0 .53-.39 1.39-2.1 1.39-1.6 0-2.23-.72-2.32-1.64H8.04c.1 1.7 1.36 2.66 2.86 2.97V19h2.34v-1.67c1.52-.29 2.72-1.16 2.73-2.77-.01-2.2-1.9-2.96-3.66-3.42z"/>
                      </svg>
                      ฿{{ item.price.toFixed(2) }}
                    </span>
                    <span>×</span>
                    <span class="bg-pink-500/20 text-pink-300 px-2 py-0.5 rounded">จำนวน: {{ item.quantity }}</span>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-pink-400 font-bold text-lg">฿{{ (item.price * item.quantity).toFixed(2) }}</p>
                </div>
              </div>
            </div>

            <!-- Empty Cart -->
            <div v-else class="text-center py-12">
              <div class="text-6xl mb-4">🛒</div>
              <p class="text-gray-400 text-lg">ตะกร้าสินค้าของคุณว่างเปล่า</p>
              <NuxtLink to="/dashboard" class="inline-block mt-4 bg-pink-600 hover:bg-pink-700 text-white px-6 py-2 rounded-lg transition">
                เลือกซื้อสินค้า
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Right Column: Summary & Payment -->
        <div class="space-y-4">
          <!-- Order Summary -->
          <div class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm rounded-xl p-6 border border-gray-700 sticky top-6 pb-1">
            <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-green-400" viewBox="0 0 24 24">
                <path fill="currentColor" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-7-2h2v-4h4v-2h-4V7h-2v4H7v2h4z"/>
              </svg>
              สรุปคำสั่งซื้อ
            </h2>

            <!-- Account Info -->
            <div class="bg-gray-700/30 rounded-lg p-4 mb-4 border border-gray-600">
              <p class="text-gray-400 text-sm mb-2">บัญชีผู้ใช้</p>
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-pink-400" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M12 12q-1.65 0-2.825-1.175T8 8t1.175-2.825T12 4t2.825 1.175T16 8t-1.175 2.825T12 12m-8 8v-2.8q0-.85.438-1.562T5.6 14.55q1.55-.775 3.15-1.162T12 13t3.25.388t3.15 1.162q.725.375 1.163 1.088T20 17.2V20z"/>
                </svg>
                <p class="text-white font-semibold">{{ username }}</p>
              </div>
            </div>

            <!-- Payment Method -->
            <div class="bg-gray-700/30 rounded-lg p-4 mb-4 border border-gray-600">
              <div class="flex items-center justify-between mb-2">
                <p class="text-gray-400 text-sm">วิธีชำระเงิน</p>
                <NuxtLink
                  to="/paymentMethod"
                  class="text-blue-400 text-sm hover:text-blue-300 flex items-center gap-1 transition"
                >
                  <span>เปลี่ยน</span>
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24">
                    <path fill="currentColor" d="m14.475 12l-7.35-7.35q-.375-.375-.363-.888t.388-.887t.888-.375t.887.375l7.675 7.7q.3.3.45.675t.15.75t-.15.75t-.45.675l-7.7 7.7q-.375.375-.875.363T7.15 21.1t-.375-.888t.375-.887z"/>
                  </svg>
                </NuxtLink>
              </div>
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-green-400" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2m0 14H4v-6h16zm0-10H4V6h16z"/>
                </svg>
                <p class="text-white font-semibold">{{ paymentMethod }}</p>
              </div>
            </div>

            <!-- Price Breakdown -->
            <div class="space-y-2 mb-4 pb-4 border-b border-gray-700">
              <div class="flex justify-between text-gray-400">
                <span>ยอดรวม ({{ cartItems.length }} รายการ)</span>
                <span>฿{{ totalPrice.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-gray-400">
                <span>ค่าจัดส่ง</span>
                <span class="text-green-400">ฟรี</span>
              </div>
            </div>

            <!-- Total -->
            <div class="flex justify-between items-center mb-6 text-xl">
              <span class="font-bold">ยอดรวมทั้งหมด</span>
              <span class="font-bold text-green-400">฿{{ totalPrice.toFixed(2) }}</span>
            </div>

            <!-- Terms & Buy Button -->
            <div class="space-y-4">
              <label class="flex items-start gap-3 cursor-pointer group">
                <input 
                  type="checkbox" 
                  v-model="termsAccepted" 
                  class="mt-1 w-5 h-5 rounded border-gray-600 bg-gray-700 text-pink-500 focus:ring-pink-500 focus:ring-offset-gray-800 cursor-pointer"
                />
                <span class="text-sm text-gray-400 group-hover:text-gray-300 transition">
                  ฉันยอมรับ
                  <a href="#" class="underline text-pink-400 hover:text-pink-300">ข้อตกลงและเงื่อนไข</a>
                  ของ P2UKAISER
                </span>
              </label>

              <button
                :disabled="!termsAccepted || cartItems.length === 0"
                @click="buyNow"
                class="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold py-4 rounded-xl transition-all duration-300 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed shadow-lg disabled:shadow-none flex items-center justify-center gap-2"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19L21 7l-1.41-1.41z"/>
                </svg>
                <span>ยืนยันการสั่งซื้อ</span>
              </button>

              <NuxtLink 
                to="/dashboard" 
                class="block w-full text-center bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 rounded-xl transition"
              >
                ← กลับไปช้อปต่อ
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const baseURL = "http://localhost:5000";
const defaultImage = "/no-image.png";

const cartItems = ref([]);
const username = ref("");
const paymentMethod = ref("MasterCard");
const termsAccepted = ref(false);

// ✅ แก้ไขฟังก์ชันสร้าง URL รูปให้รองรับทุกกรณี
const getImageUrl = (path) => {
  if (!path) return defaultImage;
  if (path.startsWith("http")) return path;
  
  // ตรวจสอบว่ามี / ข้างหน้าหรือไม่
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return `${baseURL}${cleanPath}`;
};

const onImgError = (event) => {
  console.log("Image load error:", event.target.src);
  event.target.src = defaultImage;
  event.target.onerror = null;
};

// ✅ โหลดข้อมูลจาก localStorage + query
onMounted(() => {
  // โหลดตะกร้า
  const storedCart = localStorage.getItem("cart");
  if (storedCart) {
    try {
      cartItems.value = JSON.parse(storedCart);
      console.log("Cart items loaded:", cartItems.value);
    } catch {
      cartItems.value = [];
    }
  }

  // โหลดชื่อผู้ใช้
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    try {
      username.value = JSON.parse(storedUser)?.username || "ผู้ใช้";
    } catch {
      username.value = "ผู้ใช้";
    }
  }

  // โหลดค่าชำระเงินจาก query หรือ localStorage
  if (route.query.method) {
    paymentMethod.value = route.query.method;
    localStorage.setItem("paymentMethod", route.query.method);
  } else {
    const storedMethod = localStorage.getItem("paymentMethod");
    if (storedMethod) paymentMethod.value = storedMethod;
  }
});

// รวมราคา
const totalPrice = computed(() =>
  cartItems.value.reduce(
    (sum, item) => sum + (Number(item.price) || 0) * (Number(item.quantity) || 0),
    0
  )
);

// ซื้อ
const buyNow = () => {
  if (!termsAccepted.value) return;
  alert("✅ ชำระเงินสำเร็จ! ขอบคุณที่ใช้บริการ");
  localStorage.removeItem("cart");
  router.push("/payment_success");
};
</script>