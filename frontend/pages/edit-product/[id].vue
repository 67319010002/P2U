<template>
  <div class="flex justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black p-6">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-lg text-white">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold">✏️ แก้ไขสินค้า</h1>
        <NuxtLink to="/seller-dashboard" class="text-dark-400 hover:text-white transition-colors">
          ← กลับ
        </NuxtLink>
      </div>

      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin text-4xl mb-4">⏳</div>
        <p class="text-dark-400">กำลังโหลดข้อมูลสินค้า...</p>
      </div>

      <form v-else @submit.prevent="submitProduct" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">ชื่อสินค้า</label>
          <input v-model="product.name" type="text" required class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/50 transition-all" placeholder="กรอกชื่อสินค้า" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">ราคา (บาท)</label>
          <input v-model="product.price" type="number" required min="0" class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/50 transition-all" placeholder="กรอกราคา" />
        </div>

        <!-- Category Selection -->
        <div>
          <label class="block text-sm font-medium mb-2">หมวดหมู่สินค้า</label>
          <div class="grid grid-cols-3 gap-2">
            <button
              v-for="cat in categories"
              :key="cat.id"
              type="button"
              @click="product.category = cat.id"
              class="p-3 rounded-xl border-2 transition-all duration-200 text-center"
              :class="product.category === cat.id 
                ? 'border-primary-500 bg-primary-500/20 text-white shadow-lg shadow-primary-500/30' 
                : 'border-gray-600 bg-gray-700/50 text-gray-300 hover:border-gray-500'"
            >
              <span class="text-xl block mb-1">{{ cat.icon }}</span>
              <span class="text-xs">{{ cat.name }}</span>
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">รายละเอียดสินค้า</label>
          <textarea v-model="product.description" rows="3" class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/50 transition-all" placeholder="อธิบายรายละเอียดสินค้า..."></textarea>
        </div>

        <!-- Current Image -->
        <div v-if="product.image_url">
          <label class="block text-sm font-medium mb-2">รูปภาพปัจจุบัน</label>
          <div class="relative inline-block">
            <img :src="getImageUrl(product.image_url)" class="rounded-xl max-h-40 object-contain" />
            <span class="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">ปัจจุบัน</span>
          </div>
        </div>

        <!-- Upload New Image -->
        <div>
          <label class="block text-sm font-medium mb-2">{{ product.image_url ? 'เปลี่ยนรูปภาพ (ถ้าต้องการ)' : 'รูปภาพสินค้า' }}</label>
          <div 
            class="relative border-2 border-dashed border-gray-600 rounded-xl p-6 text-center hover:border-primary-500 transition-colors cursor-pointer"
            @click="$refs.fileInput.click()"
          >
            <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" class="hidden" />
            <div v-if="imagePreview" class="mb-3">
              <img :src="imagePreview" class="max-h-40 mx-auto rounded-lg object-contain" />
              <p class="text-xs text-green-400 mt-2">✓ รูปใหม่พร้อมอัพโหลด</p>
            </div>
            <div v-else class="text-gray-400">
              <span class="text-4xl block mb-2">📷</span>
              <p>คลิกเพื่อเลือกรูปภาพใหม่</p>
              <p class="text-xs text-gray-500 mt-1">รองรับ PNG, JPG, GIF</p>
            </div>
          </div>
        </div>

        <div class="flex gap-3 pt-4">
          <button 
            type="submit" 
            :disabled="isSubmitting"
            class="flex-1 py-3 bg-gradient-to-r from-primary-500 to-pink-500 hover:from-primary-600 hover:to-pink-600 rounded-xl font-semibold transition-all duration-200 shadow-lg shadow-primary-500/30 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isSubmitting">กำลังบันทึก...</span>
            <span v-else>💾 บันทึกการเปลี่ยนแปลง</span>
          </button>
          
          <button 
            type="button"
            @click="confirmDelete"
            :disabled="isDeleting"
            class="px-6 py-3 bg-red-500/20 border border-red-500/50 hover:bg-red-500 text-red-400 hover:text-white rounded-xl font-semibold transition-all duration-200"
          >
            🗑️
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const baseURL = "http://localhost:5000";

const productId = route.params.id;
const product = ref({
  name: "",
  price: "",
  description: "",
  category: "electronics",
  image_url: ""
});
const imageFile = ref(null);
const imagePreview = ref(null);
const isSubmitting = ref(false);
const isDeleting = ref(false);
const loading = ref(true);

const categories = ref([
  { id: "electronics", name: "อิเล็กทรอนิกส์", icon: "📱" },
  { id: "fashion", name: "แฟชั่น", icon: "👗" },
  { id: "gaming", name: "เกมมิ่ง", icon: "🎮" },
  { id: "beauty", name: "ความงาม", icon: "💄" },
  { id: "home", name: "บ้าน", icon: "🏠" },
  { id: "sports", name: "กีฬา", icon: "⚽" },
  { id: "food", name: "อาหาร", icon: "🍔" },
  { id: "books", name: "หนังสือ", icon: "📚" },
  { id: "toys", name: "ของเล่น", icon: "🧸" },
  { id: "pets", name: "สัตว์เลี้ยง", icon: "🐶" },
  { id: "automotive", name: "ยานยนต์", icon: "🚗" },
]);

const getImageUrl = (url) => {
  if (!url) return '/placeholder.png';
  if (url.startsWith('http')) return url;
  return `${baseURL}${url.startsWith('/') ? '' : '/'}${url}`;
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
  }
};

const fetchProduct = async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }

  try {
    const res = await axios.get(`${baseURL}/api/seller/products/${productId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    product.value = res.data;
  } catch (err) {
    console.error("Failed to fetch product:", err);
    alert("ไม่พบสินค้าหรือไม่มีสิทธิ์เข้าถึง");
    router.push("/seller-dashboard");
  } finally {
    loading.value = false;
  }
};

const fetchCategories = async () => {
  try {
    const res = await axios.get(`${baseURL}/api/categories`);
    categories.value = res.data.filter(cat => cat.id !== 'all');
  } catch (err) {
    console.log("Using default categories");
  }
};

const submitProduct = async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }

  isSubmitting.value = true;

  try {
    // Update product info
    await axios.put(`${baseURL}/api/seller/products/${productId}`, {
      name: product.value.name,
      price: product.value.price,
      description: product.value.description,
      category: product.value.category
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Upload new image if selected
    if (imageFile.value) {
      const formData = new FormData();
      formData.append("image", imageFile.value);
      
      await axios.put(`${baseURL}/api/seller/products/${productId}/image`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data"
        }
      });
    }

    alert("อัพเดตสินค้าสำเร็จ! ✨");
    router.push("/seller-dashboard");
  } catch (err) {
    console.error("Failed to update product:", err);
    alert("ไม่สามารถอัพเดตสินค้าได้ กรุณาลองใหม่อีกครั้ง");
  } finally {
    isSubmitting.value = false;
  }
};

const confirmDelete = async () => {
  if (!confirm("❗ คุณต้องการลบสินค้านี้ใช่หรือไม่? การกระทำนี้ไม่สามารถยกเลิกได้")) {
    return;
  }

  const token = localStorage.getItem("token");
  isDeleting.value = true;

  try {
    await axios.delete(`${baseURL}/api/seller/products/${productId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert("ลบสินค้าสำเร็จ!");
    router.push("/seller-dashboard");
  } catch (err) {
    console.error("Failed to delete product:", err);
    alert("ไม่สามารถลบสินค้าได้");
  } finally {
    isDeleting.value = false;
  }
};

onMounted(() => {
  fetchProduct();
  fetchCategories();
});
</script>
