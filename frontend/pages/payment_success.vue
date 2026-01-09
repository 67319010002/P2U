<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white p-6">
    <div class="bg-green-600 rounded-full p-4 mb-6">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
    </div>

    <h1 class="text-3xl font-bold mb-2">ชำระเงินสำเร็จ!</h1>
    <p class="text-lg text-gray-300 mb-6 text-center">
      ขอบคุณที่ใช้บริการกับเรา<br />
      ระบบได้รับการชำระเงินของคุณเรียบร้อยแล้ว
    </p>

    <div class="flex gap-4">
      <button
        @click="goToOrders"
        class="bg-pink-600 hover:bg-pink-700 text-white px-6 py-2 rounded-lg transition"
      >
        ดูคำสั่งซื้อ
      </button>

      <button
        @click="goHome"
        class="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded-lg transition"
      >
        กลับไปหน้าแรก
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PaymentSuccess",

  data() {
    return {
      // ✅ เพิ่ม baseUrl ให้ชี้ไปที่ Flask
      baseUrl: 'http://localhost:5000'
    }
  },

  async mounted() {
    // สร้างออเดอร์ให้ผู้ขายทันทีหลังชำระเงินสำเร็จ
    await this.createOrderForSeller();
  },

  methods: {
    async createOrderForSeller() {
      try {
        const token = localStorage.getItem('token');
        
        // ✅ ดึงรายการสินค้าจาก Query หรือ LocalStorage ตามที่คุณเก็บไว้ในหน้า Payment
        // โค้ด Backend ของคุณต้องการ Array ของ ID ในฟิลด์ 'cart_items'
        const itemIds = this.$route.query.items ? this.$route.query.items.split(',') : [];

        if (itemIds.length === 0) {
           console.warn("ไม่พบข้อมูลสินค้าที่จะสร้างออเดอร์");
           return;
        }

        // ✅ เรียก API ไปที่ Port 5000 พร้อมแนบ Token
        const response = await axios.post(`${this.baseUrl}/api/orders`, 
          {
            cart_items: itemIds // ส่งเป็น [id1, id2, ...] ตามที่ Flask รอรับ
          }, 
          {
            headers: { 
              Authorization: `Bearer ${token}` 
            }
          }
        );

        console.log("✅ สร้างออเดอร์สำเร็จ:", response.data);
      } catch (error) {
        console.error("❌ ส่งออเดอร์ให้ผู้ขายไม่สำเร็จ:", error.response?.data || error.message);
      }
    },

    goHome() {
      this.$router.push("/dashboard");
    },

    goToOrders() {
      this.$router.push("/orders");
    },
  },
};
</script>