<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-amber-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <!-- Ambient Background Effects -->
    <div class="fixed top-20 right-0 w-[500px] h-[500px] bg-amber-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 left-0 w-[600px] h-[600px] bg-yellow-900/10 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-[0.02] pointer-events-none"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen flex justify-center py-12">
      <div class="w-full max-w-6xl animate-in-fade">
        
        <!-- Header Section -->
        <header class="mb-10 flex flex-col md:flex-row justify-between items-end gap-6">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 mb-3 backdrop-blur-md">
              <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
              <span class="text-[10px] font-bold text-amber-300 uppercase tracking-widest">Auction Currency</span>
            </div>
            <h1 class="text-4xl md:text-5xl font-extrabold text-white flex items-center gap-3 tracking-tight">
              Token Management
            </h1>
            <p class="text-gray-400 mt-2 max-w-xl font-light">
              เติม Token เพื่อใช้ในการประมูลสินค้าที่คุณต้องการ ยิ่งมีมาก ยิ่งมีโอกาสชนะการประมูลสูง
            </p>
          </div>

          <!-- Balance Card -->
          <div class="relative group w-full md:w-auto">
            <div class="absolute inset-0 bg-gradient-to-r from-amber-500 to-yellow-500 rounded-3xl blur opacity-20 group-hover:opacity-30 transition-opacity duration-500"></div>
            <div class="relative px-8 py-6 rounded-3xl bg-[#121215]/80 backdrop-blur-xl border border-amber-500/30 flex items-center gap-6 min-w-[300px]">
              <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-400 to-yellow-600 flex items-center justify-center shadow-lg shadow-amber-500/20">
                <Coins class="w-8 h-8 text-white" />
              </div>
              <div>
                <p class="text-xs text-amber-200/60 uppercase tracking-wider font-medium mb-1">Current Balance</p>
                <div class="flex items-baseline gap-1">
                  <span class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-yellow-200 to-amber-100 drop-shadow-sm">
                    {{ tokenBalance.toLocaleString() }}
                  </span>
                  <span class="text-amber-500/50 text-sm font-bold">TOKENS</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          <!-- LEFT COLUMN: Actions (QR & Upload) -->
          <div class="lg:col-span-7 space-y-6">
            
            <!-- QR Code Section -->
            <div class="bg-[#121215]/60 backdrop-blur-xl border border-white/5 rounded-[2rem] p-8 relative overflow-hidden group">
              <div class="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                <QrCode class="w-48 h-48 text-white" />
              </div>
              
              <div class="flex flex-col sm:flex-row items-center gap-8 relative z-10">
                <div class="relative">
                  <!-- QR Frame -->
                  <div class="absolute -inset-4 bg-gradient-to-br from-amber-500/20 to-transparent rounded-3xl blur-md"></div>
                  <div class="relative bg-white p-4 rounded-2xl shadow-2xl">
                    <img 
                      src="/promptpay-qr.png" 
                      alt="PromptPay QR Code" 
                      class="w-48 h-48 object-contain"
                      @error="handleQrError"
                    />
                  </div>
                  <!-- Scan Indicator -->
                  <div class="absolute top-0 left-0 w-full h-1 bg-amber-500/50 shadow-[0_0_15px_rgba(245,158,11,0.5)] animate-scan pointer-events-none rounded-t-2xl"></div>
                </div>

                <div class="text-center sm:text-left flex-1">
                  <h2 class="text-2xl font-bold text-white mb-2 flex items-center justify-center sm:justify-start gap-2">
                    <ScanLine class="w-6 h-6 text-amber-400" /> สแกนจ่าย
                  </h2>
                  <div class="space-y-1 text-gray-400">
                    <p class="text-lg text-white font-medium">นาย ศิระณัฐ ศรีบุระ</p>
                    <p class="font-mono text-amber-400/80 tracking-wider text-sm">PromptPay: xxx-xxx-5414</p>
                  </div>
                  <div class="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-bold">
                    <AlertCircle class="w-4 h-4" /> อัตราแลกเปลี่ยน: 1 บาท = 1 Token
                  </div>
                </div>
              </div>
            </div>

            <!-- Upload Section -->
            <div class="bg-[#121215]/60 backdrop-blur-xl border border-white/5 rounded-[2rem] p-8">
              <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <UploadCloud class="w-6 h-6 text-amber-500" /> ยืนยันการโอนเงิน
              </h2>

              <div 
                class="border-2 border-dashed border-white/10 rounded-3xl p-8 text-center cursor-pointer transition-all duration-300 group hover:border-amber-500/40 hover:bg-amber-500/5 relative overflow-hidden"
                :class="{ 'border-amber-500 bg-amber-500/10': isDragging }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
                @click="$refs.fileInput.click()"
              >
                <input 
                  ref="fileInput"
                  type="file" 
                  accept="image/*"
                  class="hidden"
                  @change="handleFileSelect"
                />

                <div class="transition-all duration-300" :class="{ 'opacity-0 scale-95 absolute inset-0': slipPreview }">
                   <div class="w-20 h-20 rounded-full bg-white/5 mx-auto flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 group-hover:bg-amber-500/20">
                     <ImagePlus class="w-10 h-10 text-gray-400 group-hover:text-amber-400 transition-colors" />
                   </div>
                   <p class="text-gray-300 font-medium text-lg">คลิกเพื่ออัปโหลดสลิป</p>
                   <p class="text-gray-500 text-sm mt-1">หรือลากไฟล์มาวางที่นี่ (JPG, PNG)</p>
                </div>

                <!-- Preview State -->
                <div v-if="slipPreview" class="relative z-10">
                  <img :src="slipPreview" class="max-h-64 mx-auto rounded-xl shadow-2xl" />
                  <div class="absolute inset-0 bg-black/50 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-xl">
                    <p class="text-white font-bold flex items-center gap-2"><ArrowUpRight class="w-5 h-5" /> เปลี่ยนรูปภาพ</p>
                  </div>
                  <button @click.stop="clearSlip" class="absolute top-2 right-2 p-2 rounded-full bg-red-500/80 hover:bg-red-500 text-white transition-colors">
                    <X class="w-4 h-4" />
                  </button>
                </div>
              </div>

              <!-- Verify Button -->
              <button 
                @click="verifySlip"
                :disabled="!slipFile || isVerifying"
                class="w-full mt-6 py-4 rounded-xl font-bold text-black text-lg transition-all duration-300 shadow-lg shadow-amber-900/20 transform hover:-translate-y-1 disabled:opacity-50 disabled:translate-y-0 disabled:cursor-not-allowed flex items-center justify-center gap-3 relative overflow-hidden group/btn bg-gradient-to-r from-amber-400 to-yellow-500 hover:from-amber-300 hover:to-yellow-400"
              >
                <div class="absolute inset-0 bg-white/20 translate-y-full group-hover/btn:translate-y-0 transition-transform duration-300"></div>
                
                <span v-if="isVerifying" class="flex items-center gap-2">
                  <Loader2 class="w-6 h-6 animate-spin" /> กำลังตรวจสอบ...
                </span>
                <span v-else class="flex items-center gap-2">
                   <CheckCircle2 class="w-6 h-6" /> ยืนยันการเติมเงิน
                </span>
              </button>

              <!-- Result Message -->
              <div v-if="verifyResult" class="mt-6 rounded-2xl p-4 border" :class="verifyResult.success ? 'bg-green-500/10 border-green-500/20' : 'bg-red-500/10 border-red-500/20'">
                <div class="flex items-start gap-4">
                  <div class="p-2 rounded-full" :class="verifyResult.success ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'">
                    <component :is="verifyResult.success ? CheckCircle2 : AlertTriangle" class="w-6 h-6" />
                  </div>
                  <div>
                    <h4 class="font-bold text-lg" :class="verifyResult.success ? 'text-green-400' : 'text-red-400'">
                      {{ verifyResult.success ? 'ทำรายการสำเร็จ' : 'ทำรายการไม่สำเร็จ' }}
                    </h4>
                    <p class="text-gray-400 text-sm mt-1">{{ verifyResult.msg }}</p>
                    
                    <div v-if="verifyResult.success" class="mt-3 pt-3 border-t border-white/5 grid grid-cols-2 gap-y-1 text-sm">
                      <span class="text-gray-500">ยอดเงิน:</span> <span class="text-white text-right">{{ verifyResult.amount?.toLocaleString() }} บาท</span>
                      <span class="text-gray-500">Token ที่ได้รับ:</span> <span class="text-amber-400 font-bold text-right">+{{ verifyResult.new_balance?.toLocaleString() }}</span>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- RIGHT COLUMN: History -->
          <div class="lg:col-span-5">
            <div class="bg-[#121215]/60 backdrop-blur-xl border border-white/5 rounded-[2rem] p-8 h-full">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-bold text-white flex items-center gap-2">
                  <History class="w-6 h-6 text-gray-400" /> ประวัติล่าสุด
                </h2>
                <button class="text-xs text-amber-500 hover:text-amber-400 transition-colors">ดูทั้งหมด</button>
              </div>

              <div class="space-y-4 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
                <div v-if="requests.length === 0" class="flex flex-col items-center justify-center py-20 text-gray-500">
                  <ScrollText class="w-16 h-16 mb-4 opacity-20" />
                  <p>ยังไม่มีประวัติการทำรายการ</p>
                </div>

                <div 
                  v-for="req in requests" 
                  :key="req.id"
                  class="group relative bg-white/5 hover:bg-white/10 border border-white/5 rounded-2xl p-4 transition-all duration-300 hover:border-amber-500/30"
                > 
                  <div class="flex justify-between items-start">
                    <div class="flex items-start gap-4">
                      <div class="p-3 rounded-xl" :class="getStatusIconBg(req.status)">
                        <component :is="getStatusIcon(req.status)" class="w-5 h-5" :class="getStatusColor(req.status)" />
                      </div>
                      <div>
                        <p class="text-white font-bold text-lg leading-none mb-1">+{{ req.amount.toLocaleString() }}</p>
                        <p class="text-xs text-gray-500 font-mono">{{ formatDate(req.created_at) }}</p>
                      </div>
                    </div>
                    
                    <span class="px-3 py-1 rounded-full text-[10px] font-bold border uppercase tracking-wider" :class="getStatusBadgeClass(req.status)">
                      {{ req.status }}
                    </span>
                  </div>

                  <!-- Details Slide Down -->
                  <div v-if="req.payment_proof_url" class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between">
                     <span class="text-xs text-gray-500">หลักฐานการโอน</span>
                     <button @click="showSlipModal(req.payment_proof_url)" class="text-xs text-amber-500 hover:text-amber-300 flex items-center gap-1">
                       ดูรูปภาพ <ArrowUpRight class="w-3 h-3" />
                     </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Slip Modal -->
    <Transition name="fade">
      <div v-if="slipModalUrl" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click="slipModalUrl = null">
        <div class="absolute inset-0 bg-black/90 backdrop-blur-md"></div>
        <div class="relative max-w-lg w-full bg-[#18181b] rounded-3xl p-2 border border-white/10 shadow-2xl scale-100 animate-in-pop" @click.stop>
          <img :src="`http://localhost:5000${slipModalUrl}`" alt="Slip" class="w-full rounded-2xl" />
          <button @click="slipModalUrl = null" class="absolute top-4 right-4 bg-black/50 text-white rounded-full p-2 hover:bg-black/70 transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { 
  Coins, QrCode, UploadCloud, History, CheckCircle2, XCircle, Clock, 
  ArrowUpRight, ImagePlus, Loader2, X, AlertCircle, ScanLine, AlertTriangle, ScrollText
} from 'lucide-vue-next';

