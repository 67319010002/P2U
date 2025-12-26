<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />
    
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-white flex items-center gap-2">
            📦 ประวัติคำสั่งซื้อ
          </h1>
          <p class="text-dark-400 mt-1">ดูรายละเอียดคำสั่งซื้อทั้งหมดของคุณ</p>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="flex gap-2 mb-6">
        <button 
          v-for="filter in filters" 
          :key="filter.value"
          @click="activeFilter = filter.value"
          class="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
          :class="activeFilter === filter.value ? 'bg-primary-500 text-white' : 'glass text-dark-300 hover:text-white'"
        >
          {{ filter.label }}
        </button>
      </div>

      <!-- Orders List -->
      <div v-if="filteredOrders.length" class="space-y-4">
        <div 
          v-for="order in filteredOrders" 
          :key="order.id" 
          class="card p-5 hover:shadow-glow-sm transition-all cursor-pointer"
          @click="selectedOrder = order"
        >
          <div class="flex items-start justify-between mb-4">
            <div>
              <p class="text-dark-400 text-sm">Order ID</p>
              <p class="text-white font-mono">{{ order.id }}</p>
            </div>
            <span :class="getStatusClass(order.status)" class="badge">
              {{ getStatusLabel(order.status) }}
            </span>
          </div>

          <!-- Items Preview -->
          <div class="flex items-center gap-3 mb-4">
            <div v-for="(item, idx) in order.items.slice(0, 3)" :key="idx" class="relative">
              <img :src="item.product_image || '/placeholder.png'" class="w-16 h-16 rounded-lg object-cover border border-white/10" />
              <span v-if="item.quantity > 1" class="absolute -top-2 -right-2 bg-primary-500 text-white text-xs font-bold px-1.5 py-0.5 rounded-full">
                x{{ item.quantity }}
              </span>
            </div>
            <div v-if="order.items.length > 3" class="w-16 h-16 rounded-lg bg-dark-700 flex items-center justify-center text-dark-400 text-sm">
              +{{ order.items.length - 3 }}
            </div>
          </div>

          <div class="flex items-center justify-between pt-4 border-t border-white/10">
            <p class="text-dark-400 text-sm">{{ order.created_at }}</p>
            <p class="text-xl font-bold text-green-400">฿{{ order.total_price.toLocaleString() }}</p>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="card p-12 text-center">
        <div class="w-20 h-20 rounded-full bg-dark-700 mx-auto mb-4 flex items-center justify-center text-4xl">
          📦
        </div>
        <h3 class="text-lg font-semibold text-white mb-2">ยังไม่มีคำสั่งซื้อ</h3>
        <p class="text-dark-400 mb-6">เมื่อคุณสั่งซื้อสินค้า รายการจะแสดงที่นี่</p>
        <NuxtLink to="/dashboard" class="btn-primary">
          🛒 เลือกซื้อสินค้า
        </NuxtLink>
      </div>

      <!-- Order Detail Modal -->
      <Teleport to="body">
        <Transition name="fade">
          <div v-if="selectedOrder" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="selectedOrder = null">
            <div class="glass rounded-2xl w-full max-w-lg max-h-[80vh] overflow-auto animate-in">
              <div class="p-6 border-b border-white/10">
                <div class="flex items-center justify-between">
                  <h2 class="text-lg font-semibold text-white">รายละเอียดคำสั่งซื้อ</h2>
                  <button @click="selectedOrder = null" class="text-dark-400 hover:text-white text-2xl">&times;</button>
                </div>
              </div>
              
              <div class="p-6 space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-dark-400">Order ID</span>
                  <span class="text-white font-mono text-sm">{{ selectedOrder.id }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-dark-400">สถานะ</span>
                  <span :class="getStatusClass(selectedOrder.status)" class="badge">{{ getStatusLabel(selectedOrder.status) }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-dark-400">วันที่สั่ง</span>
                  <span class="text-white">{{ selectedOrder.created_at }}</span>
                </div>

                <div class="border-t border-white/10 pt-4">
                  <p class="text-dark-400 mb-3">รายการสินค้า</p>
                  <div class="space-y-3">
                    <div v-for="item in selectedOrder.items" :key="item.product_id" class="flex items-center gap-3">
                      <img :src="item.product_image || '/placeholder.png'" class="w-12 h-12 rounded-lg object-cover" />
                      <div class="flex-1">
                        <p class="text-white text-sm">{{ item.product_name }}</p>
                        <p class="text-dark-400 text-xs">x{{ item.quantity }}</p>
                      </div>
                      <p class="text-green-400 font-medium">฿{{ (item.price * item.quantity).toLocaleString() }}</p>
                    </div>
                  </div>
                </div>

                <div class="border-t border-white/10 pt-4 flex justify-between items-center">
                  <span class="text-lg font-semibold text-white">ยอดรวม</span>
                  <span class="text-2xl font-bold text-green-400">฿{{ selectedOrder.total_price.toLocaleString() }}</span>
                </div>

                <button 
                  v-if="selectedOrder.status === 'pending'" 
                  @click="cancelOrder(selectedOrder)"
                  class="w-full btn-glass text-red-400 hover:bg-red-500/20 mt-4"
                >
                  ยกเลิกคำสั่งซื้อ
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const orders = ref([]);
const selectedOrder = ref(null);
const activeFilter = ref('all');

const filters = [
  { label: 'ทั้งหมด', value: 'all' },
  { label: 'รอดำเนินการ', value: 'pending' },
  { label: 'กำลังดำเนินการ', value: 'processing' },
  { label: 'สำเร็จ', value: 'completed' },
  { label: 'ยกเลิก', value: 'cancelled' },
];

const filteredOrders = computed(() => {
  if (activeFilter.value === 'all') return orders.value;
  return orders.value.filter(o => o.status === activeFilter.value);
});

function getStatusClass(status) {
  const classes = {
    pending: 'badge-warning',
    processing: 'badge-primary',
    completed: 'badge-success',
    cancelled: 'badge-error',
  };
  return classes[status] || 'badge-primary';
}

function getStatusLabel(status) {
  const labels = {
    pending: '⏳ รอดำเนินการ',
    processing: '🔄 กำลังดำเนินการ',
    completed: '✓ สำเร็จ',
    cancelled: '✕ ยกเลิก',
  };
  return labels[status] || status;
}

async function fetchOrders() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get('http://localhost:5000/api/orders', {
      headers: { Authorization: `Bearer ${token}` }
    });
    orders.value = res.data.orders || [];
  } catch (err) {
    console.error('Failed to fetch orders:', err);
  }
}

async function cancelOrder(order) {
  if (!confirm('ยืนยันการยกเลิกคำสั่งซื้อ?')) return;
  
  const token = localStorage.getItem('token');
  try {
    await axios.put(`http://localhost:5000/api/orders/${order.id}/cancel`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    order.status = 'cancelled';
    selectedOrder.value = null;
  } catch (err) {
    console.error('Failed to cancel order:', err);
    alert(err.response?.data?.msg || 'ไม่สามารถยกเลิกได้');
  }
}

onMounted(fetchOrders);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
