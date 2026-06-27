<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
</script>

<template>
  <div
    class="font-inter text-sm text-heading flex-2 min-h-0 bg-(--kots-blocks-color) rounded-xl p-6 overflow-auto border-b border-[color:var(--border)]"
  >
    <div class="flex items-center justify-between">
      <div class="border border-cyan-100 rounded-md px-2 py-0.5 text-gray-800 leading-none">
        <h2 class="text-cyan-100 text-sm font-medium text-heading">Protocol impact</h2>
      </div>
    </div>
  </div>
</template>
