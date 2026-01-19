<template>
  <div class="min-h-screen p-6 md:p-8">
    <!-- Header Section -->
    <div class="max-w-6xl mx-auto mb-8">
      <div class="flex items-center gap-4 mb-2">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center shadow-lg shadow-pink-500/25">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <h1 class="text-2xl md:text-3xl font-bold text-white">AI Price Estimator</h1>
          <p class="text-gray-400 text-sm">Upload product images to get AI-powered price recommendations</p>
        </div>
      </div>
    </div>

    <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Upload Section -->
      <div class="lg:col-span-2">
        <div class="card p-6 relative overflow-hidden">
          <!-- Decorative gradient -->
          <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-pink-500/10 to-purple-600/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
          
          <div class="relative">
            <h2 class="text-lg font-semibold text-white mb-6 flex items-center gap-3">
              <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-pink-500/20 to-purple-600/20 border border-pink-500/30 flex items-center justify-center">
                <svg class="w-4 h-4 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </span>
              Upload Product Image
            </h2>

            <!-- Upload Zone -->
            <div 
              class="upload-zone"
              :class="{ 'active': isDragging, 'has-image': imagePreview }"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
              @click="triggerFileInput"
            >
              <input 
                type="file" 
                ref="fileInput" 
                accept="image/*" 
                class="hidden" 
                @change="handleFileSelect"
              />
              
              <div v-if="!imagePreview" class="text-center">
                <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-dark-700 to-dark-800 border border-white/10 flex items-center justify-center">
                  <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                <p class="text-white font-medium mb-1">Drop your image here</p>
                <p class="text-gray-500 text-sm mb-4">or click to browse</p>
                <span class="text-xs text-gray-600">Supports: JPG, PNG, WebP (Max 10MB)</span>
              </div>

              <div v-else class="relative">
                <img :src="imagePreview" alt="Preview" class="max-h-64 mx-auto rounded-xl shadow-lg" />
                <button 
                  @click.stop="clearImage"
                  class="absolute top-2 right-2 w-8 h-8 rounded-full bg-red-500/80 hover:bg-red-500 text-white flex items-center justify-center transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Submit Button -->
            <button 
              @click="handleSubmit"
              :disabled="!selectedImage || isLoading"
              class="w-full mt-6 btn-primary flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              <svg v-if="isLoading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              {{ isLoading ? 'Analyzing...' : 'Analyze with AI' }}
            </button>
          </div>
        </div>

        <!-- Tips Section -->
        <div class="card p-5 mt-6">
          <h3 class="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Tips for Best Results
          </h3>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="flex items-start gap-3 p-3 rounded-xl bg-white/5 border border-white/5">
              <div class="w-8 h-8 shrink-0 rounded-lg bg-pink-500/10 flex items-center justify-center">
                <svg class="w-4 h-4 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <p class="text-white text-sm font-medium">Clear Photos</p>
                <p class="text-gray-500 text-xs mt-0.5">Use well-lit, focused images</p>
              </div>
            </div>
            <div class="flex items-start gap-3 p-3 rounded-xl bg-white/5 border border-white/5">
              <div class="w-8 h-8 shrink-0 rounded-lg bg-blue-500/10 flex items-center justify-center">
                <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                </svg>
              </div>
              <div>
                <p class="text-white text-sm font-medium">Full Product</p>
                <p class="text-gray-500 text-xs mt-0.5">Show the entire product</p>
              </div>
            </div>
            <div class="flex items-start gap-3 p-3 rounded-xl bg-white/5 border border-white/5">
              <div class="w-8 h-8 shrink-0 rounded-lg bg-purple-500/10 flex items-center justify-center">
                <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <p class="text-white text-sm font-medium">Real Photos</p>
                <p class="text-gray-500 text-xs mt-0.5">Avoid stock images</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div class="lg:col-span-1">
        <div class="card p-6 sticky top-24 border-pink-500/20">
          <h3 class="text-lg font-semibold text-white mb-6 flex items-center gap-3">
            <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500/20 to-cyan-600/20 border border-blue-500/30 flex items-center justify-center">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </span>
            AI Analysis
          </h3>

          <!-- Loading State -->
          <div v-if="isLoading" class="space-y-4">
            <div class="skeleton h-20 rounded-xl"></div>
            <div class="skeleton h-16 rounded-xl"></div>
            <div class="skeleton h-16 rounded-xl"></div>
          </div>

          <!-- Results -->
          <div v-else-if="productData" class="space-y-4">
            <!-- Price Estimate -->
            <div class="p-4 rounded-xl bg-gradient-to-br from-pink-500/10 to-purple-600/10 border border-pink-500/20">
              <div class="flex items-center gap-3 mb-2">
                <svg class="w-5 h-5 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-gray-400 text-sm">Estimated Price</span>
              </div>
              <p class="text-3xl font-bold gradient-text">{{ formatPrice(productData.price) }}</p>
            </div>

            <!-- Category -->
            <div class="p-4 rounded-xl bg-white/5 border border-white/10">
              <div class="flex items-center gap-3 mb-2">
                <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                <span class="text-gray-400 text-sm">Category</span>
              </div>
              <p class="text-white font-medium">{{ productData.category }}</p>
            </div>

            <!-- Confidence (if available) -->
            <div v-if="productData.confidence" class="p-4 rounded-xl bg-white/5 border border-white/10">
              <div class="flex items-center gap-3 mb-3">
                <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-gray-400 text-sm">Confidence</span>
              </div>
              <div class="w-full h-2 bg-dark-700 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-green-500 to-emerald-400 rounded-full transition-all duration-500"
                  :style="{ width: productData.confidence + '%' }"
                ></div>
              </div>
              <p class="text-right text-sm text-gray-400 mt-1">{{ productData.confidence }}%</p>
            </div>

            <!-- Use Price Button -->
            <button class="w-full btn-accent flex items-center justify-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Use This Price
            </button>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-8">
            <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-dark-700 to-dark-800 border border-white/10 flex items-center justify-center">
              <svg class="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <p class="text-gray-400 text-sm">Upload a product image to receive AI-powered price estimation</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const fileInput = ref(null);
