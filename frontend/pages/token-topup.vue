<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />

    <div class="max-w-5xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-white flex items-center gap-3">
            🪙 เติม Token
          </h1>
          <p class="text-dark-400 mt-1">เติม Token เพื่อใช้ในการประมูลสินค้า</p>
        </div>
      </div>

      <!-- Token Balance Card -->
      <div class="card p-6 mb-8">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-dark-400 text-sm">Token คงเหลือ</p>
            <p class="text-4xl font-bold text-primary-400 mt-1">{{ tokenBalance.toLocaleString() }}</p>
          </div>
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-3xl">
            🪙
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- QR Code & Upload Section -->
        <div class="space-y-6">
          <!-- PromptPay QR Code -->
          <div class="card p-6">
            <h2 class="text-xl font-semibold text-white mb-4">📱 สแกน QR Code เพื่อชำระเงิน</h2>
            <div class="bg-white rounded-2xl p-4 mx-auto w-fit">
              <img 
                src="/promptpay-qr.png" 
                alt="PromptPay QR Code" 
                class="w-64 h-64 object-contain"
                @error="handleQrError"
              />
            </div>
            <div class="mt-4 text-center">
              <p class="text-white font-semibold">นาย ศิระณัฐ ศรีบุระ</p>
              <p class="text-dark-400 text-sm">พร้อมเพย์: xxx-xxx-5414</p>
              <p class="text-dark-500 text-xs mt-2">💡 อัตรา 1 Token = 1 บาท</p>
            </div>
          </div>

          <!-- Slip Upload -->
          <div class="card p-6">
            <h2 class="text-xl font-semibold text-white mb-4">📤 อัปโหลดสลิปการโอนเงิน</h2>
            
            <!-- Drag & Drop Zone -->
            <div 
              class="border-2 border-dashed border-dark-600 rounded-2xl p-8 text-center cursor-pointer transition-all hover:border-primary-500 hover:bg-dark-800/50"
              :class="{ 'border-primary-500 bg-primary-500/10': isDragging }"
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
              
              <div v-if="!slipPreview">
                <div class="text-5xl mb-3">📎</div>
                <p class="text-dark-300 font-medium">ลากไฟล์มาวางที่นี่</p>
                <p class="text-dark-500 text-sm mt-1">หรือคลิกเพื่อเลือกไฟล์</p>
                <p class="text-dark-600 text-xs mt-2">รองรับ: JPG, PNG, WEBP</p>
              </div>
              
              <div v-else class="relative">
                <img :src="slipPreview" alt="Slip Preview" class="max-h-64 mx-auto rounded-xl" />
                <button 
                  @click.stop="clearSlip"
                  class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600"
                >
                  ✕
                </button>
              </div>
            </div>

            <!-- Verify Button -->
            <button 
              @click="verifySlip"
              :disabled="!slipFile || isVerifying"
              class="btn-primary w-full py-4 text-lg font-bold mt-4 disabled:opacity-50"
            >
              <span v-if="isVerifying" class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                กำลังตรวจสอบสลิป...
              </span>
              <span v-else>🔍 ตรวจสอบสลิปและเติม Token</span>
            </button>

            <!-- Verification Result -->
            <div v-if="verifyResult" class="mt-4 rounded-xl p-4" :class="verifyResult.success ? 'bg-green-500/20' : 'bg-red-500/20'">
              <div class="flex items-start gap-3">
                <span class="text-2xl">{{ verifyResult.success ? '✅' : '❌' }}</span>
                <div>
                  <p class="font-bold" :class="verifyResult.success ? 'text-green-400' : 'text-red-400'">
                    {{ verifyResult.msg }}
                  </p>
                  <div v-if="verifyResult.success" class="text-dark-300 text-sm mt-2">
                    <p>💰 ยอดเงิน: {{ verifyResult.amount?.toLocaleString() }} บาท</p>
                    <p>🧾 เลขอ้างอิง: {{ verifyResult.transaction_ref }}</p>
                    <p>👤 ผู้โอน: {{ verifyResult.sender_name }}</p>
                    <p class="text-primary-400 font-bold mt-2">Token ใหม่: {{ verifyResult.new_balance?.toLocaleString() }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: History -->
        <div class="card p-6">
          <h2 class="text-xl font-semibold text-white mb-6">📜 ประวัติการเติม Token</h2>
          
          <div v-if="requests.length" class="space-y-3 max-h-[600px] overflow-y-auto pr-2">
            <div 
              v-for="req in requests" 
              :key="req.id"
              class="glass-light rounded-xl p-4"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="text-white font-bold">{{ req.amount.toLocaleString() }} Token</span>
                <span 
                  class="badge"
                  :class="{
                    'badge-warning': req.status === 'pending',
                    'badge-success': req.status === 'approved',
                    'badge-error': req.status === 'rejected'
                  }"
                >
                  {{ statusLabels[req.status] }}
                </span>
              </div>
              <p class="text-dark-500 text-xs">{{ req.created_at }}</p>
              
              <!-- Show slip preview if available -->
              <div v-if="req.payment_proof_url" class="mt-2">
                <img 
                  :src="`http://localhost:5000${req.payment_proof_url}`" 
                  alt="Slip" 
                  class="h-20 rounded-lg cursor-pointer hover:opacity-80"
                  @click="showSlipModal(req.payment_proof_url)"
                />
              </div>
              
              <!-- Auto-approved badge -->
              <span v-if="req.is_auto_approved" class="inline-block mt-2 text-xs bg-blue-500/20 text-blue-400 px-2 py-1 rounded-full">
                ⚡ อนุมัติอัตโนมัติ
              </span>
              
              <p v-if="req.admin_note" class="text-dark-400 text-sm mt-2 italic">
                💬 {{ req.admin_note }}
              </p>
            </div>
          </div>

          <div v-else class="text-center py-8">
            <div class="w-16 h-16 rounded-full bg-dark-800 mx-auto mb-3 flex items-center justify-center text-3xl">📋</div>
            <p class="text-dark-400">ยังไม่มีประวัติการเติม Token</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Slip Modal -->
    <div v-if="slipModalUrl" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50" @click="slipModalUrl = null">
      <div class="max-w-2xl max-h-[90vh] p-4">
        <img :src="`http://localhost:5000${slipModalUrl}`" alt="Slip" class="max-h-full rounded-xl" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const tokenBalance = ref(0);
