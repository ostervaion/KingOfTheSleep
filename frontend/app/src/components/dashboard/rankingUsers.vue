<script setup>
import example from '@/assets/example.jpg'

defineProps({
  ranking: String,
  name: String,
  points: String,
  posChange: String,
})
</script>

<template>
  <li class="odd:bg-white/[0.015] even:bg-transparent">
    <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
      <div class="text-sm text-heading">{{ ranking }}</div>
      <div class="flex items-center gap-3">
        <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
        <span class="text-sm text-heading">{{ name }}</span>
      </div>

      <div class="text-right text-sm text-heading">{{ points }}</div>

      <div class="text-right text-sm font-medium text-green-400">↑ {{ posChange }}</div>
    </div>
  </li>
</template>

<style scoped></style>
