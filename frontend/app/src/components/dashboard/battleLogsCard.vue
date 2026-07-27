<script setup>
import { computed, ref } from 'vue'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'

const props = defineProps({
  combat_id: {
    type: Number,
    required: true,
  },

  victory: {
    type: Boolean,
    default: false,
  },

  enemy_id: {
    type: Number,
    default: null,
  },

  enemy_username: {
    type: String,
    default: 'Unknown enemy',
  },

  enemy_avatar: {
    type: String,
    default: null,
  },

  enemy_stats: {
    type: Object,
    default: null,
  },

  enemy_protocol: {
    type: Array,
    default: () => [],
  },

  me: {
    type: Object,
    default: null,
  },

  player_score: {
    type: Number,
    default: null,
  },

  enemy_score: {
    type: Number,
    default: null,
  },
})

const expanded = ref(true)

const stats = [
  {
    key: 'time_in_bed',
    label: 'Time in bed',
  },
  {
    key: 'awake_time',
    label: 'Awake time',
  },
  {
    key: 'light_sleep',
    label: 'Light sleep',
  },
  {
    key: 'slow_wave',
    label: 'Slow wave',
  },
  {
    key: 'rem',
    label: 'REM',
  },
  {
    key: 'disturbance',
    label: 'Disturbance',
  },
  {
    key: 'baseline',
    label: 'Baseline',
  },
  {
    key: 'debt',
    label: 'Debt',
  },
  {
    key: 'strain',
    label: 'Strain',
  },
  {
    key: 'respiratory_rate',
    label: 'Respiratory rate',
  },
  {
    key: 'performance',
    label: 'Performance',
  },
  {
    key: 'consistency',
    label: 'Consistency',
  },
  {
    key: 'efficiency',
    label: 'Efficiency',
  },
]

const playerName = computed(() => {
  return props.me?.username ?? 'You'
})


const playerStats = computed(() => {
  if (!props.me) return null

  return props.me.stats ?? props.me.sleep_stats ?? props.me
})

const playerProtocol = computed(() => {
  if (!props.me) return []

  return props.me.protocol ?? props.me.protocols ?? []
})

function getPlayerValue(key) {
  return playerStats.value?.[key] ?? null
}

function getEnemyValue(key) {
  return props.enemy_stats?.[key] ?? null
}

function formatValue(value) {
  if (value === null || value === undefined) return '—'

  if (typeof value === 'number') {
    return Number.isInteger(value) ? value : value.toFixed(2)
  }

  return value
}

function getBarWidth(value, comparisonValue) {
  const numericValue = Number(value)
  const numericComparison = Number(comparisonValue)

  if (!Number.isFinite(numericValue)) return 0

  const maxValue = Math.max(
    Number.isFinite(numericValue) ? numericValue : 0,
    Number.isFinite(numericComparison) ? numericComparison : 0,
    1,
  )

  return Math.min((numericValue / maxValue) * 50, 50)
}

const score = computed(() => ({
  player: props.player_score,
  enemy: props.enemy_score,
}))
</script>