const requests = ref([]);
const isVerifying = ref(false);

const slipFile = ref(null);
const slipPreview = ref(null);
const isDragging = ref(false);
const verifyResult = ref(null);
const slipModalUrl = ref(null);

const baseUrl = 'http://localhost:5000';

const statusLabels = {
  pending: '⏳ รอตรวจสอบ',
  approved: '✅ อนุมัติแล้ว',
  rejected: '❌ ปฏิเสธ'
};

function handleQrError(e) {
  // If QR image fails to load, use placeholder
  e.target.src = 'https://via.placeholder.com/256x256?text=QR+Code';
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    processFile(file);
  }
}

function handleDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) {
    processFile(file);
  }
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
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    return;
  }
  
  if (!slipFile.value) {
    alert('กรุณาเลือกไฟล์สลิป');
    return;
  }
  
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
      // Refresh data
      fetchTokenBalance();
      fetchRequests();
      // Clear slip after success
      setTimeout(() => {
        clearSlip();
      }, 5000);
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

onMounted(() => {
  fetchTokenBalance();
  fetchRequests();
});
</script>

<style scoped>
.badge-warning {
  background-color: rgba(234, 179, 8, 0.2);
  color: #facc15;
}
.badge-success {
  background-color: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}
.badge-error {
  background-color: rgba(239, 68, 68, 0.2);
  color: #f87171;
}
</style>
