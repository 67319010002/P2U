<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm">
      <h1 class="text-2xl font-bold text-white text-center mb-6">Register</h1>

      <!-- บัญชี -->
      <input v-model="username" placeholder="Username" class="input-style" />
      <input v-model="email" type="email" placeholder="Email" class="input-style" />
      <input v-model="password" type="password" placeholder="Password" class="input-style" />

      <!-- ข้อมูลส่วนตัว -->
      <input v-model="fullName" placeholder="Full Name" class="input-style" />
      <input v-model="phoneNumber" placeholder="Phone Number" class="input-style" />

      <!-- ข้อมูลที่อยู่ -->
      <input v-model="addressName" placeholder="Receiver's Name" class="input-style" />
      <input v-model="addressPhone" placeholder="Receiver's Phone" class="input-style" />
      <input v-model="addressLine" placeholder="Address Line" class="input-style" />
      <input v-model="district" placeholder="District" class="input-style" />
      <input v-model="province" placeholder="Province" class="input-style" />
      <input v-model="postalCode" placeholder="Postal Code" class="input-style" />

      <!-- ตัวเลือกผู้ขาย -->
      <label class="flex items-center text-sm text-white mb-4">
        <input v-model="isSeller" type="checkbox" class="mr-2" />
        Register as seller
      </label>

      <!-- รูปโปรไฟล์ -->
      <input
        type="file"
        @change="onFileChange"
        accept="image/*"
        class="mb-4 p-3 w-full text-sm text-gray-400 file:bg-gray-700 file:border-none file:p-2 file:text-white rounded-lg bg-gray-700"
      />
      <div v-if="imagePreview" class="mb-4 text-center">
        <img :src="imagePreview" alt="Preview" class="w-24 h-24 rounded-full mx-auto object-cover border" />
        <p class="text-gray-400 text-xs mt-1">Image Preview</p>
      </div>

      <!-- ปุ่มสมัคร -->
      <button
        @click="handleRegister"
        class="bg-black hover:bg-gray-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      >
        Register
      </button>

      <!-- แจ้งเตือน -->
      <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">{{ errorMsg }}</p>
      <p v-if="successMsg" class="text-green-400 text-sm mt-4 text-center">{{ successMsg }}</p>

      <!-- ลิงก์ไปหน้าเข้าสู่ระบบ -->
      <div class="text-center text-sm text-gray-400 mt-4">
        Already have an account?
        <router-link to="/login" class="underline hover:text-white">Login</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ข้อมูล
const username = ref('')
const email = ref('')
const password = ref('')
const fullName = ref('')
const phoneNumber = ref('')
const addressName = ref('')
const addressPhone = ref('')
const addressLine = ref('')
const district = ref('')
const province = ref('')
const postalCode = ref('')
const isSeller = ref(false)
const profileImage = ref(null)
const imagePreview = ref(null)

const errorMsg = ref('')
const successMsg = ref('')

const onFileChange = (e) => {
  const file = e.target.files[0]
  profileImage.value = file
  if (file) {
    imagePreview.value = URL.createObjectURL(file)
  }
}

const handleRegister = async () => {
  errorMsg.value = ''
  successMsg.value = ''

  if (!username.value || !email.value || !password.value || !fullName.value) {
    errorMsg.value = 'Please fill in all required fields.'
    return
  }

  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('email', email.value)
    formData.append('password', password.value)
    formData.append('full_name', fullName.value)
    formData.append('phone_number', phoneNumber.value)
    formData.append('is_seller', isSeller.value ? 'true' : 'false')

    formData.append('address_name', addressName.value)
    formData.append('address_phone', addressPhone.value)
    formData.append('address_line', addressLine.value)
    formData.append('district', district.value)
    formData.append('province', province.value)
    formData.append('postal_code', postalCode.value)

    if (profileImage.value) {
      formData.append('profile_image', profileImage.value)
    }

    const res = await axios.post('http://localhost:5000/api/register', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    successMsg.value = res.data.msg || 'Registration successful.'
    setTimeout(() => router.push('/login'), 1500)
  } catch (err) {
    console.error('[Register error]', err)
    errorMsg.value = err.response?.data?.msg || 'Registration failed.'
  }
}
</script>

<style scoped lang="postcss">
.input-style {
  @apply mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white;
}
</style>
