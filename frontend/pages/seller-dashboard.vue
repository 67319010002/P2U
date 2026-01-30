<template>
  <div class="min-h-screen ml-20 text-white bg-[#0a0a12] relative overflow-hidden font-sans">
    <sidebar />
    
    <!-- Background Effects -->
    <div class="fixed inset-0 pointer-events-none z-0">
      <div class="absolute top-0 left-1/2 w-[1200px] h-[600px] -translate-x-1/2 bg-gradient-to-b from-purple-900/20 via-pink-900/10 to-transparent rounded-full blur-[100px]"></div>
      <div class="absolute bottom-0 left-0 w-[400px] h-[400px] bg-blue-900/20 rounded-full blur-[80px]"></div>
      <div class="absolute bottom-0 right-0 w-[300px] h-[300px] bg-purple-900/15 rounded-full blur-[60px]"></div>
    </div>

    <main class="relative z-10 p-6 md:p-8">
      <div class="max-w-7xl mx-auto">
        
        <!-- Header -->
        <header class="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p class="text-gray-400 text-sm mb-1">สวัสดี, ยินดีต้อนรับกลับ</p>
            <ClientOnly>
              <h1 class="text-3xl md:text-4xl font-bold text-white">
                {{ user?.shop_name || user?.username || 'ร้านค้าของฉัน' }}
              </h1>
            </ClientOnly>
          </div>
          
          <!-- Search Bar -->
          <div class="relative">
            <input 
              type="text" 
              placeholder="Search..." 
              class="w-64 pl-10 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:bg-white/10 transition-all"
            />
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </header>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          
          <!-- Total Sales -->
          <div class="stat-card group">
            <div class="stat-card-inner bg-gradient-to-br from-emerald-500/10 to-green-600/5">
              <div class="flex items-center justify-between mb-4">
                <span class="text-gray-400 text-sm font-medium">ยอดขายรวม</span>
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-400 to-green-500 flex items-center justify-center shadow-lg shadow-emerald-500/30">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
              </div>
              <p class="text-3xl font-bold text-emerald-400 mb-1">฿{{ formatNumber(stats.total_sales) }}</p>
              <p class="text-xs text-emerald-400/60 flex items-center gap-1">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/></svg>
                รายได้เพิ่มขึ้น +12.5%
              </p>
            </div>
          </div>

          <!-- Products Count -->
          <div class="stat-card group">
            <div class="stat-card-inner bg-gradient-to-br from-pink-500/10 to-rose-600/5">
              <div class="flex items-center justify-between mb-4">
                <span class="text-gray-400 text-sm font-medium">จำนวนสินค้า</span>
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-pink-400 to-rose-500 flex items-center justify-center shadow-lg shadow-pink-500/30">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                  </svg>
                </div>
              </div>
              <p class="text-3xl font-bold text-white mb-1">{{ stats.total_products || 0 }}</p>
              <p class="text-xs text-pink-400/60">เพิ่มขึ้น {{ products.length > 5 ? products.length - 5 : 0 }} รายการ</p>
            </div>
          </div>

          <!-- Rating -->
          <div class="stat-card group">
            <div class="stat-card-inner bg-gradient-to-br from-amber-500/10 to-yellow-600/5">
              <div class="flex items-center justify-between mb-4">
                <span class="text-gray-400 text-sm font-medium">คะแนนเฉลี่ย</span>
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-400 to-yellow-500 flex items-center justify-center shadow-lg shadow-amber-500/30">
                  <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </div>
              </div>
              <div class="flex items-center gap-2 mb-1">
                <p class="text-3xl font-bold text-white">{{ stats.rating_avg?.toFixed(1) || '0.0' }}</p>
                <span class="text-amber-400 text-lg">/ 5.0</span>
              </div>
              <div class="flex gap-0.5">
                <svg v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= Math.round(stats.rating_avg || 0) ? 'text-amber-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <span class="text-xs text-gray-500 ml-2">จาก {{ reviews.length }} รีวิว</span>
              </div>
            </div>
          </div>

          <!-- Store Level -->
          <div class="stat-card group">
            <div class="stat-card-inner bg-gradient-to-br from-purple-500/10 to-violet-600/5">
              <div class="flex items-center justify-between mb-4">
                <span class="text-gray-400 text-sm font-medium">ระดับร้านค้า</span>
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400 to-violet-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
                  <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5 2a2 2 0 00-2 2v14l3.5-2 3.5 2 3.5-2 3.5 2V4a2 2 0 00-2-2H5zM10 12a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                  </svg>
                </div>
              </div>
              <p class="text-2xl font-bold mb-1" :class="getLevelTextClass(stats.ai_level)">{{ getLevelName(stats.ai_level) }}</p>
              <p class="text-xs text-purple-400/60">สิทธิพิเศษมากขึ้น</p>
            </div>
          </div>
        </div>

        <!-- Main Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <!-- Products Section -->
          <div class="lg:col-span-2">
            <div class="card">
              <div class="card-header">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-pink-500/20 flex items-center justify-center">
                    <svg class="w-4 h-4 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
                    </svg>
                  </div>
                  <h2 class="text-lg font-semibold text-white">รายการสินค้า</h2>
                </div>
                <div class="flex items-center gap-2">
                  <button class="px-3 py-1.5 text-xs font-medium text-gray-400 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition-colors flex items-center gap-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
                    </svg>
                    Filter
                  </button>
                  <NuxtLink to="/AddProduct" class="px-4 py-1.5 text-xs font-bold text-white bg-gradient-to-r from-pink-500 to-purple-500 rounded-lg hover:from-pink-600 hover:to-purple-600 transition-all shadow-lg shadow-pink-500/20">
                    + เพิ่มสินค้าใหม่
                  </NuxtLink>
                </div>
              </div>
              
              <div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-3">
                <div 
                  v-for="product in products.slice(0, 6)" 
                  :key="product.id || product._id" 
                  class="product-card group"
                >
                  <img 
                    :src="getImageUrl(product.image_url)" 
                    :alt="product.name"
                    class="w-16 h-16 rounded-xl object-cover shadow-md group-hover:shadow-lg transition-shadow" 
                    @error="(e) => e.target.src = '/placeholder.png'" 
                  />
                  <div class="flex-1 min-w-0">
                    <p class="text-white font-medium truncate text-sm group-hover:text-pink-300 transition-colors">{{ product.name }}</p>
                    <p class="text-lg font-bold text-emerald-400">฿{{ formatNumber(product.price) }}</p>
                    <div class="flex items-center gap-2 mt-1">
                      <span class="text-[10px] px-2 py-0.5 rounded-md bg-blue-500/20 text-blue-400 border border-blue-500/30">
                        Stock: {{ product.stock || 0 }}
                      </span>
                    </div>
                  </div>
                  <div class="flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <NuxtLink :to="`/edit-product/${product.id || product._id}`" class="w-8 h-8 rounded-lg bg-pink-500/10 hover:bg-pink-500 text-pink-400 hover:text-white flex items-center justify-center transition-all">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                    </NuxtLink>
                    <button @click="deleteProduct(product.id || product._id)" class="w-8 h-8 rounded-lg bg-red-500/10 hover:bg-red-500 text-red-400 hover:text-white flex items-center justify-center transition-all">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                    </button>
                  </div>
                </div>
                
                <div v-if="!products.length" class="col-span-2 p-12 text-center">
                  <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-800 flex items-center justify-center">
                    <svg class="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                    </svg>
                  </div>
                  <p class="text-gray-400">ยังไม่มีสินค้า</p>
                </div>
              </div>
            </div>

            <!-- Reviews Section -->
            <div class="card mt-6">
              <div class="card-header">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center">
                    <svg class="w-4 h-4 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                  </div>
                  <h2 class="text-lg font-semibold text-white">รีวิวจากลูกค้า</h2>
                </div>
              </div>
              
              <div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="review in reviews.slice(0, 4)" :key="review.id" class="review-card">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex gap-0.5">
                      <svg v-for="i in 5" :key="i" class="w-4 h-4" :class="i <= review.rating ? 'text-amber-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                      </svg>
                    </div>
                    <span class="text-[10px] text-gray-500">{{ formatDate(review.created_at) }}</span>
                  </div>
                  <p class="text-gray-300 text-sm line-clamp-2 mb-2">{{ review.comment }}</p>
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-full bg-gradient-to-br from-pink-500 to-purple-500 flex items-center justify-center text-[10px] text-white font-bold">
                      {{ review.user?.username?.charAt(0)?.toUpperCase() || 'U' }}
                    </div>
                    <span class="text-xs text-gray-400">{{ review.user?.username || 'ผู้ใช้' }}</span>
                  </div>
                </div>
                
                <div v-if="!reviews.length" class="col-span-2 p-8 text-center">
                  <p class="text-gray-400">ยังไม่มีรีวิว</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Orders Section -->
          <div class="lg:col-span-1">
            <div class="card h-full">
              <div class="card-header">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center">
                    <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                    </svg>
                  </div>
                  <h2 class="text-lg font-semibold text-white">คำสั่งซื้อล่าสุด</h2>
                </div>
                <div class="relative">
                  <input type="text" placeholder="Search" class="w-28 pl-7 pr-2 py-1 text-xs rounded-lg bg-white/5 border border-white/10 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50"/>
                  <svg class="absolute left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                  </svg>
                </div>
              </div>
              
              <div class="divide-y divide-white/5 max-h-[600px] overflow-y-auto custom-scrollbar">
                <div 
                  v-for="order in recentOrders" 
                  :key="order.id" 
                  @click="selectedOrder = order"
                  class="order-row group"
                >
                  <div class="flex items-center gap-3 flex-1 min-w-0">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center text-sm font-bold text-white">
                      {{ order.user?.charAt(0)?.toUpperCase() || 'U' }}
                    </div>
                    <div class="min-w-0 flex-1">
                      <p class="text-white font-medium text-sm truncate group-hover:text-pink-300 transition-colors">{{ order.user }}</p>
                      <p class="text-[10px] text-gray-500">{{ order.items_count }} รายการ</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="text-emerald-400 font-bold text-sm">฿{{ formatNumber(order.total) }}</p>
                    <span :class="getStatusClass(order.status)" class="text-[10px] px-2 py-0.5 rounded-md font-medium">
                      {{ getStatusLabel(order.status) }}
                    </span>
                  </div>
                </div>
                
                <div v-if="!recentOrders.length" class="p-8 text-center">
                  <p class="text-gray-400 text-sm">ยังไม่มีคำสั่งซื้อ</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Order Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedOrder" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click.self="selectedOrder = null">
          <div class="card w-full max-w-lg animate-modal">
            <div class="card-header bg-gradient-to-r from-pink-500/10 to-purple-500/10 border-b border-white/5">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-pink-500/20 flex items-center justify-center">
                  <svg class="w-5 h-5 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                <div>
                  <h2 class="text-lg font-bold text-white">รายละเอียดคำสั่งซื้อ</h2>
                  <p class="text-xs text-gray-500 font-mono">#{{ selectedOrder.id?.slice(-8)?.toUpperCase() }}</p>
                </div>
              </div>
              <button @click="selectedOrder = null" class="w-8 h-8 rounded-lg bg-white/5 hover:bg-white/10 flex items-center justify-center text-gray-400 hover:text-white transition-all">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
            
            <div class="p-6 space-y-6 max-h-[60vh] overflow-y-auto custom-scrollbar">
              <div class="flex justify-between items-start">
                <div>
                  <p class="text-xs text-gray-500 uppercase tracking-wider mb-1">ผู้ซื้อ</p>
                  <p class="text-white text-lg font-semibold">{{ selectedOrder.user }}</p>
                </div>
                <span :class="getStatusClass(selectedOrder.status)" class="text-xs px-3 py-1 rounded-lg font-medium">
                  {{ getStatusLabel(selectedOrder.status) }}
                </span>
              </div>

              <div>
                <p class="text-xs text-pink-400 uppercase tracking-wider mb-3 font-medium">รายการสินค้า</p>
                <div class="space-y-2">
                  <div v-for="item in selectedOrder.rawItems" :key="item.product_id" class="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/5">
                    <img :src="getImageUrl(item.image)" class="w-12 h-12 rounded-lg object-cover" />
                    <div class="flex-1 min-w-0">
                      <p class="text-white text-sm font-medium truncate">{{ item.product_name }}</p>
                      <p class="text-gray-500 text-xs">x{{ item.quantity }}</p>
                    </div>
                    <p class="text-white font-bold">฿{{ formatNumber(item.price * item.quantity) }}</p>
                  </div>
                </div>
              </div>

              <div class="pt-4 border-t border-white/10 flex justify-between items-center">
                <span class="text-gray-400">ยอดรวม</span>
                <span class="text-2xl font-bold text-emerald-400">฿{{ formatNumber(selectedOrder.total) }}</span>
              </div>
            </div>

            <div class="p-6 border-t border-white/5 bg-white/[0.02]">
              <button 
                v-if="selectedOrder.status === 'paid'" 
                :disabled="isUpdating"
                @click="updateOrderStatus(selectedOrder.id, 'processing')"
                class="w-full py-3 rounded-xl bg-gradient-to-r from-pink-500 to-purple-500 text-white font-bold hover:from-pink-600 hover:to-purple-600 transition-all shadow-lg shadow-pink-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <svg v-if="isUpdating" class="animate-spin w-5 h-5" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/></svg>
                <span v-if="isUpdating">กำลังดำเนินการ...</span>
                <span v-else>ยืนยันการจัดส่ง</span>
              </button>
              <button v-else @click="selectedOrder = null" class="w-full py-3 rounded-xl bg-white/10 text-white font-medium hover:bg-white/20 transition-all">
                ปิด
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user = ref(null);
const isUpdating = ref(false);
const stats = ref({ total_sales: 0, total_products: 0, rating_avg: 0, ai_level: 'C' });
const products = ref([]);
const reviews = ref([]);
const recentOrders = ref([]);
const selectedOrder = ref(null);
const baseUrl = 'http://localhost:5000';

