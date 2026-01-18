<template>
  <div class="relative min-h-full">
    <div class="mb-8 animate-in-fade">
      <h1 class="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
        <span class="p-2 rounded-lg bg-yellow-500/10 text-yellow-500 text-2xl">💳</span>
        Top-up Balance
      </h1>
      <p class="text-gray-400 mt-2 ml-1">เติม Coin เพื่อซื้อสินค้าและบริการ (อัตราแลกเปลี่ยน 1 THB = 1 Coin)</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start animate-in-fade delay-100">
      
      <div class="lg:col-span-5 space-y-6">
        <div class="relative overflow-hidden rounded-[2rem] border border-white/10 bg-[#18181b]/60 backdrop-blur-xl p-8 group">
          <div class="absolute top-0 right-0 -mr-10 -mt-10 w-48 h-48 bg-yellow-500/10 blur-[80px] rounded-full group-hover:bg-yellow-500/20 transition-all duration-700"></div>
          
          <div class="relative z-10">
            <h3 class="text-gray-400 font-medium text-sm uppercase tracking-wider mb-1">Current Balance</h3>
            <div class="flex items-baseline gap-3 mt-2">
              <span class="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-yellow-100 to-yellow-500 tracking-tight drop-shadow-lg">
                {{ userStore.coinBalance?.toLocaleString() || '0' }}
              </span>
              <span class="text-lg font-bold text-yellow-500/80">Coins</span>
            </div>
            
            <div class="mt-8 pt-6 border-t border-white/5 grid grid-cols-2 gap-4">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-green-500/10 flex items-center justify-center text-green-500 text-sm">⚡</div>
                <div>
                  <div class="text-white text-sm font-bold">Instant</div>
                  <div class="text-gray-500 text-xs">เข้าทันที</div>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-500 text-sm">🛡️</div>
                <div>
                  <div class="text-white text-sm font-bold">Secure</div>
                  <div class="text-gray-500 text-xs">ปลอดภัย 100%</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="p-6 rounded-[2rem] bg-white/5 border border-white/5">
          <h4 class="text-white font-bold mb-3 flex items-center gap-2">
            ℹ️ เงื่อนไขการเติมเงิน
          </h4>
          <ul class="space-y-3 text-sm text-gray-400">
            <li class="flex items-start gap-2">
              <span class="text-yellow-500 mt-1">•</span>
              รองรับการโอนผ่าน Mobile Banking ทุกธนาคาร
            </li>
            <li class="flex items-start gap-2">
              <span class="text-yellow-500 mt-1">•</span>
              ระบบตรวจสอบยอดอัตโนมัติภายใน 1-2 นาที
            </li>
            <li class="flex items-start gap-2">
              <span class="text-yellow-500 mt-1">•</span>
              หากยอดไม่เข้าเกิน 5 นาที กรุณาติดต่อ Admin
            </li>
          </ul>
        </div>
      </div>

      <div class="lg:col-span-7">
        <div class="bg-[#18181b]/80 backdrop-blur-xl border border-white/10 p-8 md:p-10 rounded-[2.5rem] shadow-2xl relative overflow-hidden">
          
          <div class="mb-8">
            <label class="block text-gray-400 text-sm font-bold mb-3 ml-1">ระบุจำนวนเงิน (THB)</label>
            <div class="relative group">
              <input
                type="text"
                :value="amount"
                @input="handleInput"
                class="w-full bg-[#0b0b0f] border-2 border-white/10 rounded-2xl py-6 pl-8 pr-20 text-4xl font-black text-white placeholder-gray-700 focus:outline-none focus:border-yellow-500 transition-all shadow-inner"
                placeholder="0"
                inputmode="numeric"
              />
              <span class="absolute right-8 top-1/2 -translate-y-1/2 text-gray-500 font-bold text-xl select-none">THB</span>
            </div>
          </div>

          <div class="grid grid-cols-3 sm:grid-cols-3 gap-4 mb-8">
            <button 
              v-for="val in [100, 300, 500, 1000, 3000, 5000]" 
              :key="val"
              @click="amount = val"
              class="relative overflow-hidden py-3 rounded-xl border transition-all duration-300 group"
              :class="amount === val 
                ? 'bg-yellow-500 border-yellow-500 text-black font-bold shadow-[0_0_20px_rgba(234,179,8,0.3)] scale-[1.02]' 
                : 'bg-white/5 border-white/5 text-gray-400 hover:bg-white/10 hover:border-white/20'"
            >
              <span class="relative z-10">฿{{ val.toLocaleString() }}</span>
            </button>
          </div>

          <Transition name="fade">
            <div v-if="error" class="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center gap-3 text-red-400 text-sm">
              <span class="text-lg">⚠️</span> {{ error }}
            </div>
          </Transition>

          <button
            @click="createTopup"
            :disabled="loading || !amount || amount < 1"
            class="w-full py-5 rounded-2xl font-bold text-xl shadow-xl transition-all duration-300 relative overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            :class="!loading && amount >= 1 ? 'bg-gradient-to-r from-yellow-400 to-yellow-600 text-black hover:scale-[1.01] hover:shadow-yellow-500/20' : 'bg-gray-700 text-gray-400'"
          >
            <div class="relative z-10 flex items-center justify-center gap-3">
              <span v-if="loading" class="w-6 h-6 border-2 border-current border-t-transparent rounded-full animate-spin"></span>
              <span>{{ loading ? 'กำลังสร้าง QR Code...' : 'สร้าง QR Code ชำระเงิน' }}</span>
              <span v-if="!loading" class="group-hover:translate-x-1 transition-transform">➔</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700 ease-in-out"></div>
          </button>

          <Transition name="expand">
            <div v-if="qrData" class="mt-8 pt-8 border-t border-white/10">
              <div class="text-center">
                <p class="text-gray-400 mb-6 font-medium">สแกน QR Code ด้านล่างเพื่อชำระเงิน</p>
                
                <div class="relative inline-block group cursor-pointer">
                  <div class="absolute -inset-4 bg-yellow-500/20 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  
                  <div class="relative p-4 bg-white rounded-3xl shadow-2xl overflow-hidden">
                    <img :src="qrData.qr_url" alt="Topup QR" class="w-64 h-64 object-contain mix-blend-multiply" />
                    
                    <div class="absolute top-4 left-4 w-6 h-6 border-l-4 border-t-4 border-black/80 rounded-tl-lg"></div>
                    <div class="absolute top-4 right-4 w-6 h-6 border-r-4 border-t-4 border-black/80 rounded-tr-lg"></div>
                    <div class="absolute bottom-4 left-4 w-6 h-6 border-l-4 border-b-4 border-black/80 rounded-bl-lg"></div>
                    <div class="absolute bottom-4 right-4 w-6 h-6 border-r-4 border-b-4 border-black/80 rounded-br-lg"></div>
                  </div>
                </div>

                <div class="mt-6 flex flex-col items-center gap-2">
                  <div class="inline-flex items-center gap-2 bg-yellow-500/10 px-6 py-2 rounded-full border border-yellow-500/20">
                    <span class="text-gray-400 text-sm">ยอดชำระ:</span>
                    <span class="text-2xl font-black text-yellow-500">{{ qrData.amount?.toLocaleString() }}</span>
                    <span class="text-gray-400 text-xs font-bold">THB</span>
                  </div>
                  <p class="text-xs text-gray-600 mt-2">Ref: {{ qrData.ref_no || 'Unknown' }}</p>
                </div>
              </div>
            </div>
          </Transition>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/user";

