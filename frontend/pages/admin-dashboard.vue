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
          
          <div v-if="activeTab === 'orders'">
            <div class="p-6 border-b border-white/10 bg-white/5">
                <h2 class="text-lg font-bold text-white">🛒 รายการสั่งซื้อ</h2>
            </div>
            <div class="overflow-x-auto">
               <table class="w-full">
                  <thead class="bg-black/20 text-gray-400 text-xs uppercase tracking-wider font-semibold">
                     <tr>
                        <th class="text-left p-5">Order ID</th>
                        <th class="text-left p-5">Customer</th>
                        <th class="text-left p-5">Total</th>
                        <th class="text-left p-5">Status</th>
                        <th class="text-left p-5">Date</th>
                     </tr>
                  </thead>
                  <tbody class="divide-y divide-white/5">
                     <tr v-for="order in orders" :key="order.id" class="hover:bg-white/5 transition-colors">
                        <td class="p-5 font-mono text-gray-400 text-sm">#{{ order.id.slice(0,8) }}...</td>
                        <td class="p-5 text-white">{{ order.user?.username }}</td>
                        <td class="p-5 font-mono text-green-400">฿{{ order.total_price.toLocaleString() }}</td>
                        <td class="p-5">
                           <select 
                              v-model="order.status" 
                              @change="updateOrderStatus(order)"
                              class="bg-black/30 text-sm text-white border border-white/10 rounded-lg px-2 py-1 focus:border-red-500 outline-none cursor-pointer"
                           >
                              <option value="pending">🟡 รอตรวจสอบ</option>
                              <option value="processing">🔵 กำลังดำเนินการ</option>
                              <option value="completed">🟢 สำเร็จ</option>
                              <option value="cancelled">🔴 ยกเลิก</option>
                           </select>
                        </td>
                        <td class="p-5 text-gray-500 text-sm">{{ new Date(order.created_at).toLocaleDateString() }}</td>
                     </tr>
                  </tbody>
               </table>
            </div>
          </div>

          <div v-if="activeTab === 'tokens'" class="w-full">
            <div class="p-6 border-b border-white/10 flex items-center justify-between bg-white/5">
              <h2 class="text-lg font-bold text-white flex items-center gap-2">🪙 คำขอเติม Token</h2>
              <div class="flex gap-2 text-xs">
                <span class="bg-yellow-500/20 text-yellow-400 px-3 py-1 rounded-full border border-yellow-500/30">
                  {{ tokenStats.pending || 0 }} รอตรวจสอบ
                </span>
                <span class="bg-green-500/20 text-green-400 px-3 py-1 rounded-full border border-green-500/30">
                  {{ tokenStats.approved || 0 }} อนุมัติแล้ว
                </span>
              </div>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead class="bg-black/20 text-gray-400 text-xs uppercase tracking-wider font-semibold">
                  <tr>
                    <th class="text-left p-5">ผู้ใช้</th>
                    <th class="text-left p-5">จำนวน Token</th>
                    <th class="text-left p-5">สลิป</th>
                    <th class="text-left p-5">สถานะ</th>
                    <th class="text-left p-5">วันที่</th>
                    <th class="text-right p-5">การจัดการ</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-white/5">
                  <tr v-for="req in tokenRequests" :key="req.id" class="hover:bg-white/5 transition-colors">
                    <td class="p-5">
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-gradient-to-r from-yellow-600 to-amber-600 flex items-center justify-center text-xs font-bold text-white">
                           {{ req.user?.username?.charAt(0).toUpperCase() }}
                        </div>
                        <div>
                          <p class="text-white text-sm font-medium">{{ req.user?.username }}</p>
                          <p class="text-gray-500 text-xs">{{ req.user?.email }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="p-5">
                      <p class="text-yellow-400 font-bold text-base font-mono">🪙 {{ req.amount?.toLocaleString() }}</p>
                      <p v-if="req.transaction_ref" class="text-gray-500 text-xs mt-1 font-mono">
                        REF: {{ req.transaction_ref }}
                      </p>
                    </td>
                    <td class="p-5">
                      <div v-if="req.payment_proof_url" class="relative group w-fit">
                        <img 
                          :src="`http://localhost:5000${req.payment_proof_url}`" 
                          alt="Slip" 
                          class="h-12 w-12 object-cover rounded-lg cursor-pointer border border-white/10 group-hover:border-white/30 transition-all"
                          @click="showSlipModal(req)"
                        />
                        <div v-if="req.is_auto_approved" class="absolute -top-2 -right-2 bg-blue-500 text-white text-[10px] px-1.5 py-0.5 rounded-full shadow-lg">
                          AUTO
                        </div>
                      </div>
                      <span v-else class="text-gray-500 text-xs italic">ไม่มีสลิป</span>
                    </td>
                    <td class="p-5">
                      <span 
                        class="px-2 py-1 rounded-md text-xs font-medium border block w-fit"
                        :class="{
                          'bg-yellow-500/10 text-yellow-400 border-yellow-500/20': req.status === 'pending',
                          'bg-green-500/10 text-green-400 border-green-500/20': req.status === 'approved',
                          'bg-red-500/10 text-red-400 border-red-500/20': req.status === 'rejected'
                        }"
                      >
                        {{ req.status === 'pending' ? 'รอตรวจสอบ' : req.status === 'approved' ? 'อนุมัติแล้ว' : 'ปฏิเสธ' }}
                      </span>
                    </td>
                    <td class="p-5 text-gray-500 text-sm">{{ new Date(req.created_at).toLocaleDateString() }}</td>
                    <td class="p-5 text-right">
                      <div v-if="req.status === 'pending'" class="flex gap-2 justify-end">
                        <button @click="approveToken(req)" class="p-2 rounded-lg bg-green-500/10 text-green-400 hover:bg-green-500 hover:text-white border border-green-500/20 transition-all text-sm" title="อนุมัติ">
                          ✓
                        </button>
                        <button @click="rejectToken(req)" class="p-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white border border-red-500/20 transition-all text-sm" title="ปฏิเสธ">
                          ✕
                        </button>
                      </div>
                      <span v-else class="text-xs text-gray-500 italic">{{ req.admin_note || 'เรียบร้อย' }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>

      <div v-if="selectedSlip" class="fixed inset-0 bg-black/90 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click="selectedSlip = null">
        <div class="max-w-xl w-full bg-[#1a1a1f] border border-white/10 rounded-2xl overflow-hidden shadow-2xl animate-fade-in-up" @click.stop>
          <div class="p-5 border-b border-white/10 flex items-center justify-between bg-white/5">
            <h3 class="text-lg font-bold text-white">🧾 รายละเอียดสลิป</h3>
            <button @click="selectedSlip = null" class="text-gray-400 hover:text-white text-2xl leading-none">&times;</button>
          </div>
          
          <div class="p-6">
            <div class="flex flex-col md:flex-row gap-6">
              <div class="w-full md:w-1/2 bg-black rounded-xl overflow-hidden border border-white/10 flex items-center justify-center">
                <img 
                  :src="`http://localhost:5000${selectedSlip.payment_proof_url}`" 
                  alt="Slip Full" 
                  class="w-full h-auto max-h-[400px] object-contain"
                />
              </div>
              
              <div class="w-full md:w-1/2 space-y-4">
                <div class="bg-white/5 rounded-xl p-3 border border-white/5">
                  <p class="text-gray-500 text-xs uppercase mb-1">ผู้ใช้</p>
                  <p class="text-white font-medium">{{ selectedSlip.user?.username }}</p>
                </div>
                
                <div class="bg-white/5 rounded-xl p-3 border border-white/5">
                  <p class="text-gray-500 text-xs uppercase mb-1">จำนวน Token</p>
                  <p class="text-yellow-400 font-bold text-xl font-mono">🪙 {{ selectedSlip.amount?.toLocaleString() }}</p>
                </div>
                
                <div v-if="selectedSlip.transaction_ref" class="bg-white/5 rounded-xl p-3 border border-white/5">
                  <p class="text-gray-500 text-xs uppercase mb-1">เลขอ้างอิง (Ref)</p>
                  <p class="text-white font-mono text-sm break-all">{{ selectedSlip.transaction_ref }}</p>
                </div>
                
                <div v-if="selectedSlip.sender_name" class="bg-white/5 rounded-xl p-3 border border-white/5">
                  <p class="text-gray-500 text-xs uppercase mb-1">ชื่อผู้โอน</p>
                  <p class="text-white text-sm">{{ selectedSlip.sender_name }}</p>
                </div>
                
                <div v-if="selectedSlip.is_auto_approved" class="bg-blue-500/10 border border-blue-500/20 rounded-xl p-3 flex items-center gap-2">
                  <span class="text-blue-400">⚡</span>
                  <p class="text-blue-400 text-xs">ตรวจสอบอัตโนมัติโดย SlipOK</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="p-4 bg-black/20 border-t border-white/10 flex justify-end gap-3">
             <button @click="selectedSlip = null" class="px-4 py-2 rounded-lg text-sm text-gray-400 hover:text-white hover:bg-white/5 transition-colors">ปิดหน้าต่าง</button>
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
// ⚠️ สำคัญมาก: คำสั่งนี้จะปิด Navbar
// แต่ต้องมีไฟล์ layouts/admin.vue ด้วยนะครับ
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

// Fetch Data logic
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
    
    fetchTokenRequests();
  } catch (err) {
    console.error('Failed to fetch admin data:', err);
    if (err.response?.status === 401 || err.response?.status === 403) {
      router.push('/admin-login');
    }
  }
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

// Action Handlers
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
  if (reason === null) return;
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

function handleLogout() {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
  router.push('/admin-login');
}

function showSlipModal(req) {
  selectedSlip.value = req;
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