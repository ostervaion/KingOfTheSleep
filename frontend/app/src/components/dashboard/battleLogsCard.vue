<script setup>
import example from '@/assets/example.jpg'

const props = defineProps({
  victory: Boolean,
  enemy_user_name: String,
  enemy_avatar: String,
  enemy_stats: Object,
  enemy_protocol: Array,
})
</script>

<template>
  <li class="odd:bg-white/[0.015] even:bg-transparent">
    <div class="grid grid-cols-[60px_1fr_120px] items-center px-6 py-2">

      <!-- Victory / Defeat -->
      <div
        class="text-sm font-semibold"
        :class="props.victory ? 'text-green-400' : 'text-red-400'"
      >
        {{ props.victory ? 'VICTORY' : 'LOSS' }}
      </div>

      <!-- Enemy -->
      <div class="flex items-center gap-3">
        <img
          class="h-8 w-8 rounded-full object-cover"
          :src="props.enemy_avatar || example"
          alt=""
        />

        <span class="text-sm text-heading">
          {{ props.enemy_user_name }}
        </span>
      </div>

      <!-- Stats (placeholder until you decide what to show) -->
      <div class="text-right text-sm text-heading">
        {{ props.enemy_stats.wins }}W · {{ props.enemy_stats.losses }}L
      </div>

    </div>
  </li>
</template>