function formatNumber(num) {
  if (!num) return '0';
  return new Intl.NumberFormat('th-TH').format(num);
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('th-TH', { day: '2-digit', month: '2-digit', year: '2-digit' });
}

function getImageUrl(url) {
  if (!url) return '/placeholder.png';
  if (url.startsWith('http')) return url;
  return `${baseUrl}${url.startsWith('/') ? '' : '/'}${url}`;
}

function getLevelName(level) {
  const names = { S: 'เพชร (Diamond)', A: 'ทอง (Gold)', B: 'เงิน (Silver)', C: 'ทองแดง (Bronze)' };
  return names[level] || 'ทองแดง (Bronze)';
}

function getLevelTextClass(level) {
  const classes = { S: 'text-cyan-400', A: 'text-amber-400', B: 'text-gray-300', C: 'text-orange-400' };
  return classes[level] || 'text-orange-400';
}

function getStatusClass(status) {
  const classes = { 
    pending: 'bg-amber-500/20 text-amber-400 border border-amber-500/30', 
    paid: 'bg-pink-500/20 text-pink-400 border border-pink-500/30', 
    processing: 'bg-blue-500/20 text-blue-400 border border-blue-500/30', 
    completed: 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30', 
    cancelled: 'bg-red-500/20 text-red-400 border border-red-500/30' 
  };
  return classes[status] || 'bg-white/10 text-white';
}