<template>
  <li
    class="relative w-full odd:bg-white/[0.015] even:bg-transparent"
    :class="props.victory ? 'battle-win' : 'battle-loss'"
  >
    <button
      type="button"
      class="group flex w-full items-center gap-2.5 px-4 py-3 text-left sm:px-6 sm:py-4 md:px-8"
      :aria-expanded="expanded"
      @click="expanded = !expanded"
    >
      <TriangleUp
        v-if="props.victory"
        class="h-3 w-3 shrink-0"
      />

      <TriangleDown
        v-else
        class="h-3 w-3 shrink-0"
      />

      <p class="min-w-0 flex-1 truncate text-xs font-medium text-white sm:text-sm">
        {{ props.enemy_username }}
      </p>

      <span
        class="text-[10px] font-medium uppercase"
        :class="props.victory ? 'text-green-400' : 'text-red-400'"
      >
        {{ props.victory ? 'Victory' : 'Defeat' }}
      </span>

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

    <div
      v-show="expanded"
      class="px-4 pb-4 sm:px-6 sm:pb-5 md:px-8"
    >
      <div class="grid gap-4 lg:grid-cols-[minmax(0,1fr)_220px] lg:gap-6">
        <div class="min-w-0">
          <div
            class="mb-2.5 grid grid-cols-[82px_38px_minmax(100px,1fr)_38px] items-center gap-2 text-[10px] font-medium text-zinc-400 sm:grid-cols-[130px_48px_minmax(160px,1fr)_48px] sm:text-xs"
          >
            <span>Metric</span>
            <span class="text-right">You</span>
            <span />
            <span>Enemy</span>
          </div>

          <div
            v-if="props.enemy_stats"
            class="space-y-2"
          >
            <div
              v-for="stat in stats"
              :key="stat.key"
              class="grid grid-cols-[82px_38px_minmax(100px,1fr)_38px] items-center gap-2 sm:grid-cols-[130px_48px_minmax(160px,1fr)_48px]"
            >
              <span class="truncate text-[10px] text-zinc-400 sm:text-xs">
                {{ stat.label }}
              </span>

              <span
                class="text-right text-[10px] font-medium tabular-nums text-green-400 sm:text-xs"
              >
                {{ formatValue(getPlayerValue(stat.key)) }}
              </span>

              <div class="relative h-2 overflow-hidden rounded-full bg-white/10">
                <div
                  class="absolute right-1/2 top-0 h-full rounded-l-full bg-green-400"
                  :style="{
                    width: `${getBarWidth(
                      getPlayerValue(stat.key),
                      getEnemyValue(stat.key),
                    )}%`,
                  }"
                />

                <div
                  class="absolute left-1/2 top-0 h-full rounded-r-full bg-red-500"
                  :style="{
                    width: `${getBarWidth(
                      getEnemyValue(stat.key),
                      getPlayerValue(stat.key),
                    )}%`,
                  }"
                />

                <div
                  class="absolute left-1/2 top-[-1px] z-10 h-[calc(100%+2px)] w-[2px] -translate-x-1/2 rounded-full bg-[#171715]"
                />
              </div>

              <span
                class="text-[10px] font-medium tabular-nums text-red-500 sm:text-xs"
              >
                {{ formatValue(getEnemyValue(stat.key)) }}
              </span>
            </div>
          </div>

          <div
            v-else
            class="rounded-lg border border-white/10 p-4 text-center text-xs text-zinc-400"
          >
            No statistics available for this enemy.
          </div>
        </div>

        <aside class="min-w-0">
          <p class="text-body mb-2.5 text-xs font-medium text-zinc-400">
            Protocols
          </p>

          <div class="space-y-2 text-xs leading-relaxed text-zinc-400">
            <p>
              <span class="font-medium text-white">
                {{ playerName }}:
              </span>

              <template v-if="playerProtocol.length">
                {{ playerProtocol.join(', ') }}
              </template>

              <span v-else>
                No protocol
              </span>
            </p>

            <p>
              <span class="font-medium text-white">
                {{ props.enemy_username }}:
              </span>

              <template v-if="props.enemy_protocol.length">
                {{ props.enemy_protocol.join(', ') }}
              </template>

              <span v-else>
                No protocol
              </span>
            </p>
          </div>

          <div
            v-if="score.player !== null || score.enemy !== null"
            class="mt-4 rounded-lg bg-white/[0.03] p-3"
          >
            <p class="mb-2 text-xs text-zinc-400">
              Score
            </p>

            <div class="flex items-center justify-between text-sm font-medium">
              <span class="text-green-400">
                {{ score.player ?? '—' }}
              </span>

              <span class="text-zinc-500">
                -
              </span>

              <span class="text-red-400">
                {{ score.enemy ?? '—' }}
              </span>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </li>
</template>