<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-amber-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-20 right-0 w-[500px] h-[500px] bg-amber-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 left-0 w-[600px] h-[600px] bg-yellow-900/10 blur-[120px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen flex justify-center">
      <div class="w-full max-w-6xl animate-in-fade">
        
        <header class="mb-10">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 mb-3">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
            <span class="text-[10px] font-bold text-amber-300 uppercase tracking-widest">Auction Currency</span>
          </div>
          <h1 class="text-4xl font-extrabold text-white flex items-center gap-3">
            🪙 Token Management
          </h1>
          <p class="text-gray-400 mt-2 max-w-xl">
            เติม Token เพื่อใช้ในการประมูลสินค้าที่คุณต้องการ ยิ่งมีมาก ยิ่งมีโอกาสชนะการประมูลสูง
          </p>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          <div class="lg:col-span-7 space-y-6">
            
            <div class="relative overflow-hidden rounded-[2rem] bg-gradient-to-br from-[#1e1e24] to-[#121215] border border-amber-500/20 p-8 shadow-2xl group">
              <div class="absolute top-0 right-0 w-32 h-32 bg-amber-500/20 blur-[50px] rounded-full group-hover:bg-amber-500/30 transition-all duration-500"></div>
              
              <div class="relative z-10 flex items-center justify-between">
                <div>
                  <p class="text-amber-500/80 font-bold text-sm uppercase tracking-wider mb-2">My Balance</p>
                  <div class="flex items-baseline gap-2">
                    <span class="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-amber-100 to-amber-400 tracking-tighter">
                      {{ tokenBalance.toLocaleString() }}
                    </span>
                    <span class="text-xl text-gray-500 font-medium">Tokens</span>
                  </div>
                </div>
                <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-amber-500/20 to-transparent border border-amber-500/30 flex items-center justify-center text-4xl shadow-[0_0_30px_rgba(245,158,11,0.2)]">
                  🪙
                </div>
              </div>
            </div>

            <div class="bg-[#121215]/60 backdrop-blur-xl border border-white/5 rounded-[2rem] p-8 shadow-lg">
              <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                📝 ส่งคำขอเติม Token
              </h2>
              
              <div class="space-y-6">
                <div>
                  <label class="block text-gray-400 text-sm font-semibold mb-2 ml-1">จำนวน Token ที่ต้องการ</label>
                  <div class="relative">
                    <input 
                      v-model.number="requestAmount" 
                      type="number" 
                      min="1"
                      class="w-full bg-[#0b0b0f] border border-white/10 rounded-2xl py-4 pl-5 pr-4 text-2xl font-bold text-white placeholder-gray-700 focus:outline-none focus:border-amber-500/50 focus:ring-1 focus:ring-amber-500/20 transition-all"
                      placeholder="0"
                    />
                    <div class="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-2 pointer-events-none opacity-50">
                      <span class="text-xs text-gray-500">TOKENS</span>
                    </div>
                  </div>
                </div>

                <div class="grid grid-cols-4 gap-3">
                  <button 
                    v-for="amount in [100, 500, 1000, 5000]" 
                    :key="amount"
                    @click="requestAmount = amount"
                    class="py-2.5 rounded-xl text-sm font-bold transition-all border"
                    :class="requestAmount === amount 
                      ? 'bg-amber-500 text-black border-amber-500 shadow-lg shadow-amber-500/20' 
                      : 'bg-transparent text-gray-400 border-white/10 hover:bg-white/5 hover:border-white/20'"
                  >
                    +{{ amount.toLocaleString() }}
                  </button>
                </div>

                <div class="bg-white/5 rounded-2xl p-5 border border-white/5 flex items-center justify-between">
                  <div>
                    <span class="text-gray-400 text-sm block">ราคาที่ต้องชำระ</span>
                    <span class="text-[10px] text-gray-600">*อัตราแลกเปลี่ยน 1:1</span>
                  </div>
                  <div class="text-right">
                    <span class="text-2xl font-bold text-green-400">฿{{ requestAmount?.toLocaleString() || 0 }}</span>
                    <span class="text-gray-500 text-xs ml-1">THB</span>
                  </div>
                </div>

                <button 
                  @click="submitRequest"
                  :disabled="!requestAmount || requestAmount < 1 || isLoading"
                  class="w-full py-4 rounded-2xl font-bold text-lg shadow-lg shadow-amber-900/20 transition-all duration-300 relative overflow-hidden group"
                  :class="isLoading || !requestAmount 
                    ? 'bg-gray-800 text-gray-500 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-amber-500 to-yellow-600 text-black hover:scale-[1.02] active:scale-95'"
                >
                  <span class="relative z-10 flex items-center justify-center gap-2">
                    {{ isLoading ? '⏳ กำลังประมวลผล...' : '📤 ยืนยันคำขอเติม Token' }}
                  </span>
                  <div v-if="!isLoading" class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                </button>
                
                <p class="text-gray-500 text-xs text-center mt-2">
                  * หลังส่งคำขอ Admin จะตรวจสอบและอนุมัติภายใน 24 ชม.
                </p>
              </div>
            </div>
          </div>

          <div class="lg:col-span-5 h-full">
            <div class="bg-[#121215]/60 backdrop-blur-xl border border-white/5 rounded-[2rem] p-6 shadow-lg h-full flex flex-col">
              <div class="flex items-center justify-between mb-6 px-2">
                <h2 class="text-xl font-bold text-white flex items-center gap-2">
                  📜 ประวัติคำขอ
                </h2>
                <span class="text-xs text-gray-500 bg-white/5 px-2 py-1 rounded-md">{{ requests.length }} รายการ</span>
              </div>
              
              <div class="flex-1 overflow-y-auto custom-scrollbar pr-2 space-y-3 max-h-[600px]">
                <div 
                  v-for="req in requests" 
                  :key="req.id"
                  class="group p-4 rounded-2xl border transition-all hover:bg-white/5 relative overflow-hidden"
                  :class="getStatusBorderColor(req.status)"
                >
                  <div class="flex justify-between items-start mb-2 relative z-10">
                    <div>
                      <span class="block text-lg font-bold text-white tracking-wide">
                        {{ req.amount.toLocaleString() }} <span class="text-xs font-normal text-gray-500">Token</span>
                      </span>
                      <span class="text-[10px] text-gray-500 font-mono">{{ formatDate(req.created_at) }}</span>
                    </div>
                    <span 
                      class="px-3 py-1 rounded-full text-xs font-bold border backdrop-blur-md"
                      :class="getStatusBadgeClass(req.status)"
                    >
                      {{ statusLabels[req.status] }}
                    </span>
                  </div>

                  <div v-if="req.admin_note" class="mt-3 pt-3 border-t border-white/5 flex gap-2 items-start">
                    <span class="text-xs">💬</span>
                    <p class="text-xs text-gray-400 italic leading-relaxed">"{{ req.admin_note }}"</p>
                  </div>

                  <div class="absolute -right-4 -top-4 w-20 h-20 blur-[40px] rounded-full opacity-20 pointer-events-none" :class="getStatusGlowColor(req.status)"></div>
                </div>

                <div v-if="!requests.length" class="h-64 flex flex-col items-center justify-center text-center opacity-50">
                  <div class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center text-2xl mb-3 grayscale">📋</div>
                  <p class="text-gray-400 text-sm">ยังไม่มีประวัติการทำรายการ</p>
                </div>
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
import axios from 'axios';

const tokenBalance = ref(0);
const requestAmount = ref(100);
const requests = ref([]);
const isLoading = ref(false);

const baseUrl = 'http://localhost:5000';

const statusLabels = {
  pending: 'รอตรวจสอบ',
  approved: 'สำเร็จ',
  rejected: 'ปฏิเสธ'
};

// CSS Classes Helpers
const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    approved: 'bg-green-500/10 text-green-400 border-green-500/20',
    rejected: 'bg-red-500/10 text-red-400 border-red-500/20'
  };
  return classes[status] || 'bg-gray-500/10 text-gray-400';
};

