<template>
  <div class="mb-8">
    <div class="flex items-center gap-2 mb-4">
      <Tags class="w-5 h-5 text-pink-500" />
      <h2 class="text-lg font-bold text-white tracking-wide">หมวดหมู่สินค้า</h2>
    </div>
    
    <div class="relative">
      <div class="flex flex-wrap gap-3">
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          @click="selectCategory(cat.id)"
          class="flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-300 border shrink-0 backdrop-blur-md"
          :class="selectedCategory === cat.id 
            ? 'bg-gradient-to-r from-pink-600 to-purple-600 border-transparent text-white shadow-lg shadow-purple-900/40 scale-105' 
            : 'bg-[#18181b]/80 border-white/5 text-gray-400 hover:text-white hover:bg-white/10 hover:border-white/20'"
        >
          <component :is="getCategoryIcon(cat.id)" class="w-4 h-4" :class="selectedCategory === cat.id ? 'text-white' : 'text-gray-500 group-hover:text-current'" />
          {{ cat.name }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { 
  ShoppingBag, 
  Smartphone, 
  Shirt, 
  Gamepad2, 
  Sparkles, 
  Home, 
  Dumbbell, 
  Utensils, 
  BookOpen, 
  Rocket, 
  PawPrint, 
  Car,
  Tags,
  LayoutGrid
} from 'lucide-vue-next';

const emit = defineEmits(['category-change']);

const selectedCategory = ref('all');

// Default categories (Fallback)
const categories = ref([
  { id: 'all', name: 'ทั้งหมด' },
  { id: 'electronics', name: 'อิเล็กทรอนิกส์' },
  { id: 'fashion', name: 'แฟชั่น' },
  { id: 'gaming', name: 'เกมมิ่ง' },
  { id: 'beauty', name: 'ความงาม' },
  { id: 'home', name: 'บ้าน & สวน' },
  { id: 'sports', name: 'กีฬา' },
  { id: 'food', name: 'อาหาร' },
  { id: 'books', name: 'หนังสือ' },
  { id: 'toys', name: 'ของเล่น' },
  { id: 'pets', name: 'สัตว์เลี้ยง' },
  { id: 'automotive', name: 'ยานยนต์' },
]);

// Icon Mapping
const iconMap = {
  all: ShoppingBag,
  electronics: Smartphone,
  fashion: Shirt,
  gaming: Gamepad2,
  beauty: Sparkles,
  home: Home,
  sports: Dumbbell,
  food: Utensils,
  books: BookOpen,
  toys: Rocket,
  pets: PawPrint,
  automotive: Car
};

function getCategoryIcon(id) {
  return iconMap[id] || LayoutGrid; // Default icon if not found
}

const fetchCategories = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/categories');
    if (res.data && res.data.length > 0) {
      categories.value = res.data.map(c => ({
        ...c,
        name: c.name || c.title 
      }));
    }
  } catch (err) {
    console.log('Using default categories');
  }
};

function selectCategory(id) {
  selectedCategory.value = id;
  emit('category-change', id);
}

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
