<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
</script>

<template>
  <div class="flex-1 min-h-0 bg-(--surface) border border-(--border) rounded-xl p-6 overflow-auto">
    TODAY STATS
  </div>
</template>
