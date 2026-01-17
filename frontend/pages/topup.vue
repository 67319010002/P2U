<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-yellow-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-yellow-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[500px] h-[500px] bg-amber-900/10 blur-[120px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen flex items-center justify-center">
      
      <div class="w-full max-w-5xl grid grid-cols-1 md:grid-cols-2 gap-8 items-start animate-in-fade">
        
        <div class="space-y-6">
          <div class="bg-gradient-to-br from-[#1e1e24] to-[#121215] border border-white/5 p-8 rounded-[2.5rem] relative overflow-hidden shadow-2xl group">
            <div class="absolute top-0 right-0 w-40 h-40 bg-yellow-500/20 blur-[60px] rounded-full group-hover:bg-yellow-500/30 transition-all duration-500"></div>
            
            <h2 class="text-gray-400 font-medium mb-1 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-yellow-500 animate-pulse"></span>
              Current Balance
            </h2>
            <div class="flex items-baseline gap-2 mt-4">
              <span class="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-200 via-yellow-400 to-amber-600 tracking-tight">
                {{ userStore.coinBalance?.toLocaleString() || '0' }}
              </span>
              <span class="text-xl text-yellow-500/80 font-bold">Coins</span>
            </div>
            
            <p class="text-gray-500 text-sm mt-6 leading-relaxed max-w-sm">
              เหรียญของคุณสามารถใช้แลกซื้อสินค้าพิเศษ และเข้าร่วมกิจกรรมต่างๆ ได้ทันที เติมเงินง่าย ปลอดภัย รวดเร็ว
            </p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="p-4 rounded-2xl bg-white/5 border border-white/5 flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-yellow-500/10 flex items-center justify-center text-xl">⚡</div>
              <div class="text-sm">
                <p class="text-white font-bold">Instant</p>
                <p class="text-gray-500 text-xs">เข้าทันที</p>
              </div>
            </div>
            <div class="p-4 rounded-2xl bg-white/5 border border-white/5 flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-yellow-500/10 flex items-center justify-center text-xl">🔒</div>
              <div class="text-sm">
                <p class="text-white font-bold">Secure</p>
                <p class="text-gray-500 text-xs">ปลอดภัย 100%</p>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-[#121215]/60 backdrop-blur-xl border border-white/10 p-8 rounded-[2.5rem] shadow-2xl relative">
          <h1 class="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            💰 เติมเงิน (Top-up)
          </h1>

          <div class="space-y-6">
            <div>
              <label class="block text-gray-400 text-sm font-semibold mb-2 ml-1">จำนวนเงินที่ต้องการ (THB)</label>
              <div class="relative group">
                <input
                  type="number"
                  v-model.number="amount"
                  min="1"
                  class="w-full bg-[#0b0b0f] border border-white/10 rounded-2xl py-4 pl-5 pr-16 text-2xl font-bold text-white placeholder-gray-700 focus:outline-none focus:border-yellow-500/50 focus:ring-1 focus:ring-yellow-500/20 transition-all"
                  placeholder="0.00"
                  @keypress="isNumber($event)"
                />
                <span class="absolute right-6 top-1/2 -translate-y-1/2 text-gray-500 font-bold">THB</span>
              </div>
            </div>

            <div class="grid grid-cols-3 gap-3">
              <button 
                v-for="val in [100, 300, 500, 1000, 2000, 5000]" 
                :key="val"
                @click="amount = val"
                class="py-2 rounded-xl border border-white/5 text-sm font-medium transition-all hover:bg-white/5 active:scale-95"
                :class="amount === val ? 'bg-yellow-500 text-black font-bold border-yellow-500' : 'text-gray-400 bg-transparent'"
              >
                ฿{{ val.toLocaleString() }}
              </button>
            </div>

            <div v-if="error" class="p-3 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center gap-2 text-red-400 text-sm animate-pulse">
              <span>⚠️</span> {{ error }}
            </div>

            <button
              @click="createTopup"
              :disabled="loading || amount < 1"
              class="w-full py-4 rounded-2xl font-bold text-lg shadow-lg shadow-yellow-500/20 transition-all duration-300 relative overflow-hidden group"
              :class="loading || amount < 1 ? 'bg-gray-700 text-gray-500 cursor-not-allowed' : 'bg-gradient-to-r from-yellow-400 to-amber-600 text-black hover:scale-[1.02] active:scale-95'"
            >
              <span class="relative z-10 flex items-center justify-center gap-2">
                <span v-if="loading" class="animate-spin">⏳</span>
                {{ loading ? 'กำลังสร้าง QR Code...' : '💳 สร้าง QR Code ชำระเงิน' }}
              </span>
              <div v-if="!loading && amount >= 1" class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
            </button>
          </div>

          <Transition name="expand">
            <div v-if="qrData" class="mt-8 pt-8 border-t border-white/10 flex flex-col items-center text-center overflow-hidden">
              <p class="text-gray-400 mb-4 text-sm">สแกน QR Code ด้านล่างเพื่อชำระเงิน</p>
              
              <div class="p-4 bg-white rounded-3xl shadow-[0_0_40px_-10px_rgba(251,191,36,0.3)] mx-auto mb-4 relative group cursor-pointer hover:scale-105 transition-transform duration-300">
                <img :src="qrData.qr_url" alt="Topup QR" class="w-56 h-56 object-contain" />
                
                <div class="absolute top-2 left-2 w-4 h-4 border-l-2 border-t-2 border-black"></div>
                <div class="absolute top-2 right-2 w-4 h-4 border-r-2 border-t-2 border-black"></div>
                <div class="absolute bottom-2 left-2 w-4 h-4 border-l-2 border-b-2 border-black"></div>
                <div class="absolute bottom-2 right-2 w-4 h-4 border-r-2 border-b-2 border-black"></div>
              </div>

              <div class="bg-white/5 px-6 py-2 rounded-full border border-white/10">
                <span class="text-gray-400 text-sm mr-2">ยอดชำระ:</span>
                <span class="text-2xl font-bold text-yellow-400">{{ qrData.amount?.toLocaleString() }}</span>
                <span class="text-gray-400 text-sm ml-1">THB</span>
              </div>
              
              <p class="text-xs text-gray-500 mt-4">
                *ระบบจะเติม Coin ให้ท่านอัตโนมัติภายใน 1-2 นาทีหลังชำระเงิน
              </p>
            </div>
          </Transition>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();

const amount = ref(''); // เปลี่ยนเป็น string ว่างเริ่มต้นเพื่อให้ placeholder ทำงาน
const loading = ref(false);
const error = ref(null);
const qrData = ref(null);

// ป้องกันการพิมพ์ตัวอักษร
const isNumber = (evt) => {
  evt = (evt) ? evt : window.event;
  var charCode = (evt.which) ? evt.which : evt.keyCode;
  if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
    evt.preventDefault();
  } else {
    return true;
  }
};

const createTopup = async () => {
  if (!amount.value || amount.value < 1) return;

  loading.value = true;
  error.value = null;
  qrData.value = null; // Reset QR เก่า

  try {
    const res = await userStore.topupCoin(amount.value);
    
    // จำลอง Delay นิดหน่อยให้ดูเหมือนกำลังประมวลผล (ถ้า API ตอบกลับเร็วเกินไป)
    await new Promise(resolve => setTimeout(resolve, 800));

    qrData.value = res;
    
    // Optional: สั่งโหลด User ใหม่ (ถ้า backend อัปเดตทันที หรือใช้ websocket)
    // userStore.loadUser(); 
  } catch (err) {
    console.error(err);
    error.value = err.response?.data?.msg || "เกิดข้อผิดพลาดในการเชื่อมต่อ กรุณาลองใหม่";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Animations */
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* Expand Animation for QR */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 500px;
  opacity: 1;
}
.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}
</style>