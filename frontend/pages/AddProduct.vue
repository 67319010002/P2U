<template>
  <div class="flex justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black p-6">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-lg text-white">
      <h1 class="text-2xl font-bold mb-6">🛍️ เพิ่มสินค้าใหม่</h1>

      <form @submit.prevent="submitProduct" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">ชื่อสินค้า</label>
          <input v-model="name" type="text" required class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/50 transition-all" placeholder="กรอกชื่อสินค้า" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">ราคา (บาท)</label>
          <input v-model="price" type="number" required min="0" class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/50 transition-all" placeholder="กรอกราคา" />
        </div>

        <!-- Category Selection -->
        <div>
          <label class="block text-sm font-medium mb-2">หมวดหมู่สินค้า</label>
          <div class="grid grid-cols-3 gap-2">
            <button
              v-for="cat in categories"
              :key="cat.id"
              type="button"
              @click="selectedCategory = cat.id"
              class="p-3 rounded-xl border-2 transition-all duration-200 text-center"
              :class="selectedCategory === cat.id 
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
          <textarea v-model="description" rows="3" class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/50 transition-all" placeholder="อธิบายรายละเอียดสินค้า..."></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium mb-2">รูปภาพสินค้า</label>
          <div 
            class="relative border-2 border-dashed border-gray-600 rounded-xl p-6 text-center hover:border-primary-500 transition-colors cursor-pointer"
            @click="$refs.fileInput.click()"
          >
            <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" class="hidden" />
            <div v-if="imagePreview" class="mb-3">
              <img :src="imagePreview" class="max-h-40 mx-auto rounded-lg object-contain" />
            </div>
            <div v-else class="text-gray-400">
              <span class="text-4xl block mb-2">📷</span>
              <p>คลิกเพื่อเลือกรูปภาพ</p>
              <p class="text-xs text-gray-500 mt-1">รองรับ PNG, JPG, GIF</p>
            </div>
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="isSubmitting"
          class="w-full py-3 bg-gradient-to-r from-primary-500 to-pink-500 hover:from-primary-600 hover:to-pink-600 rounded-xl font-semibold transition-all duration-200 shadow-lg shadow-primary-500/30 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isSubmitting">กำลังบันทึก...</span>
          <span v-else>💾 บันทึกสินค้า</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const baseURL = "http://localhost:5000";

const name = ref("");
const price = ref("");
const description = ref("");
const imageFile = ref(null);
const imagePreview = ref(null);
const selectedCategory = ref("electronics");
const isSubmitting = ref(false);

// Categories list (สามารถดึงจาก API ได้เช่นกัน)
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

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    // Create preview URL
    imagePreview.value = URL.createObjectURL(file);
  }
};

const fetchCategories = async () => {
  try {
    const res = await axios.get(`${baseURL}/api/categories`);
    // Filter out 'all' category since seller should pick a specific one
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

  const formData = new FormData();
  formData.append("name", name.value);
  formData.append("price", price.value);
  formData.append("description", description.value);
  formData.append("category", selectedCategory.value);
  if (imageFile.value) {
    formData.append("image", imageFile.value);
  }

  try {
    await axios.post(`${baseURL}/api/seller/products`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "multipart/form-data"
      }
    });
    alert("เพิ่มสินค้าสำเร็จ!");
    router.push("/seller-dashboard");
  } catch (err) {
    console.error("Failed to add product:", err);
    alert("ไม่สามารถเพิ่มสินค้าได้ กรุณาลองใหม่อีกครั้ง");
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(() => {
  fetchCategories();
});
</script>
