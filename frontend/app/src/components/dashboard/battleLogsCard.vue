<script setup>
import { computed, ref } from 'vue'

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
  <li
    class="relative border-t border-white/[0.055] first:border-t-0"
    :class="props.victory ? 'battle-win' : 'battle-loss'"
  >
    <button
      type="button"
      class="group flex w-full items-center gap-2.5 px-1 py-3 text-left sm:px-2 sm:py-4"
      :aria-expanded="expanded"
      @click="expanded = !expanded"
    >
      <span
        class="absolute left-0 top-3 h-8 w-0.5 rounded-full sm:top-4"
        :class="props.victory ? 'bg-green-400' : 'bg-red-500'"
      />

      <span
        class="grid h-5 w-5 shrink-0 place-items-center rounded-full border"
        :class="props.victory ? 'border-green-400 text-green-400' : 'border-red-500 text-red-500'"
      >
        <svg v-if="props.victory" viewBox="0 0 24 24" class="h-3 w-3" fill="none" aria-hidden="true">
          <path d="m6.5 12.5 3.2 3.2 7.8-8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <svg v-else viewBox="0 0 24 24" class="h-3 w-3" fill="none" aria-hidden="true">
          <path d="m8 8 8 8M16 8l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
      </span>

      <p class="min-w-0 flex-1 truncate text-xs font-medium text-white sm:text-sm">
        {{ player.name }} <span class="font-normal text-neutral-400">vs</span> {{ props.enemy_user_name }}
      </p>

      <div class="flex shrink-0 items-center gap-3 sm:gap-4">
        <p class="text-xs font-medium tabular-nums sm:text-sm">
          <span :class="props.victory ? 'text-green-400' : 'text-red-500'">{{ score.player }}</span>
          <span class="mx-1 font-normal text-neutral-400">–</span>
          <span :class="props.victory ? 'text-neutral-400' : 'text-red-500'">{{ score.enemy }}</span>
        </p>

        <svg
          viewBox="0 0 24 24"
          class="h-3.5 w-3.5 text-neutral-400 transition-transform duration-200"
          :class="expanded ? 'rotate-180' : ''"
          fill="none"
          aria-hidden="true"
        >
          <path d="m6 14 6-6 6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    </button>

    <div v-show="expanded" class="px-1 pb-4 sm:px-2 sm:pb-5">
      <div class="grid gap-4 lg:grid-cols-[minmax(0,1fr)_220px] lg:gap-6">
        <div class="min-w-0">
          <div
            class="mb-2.5 grid grid-cols-[82px_30px_minmax(100px,1fr)_30px] items-center gap-2 text-[10px] font-medium text-neutral-400 sm:grid-cols-[130px_38px_minmax(160px,1fr)_38px] sm:text-xs"
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
              <span class="truncate text-[10px] text-neutral-400 sm:text-xs">
                {{ statLabels[stat] || stat }}
              </span>

              <span class="text-right text-[10px] font-medium tabular-nums text-green-400 sm:text-xs">
                {{ playerValue }}
              </span>

              <div class="relative h-2 overflow-hidden rounded-full bg-white/10">
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

              <span class="text-[10px] font-medium tabular-nums text-red-500 sm:text-xs">
                {{ props.enemy_stats?.[stat] ?? 0 }}
              </span>
            </div>
          </div>
        </div>

        <aside class="min-w-0">
          <p class="mb-2.5 text-xs font-medium text-body text-neutral-400">Protocols</p>

          <div class="space-y-2 text-xs leading-relaxed text-neutral-400">
            <p>
              <span class="font-medium text-white">{{ player.name }}:</span>
              <template v-if="player.protocol.length">
                {{ player.protocol.join(', ') }}
              </template>
              <span v-else>No protocol</span>
            </p>

            <p>
              <span class="font-medium text-white">{{ props.enemy_user_name }}:</span>
              <template v-if="props.enemy_protocol.length">
                {{ props.enemy_protocol.join(', ') }}
              </template>
              <span v-else>No protocol</span>
            </p>
          </div>
        </aside>
      </div>
    </div>
  </li>
</template>