const imagePreview = ref(null);
const selectedImage = ref(null);
const productData = ref(null);
const isLoading = ref(false);
const isDragging = ref(false);

const formatPrice = (price) => {
  return new Intl.NumberFormat('th-TH', {
    style: 'currency',
    currency: 'THB',
    minimumFractionDigits: 0,
  }).format(price);
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    processFile(file);
  }
};

const handleDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) {
    processFile(file);
  }
};

const processFile = (file) => {
  selectedImage.value = file;
  const reader = new FileReader();
  reader.onload = () => {
    imagePreview.value = reader.result;
  };
  reader.readAsDataURL(file);
};

const clearImage = () => {
  imagePreview.value = null;
  selectedImage.value = null;
  productData.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const handleSubmit = async () => {
  if (!selectedImage.value) return;
  
  isLoading.value = true;
  const formData = new FormData();
  formData.append('productImage', selectedImage.value);

  try {
    const response = await fetch('http://localhost:5678/webhook-test/upload-image', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();
      productData.value = result;
    } else {
      alert('An error occurred during analysis');
    }
  } catch (error) {
    console.error('Error uploading image:', error);
    alert('An error occurred while uploading the image');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.upload-zone {
  position: relative;
  padding: 2rem;
  border-radius: 1rem;
  border: 2px dashed rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(180deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.5) 100%);
}

.upload-zone:hover,
.upload-zone.active {
  border-color: rgba(236, 72, 153, 0.5);
  background: linear-gradient(180deg, rgba(236, 72, 153, 0.05) 0%, rgba(30, 41, 59, 0.5) 100%);
}

.upload-zone.has-image {
  border-color: rgba(255, 255, 255, 0.2);
}
</style>