const tokenBalance = ref(0);
const requests = ref([]);
const isVerifying = ref(false);
const slipFile = ref(null);
const slipPreview = ref(null);
const isDragging = ref(false);
const verifyResult = ref(null);
const slipModalUrl = ref(null);
const baseUrl = 'http://localhost:5000';

const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
    approved: 'bg-green-500/10 text-green-500 border-green-500/20',
    rejected: 'bg-red-500/10 text-red-500 border-red-500/20'
  };
  return classes[status] || 'bg-gray-500/10 text-gray-500';
};

const getStatusColor = (status) => {
  return {
    pending: 'text-yellow-500',
    approved: 'text-green-500',
    rejected: 'text-red-500'
  }[status] || 'text-gray-500';
};

const getStatusIconBg = (status) => {
  return {
    pending: 'bg-yellow-500/10',
    approved: 'bg-green-500/10',
    rejected: 'bg-red-500/10'
  }[status] || 'bg-gray-500/10';
};

const getStatusIcon = (status) => {
  return {
    pending: Clock,
    approved: CheckCircle2,
    rejected: XCircle
  }[status] || AlertCircle;
};

function formatDate(dateStr) {
  if(!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('th-TH', {
    day: 'numeric', month: 'short',
    hour: '2-digit', minute: '2-digit'
  });
}

function handleQrError(e) {
  e.target.src = 'https://via.placeholder.com/256x256?text=QR+Code';
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) processFile(file);
}

function handleDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) processFile(file);
}

function processFile(file) {
  slipFile.value = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    slipPreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
  verifyResult.value = null;
}

function clearSlip() {
  slipFile.value = null;
  slipPreview.value = null;
  verifyResult.value = null;
}

async function verifySlip() {
  const token = localStorage.getItem('token');
  if (!token) return alert('กรุณาเข้าสู่ระบบก่อน');
  if (!slipFile.value) return alert('กรุณาเลือกไฟล์สลิป');
  
  isVerifying.value = true;
  verifyResult.value = null;
  
  try {
    const formData = new FormData();
    formData.append('slip', slipFile.value);
    
    const res = await axios.post(`${baseUrl}/api/token/verify-slip`, formData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    
    verifyResult.value = res.data;
    
    if (res.data.success) {
      fetchTokenBalance();
      fetchRequests();
      setTimeout(clearSlip, 5000);
    }
  } catch (err) {
    verifyResult.value = {
      success: false,
      msg: err.response?.data?.msg || 'เกิดข้อผิดพลาดในการตรวจสอบสลิป'
    };
  } finally {
    isVerifying.value = false;
  }
}

function showSlipModal(url) {
  slipModalUrl.value = url;
}

async function fetchTokenBalance() {
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    const res = await axios.get(`${baseUrl}/api/token/balance`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    tokenBalance.value = res.data.token_balance || 0;
  } catch (err) { console.error(err); }
}

async function fetchRequests() {
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    const res = await axios.get(`${baseUrl}/api/token/my-requests`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    requests.value = res.data.requests || [];
  } catch (err) { console.error(err); }
}

onMounted(() => {
  fetchTokenBalance();
  fetchRequests();
});
</script>

<style scoped>
.animate-in-fade {
  animation: fadeIn 0.8s ease-out forwards;
}

.animate-in-pop {
  animation: popIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes popIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes scan {
  0% { top: 0; opacity: 1; }
  50% { top: 100%; opacity: 1; }
  51% { top: 100%; opacity: 0; }
  52% { top: 0; opacity: 0; }
  53% { top: 0; opacity: 1; }
  100% { top: 0; opacity: 1; }
}

.animate-scan {
  animation: scan 3s linear infinite;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(245, 158, 11, 0.2);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(245, 158, 11, 0.4);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>