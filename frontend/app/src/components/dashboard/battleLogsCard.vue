<script setup>
import { ref } from 'vue'
import example from '@/assets/example.jpg'

const playerStats = ref({
  victory: true,
  player_user_name: 'Martin',
  player_avatar: '',
  player_stats: {
    timeInBed: 5,
    awakeTime: 2,
    lightSleep: 6,
    slowWave: 3,
    rem: 6,
    disturbance: 2,
    baseline: 3,
    debt: 2,
    strain: 7,
    respiratoryRate: 18,
    performance: 88,
    consistency: 89,
    efficiency: 95,
  },
  player_protocol: [],
})


const props = defineProps({
  victory: Boolean,
  enemy_user_name: String,
  enemy_avatar: String,
  enemy_stats: Object,
  enemy_protocol: Array,
})
</script>
<template>
  <li class="font-inter h-full odd:bg-gray-300/[0.03] even:bg-transparent">
    <div
      class="p-4 flex h-full flex-col"
    >
      <!-- Header -->
      <div class="p-3 bg-(--kots-blocks-color) rounded-lg">
      <div class="mb-3 flex items-center justify-between shrink-0 ">
        <div
          class="tracking-wide text-xs font-semibold"
          :class="props.victory ? 'text-green-500' : 'text-red-400'"
        >
          {{ props.victory ? 'WIN' : 'LOSS' }}
        </div>

        <div class="flex items-center gap-2 text-xs text-heading">
          <span>{{ playerStats.player_user_name }}</span>
          <span class="text-body">vs</span>
          <span>{{ props.enemy_user_name }}</span>
        </div>
      </div>
      
      <div class="grid flex-1 min-h-0 grid-cols-[1fr_150px] gap-4">
<!-- LEFT: Stats -->
<div class="min-h-0 space-y-2.5 overflow-y-auto rounded-lg bg-white/[0.02] p-3 px-4">
<div
  v-for="(playerValue, stat) in playerStats.player_stats"
  :key="stat"
  class="grid grid-cols-[110px_24px_1fr_24px] items-center gap-2"
>
  <!-- Icon + Label -->
  <div class="flex items-center gap-1.5 min-w-0">
    <span class="h-3 w-3 shrink-0 rounded-full bg-white/20"></span>
    <span class="truncate text-[10px] text-white">
      {{ stat }}
    </span>
  </div>

  <!-- Player value -->
  <div class="text-right text-[10px] font-medium text-white">
    {{ playerValue }}
  </div>

  <!-- Graph -->
  <div class="relative h-2.5 overflow-hidden rounded-full bg-white/10">
    <div
      class="absolute right-1/2 top-0 h-full rounded-l-full bg-green-400"
      :style="{ width: `${Math.min(playerValue * 5, 50)}%` }"
    />

    <div
      class="absolute left-1/2 top-0 h-full rounded-r-full bg-red-500"
      :style="{ width: `${Math.min((props.enemy_stats?.[stat] || 0) * 5, 50)}%` }"
    />

    <div class="absolute left-1/2 top-0 h-full w-px bg-white/30"></div>
  </div>

  <!-- Enemy value -->
  <div class="text-left text-[10px] font-medium text-white">
    {{ props.enemy_stats?.[stat] || 0 }}
  </div>
</div>
</div>
        <!-- RIGHT: Protocols -->
        <div class="min-h-0 rounded-lg bg-white/[0.02] p-2">
          <div class="mb-2 text-[10px] font-semibold uppercase tracking-wide text-body">
            protocols
          </div>

          <div class="space-y-3 text-[10px]">
            <div>
              <div class="mb-1 text-cyan-300">
                {{ playerStats.player_user_name }}
              </div>

              <div class="flex flex-wrap gap-1">
                <span
                  v-for="protocol in playerStats.player_protocol"
                  :key="protocol"
                  class="rounded-full bg-cyan-300/10 px-2 py-0.5 text-cyan-100"
                >
                  {{ protocol }}
                </span>

                <span
                  v-if="playerStats.player_protocol.length === 0"
                  class="text-body"
                >
                  No protocol
                </span>
              </div>
            </div>

            <div>
              <div class="mb-1 text-red-300">
                {{ props.enemy_user_name }}
              </div>

              <div class="flex flex-wrap gap-1">
                <span
                  v-for="protocol in props.enemy_protocol"
                  :key="protocol"
                  class="rounded-full bg-red-300/10 px-2 py-0.5 text-red-100"
                >
                  {{ protocol }}
                </span>

                <span
                  v-if="!props.enemy_protocol || props.enemy_protocol.length === 0"
                  class="text-body"
                >
                  No protocol
                </span>
              </div>
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>
  </li>
</template>