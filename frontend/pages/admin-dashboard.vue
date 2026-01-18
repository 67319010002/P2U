<template>
  <div class="min-h-screen bg-[#0b0b0f] text-white font-sans selection:bg-red-500/30 relative overflow-x-hidden">
    
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
       <div class="absolute top-[-10%] right-[-5%] w-[600px] h-[600px] bg-red-600/10 rounded-full blur-[120px] mix-blend-screen animate-pulse-slow"></div>
       <div class="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-orange-600/10 rounded-full blur-[100px] mix-blend-screen animate-pulse-slow" style="animation-delay: 2s;"></div>
    </div>

    <div class="relative z-10 max-w-7xl mx-auto p-6 lg:p-10">
      
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10 animate-fade-in-down">
        <div>
          <h1 class="text-3xl font-bold flex items-center gap-3">
            <span class="w-2 h-8 bg-gradient-to-b from-red-500 to-orange-500 rounded-full"></span>
            Admin Command Center
          </h1>
          <p class="text-gray-400 mt-2 ml-5 text-sm">
            ยินดีต้อนรับ, <span class="text-white font-semibold">{{ adminUser?.username || 'Admin' }}</span>
          </p>
        </div>

        <button 
          @click="handleLogout" 
          class="group flex items-center gap-2 px-5 py-2.5 rounded-xl border border-red-500/30 text-red-400 hover:bg-red-500 hover:text-white transition-all duration-300 hover:shadow-[0_0_15px_rgba(239,68,68,0.4)]"
        >
          <span>🚪</span>
          <span class="font-medium">ออกจากระบบ</span>
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10 animate-fade-in-up">
        <div class="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl hover:border-blue-500/50 transition-colors group">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">ผู้ใช้ทั้งหมด</p>
              <h3 class="text-3xl font-bold text-white group-hover:text-blue-400 transition-colors">{{ stats.total_users || 0 }}</h3>
            </div>
            <div class="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">👥</div>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl hover:border-purple-500/50 transition-colors group">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">ผู้ขาย</p>
              <h3 class="text-3xl font-bold text-white group-hover:text-purple-400 transition-colors">{{ stats.total_sellers || 0 }}</h3>
            </div>
            <div class="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">🏪</div>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl hover:border-pink-500/50 transition-colors group">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">สินค้าทั้งหมด</p>
              <h3 class="text-3xl font-bold text-white group-hover:text-pink-400 transition-colors">{{ stats.total_products || 0 }}</h3>
            </div>
            <div class="w-12 h-12 rounded-xl bg-pink-500/10 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">📦</div>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl hover:border-green-500/50 transition-colors group">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">รายได้รวม</p>
              <h3 class="text-3xl font-bold text-green-400 group-hover:text-green-300 transition-colors">฿{{ stats.total_revenue?.toLocaleString() || 0 }}</h3>
            </div>
            <div class="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">💰</div>
          </div>
        </div>
      </div>

      <div class="animate-fade-in-up" style="animation-delay: 0.1s;">
        
        <div class="flex flex-wrap gap-2 mb-6 p-1 bg-white/5 rounded-2xl w-fit backdrop-blur-sm border border-white/5">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="px-6 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 flex items-center gap-2"
            :class="activeTab === tab.id 
              ? 'bg-gradient-to-r from-red-600 to-orange-600 text-white shadow-lg shadow-red-500/20' 
              : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            <span>{{ tab.icon }}</span>
            {{ tab.name }}
            <span v-if="tab.id === 'tokens' && tokenStats.pending > 0" class="ml-1 w-2 h-2 rounded-full bg-red-400 animate-pulse"></span>
          </button>
        </div>

        <div class="bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden shadow-2xl min-h-[500px]">
          
          <div v-if="activeTab === 'users'">
             <div class="p-6 border-b border-white/10 flex items-center justify-between bg-white/5">
                <h2 class="text-lg font-bold text-white flex items-center gap-2">
                   👥 รายชื่อผู้ใช้ในระบบ
                   <span class="text-xs font-normal text-gray-400 bg-white/10 px-2 py-1 rounded-full">{{ users.length }} users</span>
                </h2>
             </div>
             <div class="overflow-x-auto">
                <table class="w-full">
                   <thead class="bg-black/20 text-gray-400 text-xs uppercase tracking-wider font-semibold">
                      <tr>
                         <th class="text-left p-5">User Info</th>
                         <th class="text-left p-5">Role</th>
                         <th class="text-left p-5">Status</th>
                         <th class="text-left p-5">Balance</th>
                         <th class="text-right p-5">Actions</th>
                      </tr>
                   </thead>
                   <tbody class="divide-y divide-white/5">
                      <tr v-for="user in users" :key="user.id" class="hover:bg-white/5 transition-colors">
                         <td class="p-5">
                            <div class="flex items-center gap-4">
                               <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-700 to-gray-600 flex items-center justify-center font-bold text-white shadow-inner border border-white/10">
                                  {{ user.username.charAt(0).toUpperCase() }}
                               </div>
                               <div>
                                  <div class="font-medium text-white">{{ user.username }}</div>
                                  <div class="text-xs text-gray-500">{{ user.email }}</div>
                               </div>
                            </div>
                         </td>
                         <td class="p-5">
                            <span :class="user.is_seller ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' : 'bg-blue-500/20 text-blue-300 border-blue-500/30'" class="px-3 py-1 rounded-full text-xs border font-medium">
                               {{ user.is_seller ? 'Seller' : 'Member' }}
                            </span>
                         </td>
                         <td class="p-5">
                            <span :class="user.is_active ? 'text-green-400' : 'text-red-400'" class="flex items-center gap-1.5 text-sm">
                               <span class="w-1.5 h-1.5 rounded-full" :class="user.is_active ? 'bg-green-400' : 'bg-red-400'"></span>
                               {{ user.is_active ? 'Active' : 'Banned' }}
                            </span>
                         </td>
                         <td class="p-5 font-mono text-yellow-500">
                            🪙 {{ user.coin_balance?.toLocaleString() }}
                         </td>
                         <td class="p-5 text-right space-x-2">
                            <button @click="toggleBanUser(user)" :class="user.is_active ? 'text-yellow-500 hover:bg-yellow-500/10' : 'text-green-500 hover:bg-green-500/10'" class="p-2 rounded-lg transition-colors" :title="user.is_active ? 'Ban User' : 'Unban User'">
                               {{ user.is_active ? '🚫' : '✅' }}
                            </button>
                            <button @click="deleteUser(user)" class="p-2 rounded-lg text-red-500 hover:bg-red-500/10 transition-colors" title="Delete User">
                               🗑️
                            </button>
                         </td>
                      </tr>
                   </tbody>
                </table>
             </div>
          </div>

          <div v-if="activeTab === 'products'">
            <div class="p-6 border-b border-white/10 bg-white/5">
                <h2 class="text-lg font-bold text-white">📦 คลังสินค้า</h2>
             </div>
             <div class="overflow-x-auto">
                <table class="w-full">
                   <thead class="bg-black/20 text-gray-400 text-xs uppercase tracking-wider font-semibold">
                      <tr>
                         <th class="text-left p-5">Product</th>
                         <th class="text-left p-5">Price</th>
                         <th class="text-left p-5">Seller</th>
                         <th class="text-left p-5">Added Date</th>
                         <th class="text-right p-5">Actions</th>
                      </tr>
                   </thead>
                   <tbody class="divide-y divide-white/5">
                      <tr v-for="product in products" :key="product.id" class="hover:bg-white/5 transition-colors">
                         <td class="p-5">
                            <div class="flex items-center gap-4">
                               <img :src="product.image_url || '/placeholder.png'" class="w-10 h-10 rounded-lg object-cover bg-gray-800" />
                               <span class="font-medium text-white">{{ product.name }}</span>
                            </div>
                         </td>
                         <td class="p-5 font-mono text-green-400">฿{{ product.price.toLocaleString() }}</td>
                         <td class="p-5 text-gray-400">{{ product.seller?.username }}</td>
                         <td class="p-5 text-gray-500 text-sm">{{ new Date(product.created_at).toLocaleDateString() }}</td>
                         <td class="p-5 text-right">
                            <button @click="deleteProduct(product)" class="px-3 py-1.5 rounded-lg border border-red-500/30 text-red-400 hover:bg-red-500 hover:text-white transition-colors text-sm">
                               ลบสินค้า
                            </button>
                         </td>
                      </tr>
                   </tbody>
                </table>
             </div>
          </div>

      <!-- Token Requests Table -->
      <div v-if="activeTab === 'tokens'" class="card overflow-hidden">
        <div class="p-4 border-b border-white/10 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-white">คำขอเติม Token</h2>
          <div class="flex gap-2">
            <span class="badge badge-warning">{{ tokenStats.pending || 0 }} รอตรวจสอบ</span>
            <span class="badge badge-success-outline">{{ tokenStats.approved || 0 }} อนุมัติแล้ว</span>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-dark-800/50">
              <tr>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">ผู้ใช้</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">จำนวน Token</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">สลิป</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">สถานะ</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">วันที่</th>
                <th class="text-right p-4 text-dark-400 text-sm font-medium">การจัดการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in tokenRequests" :key="req.id" class="border-b border-white/5 hover:bg-white/5">
                <td class="p-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center text-white font-bold">
                      {{ req.user?.username?.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <p class="text-white font-medium">{{ req.user?.username }}</p>
                      <p class="text-dark-500 text-xs">{{ req.user?.email }}</p>
                    </div>
                  </div>
                </td>
                <td class="p-4">
                  <p class="text-primary-400 font-bold text-lg">🪙 {{ req.amount?.toLocaleString() }}</p>
                  <!-- Show transaction ref if available -->
                  <p v-if="req.transaction_ref" class="text-dark-500 text-xs mt-1">
                    🧾 {{ req.transaction_ref }}
                  </p>
                </td>
                <td class="p-4">
                  <!-- Slip Image Preview -->
                  <div v-if="req.payment_proof_url" class="relative">
                    <img 
                      :src="`http://localhost:5000${req.payment_proof_url}`" 
                      alt="Slip" 
                      class="h-16 rounded-lg cursor-pointer hover:opacity-80 transition-opacity"
                      @click="showSlipModal(req)"
                    />
                    <!-- Auto-approved badge -->
                    <span v-if="req.is_auto_approved" class="absolute -top-1 -right-1 bg-blue-500 text-white text-xs px-1.5 py-0.5 rounded-full">
                      ⚡
                    </span>
                  </div>
                  <span v-else class="text-dark-500 text-sm">ไม่มีสลิป</span>
                </td>
                <td class="p-4">
                  <span 
                    class="badge"
                    :class="{
                      'bg-yellow-500/20 text-yellow-400': req.status === 'pending',
                      'bg-green-500/20 text-green-400': req.status === 'approved',
                      'bg-red-500/20 text-red-400': req.status === 'rejected'
                    }"
                  >
                    {{ req.status === 'pending' ? '⏳ รอตรวจสอบ' : req.status === 'approved' ? '✅ อนุมัติแล้ว' : '❌ ปฏิเสธ' }}
                  </span>
                  <!-- Show auto-approved label -->
                  <span v-if="req.is_auto_approved" class="block text-xs text-blue-400 mt-1">
                    ⚡ อนุมัติอัตโนมัติ
                  </span>
                </td>
                <td class="p-4 text-dark-400 text-sm">{{ req.created_at }}</td>
                <td class="p-4 text-right">
                  <div v-if="req.status === 'pending'" class="flex gap-2 justify-end">
                    <button 
                      @click="approveToken(req)" 
                      class="px-3 py-1.5 rounded-lg text-sm bg-green-500/20 text-green-400 hover:bg-green-500/30 transition-colors"
                    >
                      ✅ อนุมัติ
                    </button>
                    <button 
                      @click="rejectToken(req)" 
                      class="px-3 py-1.5 rounded-lg text-sm bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-colors"
                    >
                      ❌ ปฏิเสธ
                    </button>
                  </div>
                  <span v-else class="text-dark-500 text-sm">{{ req.admin_note || 'ดำเนินการแล้ว' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Slip Detail Modal -->
      <div v-if="selectedSlip" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50" @click="selectedSlip = null">
        <div class="max-w-2xl bg-dark-900 rounded-2xl p-6 m-4" @click.stop>
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-white">รายละเอียดสลิป</h3>
            <button @click="selectedSlip = null" class="text-dark-400 hover:text-white text-2xl">&times;</button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Slip Image -->
            <div>
              <img 
                :src="`http://localhost:5000${selectedSlip.payment_proof_url}`" 
                alt="Slip" 
                class="w-full rounded-xl"
              />
            </div>
            
            <!-- Slip Details -->
            <div class="space-y-4">
              <div class="glass-light rounded-xl p-4">
                <p class="text-dark-400 text-sm">ผู้ใช้</p>
                <p class="text-white font-bold">{{ selectedSlip.user?.username }}</p>
              </div>
              
              <div class="glass-light rounded-xl p-4">
                <p class="text-dark-400 text-sm">จำนวน Token</p>
                <p class="text-primary-400 font-bold text-2xl">🪙 {{ selectedSlip.amount?.toLocaleString() }}</p>
              </div>
              
              <div v-if="selectedSlip.transaction_ref" class="glass-light rounded-xl p-4">
                <p class="text-dark-400 text-sm">เลขอ้างอิง</p>
                <p class="text-white font-mono">{{ selectedSlip.transaction_ref }}</p>
              </div>
              
              <div v-if="selectedSlip.sender_name" class="glass-light rounded-xl p-4">
                <p class="text-dark-400 text-sm">ผู้โอน</p>
                <p class="text-white">{{ selectedSlip.sender_name }}</p>
              </div>
              
              <div v-if="selectedSlip.is_auto_approved" class="bg-blue-500/20 rounded-xl p-4">
                <p class="text-blue-400 font-medium">⚡ อนุมัติอัตโนมัติโดย SlipOK</p>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// ------------------------------------------
// 🔑 บรรทัดนี้สำคัญมาก! สั่งใช้ Layout "admin" 
// เพื่อไม่ให้ Navbar ของหน้าปกติโผล่มา
// ------------------------------------------
definePageMeta({
  layout: 'admin'
});

const router = useRouter();
const adminUser = ref(null);
const stats = ref({});
const users = ref([]);
const products = ref([]);
const orders = ref([]);
const tokenRequests = ref([]);
const tokenStats = ref({});
const activeTab = ref('users');
const selectedSlip = ref(null);

const tabs = [
  { id: 'users', name: 'Users', icon: '👥' },
  { id: 'products', name: 'Products', icon: '📦' },
  { id: 'orders', name: 'Orders', icon: '🛒' },
  { id: 'tokens', name: 'Tokens', icon: '🪙' },
];

const baseUrl = 'http://localhost:5000';

async function fetchData() {
  const token = localStorage.getItem('admin_token');
  if (!token) {
    router.push('/admin-login');
    return;
  }

  const headers = { Authorization: `Bearer ${token}` };

  try {
    const [statsRes, usersRes, productsRes, ordersRes] = await Promise.all([
      axios.get(`${baseUrl}/api/admin/stats`, { headers }),
      axios.get(`${baseUrl}/api/admin/users`, { headers }),
      axios.get(`${baseUrl}/api/admin/products`, { headers }),
      axios.get(`${baseUrl}/api/admin/orders`, { headers }),
    ]);

    stats.value = statsRes.data;
    users.value = usersRes.data;
    products.value = productsRes.data;
    orders.value = ordersRes.data;
    
    // Fetch token requests separately
    fetchTokenRequests();
  } catch (err) {
    console.error('Failed to fetch admin data:', err);
    if (err.response?.status === 401 || err.response?.status === 403) {
      router.push('/admin-login');
    }
  }
}

async function toggleBanUser(user) {
  const token = localStorage.getItem('admin_token');
  try {
    const res = await axios.put(`${baseUrl}/api/admin/users/${user.id}/toggle-ban`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    user.is_active = res.data.is_active;
  } catch (err) {
    console.error('Failed to toggle ban:', err);
  }
}

async function deleteUser(user) {
  if (!confirm(`ยืนยันการลบผู้ใช้ ${user.username}?`)) return;
  
  const token = localStorage.getItem('admin_token');
  try {
    await axios.delete(`${baseUrl}/api/admin/users/${user.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    users.value = users.value.filter(u => u.id !== user.id);
  } catch (err) {
    console.error('Failed to delete user:', err);
  }
}

async function deleteProduct(product) {
  if (!confirm(`ยืนยันการลบสินค้า ${product.name}?`)) return;
  
  const token = localStorage.getItem('admin_token');
  try {
    await axios.delete(`${baseUrl}/api/admin/products/${product.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    products.value = products.value.filter(p => p.id !== product.id);
  } catch (err) {
    console.error('Failed to delete product:', err);
  }
}

async function updateOrderStatus(order) {
  const token = localStorage.getItem('admin_token');
  try {
    await axios.put(`${baseUrl}/api/admin/orders/${order.id}/status`, 
      { status: order.status },
      { headers: { Authorization: `Bearer ${token}` } }
    );
  } catch (err) {
    console.error('Failed to update order status:', err);
  }
}

function handleLogout() {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
  router.push('/admin-login');
}

function showSlipModal(req) {
  selectedSlip.value = req;
}

async function fetchTokenRequests() {
  const token = localStorage.getItem('admin_token');
  if (!token) return;
  
  try {
    const [requestsRes, statsRes] = await Promise.all([
      axios.get(`${baseUrl}/api/admin/token-requests`, {
        headers: { Authorization: `Bearer ${token}` }
      }),
      axios.get(`${baseUrl}/api/admin/token-stats`, {
        headers: { Authorization: `Bearer ${token}` }
      })
    ]);
    tokenRequests.value = requestsRes.data.requests || [];
    tokenStats.value = statsRes.data || {};
  } catch (err) {
    console.error('Failed to fetch token requests:', err);
  }
}

async function approveToken(req) {
  if (!confirm(`อนุมัติ ${req.amount.toLocaleString()} Token ให้ ${req.user?.username}?`)) return;
  
  const token = localStorage.getItem('admin_token');
  try {
    await axios.put(`${baseUrl}/api/admin/token-requests/${req.id}/approve`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert(`✅ อนุมัติสำเร็จ!`);
    fetchTokenRequests();
  } catch (err) {
    alert(err.response?.data?.msg || 'อนุมัติไม่สำเร็จ');
  }
}

async function rejectToken(req) {
  const reason = prompt('ระบุเหตุผลในการปฏิเสธ (ถ้ามี):', '');
  if (reason === null) return; // Cancelled
  
  const token = localStorage.getItem('admin_token');
  try {
    await axios.put(`${baseUrl}/api/admin/token-requests/${req.id}/reject`, {
      admin_note: reason || 'ไม่ผ่านการตรวจสอบ'
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert(`❌ ปฏิเสธคำขอเรียบร้อยแล้ว`);
    fetchTokenRequests();
  } catch (err) {
    alert(err.response?.data?.msg || 'ปฏิเสธไม่สำเร็จ');
  }
}

onMounted(() => {
  const storedAdmin = localStorage.getItem('admin_user');
  if (storedAdmin) {
    adminUser.value = JSON.parse(storedAdmin);
  }
  fetchData();
});
</script>

<style scoped>
/* Animations */
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-down {
  animation: fadeInDown 0.6s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.1; transform: scale(1); }
  50% { opacity: 0.2; transform: scale(1.1); }
}
.animate-pulse-slow {
  animation: pulse-slow 8s infinite ease-in-out;
}

/* Custom Scrollbar for tables */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>