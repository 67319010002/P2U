<template>
  <section class="layout-full relative min-h-screen bg-slate-950 text-white overflow-hidden">
    <!-- Animated Background Gradients -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -right-20 -top-20 w-96 h-96 bg-pink-500/20 blur-3xl animate-pulse"></div>
      <div class="absolute -left-20 top-1/3 w-80 h-80 bg-purple-500/15 blur-3xl animate-pulse" style="animation-delay: 1s"></div>
      <div class="absolute right-1/4 bottom-0 w-96 h-96 bg-indigo-500/20 blur-3xl animate-pulse" style="animation-delay: 2s"></div>
    </div>

    <!-- Grid Pattern Overlay -->
    <div class="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,black,transparent)]"></div>

    <div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 py-12">
      <!-- Login Card -->
      <div class="w-full max-w-md">
        <!-- Decorative Elements -->
        <div class="absolute -top-4 -left-4 w-24 h-24 bg-pink-500/10 blur-2xl"></div>
        <div class="absolute -bottom-4 -right-4 w-32 h-32 bg-indigo-500/10 blur-2xl"></div>
        
        <div class="relative rounded-3xl border border-white/10 bg-slate-900/40 backdrop-blur-xl p-8 shadow-2xl shadow-black/50 hover:border-white/20 transition-all duration-300">

          <!-- Header -->
          <div class="text-center space-y-2 mb-8">
            <p class="text-4xl uppercase  text-pink-400 font-semibold  font-bold">P2U Kaiser</p>
            <h1 class="text-2xl font-bold text-white">
              ยินดีต้อนรับกลับ
            </h1>
            <p class="text-sm text-gray-400">เข้าสู่ระบบเพื่อจัดการสินค้าที่คุณรัก</p>
          </div>

          <!-- Login Form -->
          <form class="space-y-5" @submit.prevent="handleLogin">
            <!-- Username Input -->
            <div class="space-y-2">
              <div class="flex items-center justify-between mb-1">
                <label class="text-xs uppercase tracking-widest text-gray-300 font-medium">ชื่อผู้ใช้</label>
                <span class="text-[0.65rem] text-gray-500">ใช้ชื่อที่จดจำง่าย</span>
              </div>
              <div class="group relative">
                <div class="absolute -inset-0.5 bg-pink-500/50 rounded-full opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 blur transition duration-300"></div>
                <div class="relative flex items-center rounded-md bg-slate-950/90 border border-white/10 group-focus-within:border-pink-500/50 transition-all duration-300">
                  <span class="absolute left-4 text-gray-400 group-focus-within:text-pink-400 transition-colors">
                    <i class="bx bxs-user text-xl"></i>
                  </span>
                  <input 
                    v-model="username" 
                    placeholder="username" 
                    class="w-full bg-transparent pl-12 pr-4 py-3.5 text-white placeholder-gray-500 focus:outline-none rounded-md" 
                    autocomplete="username" 
                  />
                </div>
              </div>
            </div>

            <!-- Password Input -->
            <div class="space-y-2">
              <div class="flex items-center justify-between mb-1">
                <label class="text-xs uppercase tracking-widest text-gray-300 font-medium">รหัสผ่าน</label>
                <span class="text-[0.65rem] text-gray-500">เก็บข้อมูลของคุณให้ปลอดภัย</span>
              </div>
              <div class="group relative">
                <div class="absolute -inset-0.5 bg-pink-500/50 rounded-full opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 blur transition duration-300"></div>
                <div class="relative flex items-center rounded-md bg-slate-950/90 border border-white/10 group-focus-within:border-pink-500/50 transition-all duration-300">
                  <span class="absolute left-4 text-gray-400 group-focus-within:text-pink-400 transition-colors">
                    <i class='bxr  bxs-lock-keyhole' ></i> 
                  </span>
                  <input 
                    v-model="password" 
                    type="password" 
                    placeholder="••••••••" 
                    class="w-full bg-transparent pl-12 pr-4 py-3.5 text-white placeholder-gray-500 focus:outline-none rounded-md"
                    autocomplete="current-password" 
                  />
                </div>
              </div>
            </div>

            <!-- Login Button -->
            <button 
              type="submit"
              class="relative w-full mt-6 rounded-full bg-pink-600 hover:bg-pink-500 text-white font-semibold py-3.5 transition-all duration-300 shadow-lg shadow-pink-500/30 hover:shadow-pink-500/50 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:ring-offset-2 focus:ring-offset-slate-900 disabled:opacity-50 disabled:cursor-not-allowed group overflow-hidden"
              :disabled="loading"
            >
              <span class="absolute inset-0 w-full h-full bg-white/20 scale-0 group-hover:scale-110 transition-transform duration-300 rounded-full"></span>
              <span class="relative flex items-center justify-center gap-2">
                <span v-if="!loading">เข้าสู่ระบบ</span>
                <span v-else class="flex items-center gap-2">
                  <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  กำลังเข้าสู่ระบบ...
                </span>
              </span>
            </button>
          </form>

          <!-- Error Message -->
          <div v-if="errorMsg" class="mt-4 p-3 rounded-full bg-red-500/10 border border-red-500/30 backdrop-blur-sm">
            <p class="text-center text-sm text-red-300 flex items-center justify-center gap-2">
              <i class="bx bxs-error-circle"></i>
              {{ errorMsg }}
            </p>
          </div>

          <!-- Register Link -->
          <div class="mt-6 pt-6 border-t border-white/10">
            <p class="text-center text-sm text-gray-400">
              ไม่มีบัญชี?
              <NuxtLink to="/register" class="text-pink-400 font-semibold hover:text-pink-300 transition-all">
                ลงทะเบียน
              </NuxtLink>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <Loading v-if="loading" />
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Loading from '@/components/loading.vue';

const username = ref('');
const password = ref('');
const errorMsg = ref('');
const loading = ref(false);
const router = useRouter();

const handleLogin = async () => {
  errorMsg.value = '';
  if (!username.value || !password.value) {
    errorMsg.value = 'กรุณากรอกชื่อผู้ใช้และรหัสผ่าน';
    return;
  }

  loading.value = true;

  try {
    const res = await axios.post('http://localhost:5000/api/login', {
      username: username.value,
      password: password.value
    });

    const user = res.data.user;

    if (user) {
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('user', JSON.stringify({
        id: user.id,
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        profile_image_url: user.profile_image_url,
        is_seller: user.is_seller
      }));
      window.dispatchEvent(new Event('user-updated'));

      router.push('/dashboard');
    }

  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'เข้าสู่ระบบไม่สำเร็จ กรุณาลองใหม่อีกครั้ง';
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="postcss" scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 0.15;
    transform: scale(1);
  }
  50% {
    opacity: 0.25;
    transform: scale(1.05);
  }
}

.animate-pulse {
  animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>