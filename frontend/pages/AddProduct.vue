<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30 overflow-hidden relative">
    
    <!-- Background Effects -->
    <div class="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div class=" absolute top-[20%] right-[20%] w-[500px] h-[500px] bg-pink-600/20 rounded-full blur-[120px] mix-blend-screen animate-pulse-slow"></div>
        <div class="absolute bottom-[20%] left-[10%] w-[400px] h-[400px] bg-purple-600/20 rounded-full blur-[100px] mix-blend-screen"></div>
        <div class="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-[0.03]"></div>
    </div>

    <sidebar />

    <div class="ml-20 flex justify-center items-center min-h-screen p-6 relative z-10 py-12">
      
      <div class="w-full max-w-2xl transform transition-all duration-500 ease-out">
        
        <div class="mb-8 flex items-end justify-between">
          <div>
            <h1 class="text-4xl font-bold text-white flex items-center gap-3">
              <span class="bg-gradient-to-tr from-pink-500 to-purple-500 w-3 h-10 rounded-full shadow-[0_0_15px_rgba(236,72,153,0.5)]"></span>
              เพิ่มสินค้าใหม่
            </h1>
            <p class="text-gray-400 text-sm mt-2 ml-6 font-light">กรอกข้อมูลสินค้าของคุณให้ครบถ้วนเพื่อลงขาย</p>
          </div>
          <NuxtLink to="/seller-dashboard" class="group flex items-center gap-2 text-gray-400 hover:text-white transition-colors px-4 py-2 rounded-full hover:bg-white/5 border border-transparent hover:border-white/10">
            <span class="text-xs font-medium">ยกเลิก</span>
            <div class="bg-white/5 p-1 rounded-full group-hover:bg-white/10 transition-colors">
               <X class="w-4 h-4" />
            </div>
          </NuxtLink>
        </div>

        <div class="relative bg-[#121215]/80 backdrop-blur-2xl border border-white/10 p-8 rounded-[2rem] shadow-2xl overflow-hidden group/card hover:border-pink-500/20 transition-colors duration-500">
          
          <!-- Top Glow Line -->
          <div class="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-pink-500/50 to-transparent opacity-70"></div>

          <form @submit.prevent="submitProduct" class="space-y-8 relative z-10">
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Name Input -->
              <div class="space-y-2 col-span-2 md:col-span-1">
                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider ml-1 flex items-center gap-1.5">
                  <Tag class="w-3 h-3 text-pink-500" /> ชื่อสินค้า
                </label>
                <div class="relative group">
                  <input 
                    v-model="name" 
                    type="text" 
                    required 
                    class="w-full pl-4 pr-10 py-3.5 rounded-2xl bg-[#09090b]/50 border border-white/5 focus:border-pink-500/50 focus:bg-[#09090b] text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-pink-500/10 hover:border-white/10" 
                    placeholder="เช่น หูฟังไร้สาย Gen 2" 
                  />
                  <div class="absolute right-3 top-3.5 text-gray-600 group-focus-within:text-pink-500 transition-colors">
                    <PenLine class="w-5 h-5" />
                  </div>
                </div>
              </div>

              <!-- Price Input -->
              <div class="space-y-2 col-span-2 md:col-span-1">
                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider ml-1 flex items-center gap-1.5">
                  <Coins class="w-3 h-3 text-green-500" /> ราคา
                </label>
                <div class="relative group">
                  <span class="absolute left-4 top-3.5 text-gray-500 font-sans group-focus-within:text-green-400 transition-colors">฿</span>
                  <input 
                    v-model="price" 
                    type="number" 
                    required 
                    min="0" 
                    class="w-full pl-10 pr-4 py-3.5 rounded-2xl bg-[#09090b]/50 border border-white/5 focus:border-green-500/50 focus:bg-[#09090b] text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-green-500/10 font-mono text-lg hover:border-white/10" 
                    placeholder="0.00" 
                  />
                </div>
              </div>

              <!-- Stock Input -->
              <div class="space-y-2 col-span-2 md:col-span-1">
                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider ml-1 flex items-center gap-1.5">
                  <Package class="w-3 h-3 text-blue-500" /> จำนวนสต็อก
                </label>
                <div class="relative group">
                  <input 
                    v-model="stock" 
                    type="number" 
                    required 
                    min="1" 
                    class="w-full pl-4 pr-4 py-3.5 rounded-2xl bg-[#09090b]/50 border border-white/5 focus:border-blue-500/50 focus:bg-[#09090b] text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-blue-500/10 font-mono text-lg hover:border-white/10" 
                    placeholder="1" 
                  />
                </div>
              </div>
            </div>

            <!-- Categories (Multiple Selection) -->
            <div class="space-y-3">
              <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider ml-1 flex items-center gap-1.5">
                <LayoutGrid class="w-3 h-3 text-blue-500" /> หมวดหมู่ <span class="text-[9px] text-gray-500 normal-case">(เลือกได้มากกว่า 1)</span>
              </label>
              <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 pr-2">
                <button
                  v-for="cat in categories"
                  :key="cat.id"
                  type="button"
                  @click="toggleCategory(cat.id)"
                  class="group relative aspect-square rounded-2xl border transition-all duration-300 flex flex-col items-center justify-center gap-3 overflow-hidden"
                  :class="selectedCategories.includes(cat.id) 
                    ? 'border-pink-500/50 bg-gradient-to-br from-pink-500/20 to-purple-500/20 text-white shadow-[0_0_20px_rgba(236,72,153,0.15)] ring-1 ring-pink-500/30' 
                    : 'border-white/5 bg-[#09090b]/40 text-gray-500 hover:bg-white/5 hover:border-white/20 hover:text-gray-200'"
                >
                  <div class="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <component 
                    :is="getCategoryIcon(cat.id)" 
                    class="w-6 h-6 transition-all duration-300 transform group-hover:scale-110" 
                    :class="selectedCategories.includes(cat.id) ? 'text-pink-400 drop-shadow-[0_0_8px_rgba(244,114,182,0.5)]' : 'group-hover:text-white'"
                  />
                  <span class="text-[10px] font-medium tracking-wide">{{ cat.name }}</span>
                  
                  <!-- Active Indicator with Checkmark -->
                  <div v-if="selectedCategories.includes(cat.id)" class="absolute top-2 right-2 w-5 h-5 rounded-full bg-pink-500 shadow-[0_0_5px_rgba(236,72,153,0.8)] flex items-center justify-center">
                    <Check class="w-3 h-3 text-white" />
                  </div>
                </button>
              </div>
            </div>

            <!-- Description -->
            <div class="space-y-2">
              <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider ml-1 flex items-center gap-1.5">
                <FileText class="w-3 h-3 text-purple-500" /> รายละเอียด
              </label>
              <div class="relative">
                <textarea 
                  v-model="description" 
                  rows="4" 
                  class="w-full p-4 rounded-2xl bg-[#09090b]/50 border border-white/5 focus:border-purple-500/50 focus:bg-[#09090b] text-white placeholder-gray-600 transition-all outline-none resize-none focus:ring-4 focus:ring-purple-500/10 leading-relaxed hover:border-white/10" 
                  placeholder="บอกเล่าเรื่องราวสินค้าของคุณ..."
                ></textarea>
                <div class="absolute bottom-3 right-3 pointer-events-none">
                   <Sparkles class="w-4 h-4 text-purple-500/20" />
                </div>
              </div>
            </div>

            <!-- Image Upload -->
            <div class="space-y-2">
              <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider ml-1 flex items-center gap-1.5">
                <ImagePlus class="w-3 h-3 text-orange-500" /> รูปภาพ
              </label>
              <div 
                class="relative w-full border-2 border-dashed rounded-3xl p-1 transition-all group overflow-hidden cursor-pointer"
                :class="imagePreview ? 'border-pink-500/30 bg-pink-500/5' : 'border-white/10 hover:border-pink-500/30 hover:bg-white/5'"
                @click="$refs.fileInput.click()"
              >
                <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" class="hidden" />
                
                <div class="flex flex-col items-center justify-center py-10 relative z-10 transition-all duration-300 min-h-[200px]">
                  <div v-if="imagePreview" class="absolute inset-0 w-full h-full p-2">
                    <img :src="imagePreview" class="w-full h-full object-contain rounded-2xl shadow-lg" />
                    <div class="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 mx-2 my-2 rounded-2xl">
                       <Camera class="w-8 h-8 text-pink-400 mb-2" />
                       <p class="text-white font-medium text-sm">เปลี่ยนรูปภาพ</p>
                    </div>
                  </div>
                  
                  <div v-else class="text-center space-y-4">
                    <div class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto group-hover:scale-110 group-hover:bg-pink-500/10 group-hover:text-pink-500 transition-all duration-300 text-gray-500 border border-white/5 group-hover:border-pink-500/20">
                      <ImagePlus class="w-8 h-8" />
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-300 group-hover:text-white transition-colors">คลิกเพื่ออัปโหลดรูปภาพ</p>
                      <p class="text-[10px] text-gray-500 mt-1 font-mono">PNG, JPG, GIF (Max 5MB)</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <div class="pt-6 border-t border-white/5">
               <button 
                type="submit" 
                :disabled="isSubmitting"
                class="w-full py-4 rounded-2xl font-bold text-white transition-all duration-300 shadow-lg transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 relative overflow-hidden group btn-gradient"
              >
                <!-- Shimmer Effect -->
                <div class="absolute inset-0 -translate-x-full group-hover:translate-x-full bg-gradient-to-r from-transparent via-white/20 to-transparent transition-transform duration-1000 ease-in-out"></div>
                
                <span v-if="isSubmitting" class="animate-spin"><Loader2 class="w-6 h-6" /></span>
                <span v-else class="flex items-center gap-2 text-lg relative z-10">
                   <Sparkles class="w-5 h-5" /> บันทึกสินค้า
                </span>
              </button>
            </div>

          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { 
  X, Tag, Coins, LayoutGrid, FileText, ImagePlus, Camera, Sparkles, Loader2, PenLine,
  ShoppingBag, Smartphone, Shirt, Gamepad2, Home, Dumbbell, Utensils, BookOpen, Rocket, PawPrint, Car,
  Laptop, Package, Check
} from 'lucide-vue-next';

