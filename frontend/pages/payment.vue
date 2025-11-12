<template>
  <div class="min-h-screen bg-gray-900 text-white p-6 flex flex-col items-center">
    <!-- Header -->
    <h1 class="text-3xl font-bold mb-6">Payment Checkout</h1>

    <!-- Products List -->
    <div
      v-for="(item, index) in cartItems"
      :key="index"
      class="w-full max-w-3xl bg-gray-800 rounded-lg p-6 mb-4"
    >
      <div class="flex items-center gap-4 mb-4">
        <img
          :src="getImageUrl(item.image)"
          alt="product"
          class="w-20 h-20 object-cover rounded"
          @error="onImgError($event)"
        />
        <div>
          <h2 class="font-semibold text-lg">{{ item.name }}</h2>
          <div class="flex gap-2 text-gray-400 text-sm mt-1">
            <span>Price: ฿{{ item.price.toFixed(2) }}</span>
          </div>
          <p class="text-gray-400 text-xs mt-1">Qty: {{ item.quantity }}</p>
        </div>
      </div>
      <div class="text-gray-300 text-sm">
        <p>Subtotal: ฿{{ (item.price * item.quantity).toFixed(2) }}</p>
      </div>
    </div>

    <!-- Total Price -->
    <div
      class="w-full max-w-3xl bg-gray-800 rounded-lg p-6 mb-6 flex justify-between items-center"
    >
      <p class="font-semibold text-lg">Total:</p>
      <p class="font-bold text-green-400 text-lg">฿{{ totalPrice.toFixed(2) }}</p>
    </div>

    <!-- Payment Info -->
    <div class="w-full max-w-3xl bg-gray-800 rounded-lg p-6 mb-6">
      <p class="text-gray-400">Payment Method:</p>
      <div class="flex items-center justify-between mb-2">
        <p class="text-green-400 font-semibold">{{ paymentMethod }}</p>
        <NuxtLink
          to="/paymentMethod"
          class="text-blue-400 text-sm hover:underline hover:text-white"
        >
          (Change)
        </NuxtLink>
      </div>

      <p class="text-gray-400 mt-4 mb-2">Account:</p>
      <p class="text-white font-semibold">{{ username }}</p>

      <div class="flex items-center mt-4 mb-4">
        <input type="checkbox" id="terms" class="mr-2" v-model="termsAccepted" />
        <label for="terms" class="text-gray-400 text-sm">
          I accept the terms of
          <a href="#" class="underline text-blue-400">P2UKAISER</a>
        </label>
      </div>

      <button
        :disabled="!termsAccepted || cartItems.length === 0"
        @click="buyNow"
        class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Buy
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute(); // ✅ ใช้เพื่ออ่าน query

const baseURL = "http://localhost:5000";
const defaultImage = "/no-image.png";

const cartItems = ref([]);
const username = ref("");
const paymentMethod = ref("MasterCard");
const termsAccepted = ref(false);

// ✅ ฟังก์ชันสร้าง URL รูป
const getImageUrl = (path) => {
  if (!path) return defaultImage;
  if (path.startsWith("http")) return path;
  return `${baseURL}/${path.replace(/^\/+/, "")}`;
};

const onImgError = (event) => {
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
    } catch {
      cartItems.value = [];
    }
  }

  // โหลดชื่อผู้ใช้
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    try {
      username.value = JSON.parse(storedUser)?.username || "";
    } catch {
      username.value = "";
    }
  }

  // ✅ โหลดค่าชำระเงินจาก query หรือ localStorage
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
  alert("Payment successful!");
  localStorage.removeItem("cart");
  router.push("/payment_success");
};
</script>
