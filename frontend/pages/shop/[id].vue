<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <main class="ml-20 p-6 md:p-10 min-h-screen">
      <div v-if="loading" class="flex flex-col items-center justify-center min-h-[60vh]">
        <Loader2 class="w-12 h-12 text-pink-500 animate-spin mb-4" />
        <p class="text-gray-400 animate-pulse">กำลังโหลดข้อมูลร้านค้า...</p>
      </div>

      <div v-else-if="error" class="flex flex-col items-center justify-center min-h-[60vh]">
        <AlertTriangle class="w-16 h-16 text-red-500 mb-4 opacity-50" />
        <h2 class="text-2xl font-bold text-white mb-2">ไม่พบร้านค้า</h2>
        <p class="text-gray-400 mb-6">{{ error }}</p>
        <button @click="$router.push('/dashboard')" class="px-6 py-2 bg-white/10 hover:bg-white/20 rounded-xl transition-colors">
          กลับสู่หน้าหลัก
        </button>
      </div>

      <div v-else class="max-w-7xl mx-auto animate-in-fade">
        
        <!-- Shop Header -->
        <div class="relative w-full rounded-[2rem] overflow-hidden bg-[#121215] border border-white/5 shadow-2xl mb-10 group">
          <!-- Cover -->
          <div class="h-48 md:h-64 bg-gradient-to-r from-pink-900/40 via-purple-900/40 to-indigo-900/40 relative overflow-hidden">
             <div class="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-10"></div>
             <div class="absolute inset-0 bg-gradient-to-t from-[#121215] to-transparent"></div>
          </div>

          <!-- Profile Info -->
          <div class="relative px-8 pb-8 -mt-20 flex flex-col md:flex-row items-end md:items-center gap-6">
            
            <!-- Avatar -->
            <div class="relative group/avatar">
              <div class="absolute -inset-1 bg-gradient-to-br from-pink-500 to-purple-500 rounded-full blur opacity-70 group-hover/avatar:opacity-100 transition-opacity"></div>
              <div class="relative w-32 h-32 md:w-40 md:h-40 rounded-full p-1 bg-[#121215]">
                <img 
                  :src="seller?.profile_image_url ? (seller.profile_image_url.startsWith('http') ? seller.profile_image_url : baseUrl + seller.profile_image_url) : '/guest-profile.png'" 
                  class="w-full h-full rounded-full object-cover border-4 border-[#121215]"
                />
              </div>
            </div>

            <!-- Text Info -->
            <div class="flex-1 text-center md:text-left">
              <div class="flex flex-col md:flex-row items-center gap-3 mb-2">
                <h1 class="text-3xl md:text-4xl font-extrabold text-white flex items-center gap-2">
                  {{ seller?.shop_name || seller?.username }}
                  <BadgeCheck class="w-6 h-6 text-blue-400" />
                </h1>
                <span v-if="seller?.is_verified" class="px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold uppercase tracking-wider">
                  Verified Seller
                </span>
              </div>
              <p class="text-gray-400 max-w-2xl text-sm md:text-base font-light">
                {{ seller?.description }}
              </p>
              
              <div class="flex items-center justify-center md:justify-start gap-6 mt-6">
                <div class="flex items-center gap-2 text-white">
                  <Package class="w-5 h-5 text-gray-500" />
                  <span class="font-bold">{{ products.length }}</span>
                  <span class="text-gray-500 text-sm">สินค้า</span>
                </div>
                 <div class="flex items-center gap-2 text-white">
                  <Users class="w-5 h-5 text-pink-500" />
                  <span class="font-bold">{{ followerCount }}</span>
                  <span class="text-gray-500 text-sm">ผู้ติดตาม</span>
                </div>
                 <div class="flex items-center gap-2 text-white">
                  <Star class="w-5 h-5 text-yellow-500" />
                  <span class="font-bold">4.9</span>
                  <span class="text-gray-500 text-sm">คะแนนร้านค้า</span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-3 mt-4 md:mt-0 pb-2">
              <button 
                @click="openChat"
                class="px-6 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-white font-medium transition-all flex items-center gap-2"
              >
                <div v-if="chatLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                <MessageCircle v-else class="w-4 h-4" /> 
                แชท
              </button>
              
              <button 
                @click="toggleFollow"
                class="px-6 py-2.5 rounded-xl text-white font-bold shadow-lg transition-all flex items-center gap-2"
                :class="isFollowing ? 'bg-white/10 hover:bg-white/20 border border-white/10' : 'bg-pink-600 hover:bg-pink-500 shadow-pink-900/20'"
              >
                <div v-if="followLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                <template v-else>
                  <Heart class="w-4 h-4" :class="{ 'fill-white text-white': isFollowing }" /> 
                  {{ isFollowing ? 'ติดตามแล้ว' : 'ติดตาม' }}
                </template>
              </button>
            </div>

          </div>
        </div>

        <!-- Product Grid -->
        <h2 class="text-2xl font-bold text-white mb-6 pl-2 flex items-center gap-2">
          <Store class="w-6 h-6 text-pink-500" /> สินค้าทั้งหมด
        </h2>

        <div v-if="products.length === 0" class="text-center py-20 bg-white/5 rounded-3xl border border-white/5">
           <PackageOpen class="w-16 h-16 text-gray-600 mx-auto mb-4" />
           <p class="text-gray-400">ยังไม่มีสินค้าในร้านนี้</p>
        </div>

        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div 
            v-for="product in products" 
            :key="product.id"
            class="group bg-[#121215] rounded-2xl border border-white/5 overflow-hidden hover:border-pink-500/30 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl cursor-pointer"
            @click="$router.push(`/dashboard?q=${product.name}`)" 
          >
            <!-- Note: Redirect back to dashboard search for view/buy interactions for now to reuse dashboard modal logic -->

            <div class="aspect-[4/5] relative bg-[#09090b] overflow-hidden">
              <img 
                :src="product.image_url ? (product.image_url.startsWith('http') ? product.image_url : baseUrl + product.image_url) : '/default-item.svg'" 
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
              />
              <div class="absolute top-2 right-2 bg-black/60 backdrop-blur rounded-lg px-2 py-1 text-xs font-bold text-white border border-white/10">
                {{ product.category }}
              </div>
            </div>
            
            <div class="p-4">
              <h3 class="text-white font-medium truncate mb-1 group-hover:text-pink-400 transition-colors">{{ product.name }}</h3>
              <div class="flex items-center justify-between">
                <span class="text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                  ฿{{ product.price.toLocaleString() }}
                </span>
                <button class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center text-gray-400 hover:bg-pink-500 hover:text-white transition-all">
                  <ShoppingCart class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { 
  BadgeCheck, Package, Star, Calendar, MessageCircle, Heart, Store,
  PackageOpen, ShoppingCart, Loader2, AlertTriangle, Users
} from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const seller = ref(null);
const products = ref([]);
const loading = ref(true);
const error = ref(null);
const baseUrl = 'http://localhost:5000';