// เรียกใช้ Layout Admin เพื่อให้มี Sidebar และ Background หลัก
definePageMeta({
  layout: 'admin'
});

const userStore = useUserStore();

const amount = ref(''); 
const loading = ref(false);
const error = ref(null);
const qrData = ref(null);

// Validate Input ให้พิมพ์ได้แค่ตัวเลข
const handleInput = (e) => {
  const val = e.target.value.replace(/[^0-9]/g, '');
  amount.value = val ? parseInt(val) : '';
};

const createTopup = async () => {
  if (!amount.value || amount.value < 1) return;

  loading.value = true;
  error.value = null;
  qrData.value = null;

  try {
    const res = await userStore.topupCoin(amount.value);
    
    // Simulate slight delay for better UX
    await new Promise(resolve => setTimeout(resolve, 600));

    qrData.value = res;
    
    // Optional: Scroll to QR section
    setTimeout(() => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }, 100);

  } catch (err) {
    console.error(err);
    error.value = err.response?.data?.message || "เกิดข้อผิดพลาดในการเชื่อมต่อ";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Fade In Animation */
.animate-in-fade {
  animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(10px);
}
.delay-100 {
  animation-delay: 0.1s;
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Smooth Expand */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 800px;
  opacity: 1;
}
.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-20px);
}

/* Fade util */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>