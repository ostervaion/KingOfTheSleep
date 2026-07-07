<script setup>
import { computed } from 'vue'
import example from '@/assets/example.jpg'

const props = defineProps({
  ranking: String,
  name: String,
  points: String,
  posChange: String,
  trend: {
    type: String,
    default: 'same',
  },
})

const trendClass = computed(() => {
  if (props.trend === 'up') return 'text-green-400'
  if (props.trend === 'down') return 'text-red-400'
  return 'text-gray-400'
})
</script>

<template>
  <li class="odd:bg-white/[0.015] even:bg-transparent">
    <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
      <div class="text-sm text-heading">{{ props.ranking }}</div>
      <div class="flex items-center gap-3">
        <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
        <span class="text-sm text-heading">{{ props.name }}</span>
      </div>

      <div class="text-right text-sm text-heading">{{ props.points }}</div>

      <div class="text-right text-sm font-medium" :class="trendClass">
        <span v-if="props.trend === 'up'">↑</span>
        <span v-else-if="props.trend === 'down'">↓</span>
        <span v-else>→</span>
        {{ props.posChange }}
      </div>
    </div>
  </li>
</template>

<style scoped></style>
