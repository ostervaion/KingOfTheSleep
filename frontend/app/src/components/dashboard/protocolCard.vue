<script setup>
import example from '@/assets/example.jpg'

defineProps({
  type: String,
  ranking: Number,
  name: String,
  usage: Number,
  winrate: String,
})
</script>

<template>
  <li class="odd:bg-white/[0.015] even:bg-transparent">
    <div class="grid grid-cols-[30px_1fr_70px_70px] items-center px-6 py-1.5">
      <div class="text-xs text-heading md:text-sm">{{ ranking }}</div>

      <div class="flex items-center gap-3">
        <span class="text-xs text-heading md:text-sm">{{ name }}</span>
      </div>

      <div class="text-xs text-right text-heading md:text-sm">{{ usage }}</div>

      <div
        class="text-right text-xs md:text-sm font-medium"
        :class="type === 'winner' ? 'text-green-400' : 'text-red-400'"
      >
        {{ winrate }}
      </div>
    </div>
  </li>
</template>

<style scoped></style>
