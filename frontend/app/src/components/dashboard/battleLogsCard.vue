<script setup>
import { computed, ref } from 'vue'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'

const props = defineProps({
  victory: Boolean,
  enemy_user_name: String,
  enemy_avatar: String,
  enemy_stats: {
    type: Object,
    default: () => ({}),
  },
  enemy_protocol: {
    type: Array,
    default: () => [],
  },
  player_score: Number,
  enemy_score: Number,
})

const expanded = ref(true)

const player = {
  name: 'Martin',
  stats: {
    timeInBed: 5,
    awakeTime: 2,
    lightSleep: 5,
    slowWave: 6,
    rem: 2,
    disturbance: 3,
    baseline: 2,
    debt: 2,
    strain: 2,
    respiratoryRate: 18,
    performance: 88,
    consistency: 88,
    efficiency: 90,
  },
  protocol: [],
}

const statLabels = {
  timeInBed: 'timeInBed',
  awakeTime: 'awakeTime',
  lightSleep: 'lightSleep',
  slowWave: 'slowWave',
  rem: 'rem',
  disturbance: 'disturbance',
  baseline: 'baseline',
  debt: 'debt',
  strain: 'strain',
  respiratoryRate: 'respiratoryRate',
  performance: 'performance',
  consistency: 'consistency',
  efficiency: 'efficiency',
}

const score = computed(() => ({
  player: props.player_score ?? (props.victory ? 13 : 8),
  enemy: props.enemy_score ?? (props.victory ? 8 : 13),
}))
</script>

<template>
  <!--
    This li occupies the complete width of the popup.

    The background is applied here, while the padding is applied
    to the internal content.
  -->
  <li
    class="relative w-full odd:bg-white/[0.015] even:bg-transparent"
    :class="props.victory ? 'battle-win' : 'battle-loss'"
  >
    <!-- Battle header -->
    <button
      type="button"
      class="group flex w-full items-center gap-2.5 px-4 py-3 text-left sm:px-6 sm:py-4 md:px-8"
      :aria-expanded="expanded"
      @click="expanded = !expanded"
    >
      <TriangleUp v-if="props.victory" class="h-3 w-3 shrink-0" />
      <TriangleDown v-else class="h-3 w-3 shrink-0" />
      <p class="min-w-0 flex-1 truncate text-xs font-medium text-white sm:text-sm">
        {{ props.enemy_user_name }}
      </p>

      <div class="flex shrink-0 items-center gap-3 sm:gap-4">
        <svg
          viewBox="0 0 24 24"
          class="h-3.5 w-3.5 text-zinc-400 transition-transform duration-200"
          :class="expanded ? 'rotate-180' : ''"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="m6 14 6-6 6 6"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
    </button>

    <!-- Expanded battle information -->
    <div v-show="expanded" class="px-4 pb-4 sm:px-6 sm:pb-5 md:px-8">
      <div class="grid gap-4 lg:grid-cols-[minmax(0,1fr)_220px] lg:gap-6">
        <!-- Stats -->
        <div class="min-w-0">
          <div
            class="mb-2.5 grid grid-cols-[82px_30px_minmax(100px,1fr)_30px] items-center gap-2 text-[10px] font-medium text-zinc-400 sm:grid-cols-[130px_38px_minmax(160px,1fr)_38px] sm:text-xs"
          >
            <span>Metric</span>
            <span class="text-right">You</span>
            <span></span>
            <span>Enemy</span>
          </div>

          <div class="space-y-2">
            <div
              v-for="(playerValue, stat) in player.stats"
              :key="stat"
              class="grid grid-cols-[82px_30px_minmax(100px,1fr)_30px] items-center gap-2 sm:grid-cols-[130px_38px_minmax(160px,1fr)_38px]"
            >
              <span class="truncate text-[10px] text-zinc-400 sm:text-xs">
                {{ statLabels[stat] || stat }}
              </span>

              <span
                class="text-right text-[10px] font-medium tabular-nums text-green-400 sm:text-xs"
              >
                {{ playerValue }}
              </span>

              <!-- Split comparison bar -->
              <div class="relative h-2 overflow-hidden rounded-full bg-white/10">
                <!-- Player value -->
                <div
                  class="absolute right-1/2 top-0 h-full rounded-l-full bg-green-400"
                  :style="{
                    width: `${Math.min(playerValue * 5, 50)}%`,
                  }"
                />

                <!-- Enemy value -->
                <div
                  class="absolute left-1/2 top-0 h-full rounded-r-full bg-red-500"
                  :style="{
                    width: `${Math.min((props.enemy_stats?.[stat] || 0) * 5, 50)}%`,
                  }"
                />

                <!-- Center divider -->
                <div
                  class="absolute left-1/2 top-[-1px] z-10 h-[calc(100%+2px)] w-[2px] -translate-x-1/2 rounded-full bg-[#171715]"
                />
              </div>

              <span class="text-[10px] font-medium tabular-nums text-red-500 sm:text-xs">
                {{ props.enemy_stats?.[stat] ?? 0 }}
              </span>
            </div>
          </div>
        </div>

        <!-- Protocols -->
        <aside class="min-w-0">
          <p class="text-body mb-2.5 text-xs font-medium text-zinc-400">Protocols</p>

          <div class="space-y-2 text-xs leading-relaxed text-zinc-400">
            <p>
              <span class="font-medium text-white"> {{ player.name }}: </span>

              <template v-if="player.protocol.length">
                {{ player.protocol.join(', ') }}
              </template>

              <span v-else> No protocol </span>
            </p>

            <p>
              <span class="font-medium text-white"> {{ props.enemy_user_name }}: </span>

              <template v-if="props.enemy_protocol.length">
                {{ props.enemy_protocol.join(', ') }}
              </template>

              <span v-else> No protocol </span>
            </p>
          </div>
        </aside>
      </div>
    </div>
  </li>
</template>
