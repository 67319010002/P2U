<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-0 left-0 w-[600px] h-[600px] bg-purple-900/20 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[800px] h-[600px] bg-pink-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <div class="ml-20 relative z-10 p-6 md:p-10 pb-24">
      <div class="max-w-3xl mx-auto animate-in-fade">
        
        <div class="flex items-center gap-4 mb-10">
          <NuxtLink to="/auction" class="w-10 h-10 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-gray-400 hover:text-white transition-colors">
            ←
          </NuxtLink>
          <div>
            <h1 class="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-pink-200 to-purple-200 tracking-tight flex items-center gap-3">
              <span>➕</span> สร้างการประมูล
            </h1>
            <p class="text-gray-400 mt-1">ลงขายสินค้าของคุณในลานประมูล</p>
          </div>
        </div>

        <div class="bg-[#121215]/60 backdrop-blur-md rounded-3xl border border-white/10 p-8 space-y-6">
          
          <!-- Title -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-bold text-gray-300">ชื่อสินค้า</label>
              <button @click="openProductModal" class="text-xs text-pink-400 hover:text-pink-300 font-bold bg-pink-500/10 px-3 py-1 rounded-full border border-pink-500/20 transition-colors">
                📦 เลือกจากสินค้าของฉัน
              </button>
            </div>
            <input 
              v-model="form.title" 
              type="text" 
              class="w-full bg-[#09090b] border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-pink-500 transition-colors placeholder-gray-600"
              placeholder="เช่น iPhone 15 Pro Max Limited Edition"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-bold text-gray-300 mb-2">รายละเอียด</label>
            <textarea 
              v-model="form.description" 
              rows="3"
              class="w-full bg-[#09090b] border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-pink-500 transition-colors placeholder-gray-600 resize-none"
              placeholder="อธิบายสินค้าของคุณ..."
            ></textarea>
          </div>

          <!-- Image Upload -->
          <div>
            <label class="block text-sm font-bold text-gray-300 mb-2">รูปภาพสินค้า</label>
            <div 
              class="relative w-full h-48 bg-[#09090b] border-2 border-dashed border-white/10 rounded-xl flex flex-col items-center justify-center cursor-pointer hover:border-pink-500/50 hover:bg-white/[0.02] transition-all group"
              @click="triggerFileInput"
            >
              <input 
                ref="fileInput"
                type="file" 
                accept="image/*"
                class="hidden"
                @change="handleFileChange"
              />
              
              <div v-if="previewUrl" class="absolute inset-0 w-full h-full rounded-xl overflow-hidden">
                 <img :src="previewUrl" class="w-full h-full object-cover" />
                 <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <span class="text-white font-bold">📷 เปลี่ยนรูปภาพ</span>
                 </div>
              </div>
              
              <div v-else class="text-center text-gray-500 group-hover:text-gray-300 transition-colors">
                 <span class="text-3xl mb-2 block">📷</span>
                 <p class="text-sm">คลิกเพื่ออัปโหลดรูปภาพ</p>
                 <p class="text-xs text-gray-600 mt-1">PNG, JPG, GIF (Max 5MB)</p>
              </div>
            </div>
          </div>

          <!-- Category -->
          <div>
            <label class="block text-sm font-bold text-gray-300 mb-2">หมวดหมู่</label>
            <select 
              v-model="form.category"
              class="w-full bg-[#09090b] border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-pink-500 transition-colors"
            >
              <option value="electronics">📱 อิเล็กทรอนิกส์</option>
              <option value="fashion">👗 แฟชั่น</option>
              <option value="gaming">🎮 เกมมิ่ง</option>
              <option value="beauty">💄 ความงาม</option>
              <option value="all">🔨 อื่นๆ</option>
            </select>
          </div>

          <!-- Starting Price -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-bold text-gray-300 mb-2">ราคาเริ่มต้น (Token)</label>
              <div class="relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">🪙</span>
                <input 
                  v-model.number="form.starting_price" 
                  type="number" 
                  min="100"
                  class="w-full bg-[#09090b] border border-white/10 rounded-xl py-3 pl-10 pr-4 text-white focus:outline-none focus:border-pink-500 transition-colors"
                  placeholder="0"
                />
              </div>
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-300 mb-2">ระยะเวลา (ชั่วโมง)</label>
              <select 
                v-model.number="form.duration_hours"
                class="w-full bg-[#09090b] border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-pink-500 transition-colors"
                @change="onDurationChange"
              >
                <option :value="0.016">1 นาที (ทดสอบ)</option>
                <option :value="1">1 ชั่วโมง</option>
                <option :value="6">6 ชั่วโมง</option>
                <option :value="12">12 ชั่วโมง</option>
                <option :value="24">24 ชั่วโมง (1 วัน)</option>
                <option :value="48">48 ชั่วโมง (2 วัน)</option>
                <option :value="72">72 ชั่วโมง (3 วัน)</option>
              </select>
            </div>
          </div>

          <!-- Submit -->
          <button 
            @click="createAuction"
            :disabled="isLoading || !form.title || form.starting_price < 100"
            class="w-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-pink-600/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
          >
            <span v-if="isLoading">กำลังสร้าง...</span>
            <span v-else>🔨 เริ่มการประมูล</span>
          </button>

          <p v-if="errorMsg" class="text-red-400 text-sm text-center">{{ errorMsg }}</p>
          
        </div>
      </div>
    </div>

    <!-- Product Selection Modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showProductModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="showProductModal = false"></div>
          
          <div class="relative bg-[#121215] w-full max-w-2xl rounded-2xl border border-white/10 shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">
            <div class="p-6 border-b border-white/5 flex justify-between items-center">
              <h3 class="text-xl font-bold text-white">เลือกสินค้าที่จะลงประมูล</h3>
              <button @click="showProductModal = false" class="text-gray-400 hover:text-white">✕</button>
            </div>
            
            <div class="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
              <div v-if="loadingProducts" class="text-center py-10 text-gray-500">
                กำลังโหลดสินค้า...
              </div>
              
              <div v-else-if="myProducts.length === 0" class="text-center py-10">
                <p class="text-gray-400 mb-4">คุณยังไม่มีสินค้าในร้าน</p>
                <NuxtLink to="/seller-dashboard" class="text-pink-400 hover:text-pink-300 underline">
                  ไปเพิ่มสินค้าก่อน
                </NuxtLink>
              </div>
              
              <div 
                v-else
                v-for="product in myProducts" 
                :key="product.id"
                @click="selectProduct(product)"
                class="flex items-center gap-4 p-4 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/[0.05] hover:border-pink-500/30 cursor-pointer transition-all group"
              >
                <img :src="getImageUrl(product.image_url)" class="w-16 h-16 object-cover rounded-lg bg-black/20" />
                <div class="flex-1 min-w-0">
                  <h4 class="font-bold text-gray-200 group-hover:text-pink-300 truncate">{{ product.name }}</h4>
                  <p class="text-sm text-gray-500 truncate">{{ product.description }}</p>
                  <div class="flex gap-3 mt-1 text-xs">
                    <span class="text-gray-400">ราคาขาย: ฿{{ product.price }}</span>
                    <span class="text-gray-400">หมวดหมู่: {{ product.category }}</span>
                  </div>
                </div>
                <div class="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center text-gray-500 group-hover:bg-pink-500 group-hover:text-white group-hover:border-transparent transition-all">
                  ➔
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const baseUrl = 'http://localhost:5000';

