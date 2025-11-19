<template>
  <div>
    <!-- Top Navigation Bar -->
    <nav class="bg-gradient-to-r from-black to-pink-950 text-white px-6 py-4 flex items-center shadow-md relative">
      <!-- Logo -->
      <NuxtLink :to="hideNavbar ? '#' : '/dashboard'" class="font-bold text-2xl flex-shrink-0 transition transform hover:scale-110">
        <span class="text-white transition-colors duration-300">P2U</span>
        <span class="text-pink-500 transition-colors duration-300">KAISER</span>
      </NuxtLink>
      
      <!-- Search Bar (Centered) -->
      <div v-if="!hideNavbar" class="absolute left-1/2 transform -translate-x-1/2 flex items-center bg-white rounded-2xl overflow-hidden w-1/2 shadow-lg">
        <input 
          v-model="searchQuery" 
          @keyup.enter="handleSearch" 
          type="text" 
          placeholder="ค้นหาสินค้า, ร้านค้า, หมวดหมู่..."
          class="w-full px-4 py-2 text-black outline-none placeholder:text-gray-400" 
        />
        <button 
          @click="handleSearch" 
          class="bg-pink-600 text-white px-6 py-2 hover:bg-pink-700 transition transform hover:scale-105 font-semibold flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24">
            <path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5A6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5S14 7.01 14 9.5S11.99 14 9.5 14"/>
          </svg>
          <span>ค้นหา</span>
        </button>
      </div>

      <div class="ml-auto flex items-center gap-4 relative">
        <!-- Profile Picture -->
        <NuxtLink v-if="!hideNavbar && user" to="/profile"
          class="w-10 h-10 rounded-full overflow-hidden border-2 border-pink-400 hover:scale-105 transition bg-white hover:border-pink-300"
          title="My Profile">
          <img :src="profileImageUrl" alt="Profile" class="w-full h-full object-cover" />
        </NuxtLink>

        <!-- Settings Menu -->
        <div v-if="!hideNavbar && user" class="relative">
          <button @click="toggleSettings" class="text-pink-300 hover:scale-110 hover:text-pink-200 text-2xl transition" title="Settings">
            ⚙️
          </button>
          <div v-if="showSettings" class="absolute right-0 mt-2 w-40 bg-white text-black rounded-lg shadow-xl z-50 overflow-hidden border border-gray-200">
            <NuxtLink to="/about">
              <button class="w-full text-left px-4 py-3 hover:bg-gray-100 transition flex items-center gap-2">
                <span>📋</span>
                <span>About</span>
              </button>
            </NuxtLink>
            <button @click="handleLogout" class="w-full text-left px-4 py-3 hover:bg-red-50 transition flex items-center gap-2 text-red-600">
              <span>🚪</span>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Secondary Navigation Bar with Active State -->
    <nav v-if="!hideNavbar" class="bg-pink-900 text-white px-6 py-3 flex justify-center items-center gap-10 shadow-md">
      <NuxtLink 
        to="/dashboard" 
        class="relative py-2 hover:text-pink-200 transform transition font-semibold group"
        :class="{ 'text-pink-200': isActive('/dashboard') }">
        <span>หน้าแรก</span>
        <span 
          class="absolute bottom-0 left-0 w-full h-0.5 bg-pink-300 transform transition-all duration-300"
          :class="isActive('/dashboard') ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'">
        </span>
      </NuxtLink>

      <NuxtLink 
        to="/shop" 
        class="relative py-2 hover:text-pink-200 transform transition font-semibold group"
        :class="{ 'text-pink-200': isActive('/shop') }">
        <span>สินค้า</span>
        <span 
          class="absolute bottom-0 left-0 w-full h-0.5 bg-pink-300 transform transition-all duration-300"
          :class="isActive('/shop') ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'">
        </span>
      </NuxtLink>

      <NuxtLink 
        to="/about" 
        class="relative py-2 hover:text-pink-200 transform transition font-semibold group"
        :class="{ 'text-pink-200': isActive('/about') }">
        <span>เกี่ยวกับ</span>
        <span 
          class="absolute bottom-0 left-0 w-full h-0.5 bg-pink-300 transform transition-all duration-300"
          :class="isActive('/about') ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'">
        </span>
      </NuxtLink>

      <NuxtLink 
        to="/help" 
        class="relative py-2 hover:text-pink-200 transform transition font-semibold group"
        :class="{ 'text-pink-200': isActive('/help') }">
        <span>ช่วยเหลือ</span>
        <span 
          class="absolute bottom-0 left-0 w-full h-0.5 bg-pink-300 transform transition-all duration-300"
          :class="isActive('/help') ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'">
        </span>
      </NuxtLink>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

const route = useRoute();
const router = useRouter();
const user = ref(null);
const showSettings = ref(false);
const searchQuery = ref("");

// ฟังก์ชันค้นหา
const handleSearch = () => {
  const query = searchQuery.value.trim();
  if (!query) return;
  
  // นำทางไปหน้า dashboard พร้อมกับ query parameter
  router.push({
    path: "/dashboard",
    query: { search: query },
  });
  
  // ส่ง event เพื่อให้หน้า dashboard รับค่าการค้นหา
  window.dispatchEvent(new CustomEvent('search-products', { detail: query }));
};

// ตรวจสอบว่าอยู่ในหน้าไหน
const isActive = (path) => {
  return route.path === path;
};

const hideNavbar = computed(() => {
  const hiddenPages = ["/login", "/register"];
  return hiddenPages.includes(route.path);
});

function loadUser() {
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

const baseUrl = "http://localhost:5000";
const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) {
    return "/guest-profile.png";
  }

  const imagePath = user.value.profile_image_url;
  if (/^https?:\/\//i.test(imagePath)) {
    return imagePath;
  }

  const normalizedBase = baseUrl.replace(/\/$/, "");
  const normalizedPath = imagePath.startsWith("/") ? imagePath : `/${imagePath}`;
  return `${normalizedBase}${normalizedPath}`;
});

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
  window.dispatchEvent(new Event("user-updated"));
};

onMounted(() => {
  loadUser();
  window.addEventListener("user-updated", loadUser);
});

onBeforeUnmount(() => {
  window.removeEventListener("user-updated", loadUser);
});
</script>