function getStatusLabel(status) {
  const labels = { pending: 'รอชำระ', paid: 'ชำระแล้ว', processing: 'กำลังส่ง', completed: 'สำเร็จ', cancelled: 'ยกเลิก' };
  return labels[status] || status;
}

async function deleteProduct(productId) {
  if (!confirm('คุณต้องการลบสินค้านี้ใช่หรือไม่?')) return;
  const token = localStorage.getItem('token');
  try {
    await axios.delete(`${baseUrl}/api/seller/products/${productId}`, { headers: { Authorization: `Bearer ${token}` } });
    alert('ลบสินค้าสำเร็จ!');
    await fetchData();
  } catch (err) {
    alert('ไม่สามารถลบสินค้าได้');
  }
}

async function updateOrderStatus(orderId, newStatus) {
  if (isUpdating.value) return;
  const token = localStorage.getItem('token');
  if (!confirm('ยืนยันการจัดส่งสินค้า?')) return;
  isUpdating.value = true;
  try {
    await axios.put(`${baseUrl}/api/orders/${orderId}/status`, { status: newStatus }, { headers: { Authorization: `Bearer ${token}` } });
    alert('อัปเดตสถานะสำเร็จ!');
    selectedOrder.value = null;
    await fetchData();
  } catch (err) {
    alert('ไม่สามารถอัปเดตสถานะได้');
  } finally {
    isUpdating.value = false;
  }
}

