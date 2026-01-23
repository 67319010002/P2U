<template>
  <Teleport to="body">
    <Transition name="modal">
      <div 
        v-if="isOpen" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
      >
        <!-- Backdrop -->
        <div 
          class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
          @click="close"
        ></div>

        <!-- Modal Content -->
        <div 
          class="relative w-full max-w-md bg-[#0f0f13] border border-white/10 rounded-3xl shadow-[0_0_50px_-12px_rgba(168,85,247,0.5)] overflow-hidden transform transition-all"
          role="dialog"
          aria-modal="true"
        >
          <!-- Decorative Header Blur -->
          <div class="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-purple-500/10 to-transparent pointer-events-none"></div>

          <!-- Content Wrapper -->
          <div class="relative p-6">
            <!-- Header -->
            <div class="flex items-start justify-between mb-4">
              <h3 class="text-xl font-bold text-white flex items-center gap-2">
                <slot name="title">Title</slot>
              </h3>
              <button 
                @click="close"
                class="text-gray-400 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>

            <!-- Body -->
            <div class="text-gray-300 text-sm leading-relaxed mb-6">
              <slot></slot>
            </div>

            <!-- Footer -->
            <div class="flex justify-end gap-3">
              <slot name="footer">
                <button 
                  @click="close"
                  class="px-4 py-2 rounded-xl text-sm font-medium text-gray-400 hover:text-white hover:bg-white/5 transition-all"
                >
                  ยกเลิก
                </button>
                <button 
                  @click="confirm"
                  class="px-4 py-2 rounded-xl text-sm font-bold bg-pink-600 hover:bg-pink-500 text-white shadow-lg shadow-pink-900/20 transition-all"
                >
                  ยืนยัน
                </button>
              </slot>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['close', 'confirm']);

function close() {
  emit('close');
}

function confirm() {
  emit('confirm');
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .transform,
.modal-leave-active .transform {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-enter-from .transform,
.modal-leave-to .transform {
  transform: scale(0.95) translateY(10px);
}
</style>
