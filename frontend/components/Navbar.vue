<template>
  <nav 
    v-if="!hideNavbar" 
    class="sticky top-0 z-50 h-[80px] w-full transition-all duration-300"
  >
    <div class="absolute inset-0 bg-[#09090b]/80 backdrop-blur-xl border-b border-white/5 shadow-[0_4px_30px_rgba(0,0,0,0.5)]">
      <div class="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-pink-500/50 to-transparent opacity-50"></div>
    </div>

    <div class="relative container mx-auto px-6 h-full flex items-center justify-between gap-8">
      
      <!-- Brand Logo -->
      <NuxtLink to="/dashboard" class="flex items-center gap-3 group shrink-0">
        <div class="relative w-11 h-11">
          <div class="absolute inset-0 bg-gradient-to-tr from-pink-600 to-purple-600 rounded-xl blur opacity-60 group-hover:opacity-100 transition duration-500"></div>
          <div class="relative w-full h-full bg-[#09090b] border border-white/10 rounded-xl flex items-center justify-center transform group-hover:-rotate-6 transition-transform duration-300 ease-out">
            <span class="text-2xl drop-shadow-lg filter group-hover:scale-110 transition-transform">👑</span>
          </div>
        </div>
        <div class="flex flex-col">
          <span class="font-display font-bold text-xl tracking-wide bg-gradient-to-r from-white via-pink-200 to-purple-200 bg-clip-text text-transparent group-hover:text-white transition-colors">
            P2UKAISER
          </span>
          <span class="text-[10px] font-medium text-gray-500 tracking-[0.2em] uppercase group-hover:text-pink-400 transition-colors">
            Premium Shop
          </span>
        </div>
      </NuxtLink>

      <!-- Search Bar -->
      <div class="flex-1 max-w-2xl hidden md:block group/search">
        <div class="relative w-full transition-all duration-300">
          
          <div class="absolute -inset-0.5 bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 rounded-full opacity-20 group-focus-within/search:opacity-60 blur transition duration-500"></div>
          
          <div class="relative flex items-center bg-[#18181b] rounded-full border border-white/10 shadow-inner overflow-hidden group-focus-within/search:border-white/20">
            
            <div class="pl-4 text-gray-400 group-focus-within/search:text-pink-400 transition-colors">
              <Search class="w-5 h-5" />
            </div>

            <input 
              v-model="searchQuery" 
              @keyup.enter="handleSearch" 
              type="text" 
              placeholder="ค้นหาสินค้า..."
              class="w-full bg-transparent border-none text-white px-4 py-2.5 focus:ring-0 placeholder-gray-500 text-sm"
            />
            
            <button 
              @click="handleSearch" 
              class="m-1 px-5 py-1.5 rounded-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white text-xs font-bold tracking-wide shadow-lg transform active:scale-95 transition-all duration-200 border border-white/10"
            >
              ค้นหา
            </button>
          </div>
        </div>
      </div>

      <!-- Right Actions -->
      <div class="flex items-center gap-2 sm:gap-4 shrink-0">
        
        <!-- Notifications -->
        <NuxtLink v-if="user" to="/notifications" class="relative group p-2.5 rounded-xl transition-all duration-300 hover:bg-white/5">
          <div class="absolute inset-0 bg-pink-500/20 rounded-xl blur opacity-0 group-hover:opacity-100 transition duration-300"></div>
          <Bell class="relative w-6 h-6 text-zinc-400 group-hover:text-pink-400 transition-colors duration-300" />
          <span v-if="notificationCount > 0" class="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full ring-2 ring-[#09090b] z-10 animate-pulse"></span>
        </NuxtLink>

        <!-- Chat -->
        <NuxtLink v-if="user" to="/chat" class="relative group p-2.5 rounded-xl transition-all duration-300 hover:bg-white/5">
          <div class="absolute inset-0 bg-cyan-500/20 rounded-xl blur opacity-0 group-hover:opacity-100 transition duration-300"></div>
          <MessageCircle class="relative w-6 h-6 text-zinc-400 group-hover:text-cyan-400 transition-colors duration-300" />
          <span v-if="unreadMessages > 0" class="absolute top-1.5 right-1.5 min-w-[16px] h-[16px] flex items-center justify-center bg-cyan-500 text-[9px] font-bold text-black rounded-full ring-2 ring-[#09090b]">
            {{ unreadMessages > 9 ? '9+' : unreadMessages }}
          </span>
        </NuxtLink>

        <!-- Wishlist -->
        <NuxtLink v-if="user" to="/wishlist" class="relative group p-2.5 rounded-xl transition-all duration-300 hover:bg-white/5 hidden sm:block">
          <div class="absolute inset-0 bg-red-500/20 rounded-xl blur opacity-0 group-hover:opacity-100 transition duration-300"></div>
          <Heart class="relative w-6 h-6 text-zinc-400 group-hover:text-red-400 transition-colors duration-300" />
        </NuxtLink>

        <div class="w-[1px] h-8 bg-white/10 mx-1 hidden sm:block"></div>

        <!-- User Dropdown -->
        <div v-if="user" class="relative" ref="dropdownRef">
          <button 
            @click="toggleSettings" 
            class="flex items-center gap-3 pl-1 pr-3 py-1 rounded-full transition-all duration-300 hover:bg-white/5 border border-transparent hover:border-white/10 group"
            :class="{ 'bg-white/5 border-white/10': showSettings }"
          >
            <div class="relative">
              <div class="absolute -inset-1 bg-gradient-to-tr from-pink-500 to-purple-600 rounded-full blur opacity-50 group-hover:opacity-80 transition-opacity duration-500"></div>
              <img 
                :src="profileImageUrl" 
                alt="Profile" 
                class="relative w-[38px] h-[38px] rounded-full object-cover border-2 border-[#09090b]"
              />
            </div>
            <div class="hidden lg:flex flex-col items-start mr-1">
              <span class="text-sm font-bold text-white leading-none group-hover:text-pink-200 transition-colors">{{ user.username }}</span>
              <span class="text-[10px] text-zinc-500 leading-none mt-1 group-hover:text-zinc-400">Member</span>
            </div>
            <ChevronDown 
              class="w-4 h-4 text-zinc-500 transition-transform duration-300 hidden lg:block group-hover:text-zinc-300"
              :class="{ 'rotate-180': showSettings }" 
            />
          </button>

          <Transition name="dropdown">
            <div v-if="showSettings" class="absolute right-0 mt-4 w-[280px] bg-[#0f0f13]/90 backdrop-blur-2xl rounded-3xl shadow-[0_20px_60px_-15px_rgba(0,0,0,0.8)] border border-white/10 overflow-hidden ring-1 ring-white/5 origin-top-right z-50">
              
              <!-- Dropdown Header -->
              <div class="relative p-6 bg-gradient-to-b from-white/5 to-transparent border-b border-white/5 flex flex-col items-center text-center">
                 <div class="relative mb-3">
                    <div class="absolute -inset-1 bg-gradient-to-tr from-pink-500 to-purple-600 rounded-full blur-sm opacity-60"></div>
                    <img 
                      :src="profileImageUrl" 
                      alt="Profile" 
                      class="relative w-16 h-16 rounded-full object-cover border-4 border-[#18181b]"
                    />
                 </div>
                 <h3 class="text-base font-bold text-white mb-0.5">{{ user.full_name || user.username }}</h3>
                 <p class="text-xs text-zinc-500 truncate max-w-full px-4">{{ user.email }}</p>
              </div>

              <!-- Menu Items -->
              <div class="p-2 space-y-1">
                <NuxtLink to="/profile" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-zinc-400 hover:text-white hover:bg-white/5 transition-all group">
                  <User class="w-5 h-5 text-zinc-500 group-hover:text-pink-400 transition-colors" />
                  <span class="text-sm font-medium">โปรไฟล์</span>
                </NuxtLink>

                <NuxtLink to="/orders" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-zinc-400 hover:text-white hover:bg-white/5 transition-all group">
                  <Package class="w-5 h-5 text-zinc-500 group-hover:text-blue-400 transition-colors" />
                  <span class="text-sm font-medium">คำสั่งซื้อของฉัน</span>
                </NuxtLink>

                <NuxtLink v-if="user.is_seller" to="/seller-dashboard" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-zinc-400 hover:text-white hover:bg-white/5 transition-all group">
                  <BarChart3 class="w-5 h-5 text-zinc-500 group-hover:text-purple-400 transition-colors" />
                  <span class="text-sm font-medium">แดชบอร์ดผู้ขาย</span>
                </NuxtLink>

                <NuxtLink to="/about" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-zinc-400 hover:text-white hover:bg-white/5 transition-all group">
                  <Info class="w-5 h-5 text-zinc-500 group-hover:text-emerald-400 transition-colors" />
                  <span class="text-sm font-medium">เกี่ยวกับเรา</span>
                </NuxtLink>
              </div>

              <!-- Logout -->
              <div class="p-2 border-t border-white/5 bg-red-500/5 mt-1">
                <button @click="handleLogout" class="flex items-center gap-3 px-4 py-3 w-full rounded-2xl text-red-400 hover:bg-red-500/10 transition-all group">
                  <LogOut class="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
                  <span class="text-sm font-bold">ออกจากระบบ</span>
                </button>
              </div>
            </div>
          </Transition>
        </div>

        <NuxtLink v-else to="/login" class="px-6 py-2 rounded-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white text-sm font-bold shadow-lg shadow-purple-900/20 hover:shadow-purple-500/30 transition-all duration-300 transform hover:-translate-y-0.5">
          เข้าสู่ระบบ
        </NuxtLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import { 
  Search, 
  Bell, 
  MessageCircle, 
  Heart, 
  ChevronDown, 
  User, 
  Package, 
  BarChart3, 
  Info, 
  LogOut 
} from 'lucide-vue-next';