const isFollowing = ref(false);
const followerCount = ref(0);
const followLoading = ref(false);
const chatLoading = ref(false);

const fetchShopData = async () => {
  const sellerId = route.params.id;
  if (!sellerId) {
    error.value = 'ไม่ระบุรหัสร้านค้า';
    loading.value = false;
    return;
  }

  try {
    loading.value = true;
    const res = await axios.get(`${baseUrl}/api/public/seller/${sellerId}`);
    seller.value = res.data.seller;
    products.value = res.data.products;
    followerCount.value = res.data.seller.follower_count || 0;
    
    // Check follow status if logged in
    const token = localStorage.getItem('token');
    if (token) {
        checkFollowStatus(sellerId, token);
    }
  } catch (err) {
    console.error(err);
    error.value = err.response?.data?.msg || 'ไม่สามารถโหลดข้อมูลร้านค้าได้';
  } finally {
    loading.value = false;
  }
};

const checkFollowStatus = async (sellerId, token) => {
    try {
        const res = await axios.get(`${baseUrl}/api/seller/${sellerId}/follow-status`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        isFollowing.value = res.data.is_following;
        followerCount.value = res.data.follower_count;
    } catch (err) {
        console.error('Error checking follow status:', err);
    }
};

const toggleFollow = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('กรุณาเข้าสู่ระบบก่อนทำการติดตาม');
        return;
    }
    
    followLoading.value = true;
    const sellerId = route.params.id;
    
    try {
        if (isFollowing.value) {
            // Unfollow
            const res = await axios.delete(`${baseUrl}/api/seller/${sellerId}/unfollow`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            isFollowing.value = false;
            followerCount.value = res.data.follower_count;
        } else {
            // Follow
            const res = await axios.post(`${baseUrl}/api/seller/${sellerId}/follow`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            isFollowing.value = true;
            followerCount.value = res.data.follower_count;
        }
    } catch (err) {
        console.error('Error toggling follow:', err);
        alert(err.response?.data?.msg || 'เกิดข้อผิดพลาดในการติดตาม');
    } finally {
        followLoading.value = false;
    }
};

const openChat = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('กรุณาเข้าสู่ระบบเพื่อแชท');
        return;
    }

    chatLoading.value = true;
    const sellerId = route.params.id;
    
    try {
        const res = await axios.post(`${baseUrl}/api/chat/start/${sellerId}`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        });
        
        const conversationId = res.data.conversation_id;
        router.push(`/chat?conversationId=${conversationId}`);
    } catch (err) {
        console.error('Error starting chat:', err);
        alert(err.response?.data?.msg || 'ไม่สามารถเริ่มแชทได้');
    } finally {
        chatLoading.value = false;
    }
};

onMounted(() => {
  fetchShopData();
});
</script>

<style scoped>
.animate-in-fade {
  animation: fadeIn 0.6s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
