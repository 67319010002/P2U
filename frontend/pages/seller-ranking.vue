<template>
  <div class="min-h-screen bg-[#0a0a0f] text-gray-100 relative overflow-hidden">
    <!-- Particle Background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px]"></div>
      <div class="absolute bottom-20 right-1/4 w-80 h-80 bg-pink-600/10 rounded-full blur-[100px]"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-600/5 rounded-full blur-[150px]"></div>
    </div>

    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <main class="ml-20 p-6 md:p-8 max-w-6xl mx-auto relative z-10">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl md:text-5xl font-black mb-2">
          <span class="text-6xl mr-3">🏆</span>
          <span class="bg-gradient-to-r from-amber-400 via-pink-500 to-purple-500 bg-clip-text text-transparent">
            Seller Ranking
          </span>
        </h1>
        <p class="text-gray-400 mt-2">จัดอันดับตามคะแนน AI Score</p>
      </div>

      <!-- Level Filter Pills -->
      <div class="flex justify-center gap-3 mb-10 flex-wrap">
        <button 
          v-for="level in levels" 
          :key="level.id"
          @click="selectedLevel = level.id"
          class="px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 border"
          :class="selectedLevel === level.id 
            ? 'bg-gradient-to-r from-amber-500 to-orange-600 text-white border-amber-400/50 shadow-lg shadow-amber-500/20' 
            : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-white'"
        >
          {{ level.icon }} {{ level.name }}
        </button>
      </div>

      <!-- Top 3 Podium - Premium Design -->
      <div v-if="!selectedLevel && topSellers.length >= 3" class="mb-12">
        <div class="flex justify-center items-end gap-4 md:gap-8">
          
          <!-- 2nd Place (Left) -->
          <div class="text-center animate-slideUp" style="animation-delay: 0.1s">
            <div class="relative mb-4">
              <!-- Glow Ring -->
              <div class="absolute -inset-2 bg-gradient-to-br from-gray-300 to-gray-500 rounded-full blur-md opacity-50"></div>
              <div class="relative w-20 h-20 md:w-24 md:h-24 rounded-full border-4 border-gray-300 overflow-hidden bg-[#1a1a20] shadow-xl">
                <img :src="topSellers[1]?.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
              </div>
              <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 text-3xl">🥈</div>
            </div>
            <!-- Info Card -->
            <div class="bg-gradient-to-b from-gray-400 to-gray-500 rounded-t-2xl pt-6 px-4 pb-3 w-36 md:w-44 relative">
              <div class="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent rounded-t-2xl"></div>
              <p class="text-gray-900 font-bold text-sm md:text-base truncate relative z-10">{{ topSellers[1]?.shop_name }}</p>
              <p class="text-xs text-gray-700 mb-1 relative z-10">AI Score</p>
              <p class="text-2xl md:text-3xl font-black text-gray-900 relative z-10">{{ topSellers[1]?.ai_score?.toFixed(1) || '0' }}</p>
              <span class="inline-block mt-2 px-2 py-0.5 rounded-full text-xs font-bold bg-gray-700 text-gray-200 relative z-10">
                {{ topSellers[1]?.badge?.icon }} {{ topSellers[1]?.badge?.name || 'Seller' }}
              </span>
            </div>
          </div>

          <!-- 1st Place (Center - Larger) -->
          <div class="text-center animate-slideUp -mt-8">
            <div class="relative mb-4">
              <!-- Premium Glow Ring -->
              <div class="absolute -inset-3 bg-gradient-to-br from-amber-400 via-yellow-500 to-orange-500 rounded-full blur-lg opacity-70 animate-pulse"></div>
              <div class="absolute -inset-1 bg-gradient-to-br from-amber-400 to-yellow-500 rounded-full"></div>
              <div class="relative w-28 h-28 md:w-32 md:h-32 rounded-full border-4 border-yellow-400 overflow-hidden bg-[#1a1a20] shadow-2xl">
                <img :src="topSellers[0]?.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
              </div>
              <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 text-4xl animate-bounce">🥇</div>
            </div>
            <!-- Info Card - Gold -->
            <div class="bg-gradient-to-b from-amber-400 via-yellow-500 to-orange-500 rounded-t-2xl pt-8 px-5 pb-4 w-44 md:w-52 relative shadow-xl shadow-amber-500/30">
              <div class="absolute inset-0 bg-gradient-to-b from-white/30 to-transparent rounded-t-2xl"></div>
              <div class="absolute top-2 right-2 text-lg">✨</div>
              <p class="text-gray-900 font-bold text-base md:text-lg truncate relative z-10">{{ topSellers[0]?.shop_name }}</p>
              <p class="text-xs text-gray-700 mb-1 relative z-10">AI Score</p>
              <p class="text-3xl md:text-4xl font-black text-gray-900 relative z-10">{{ topSellers[0]?.ai_score?.toFixed(1) || '0' }}</p>
              <span class="inline-block mt-2 px-3 py-1 rounded-full text-xs font-bold bg-amber-700 text-amber-100 relative z-10 shadow-md">
                {{ topSellers[0]?.badge?.icon }} {{ topSellers[0]?.badge?.name || 'Top Tier' }}
              </span>
            </div>
          </div>

          <!-- 3rd Place (Right) -->
          <div class="text-center animate-slideUp" style="animation-delay: 0.2s">
            <div class="relative mb-4">
              <!-- Glow Ring -->
              <div class="absolute -inset-2 bg-gradient-to-br from-orange-600 to-orange-800 rounded-full blur-md opacity-50"></div>
              <div class="relative w-20 h-20 md:w-24 md:h-24 rounded-full border-4 border-orange-600 overflow-hidden bg-[#1a1a20] shadow-xl">
                <img :src="topSellers[2]?.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
              </div>
              <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 text-3xl">🥉</div>
            </div>
            <!-- Info Card -->
            <div class="bg-gradient-to-b from-orange-600 to-orange-700 rounded-t-2xl pt-6 px-4 pb-3 w-36 md:w-44 relative">
              <div class="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent rounded-t-2xl"></div>
              <p class="text-white font-bold text-sm md:text-base truncate relative z-10">{{ topSellers[2]?.shop_name }}</p>
              <p class="text-xs text-orange-200 mb-1 relative z-10">AI Score</p>
              <p class="text-2xl md:text-3xl font-black text-white relative z-10">{{ topSellers[2]?.ai_score?.toFixed(1) || '0' }}</p>
              <span class="inline-block mt-2 px-2 py-0.5 rounded-full text-xs font-bold bg-orange-900 text-orange-200 relative z-10">
                {{ topSellers[2]?.badge?.icon }} {{ topSellers[2]?.badge?.name || 'Seller' }}
              </span>
            </div>
          </div>

        </div>
      </div>

      <!-- Leaderboard Table - Premium Glass Design -->
      <div class="bg-[#12121a]/80 backdrop-blur-xl rounded-3xl border border-white/10 overflow-hidden shadow-2xl">
        <!-- Table Header -->
        <div class="px-6 py-4 border-b border-white/10 flex justify-between items-center bg-white/5">
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            📊 ตารางอันดับ
          </h2>
          <span class="text-gray-400 text-sm bg-white/5 px-3 py-1 rounded-full">ทั้งหมด {{ pagination.total }} ร้าน</span>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="p-16 text-center">
          <div class="w-16 h-16 mx-auto mb-4 relative">
            <div class="absolute inset-0 rounded-full border-4 border-purple-500/20"></div>
            <div class="absolute inset-0 rounded-full border-4 border-transparent border-t-purple-500 animate-spin"></div>
          </div>
          <p class="text-gray-400">กำลังโหลดข้อมูล...</p>
        </div>

        <!-- Leaderboard Rows -->
        <div v-else-if="leaderboard.length" class="divide-y divide-white/5">
          <div 
            v-for="seller in leaderboard" 
            :key="seller.id"
            class="flex items-center justify-between px-6 py-5 hover:bg-white/5 transition-all duration-300 cursor-pointer group"
            :class="[
              seller.rank === 1 ? 'bg-gradient-to-r from-amber-500/10 to-transparent' : '',
              seller.rank === 2 ? 'bg-gradient-to-r from-gray-400/10 to-transparent' : '',
              seller.rank === 3 ? 'bg-gradient-to-r from-orange-600/10 to-transparent' : ''
            ]"
            @click="openSellerDetail(seller)"
          >
            <div class="flex items-center gap-5">
              <!-- Rank Badge -->
              <div 
                class="w-12 h-12 rounded-2xl flex items-center justify-center font-black text-xl shadow-lg"
                :class="getRankBgClass(seller.rank)"
              >
                <span v-if="seller.rank <= 3" class="text-2xl">{{ ['🥇', '🥈', '🥉'][seller.rank - 1] }}</span>
                <span v-else class="text-gray-400">{{ seller.rank }}</span>
              </div>

              <!-- Avatar with Tier Ring -->
              <div class="relative">
                <div 
                  class="absolute -inset-1 rounded-full opacity-70"
                  :style="{ background: `linear-gradient(135deg, ${seller.badge?.color || '#666'}, ${seller.badge?.color || '#666'}88)` }"
                ></div>
                <div class="relative w-14 h-14 rounded-full overflow-hidden bg-[#1a1a20] border-2 border-white/10">
                  <img :src="seller.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
                </div>
              </div>

              <!-- Seller Info -->
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <p class="text-white font-bold text-lg group-hover:text-pink-300 transition-colors">{{ seller.shop_name }}</p>
                  <span v-if="seller.is_verified" class="text-blue-400" title="ID Verified">💎</span>
                  <span v-if="seller.is_phone_verified" class="text-green-400" title="Phone Verified">📱</span>
                </div>
                <div class="flex items-center gap-3">
                  <!-- Tier Badge -->
                  <span 
                    class="px-3 py-1 rounded-full text-xs font-bold shadow-md"
                    :style="{ 
                      backgroundColor: (seller.badge?.color || '#666') + '22', 
                      color: seller.badge?.color || '#999',
                      border: `1px solid ${seller.badge?.color || '#666'}44`
                    }"
                  >
                    {{ seller.badge?.icon }} {{ seller.badge?.name }}
                  </span>
                  <!-- Rating -->
                  <span class="text-yellow-400 text-sm flex items-center gap-1">
                    <span>⭐</span>
                    <span class="text-white font-medium">{{ seller.rating_avg?.toFixed(1) || '0.0' }}</span>
                  </span>
                </div>
              </div>
            </div>

            <!-- AI Score -->
            <div class="text-right">
              <p 
                class="text-3xl md:text-4xl font-black bg-clip-text text-transparent"
                :class="seller.rank === 1 ? 'bg-gradient-to-r from-amber-400 to-orange-500' : 
                        seller.rank === 2 ? 'bg-gradient-to-r from-gray-300 to-gray-400' :
                        seller.rank === 3 ? 'bg-gradient-to-r from-orange-500 to-orange-600' :
                        'bg-gradient-to-r from-pink-400 to-purple-500'"
              >
                {{ seller.ai_score?.toFixed(1) || '0' }}
              </p>
              <p class="text-gray-500 text-xs uppercase tracking-wide">points</p>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="p-16 text-center">
          <div class="text-6xl mb-4">🔍</div>
          <p class="text-gray-400">ไม่พบข้อมูลผู้ขาย</p>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.total_pages > 1" class="p-5 border-t border-white/10 flex justify-center items-center gap-4 bg-white/5">
          <button 
            @click="changePage(pagination.page - 1)"
            :disabled="pagination.page <= 1"
            class="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-gray-400 hover:bg-white/10 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all"
          >
            ← ก่อนหน้า
          </button>
          <span class="px-5 py-2 rounded-xl bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 text-white font-medium">
            {{ pagination.page }} / {{ pagination.total_pages }}
          </span>
          <button 
            @click="changePage(pagination.page + 1)"
            :disabled="pagination.page >= pagination.total_pages"
            class="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-gray-400 hover:bg-white/10 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all"
          >
            ถัดไป →
          </button>
        </div>
      </div>

      <!-- Seller Detail Modal - Premium -->
      <Teleport to="body">
        <Transition name="modal">
          <div v-if="selectedSeller" class="fixed inset-0 bg-black/80 backdrop-blur-md z-[100] flex items-center justify-center p-4" @click="selectedSeller = null">
            <div class="bg-[#15151f] rounded-3xl w-full max-w-lg border border-white/10 shadow-2xl overflow-hidden animate-modalIn" @click.stop>
              
              <!-- Modal Header with Gradient -->
              <div class="relative p-6 pb-16 bg-gradient-to-br from-purple-600/30 via-pink-600/20 to-transparent">
                <button @click="selectedSeller = null" class="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-gray-400 hover:text-white transition-colors">
                  ✕
                </button>
                
                <!-- Avatar & Basic Info -->
                <div class="flex items-center gap-5">
                  <div class="relative">
                    <div class="absolute -inset-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full blur-lg opacity-60"></div>
                    <div class="relative w-20 h-20 rounded-full border-4 border-white/20 overflow-hidden bg-[#1a1a20]">
                      <img :src="selectedSeller.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
                    </div>
                  </div>
                  <div>
                    <h3 class="text-2xl font-bold text-white mb-1">{{ selectedSeller.shop_name }}</h3>
                    <span 
                      class="inline-block px-4 py-1.5 rounded-full text-sm font-bold shadow-lg"
                      :style="{ backgroundColor: selectedSeller.badge?.color || '#666' }"
                    >
                      {{ selectedSeller.badge?.icon }} {{ selectedSeller.badge?.name }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Stats Grid -->
              <div class="px-6 -mt-8 mb-6">
                <div class="grid grid-cols-2 gap-4">
                  <div class="bg-gradient-to-br from-purple-500/20 to-purple-600/10 rounded-2xl p-5 border border-purple-500/20 text-center">
                    <p class="text-4xl font-black bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                      {{ selectedSeller.ai_score?.toFixed(1) || '0' }}
                    </p>
                    <p class="text-gray-400 text-sm mt-1">AI Score</p>
                  </div>
                  <div class="bg-gradient-to-br from-amber-500/20 to-amber-600/10 rounded-2xl p-5 border border-amber-500/20 text-center">
                    <p class="text-4xl font-black text-amber-400">
                      {{ selectedSeller.rating_avg?.toFixed(1) || '0.0' }}
                    </p>
                    <p class="text-gray-400 text-sm mt-1">Rating ⭐</p>
                  </div>
                </div>
              </div>

              <!-- Verification Status -->
              <div class="px-6 mb-6">
                <p class="text-white font-semibold mb-3 flex items-center gap-2">✅ การยืนยันตัวตน</p>
                <div class="flex flex-wrap gap-2">
                  <span 
                    class="px-4 py-2 rounded-xl text-sm font-medium border"
                    :class="selectedSeller.verification?.email ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-white/5 border-white/10 text-gray-500'"
                  >
                    📧 Email {{ selectedSeller.verification?.email ? '✓' : '✗' }}
                  </span>
                  <span 
                    class="px-4 py-2 rounded-xl text-sm font-medium border"
                    :class="selectedSeller.verification?.phone ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-white/5 border-white/10 text-gray-500'"
                  >
                    📱 Phone {{ selectedSeller.verification?.phone ? '✓' : '✗' }}
                  </span>
                  <span 
                    class="px-4 py-2 rounded-xl text-sm font-medium border"
                    :class="selectedSeller.verification?.id_card ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-white/5 border-white/10 text-gray-500'"
                  >
                    💎 ID Card {{ selectedSeller.verification?.id_card ? '✓' : '✗' }}
                  </span>
                </div>
              </div>

              <!-- Score Breakdown -->
              <div v-if="selectedSeller.score_breakdown" class="px-6 pb-6">
                <p class="text-white font-semibold mb-4 flex items-center gap-2">📊 รายละเอียดคะแนน</p>
                <div class="space-y-4">
                  <div v-for="(value, key) in selectedSeller.score_breakdown" :key="key">
                    <div class="flex justify-between text-sm mb-2">
                      <span class="text-gray-400">{{ getScoreLabel(key) }}</span>
                      <span class="text-white font-bold">{{ value?.toFixed(0) || 0 }}%</span>
                    </div>
                    <div class="h-3 bg-white/5 rounded-full overflow-hidden border border-white/5">
                      <div 
                        class="h-full rounded-full transition-all duration-700 ease-out"
                        :class="getScoreBarColor(key)"
                        :style="{ width: (value || 0) + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </Transition>
      </Teleport>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

const baseUrl = 'http://localhost:5000';

const leaderboard = ref([]);
const loading = ref(true);
const selectedLevel = ref(null);
const selectedSeller = ref(null);
const pagination = ref({ page: 1, per_page: 20, total: 0, total_pages: 1 });

const levels = [
  { id: null, name: 'ทั้งหมด', icon: '🏆' },
  { id: 'S', name: 'Top Seller', icon: '🥇' },
  { id: 'A', name: 'Star Seller', icon: '⭐' },
  { id: 'B', name: 'Verified', icon: '✓' },
  { id: 'C', name: 'Basic', icon: '📦' },
];

const topSellers = computed(() => leaderboard.value.slice(0, 3));

const scoreLabels = {
  sales: '💰 ยอดขาย',
  rating: '⭐ คะแนนรีวิว',
  delivery: '🚚 ความเร็วจัดส่ง',
  response: '💬 อัตราตอบกลับ',
  cancel: '❌ อัตรายกเลิก',
  verification: '✅ การยืนยันตัวตน'
};

const scoreBarColors = {
  sales: 'bg-gradient-to-r from-emerald-500 to-emerald-400',
  rating: 'bg-gradient-to-r from-amber-500 to-yellow-400',
  delivery: 'bg-gradient-to-r from-blue-500 to-cyan-400',
  response: 'bg-gradient-to-r from-purple-500 to-pink-400',
  cancel: 'bg-gradient-to-r from-green-500 to-emerald-400',
  verification: 'bg-gradient-to-r from-pink-500 to-rose-400'
};

function getScoreLabel(key) {
  return scoreLabels[key] || key;
}

function getScoreBarColor(key) {
  return scoreBarColors[key] || 'bg-gradient-to-r from-gray-500 to-gray-400';
}

function getRankBgClass(rank) {
  if (rank === 1) return 'bg-gradient-to-br from-amber-500 to-orange-600';
  if (rank === 2) return 'bg-gradient-to-br from-gray-300 to-gray-400';
  if (rank === 3) return 'bg-gradient-to-br from-orange-600 to-orange-700';
  return 'bg-white/5 border border-white/10';
}

async function fetchLeaderboard(page = 1) {
  loading.value = true;
  try {
    const params = { page, per_page: 20 };
    if (selectedLevel.value) params.level = selectedLevel.value;
    
    const res = await axios.get(`${baseUrl}/api/seller/rank/leaderboard`, { params });
    leaderboard.value = res.data.leaderboard || [];
    pagination.value = res.data.pagination || { page: 1, total: 0, total_pages: 1 };
  } catch (err) {
    console.error('Failed to fetch leaderboard:', err);
  } finally {
    loading.value = false;
  }
}

async function openSellerDetail(seller) {
  try {
    const res = await axios.get(`${baseUrl}/api/seller/rank/${seller.id}`);
    selectedSeller.value = res.data;
  } catch (err) {
    console.error('Failed to fetch seller details:', err);
    selectedSeller.value = seller;
  }
}

function changePage(page) {
  if (page >= 1 && page <= pagination.value.total_pages) {
    fetchLeaderboard(page);
  }
}

watch(selectedLevel, () => {
  fetchLeaderboard(1);
});

onMounted(() => {
  fetchLeaderboard();
});
</script>

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideUp {
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-modalIn {
  animation: modalIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.modal-enter-active {
  transition: all 0.3s ease;
}

.modal-leave-active {
  transition: all 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .animate-modalIn {
  transform: scale(0.9) translateY(20px);
}
</style>
