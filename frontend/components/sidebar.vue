<template>
  <aside
    class="fixed left-4 top-24 z-50 flex flex-col transition-all duration-500 ease-[cubic-bezier(0.23,1,0.32,1)] h-[calc(100vh-8rem)]"
    :class="expand ? 'w-[280px]' : 'w-[88px]'"
    @mouseenter="expand = true"
    @mouseleave="expand = false"
  >
    <!-- Main Glass Container -->
    <div 
      class="relative flex flex-col w-full h-full bg-[#0f0f13]/60 backdrop-blur-2xl border border-white/5 rounded-[32px] shadow-[0_8px_32px_rgba(0,0,0,0.4)] overflow-hidden transition-all duration-500 group"
    >
      
      <!-- Ambient Glow Effects -->
      <div class="absolute -top-[100px] left-1/2 -translate-x-1/2 w-[200px] h-[200px] bg-purple-600/20 rounded-full blur-[80px] pointer-events-none"></div>
      <div class="absolute bottom-0 right-0 w-[150px] h-[150px] bg-pink-600/10 rounded-full blur-[60px] pointer-events-none"></div>

      <!-- Profile Section -->
      <div class="relative pt-8 pb-4 flex flex-col items-center shrink-0 z-10 transition-all duration-500">
        
        <div class="relative cursor-pointer group/avatar" @click="navigate('/profile')">
          <!-- Animated Ring -->
          <div 
            class="absolute -inset-[3px] rounded-full bg-gradient-to-tr from-pink-500 via-purple-500 to-cyan-500 opacity-70 blur-[2px] group-hover/avatar:opacity-100 group-hover/avatar:blur-[4px] transition-all duration-500"
            :class="expand ? 'w-[86px] h-[86px]' : 'w-[54px] h-[54px]'"
          ></div>
          
          <!-- Avatar Image -->
          <div 
            class="relative rounded-full overflow-hidden border-[3px] border-[#18181b] bg-[#18181b] transition-all duration-500"
            :class="expand ? 'w-[80px] h-[80px]' : 'w-[48px] h-[48px]'"
          >
            <img
              v-if="profileImageUrlLoaded"
              :src="profileImageUrl"
              class="w-full h-full object-cover transition-transform duration-700 group-hover/avatar:scale-110"
              alt="Profile"
            />
            <div v-else class="w-full h-full bg-zinc-800 flex items-center justify-center">
              <User class="w-1/2 h-1/2 text-zinc-500" />
            </div>
          </div>

          <!-- Online Status -->
          <div 
            class="absolute bottom-1 right-1 w-4 h-4 bg-[#18181b] rounded-full flex items-center justify-center z-20"
          >
             <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
          </div>
        </div>

        <!-- User Info (Expanded) -->
        <div 
          class="flex flex-col items-center mt-3 overflow-hidden transition-all duration-500"
          :class="expand ? 'max-h-[200px] opacity-100' : 'max-h-0 opacity-0'"
        >
          <div class="flex items-center gap-2">
            <h3 class="text-white font-bold text-lg tracking-tight">{{ username }}</h3>
          </div>
          
          <!-- Badges -->
           <div class="flex flex-wrap gap-2 justify-center mt-1.5 mb-3">
             <span v-if="user?.is_seller" class="px-2.5 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/20 text-[10px] font-bold text-purple-400 tracking-wide uppercase shadow-[0_0_10px_rgba(168,85,247,0.1)]">
              Seller
            </span>
            <span v-if="user?.role === 'admin'" class="px-2.5 py-0.5 rounded-full bg-red-500/10 border border-red-500/20 text-[10px] font-bold text-red-400 tracking-wide uppercase shadow-[0_0_10px_rgba(239,68,68,0.1)]">
              Admin
            </span>
           </div>

          <!-- Wallet Cards -->
          <div class="grid grid-cols-2 gap-2 w-[240px] px-2">
             <div class="flex flex-col items-center p-2 rounded-xl bg-white/5 border border-white/5 backdrop-blur-md hover:bg-white/10 transition-colors group/card">
                <div class="flex items-center gap-1.5 mb-0.5">
                  <Coins class="w-3.5 h-3.5 text-amber-400 group-hover/card:rotate-12 transition-transform duration-300"/>
                  <span class="text-amber-400 text-sm font-bold">{{ coinBalance !== null ? formatNumber(coinBalance) : '-' }}</span>
                </div>
                <span class="text-[10px] text-zinc-400 font-medium tracking-wide uppercase">Coins</span>
             </div>
             <div class="flex flex-col items-center p-2 rounded-xl bg-white/5 border border-white/5 backdrop-blur-md hover:bg-white/10 transition-colors group/card">
                <div class="flex items-center gap-1.5 mb-0.5">
                  <Gem class="w-3.5 h-3.5 text-pink-400 group-hover/card:rotate-12 transition-transform duration-300"/>
                  <span class="text-pink-400 text-sm font-bold">{{ tokenBalance !== null ? formatNumber(tokenBalance) : '-' }}</span>
                </div>
                <span class="text-[10px] text-zinc-400 font-medium tracking-wide uppercase">Tokens</span>
             </div>
          </div>
        </div>
      </div>

      <!-- Navigation Menu -->
      <nav class="flex-1 overflow-y-auto overflow-x-hidden no-scrollbar px-3 py-2 space-y-1">
        <div
          v-for="item in menuItems"
          :key="item.name"
          @click="navigate(item.route)"
          class="relative flex items-center h-[52px] px-3 rounded-xl cursor-pointer transition-all duration-300 group/item"
          :class="[
            isActive(item.route) 
              ? 'bg-gradient-to-r from-purple-500/20 to-pink-500/5 text-white shadow-[inset_0_0_20px_rgba(168,85,247,0.05)]' 
              : 'text-zinc-400 hover:text-zinc-100 hover:bg-white/5'
          ]"
        >
          <!-- Active Indicator (Left Bar) -->
          <div 
            class="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-[24px] rounded-r-full bg-gradient-to-b from-purple-500 to-pink-500 shadow-[0_0_12px_rgba(236,72,153,0.8)] transition-all duration-300"
            :class="isActive(item.route) ? 'opacity-100 scale-y-100' : 'opacity-0 scale-y-0'"
          ></div>

          <!-- Icon -->
          <div class="relative z-10 flex items-center justify-center w-[24px] h-[24px] shrink-0 transition-transform duration-300 group-hover/item:scale-110"
               :class="expand ? 'mr-3' : 'mx-auto'"
          >
             <component 
                :is="item.icon" 
                :class="[
                  'w-6 h-6 stroke-[1.5]',
                  isActive(item.route) ? 'text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.5)]' : 'text-current'
                ]" 
             />
          </div>

          <!-- Label -->
          <span 
            class="relative z-10 whitespace-nowrap font-medium text-[15px] transition-all duration-500 origin-left"
            :class="[
              expand ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4 absolute pointer-events-none',
              isActive(item.route) ? 'text-white font-semibold' : ''
            ]"
          >
            {{ item.name }}
          </span>

          <!-- Badge -->
          <span 
            v-if="item.badge && item.badge > 0" 
            class="absolute right-3 min-w-[20px] h-[20px] px-1.5 flex items-center justify-center bg-gradient-to-r from-red-500 to-rose-600 text-white text-[11px] font-bold rounded-full shadow-lg border border-red-400/20 z-20"
            :class="expand ? 'block' : 'hidden'"
          >
            {{ item.badge > 99 ? '99+' : item.badge }}
          </span>
          
           <!-- Collapsed Badge Dot -->
           <span 
             v-if="!expand && item.badge && item.badge > 0"
             class="absolute top-2 right-2 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-[#09090b] z-20 animate-pulse"
           ></span>

        </div>
      </nav>

      <!-- Bottom Actions -->
      <div class="p-4 mt-auto border-t border-white/5 bg-[#0f0f13]/80 backdrop-blur-md space-y-3 z-20">
         
         <!-- Add Product Button (Seller) -->
         <button
          v-if="user?.is_seller"
          class="group/btn relative w-full flex items-center justify-center overflow-hidden rounded-xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 p-[1px] shadow-lg shadow-purple-900/20 hover:shadow-purple-500/30 transition-shadow duration-300"
          @click="navigate('/AddProduct')"
        >
          <div class="relative w-full h-full bg-[#131315] group-hover/btn:bg-[#131315]/90 rounded-[11px] px-3 py-3 flex items-center justify-center transition-all">
             <PlusCircle class="w-5 h-5 text-purple-300 mr-2 shrink-0 group-hover/btn:rotate-90 transition-transform duration-300" />
             <span 
              class="text-sm font-semibold bg-gradient-to-r from-indigo-200 to-purple-200 bg-clip-text text-transparent whitespace-nowrap overflow-hidden transition-all duration-300"
              :class="expand ? 'w-auto opacity-100' : 'w-0 opacity-0 px-0'"
            >
              เพิ่มสินค้า
            </span>
          </div>
        </button>

        <!-- Logout Button -->
        <div
          class="flex items-center justify-center p-3 rounded-xl cursor-pointer text-zinc-500 hover:text-red-400 hover:bg-red-500/10 border border-transparent hover:border-red-500/20 transition-all duration-300 group/logout"
          @click="handleLogout"
        >
          <LogOut class="w-5 h-5 group-hover/logout:-translate-x-1 transition-transform duration-300" />
          <span 
            class="ml-3 text-sm font-medium whitespace-nowrap overflow-hidden transition-all duration-300"
            :class="expand ? 'w-auto opacity-100' : 'w-0 opacity-0'"
          >
            ออกจากระบบ
          </span>
        </div>

      </div>

    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { 
  Store, 
  ShoppingCart, 
  Gavel, 
  CalendarCheck, 
  Target, 
  Building2, 
  BarChart3, 
  Coins, 
  PlusCircle, 
  LogOut,
  User,
  Gem
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();
const expand = ref(false); 
const user = ref(null);
const profileImageUrlLoaded = ref(false);
const coinBalance = ref(null);
const tokenBalance = ref(null);

const baseUrl = "http://localhost:5000";

// Format numbers (e.g. 1.2k)
const formatNumber = (num) => {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'k';
  return num.toLocaleString();
};

const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) return "/guest-profile.png";
  return user.value.profile_image_url.startsWith("http")
    ? user.value.profile_image_url
    : baseUrl + user.value.profile_image_url;
});

