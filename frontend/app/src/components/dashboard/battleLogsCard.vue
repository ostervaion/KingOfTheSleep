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
  <li class="font-inter h-auto">
    <div class="flex flex-col">
      <div class="rounded-lg bg-(--kots-blocks-color) p-3">
        <!-- Header -->
        <div class="mb-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div
            class="tracking-wide text-xs font-semibold"
            :class="props.victory ? 'text-green-500' : 'text-red-400'"
          >
            {{ props.victory ? 'WIN' : 'LOSS' }}
          </div>

          <div class="flex flex-wrap items-center gap-2 text-xs text-heading text-white">
            <span>{{ playerStats.player_user_name }}</span>
            <span class="text-body">vs</span>
            <span>{{ props.enemy_user_name }}</span>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-3 lg:grid-cols-[1fr_250px] lg:gap-4">
          <!-- LEFT: Stats -->
          <div class="min-h-0 space-y-2 overflow-y-auto rounded-lg bg-white/[0.02] p-2 sm:px-3">
            <div
              v-for="(playerValue, stat) in playerStats.player_stats"
              :key="stat"
              class="grid grid-cols-[88px_22px_1fr_22px] items-center gap-1.5 sm:grid-cols-[110px_24px_1fr_24px] sm:gap-2"
            >
              <!-- Icon + Label -->
              <div class="flex items-center gap-1.5 min-w-0">
                <span class="h-2.5 w-2.5 shrink-0 rounded-full bg-white/20 sm:h-3 sm:w-3"></span>
                <span class="truncate text-[9px] text-white sm:text-[10px]">
                  {{ stat }}
                </span>
              </div>

              <!-- Player value -->
              <div class="text-right text-[9px] font-medium text-green-400 sm:text-[10px]">
                {{ playerValue }}
              </div>

              <!-- Graph -->
              <div class="relative h-2 overflow-hidden rounded-full bg-white/10 sm:h-2.5">
                <div
                  class="absolute right-1/2 top-0 h-full rounded-l-full bg-green-400"
                  :style="{ width: `${Math.min(playerValue * 5, 50)}%` }"
                />

                <div
                  class="absolute left-1/2 top-0 h-full rounded-r-full bg-red-500"
                  :style="{ width: `${Math.min((props.enemy_stats?.[stat] || 0) * 5, 50)}%` }"
                />

                <div
                  class="absolute left-1/2 top-[-1px] z-10 h-[calc(100%+2px)] w-[2px] -translate-x-1/2 rounded-full bg-[#171715]"
                ></div>
              </div>

              <!-- Enemy value -->
              <div class="text-left text-[9px] font-medium text-red-400 sm:text-[10px]">
                {{ props.enemy_stats?.[stat] || 0 }}
              </div>
            </div>
          </div>

          <!-- RIGHT: Protocols -->
          <div class="min-h-0 rounded-lg bg-white/[0.02] p-3">
            <div class="grid grid-cols-1 gap-3 text-[10px] sm:grid-cols-2 lg:grid-cols-1">
              <div>
                <div class="mb-1 text-white">
                  {{ playerStats.player_user_name }}
                </div>

                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="protocol in playerStats.player_protocol"
                    :key="protocol"
                    class="rounded-full bg-cyan-300/10 px-2 py-0.5 text-white"
                  >
                    {{ protocol }}
                  </span>

                  <span v-if="playerStats.player_protocol.length === 0" class="text-body text-gray-400">
                    No protocol
                  </span>
                </div>
              </div>

              <div>
                <div class="mb-1 text-white">
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
                    class="text-body text-gray-400"
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