// ================= Logic =================
const route = useRoute();
const router = useRouter();
const user = ref(null);
const showSettings = ref(false);
const searchQuery = ref("");
const notificationCount = ref(0);
const unreadMessages = ref(0);
const dropdownRef = ref(null);

// ตัวแปรสำหรับเก็บเวลา เพื่อทำ Cache Busting
const imageVersion = ref(Date.now());

const baseUrl = "http://localhost:5000";

const handleSearch = () => {
  if (!searchQuery.value.trim()) return;
  router.push({
    path: "/dashboard",
    query: { q: searchQuery.value.trim() },
  });
};

const hideNavbar = computed(() => {
  const hiddenPages = ["/login", "/register", "/admin-login"];
  return hiddenPages.includes(route.path);
});

// Logic รูปภาพพร้อม Cache Busting
const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) {
    return "/guest-profile.png";
  }
  
  let url = user.value.profile_image_url;
  
  if (!url.startsWith("http")) {
    url = baseUrl + url;
  }

  // เติม ?v= ตามด้วยเวลา เพื่อ force ให้ browser โหลดรูปใหม่
  return `${url}${url.includes('?') ? '&' : '?'}v=${imageVersion.value}`;
});

// [FIXED] ฟังก์ชัน loadUser ปรับให้รับ Event Argument
function loadUser(event) {
  // 1. ถ้ามีข้อมูลส่งมาทาง Event ให้ใช้ข้อมูลนั้นเลย (เร็วและชัวร์กว่า)
  if (event && event.detail) {
    user.value = event.detail;
  } 
  // 2. ถ้าไม่มี (เช่นโหลดหน้าเว็บครั้งแรก) ให้ดึงจาก LocalStorage
  else {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser);
      } catch {
        user.value = null;
      }
    } else {
      user.value = null;
    }
  }

  // 3. สำคัญ: อัปเดต version เพื่อให้รูปภาพเปลี่ยนทันที
  imageVersion.value = Date.now();
  
  // โหลดการแจ้งเตือน
  if (user.value) {
    fetchNotifications();
  }
}

