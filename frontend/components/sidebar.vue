<template>
    <!-- <div @click=""></div>
    <div @click=""></div>

  <div
    @mouseenter="expand = true"
    @mouseleave="expand = false"
    class="fixed left-0 top-0 h-screen bg-gray-900 text-white shadow-lg flex flex-col transition-all duration-300 z-50"
    :class="expand ? 'w-64' : 'w-20'"
  > -->
    <!-- Logo -->
    <!-- <div class="flex items-center justify-center h-16 border-b border-gray-700">
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/5/58/OpenSea_icon.svg"
        alt="logo"
        class="w-8 h-8"
      />
      <span v-if="expand" class="ml-2 text-xl font-semibold whitespace-nowrap">MySea</span>
    </div> -->

    <!-- เมนู -->
    <!-- <nav class="flex-1 overflow-y-auto p-2 space-y-2">

      <div
        v-for="item in topMenuItems"
        :key="item.name"
        @click="navigate(item.route)"
        class="flex items-center p-3 rounded-lg hover:bg-gray-800 cursor-pointer transition-all duration-200"
      >
        <span class="text-xl w-6 text-center">{{ item.icon }}</span>
        <span v-if="expand" class="ml-3 text-sm font-medium">{{ item.name }}</span>
      </div>
    </nav> -->

    <!-- Footer -->
    <!-- <div class="border-t border-gray-800 p-3">
      <div
        class="flex items-center hover:bg-red-600 bg-red-500 rounded-lg p-2 cursor-pointer transition-all"
      >
        <span class="text-xl w-6 text-center">🚪</span>
        <span v-if="expand" class="ml-2">ออกจากระบบ</span>
      </div>
    </div>
  </div> -->
</template>

<script setup>
// import { ref } from 'vue'

// const expand = ref(false)

// const menuItems = [
//   { name: 'Profile', icon: '👤' },
//   { name: 'Settings', icon: '⚙️' },
// ]


function navigate(route) {
  router.push(route)
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('cart')
  router.push('/login')
}
</script>