const username = computed(() => user.value?.username || "Guest User");

const menuItems = computed(() => [
  { name: "ร้านค้า", icon: Store, route: "/dashboard" },
  { name: "ตระกร้าสินค้า", icon: ShoppingCart, route: "/cart" },
  { name: "ประมูล", icon: Gavel, route: "/auction" },
  { name: "เช็คอิน", icon: CalendarCheck, route: "/check-in" },
  { name: "ภารกิจ", icon: Target, route: "/missions" },
  // Increased visibility for sellers/admins
  ...(user.value?.role === 'admin' || user.value?.is_seller ? [
     { name: "แอดมินจัดซื้อย่าย", icon: Building2, route: "/admin-purchasing" } 
  ] : []),
  ...(user.value?.is_seller ? [
    { name: "แดชบอร์ดผู้ขาย", icon: BarChart3, route: "/seller-dashboard" }
  ] : []),
  { name: "เติม Token", icon: Coins, route: "/token-topup" },
]);

const isActive = (path) => route.path === path;

function navigate(path) {
  router.push(path);
}

function handleLogout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  user.value = null;
  router.push("/login");
  window.dispatchEvent(new Event("user-updated"));
}

async function fetchUserProfile() {
  profileImageUrlLoaded.value = false;
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    user.value = JSON.parse(storedUser);
    
    // Fetch coin balance and token balance
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const res = await axios.get(`${baseUrl}/api/profile`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        coinBalance.value = res.data.coin_balance || 0;
      } catch (e) {
        console.error("Failed to fetch profile:", e);
      }
      
      try {
        const tokenRes = await axios.get(`${baseUrl}/api/token/balance`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        tokenBalance.value = tokenRes.data.token_balance || 0;
      } catch (e) {
        console.error("Failed to fetch token balance:", e);
      }
    }
  } else {
    user.value = null;
  }

  const img = new Image();
  img.src = profileImageUrl.value;
  img.onload = () => (profileImageUrlLoaded.value = true);
  img.onerror = () => {
    if (user.value) user.value.profile_image_url = null;
    profileImageUrlLoaded.value = true;
  };
}

onMounted(() => {
  fetchUserProfile();
  window.addEventListener("user-updated", fetchUserProfile);
});

onBeforeUnmount(() => {
  window.removeEventListener("user-updated", fetchUserProfile);
});
</script>

<style scoped>
/* Scoped utilities */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>