const getStatusBorderColor = (status) => {
  const classes = {
    pending: 'bg-white/5 border-white/5 hover:border-yellow-500/30',
    approved: 'bg-[#0f1812]/50 border-green-900/30 hover:border-green-500/30',
    rejected: 'bg-[#180f0f]/50 border-red-900/30 hover:border-red-500/30'
  };
  return classes[status] || 'border-white/5';
};

const getStatusGlowColor = (status) => {
  const classes = {
    pending: 'bg-yellow-500',
    approved: 'bg-green-500',
    rejected: 'bg-red-500'
  };
  return classes[status] || 'bg-gray-500';
};

function formatDate(dateStr) {
  if(!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('th-TH', {
    year: '2-digit', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

async function fetchTokenBalance() {
  const token = localStorage.getItem('token');
  if (!token) return;
  
  try {
    const res = await axios.get(`${baseUrl}/api/token/balance`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    tokenBalance.value = res.data.token_balance || 0;
  } catch (err) {
    console.error('Failed to fetch token balance:', err);
  }
}

async function fetchRequests() {
  const token = localStorage.getItem('token');
  if (!token) return;
  
  try {
    const res = await axios.get(`${baseUrl}/api/token/my-requests`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    requests.value = res.data.requests || [];
  } catch (err) {
    console.error('Failed to fetch requests:', err);
  }
}

async function submitRequest() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    return;
  }
  
  if (!requestAmount.value || requestAmount.value < 1) {
    alert('กรุณาระบุจำนวน Token');
    return;
  }
  
  isLoading.value = true;
  try {
    await axios.post(`${baseUrl}/api/token/request`, {
      amount: requestAmount.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    // Reset form & Refresh data
    requestAmount.value = 100;
    await fetchRequests();
    
    // Optional: Alert or Toast
    alert('🎉 ส่งคำขอเรียบร้อยแล้ว');
  } catch (err) {
    alert(err.response?.data?.msg || 'ส่งคำขอไม่สำเร็จ');
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  fetchTokenBalance();
  fetchRequests();
});
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

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>