const router = useRouter();
const baseURL = "http://localhost:5000";

const name = ref("");
const price = ref("");
const stock = ref(1);
const description = ref("");
const imageFile = ref(null);
const imagePreview = ref(null);
const selectedCategories = ref(["electronics"]); // Multiple categories
const isSubmitting = ref(false);

const categories = ref([
  { id: 'electronics', name: 'อิเล็กทรอนิกส์' },
  { id: 'fashion', name: 'แฟชั่น' },
  { id: 'gaming', name: 'เกมมิ่ง' },
  { id: 'beauty', name: 'ความงาม' },
  { id: 'home', name: 'บ้าน & สวน' },
  { id: 'sports', name: 'กีฬา' },
  { id: 'food', name: 'อาหาร' },
  { id: 'books', name: 'หนังสือ' },
  { id: 'toys', name: 'ของเล่น' },
  { id: 'pets', name: 'สัตว์เลี้ยง' },
  { id: 'automotive', name: 'ยานยนต์' },
]);

// Icon Mapping (Consistent with ProductCategories.vue)
const iconMap = {
  all: ShoppingBag,
  electronics: Smartphone,
  fashion: Shirt,
  gaming: Gamepad2,
  beauty: Sparkles,
  home: Home,
  sports: Dumbbell,
  food: Utensils,
  books: BookOpen,
  toys: Rocket,
  pets: PawPrint,
  automotive: Car
};