async function fetchNotifications() {
  const token = localStorage.getItem("token");
  if (!token) return;
  
  try {
    const res = await axios.get(`${baseUrl}/api/notifications`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    notificationCount.value = res.data.unread_count || 0;
  } catch (e) {
    console.error("Failed to fetch notifications:", e);
  }
}

const toggleSettings = () => {
  showSettings.value = !showSettings.value;
};

const handleLogout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  localStorage.removeItem("user");
  user.value = null;
  showSettings.value = false;
  router.push("/login");
  // แจ้ง component อื่นว่า logout แล้ว
  window.dispatchEvent(new Event("user-updated"));
};

const handleClickOutside = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    showSettings.value = false;
  }
};

onMounted(() => {
  loadUser(); // โหลดครั้งแรก
  window.addEventListener("user-updated", loadUser); // รอฟัง Event
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  window.removeEventListener("user-updated", loadUser);
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style scoped>
.dropdown-enter-active {
  animation: dropdown-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.dropdown-leave-active {
  animation: dropdown-out 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes dropdown-in {
  0% { opacity: 0; transform: translateY(-10px) scale(0.95); filter: blur(10px); }
  100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }
}
@keyframes dropdown-out {
  0% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }
  100% { opacity: 0; transform: translateY(-10px) scale(0.95); filter: blur(10px); }
}
</style>