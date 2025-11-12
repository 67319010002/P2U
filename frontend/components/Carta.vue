<template>
  <div class="category-container text-center mt-12">
    <h1 class="text-2xl font-bold mb-6">หมวดหมู่</h1>

    <div class="category grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6 p-6">
      <div
        v-for="(item, index) in categories"
        :key="index"
        class="item bg-red-500 p-4 rounded-xl shadow-lg text-center relative"
      >
        <!-- คลิกเพื่ออัปโหลดรูป -->
        <div
          class="image-placeholder bg-gray-300 w-20 h-20 mx-auto mb-4 overflow-hidden cursor-pointer hover:opacity-80 transition"
          @click="triggerFileInput(index)"
        >
          <img
            v-if="item.imageUrl"
            :src="item.imageUrl"
            alt="Category Image"
            class="w-full h-full object-cover"
          />
          <p v-else class="text-white text-xs">คลิกรูปเพื่ออัปโหลด</p>
        </div>

        <!-- Hidden File Input -->
        <input
          type="file"
          accept="image/*"
          class="hidden"
          :id="`fileInput-${index}`"
          @change="onFileChange($event, index)"
        />

        <p class="mt-3 text-sm text-white font-semibold">{{ item.name }}</p>
        <p class="mt-2 text-xs text-gray-200">{{ item.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categories: [
        { name: 'ความงามและของใช้ส่วนตัว', description: 'สินค้าเครื่องสำอางและของใช้ส่วนตัว', imageUrl: null },
        { name: 'เสื้อผ้าผู้ชาย', description: 'เสื้อผ้าสำหรับผู้ชาย', imageUrl: null },
        { name: 'กระเป๋า', description: 'กระเป๋าหลายแบบ', imageUrl: null },
        { name: 'รองเท้าผู้หญิง', description: 'รองเท้าสำหรับผู้หญิง', imageUrl: null },
        { name: 'นาฬิกาและแว่นตา', description: 'นาฬิกาและแว่นตาแฟชั่น', imageUrl: null },
        { name: 'อุปกรณ์อิเล็กทรอนิกส์', description: 'อุปกรณ์ไอทีและเครื่องใช้ไฟฟ้า', imageUrl: null },
        { name: 'เครื่องประดับ', description: 'เครื่องประดับหลากหลายประเภท', imageUrl: null },
        { name: 'เครื่องใช้ในบ้าน', description: 'อุปกรณ์ตกแต่งและใช้ในบ้าน', imageUrl: null },
        { name: 'มือถือและแท็บเล็ต', description: 'มือถือและแท็บเล็ตยอดนิยม', imageUrl: null },
        { name: 'คอมพิวเตอร์และแลปท็อป', description: 'คอมพิวเตอร์และโน้ตบุ๊ก', imageUrl: null },
        { name: 'อาหารและเครื่องดื่ม', description: 'อาหารและเครื่องดื่มหลากหลายประเภท', imageUrl: null },
        { name: 'กีฬาและอุปกรณ์การออกกำลังกาย', description: 'อุปกรณ์กีฬาและการออกกำลังกาย', imageUrl: null }
      ]
    };
  },
  methods: {
    triggerFileInput(index) {
      // ใช้ querySelector เพื่อกด input ของ index นั้น
      const input = document.getElementById(`fileInput-${index}`);
      if (input) input.click();
    },
    onFileChange(event, index) {
      const file = event.target.files[0];
      if (file) {
        const imageUrl = URL.createObjectURL(file);
        this.categories[index].imageUrl = imageUrl;

        // ✅ ถ้าอยากอัปโหลดไป backend (เช่น Flask / Node.js)
        // const formData = new FormData();
        // formData.append('image', file);
        // axios.post('/api/upload', formData)
        //   .then(res => this.categories[index].imageUrl = res.data.url);
      }
    }
  }
};
</script>

<style scoped>
.category-container {
  margin-top: 50px;
}

.category {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  justify-content: center;
  padding: 20px;
}

.item {
  background-color: #a35ea3;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  color: white;
  transition: transform 0.2s ease;
}

.item:hover {
  transform: scale(1.05);
}

.image-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  background-color: #f3f4f6;
  color: #6b7280;
  font-size: 12px;
}
</style>