function getCategoryIcon(id) {
  return iconMap[id] || LayoutGrid; // Default icon
}

function toggleCategory(categoryId) {
  const index = selectedCategories.value.indexOf(categoryId);
  if (index > -1) {
    // Remove category if already selected
    selectedCategories.value.splice(index, 1);
  } else {
    // Add category if not selected
    selectedCategories.value.push(categoryId);
  }
}

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
  }
};

const fetchCategories = async () => {
  try {
    const res = await axios.get(`${baseURL}/api/categories`);
    if (res.data && res.data.length > 0) {
        categories.value = res.data.filter(cat => cat.id !== 'all').map(c => ({
          ...c,
          name: c.name || c.title
        }));
    }
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

  if (!name.value || !price.value) {
    alert("กรุณากรอกชื่อสินค้าและราคา");
    return;
  }

  if (selectedCategories.value.length === 0) {
    alert("กรุณาเลือกหมวดหมู่อย่างน้อย 1 หมวดหมู่");
    return;
  }

  isSubmitting.value = true;

  const formData = new FormData();
  formData.append("name", name.value);
  formData.append("price", price.value);
  formData.append("stock", stock.value);
  formData.append("description", description.value);
  formData.append("category", selectedCategories.value[0]); // First category for backward compatibility
  formData.append("categories", JSON.stringify(selectedCategories.value)); // Multiple categories
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
    router.push("/seller-dashboard");
  } catch (err) {
    console.error("Failed to add product:", err);
    alert(err.response?.data?.msg || "ไม่สามารถเพิ่มสินค้าได้ กรุณาลองใหม่อีกครั้ง");
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.btn-gradient {
  background: linear-gradient(135deg, #ec4899 0%, #a855f7 50%, #6366f1 100%);
}
.btn-gradient:hover {
  background: linear-gradient(135deg, #db2777 0%, #9333ea 50%, #4f46e5 100%);
  box-shadow: 0 0 25px rgba(236, 72, 153, 0.4);
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}
.animate-pulse-slow {
  animation: pulse-slow 8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>