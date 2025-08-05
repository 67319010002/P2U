<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm">
      <h1 class="text-2xl font-bold text-white text-center mb-6">Login</h1>

      <input
        v-model="username"
        placeholder="Username"
        class="input-style"
        autocomplete="username"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="input-style"
        autocomplete="current-password"
      />

      <button
        @click="handleLogin"
        class="bg-black hover:bg-gray-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white mt-4"
      >
        Login
      </button>

      <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">
        {{ errorMsg }}
      </p>

      <div class="text-center text-sm text-gray-400 mt-4">
        Don’t have an account?
        <router-link to="/register" class="underline hover:text-white">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleLogin = async () => {
  errorMsg.value = ''
  if (!username.value || !password.value) {
    errorMsg.value = 'Please enter username and password.'
    return
  }

  try {
    const res = await axios.post('http://localhost:5000/api/login', {
      username: username.value,
      password: password.value
    })

    const user = res.data.user

    localStorage.setItem('token', res.data.access_token)

    if (user) {
      localStorage.setItem('user', JSON.stringify({
        id: user.id,
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        profile_image_url: user.profile_image_url,
        is_seller: user.is_seller
      }))
      // เพิ่มบรรทัดนี้เพื่อแจ้ง Navbar รีโหลด user ใหม่
      window.dispatchEvent(new Event('user-updated'))
    }

    router.push('/dashboard')
  } catch (err) {
    errorMsg.value =
      err.response?.data?.msg || 'Login failed. Please try again.'
  }
}
</script>

<style lang="postcss" scoped>
.input-style {
  @apply mb-4 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400
    focus:outline-none focus:ring-2 focus:ring-white focus:border-white;
}
</style>