async function fetchData() {
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    const profileRes = await axios.get(`${baseUrl}/api/profile`, { headers: { Authorization: `Bearer ${token}` } });
    user.value = profileRes.data;
    const currentId = user.value.id || user.value._id;
    stats.value = { ...stats.value, total_sales: profileRes.data.total_sales || 0, rating_avg: profileRes.data.rating_avg || 0, ai_level: profileRes.data.ai_level || 'C' };
    const productsRes = await axios.get(`${baseUrl}/api/products`);
    products.value = productsRes.data.filter(p => String(p.seller?.id || p.seller?._id || p.seller) === String(currentId));
    stats.value.total_products = products.value.length;
    const reviewsRes = await axios.get(`${baseUrl}/api/reviews/seller/${currentId}`);
    reviews.value = reviewsRes.data.reviews || [];
    const ordersRes = await axios.get(`${baseUrl}/api/orders/seller/${currentId}`, { headers: { Authorization: `Bearer ${token}` } });
    recentOrders.value = (ordersRes.data.orders || []).map(o => ({ id: o.id || o._id, user: o.buyer?.username || 'ไม่ทราบ', items_count: o.items?.length || 0, total: o.total_price || 0, status: o.status, rawItems: o.items || [] }));
  } catch (err) { console.error('Fetch error:', err); }
}

onMounted(fetchData);
</script>

<style scoped>
.stat-card {
  position: relative;
  border-radius: 1.25rem;
  background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  overflow: hidden;
  transition: all 0.3s ease;
}
.stat-card:hover { transform: translateY(-2px); border-color: rgba(255,255,255,0.15); }
.stat-card-inner { padding: 1.5rem; position: relative; }

.card {
  background: rgba(15, 15, 20, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 1.5rem;
  overflow: hidden;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.product-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 1rem;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
  transition: all 0.2s ease;
  cursor: pointer;
}
.product-card:hover { background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1); }

.review-card {
  padding: 1rem;
  border-radius: 1rem;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
}

.order-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.order-row:hover { background: rgba(255,255,255,0.03); }

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }

.modal-enter-active, .modal-leave-active { transition: all 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.animate-modal { animation: zoomIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes zoomIn { from { opacity: 0; transform: scale(0.95) translateY(10px); } to { opacity: 1; transform: scale(1) translateY(0); } }
</style>