const form = ref({
  title: '',
  description: '',
  image_url: '',
  category: 'electronics',
  starting_price: 1000,
  duration_hours: 24,
  duration_minutes: 0,
  min_bid_increment: 100
});

const fileInput = ref(null);
const selectedFile = ref(null);
const previewUrl = ref('');

const showProductModal = ref(false);
const myProducts = ref([]);
const loadingProducts = ref(false);

const isLoading = ref(false);
const errorMsg = ref('');

function triggerFileInput() {
  fileInput.value.click();
}

function handleFileChange(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (file.size > 5 * 1024 * 1024) {
    alert('ขนาดไฟล์ต้องไม่เกิน 5MB');
    return;
  }

  selectedFile.value = file;
  previewUrl.value = URL.createObjectURL(file);
  form.value.image_url = ''; // Clear URL input logic if we had one
}

function onDurationChange() {
  // If user selects 1 minute option (value 0.016), set minutes
  if (form.value.duration_hours === 0.016) {
    form.value.duration_minutes = 1;
  } else {
    form.value.duration_minutes = 0;
  }
}

function getImageUrl(url) {
  if (!url) return '/default-item.jpg';
  return url.startsWith('http') ? url : baseUrl + url;
}

async function createAuction() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    return;
  }
  
  if (!form.value.title || form.value.starting_price < 100) {
    errorMsg.value = 'กรุณากรอกข้อมูลให้ครบถ้วน';
    return;
  }
  
  isLoading.value = true;
  errorMsg.value = '';
  
  try {
    const formData = new FormData();
    formData.append('title', form.value.title);
    formData.append('description', form.value.description);
    formData.append('category', form.value.category);
    formData.append('starting_price', form.value.starting_price);
    formData.append('min_bid_increment', form.value.min_bid_increment);
    formData.append('duration_hours', form.value.duration_hours);
    formData.append('duration_minutes', form.value.duration_minutes);
    
    // Check priority: New file > Existing image_url (from product selection)
    if (selectedFile.value) {
       formData.append('image', selectedFile.value);
    } else if (form.value.image_url) {
       formData.append('image_url', form.value.image_url);
    }

    const res = await axios.post(`${baseUrl}/api/auctions`, formData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    
    alert('🎉 สร้างการประมูลสำเร็จ!');
    router.push('/auction');
  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'สร้างการประมูลไม่สำเร็จ';
  } finally {
    isLoading.value = false;
  }
}

async function openProductModal() {
  showProductModal.value = true;
  if (myProducts.value.length === 0) {
    await fetchMyProducts();
  }
}

async function fetchMyProducts() {
  const token = localStorage.getItem('token');
  if (!token) return;
  
  loadingProducts.value = true;
  try {
    const res = await axios.get(`${baseUrl}/api/seller/products`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    myProducts.value = res.data || [];
  } catch (err) {
    console.error('Failed to fetch products:', err);
  } finally {
    loadingProducts.value = false;
  }
}

function selectProduct(product) {
  form.value.title = product.name;
  form.value.description = product.description;
  form.value.image_url = product.image_url;
  previewUrl.value = getImageUrl(product.image_url); // Show preview from product
  selectedFile.value = null; // Clear any manual upload
  
  form.value.category = product.category;
  form.value.starting_price = Math.floor(product.price); 
  
  showProductModal.value = false;
}

onMounted(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  if (!user.is_seller) {
    alert('เฉพาะผู้ขายเท่านั้นที่สามารถสร้างการประมูลได้');
    router.push('/auction');
  }
});
</script>

<style scoped>
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
