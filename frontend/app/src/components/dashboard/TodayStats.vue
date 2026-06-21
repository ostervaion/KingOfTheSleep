<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
</script>

<template>
  <div
    class="font-inter text-base font-medium text-heading flex-1 min-h-0 bg-(--kots-blocks-color) rounded-xl p-6 overflow-auto"
  >
    Today's Stats
  </div>
</template>
