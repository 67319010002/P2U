<template>
  <div class="min-h-screen bg-[#09090b] text-white p-8 pl-24 pt-28">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
            แอดมินจัดซื้อย่าย
          </h1>
          <p class="text-gray-400 mt-2">จัดการการจัดซื้อและคำสั่งซื้อทั้งหมดที่นี่</p>
        </div>
        <div class="flex items-center gap-3">
           <button class="px-4 py-2 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors">
              Export Report
           </button>
           <button class="px-4 py-2 bg-gradient-to-r from-pink-600 to-purple-600 rounded-xl font-medium hover:opacity-90 transition-opacity">
              + New Order
           </button>
        </div>
      </div>

      <!-- Content Area -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- Stats Cards -->
        <div class="p-6 rounded-2xl bg-[#18181b] border border-white/5">
           <div class="text-gray-400 mb-2">Total Orders</div>
           <div class="text-2xl font-bold">1,245</div>
        </div>
        <div class="p-6 rounded-2xl bg-[#18181b] border border-white/5">
           <div class="text-gray-400 mb-2">Pending Adjustment</div>
           <div class="text-2xl font-bold text-amber-400">45</div>
        </div>
        <div class="p-6 rounded-2xl bg-[#18181b] border border-white/5">
           <div class="text-gray-400 mb-2">Completed Today</div>
           <div class="text-2xl font-bold text-emerald-400">128</div>
        </div>
      </div>

      <div class="rounded-2xl bg-[#18181b]/50 border border-white/5 p-8 flex flex-col items-center justify-center min-h-[400px]">
        <span class="text-6xl mb-4">📦</span>
        <h3 class="text-xl font-medium text-gray-300">Procurement Dashboard</h3>
        <p class="text-gray-500 mt-2">Select an item from the sidebar to manage.</p>
      </div>

    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ["auth"], // Ensure only auth users can access
});
</script>
