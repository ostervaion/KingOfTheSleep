<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import BattleLogsCard from '@/components/dashboard/battleLogsCard.vue'
import BoxingGlove from '@/assets/boxing-glove.svg'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'
import api from '@/api/api'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits(['close'])
const router = useRouter()
const authStore = useAuthStore()

const battleLogs = ref([])
const me = ref(null)
const isLoading = ref(false)
const loadError = ref('')

async function loadLogs() {
  isLoading.value = true
  loadError.value = ''

  try {
    const { data } = await api.get('/battleData')

    me.value = data.me ?? null

    battleLogs.value = Array.isArray(data.battles)
      ? data.battles.map((battle) => ({
          combat_id: battle.combat_id,
          victory: battle.victory,

          enemy_id: battle.enemy_id,
          enemy_username: battle.enemy_username,
          enemy_avatar: battle.enemy_avatar,

          enemy_stats: battle.enemy_stats
            ? {
                username: battle.enemy_stats.username,
                awake_time: battle.enemy_stats.awake_time,
                slow_wave: battle.enemy_stats.slow_wave,
                disturbance: battle.enemy_stats.disturbance,
                debt: battle.enemy_stats.debt,
                nap: battle.enemy_stats.nap,
                performance: battle.enemy_stats.performance,
                efficiency: battle.enemy_stats.efficiency,
                time_in_bed: battle.enemy_stats.time_in_bed,
                light_sleep: battle.enemy_stats.light_sleep,
                rem: battle.enemy_stats.rem,
                baseline: battle.enemy_stats.baseline,
                strain: battle.enemy_stats.strain,
                respiratory_rate: battle.enemy_stats.respiratory_rate,
                consistency: battle.enemy_stats.consistency,
              }
            : null,

          enemy_protocol: Array.isArray(battle.enemy_protocol) ? battle.enemy_protocol : [],
        }))
      : []
  } catch (error) {
    const status = error?.response?.status

    if (status === 401 || status === 403) {
      authStore.logout()
      router.push({ name: 'home' })
      loadError.value = 'Your session has expired or you are not authorized to view this content.'
    } else {
      loadError.value = error?.response?.data?.detail || error?.message || 'Could not load battle logs'
    }

    battleLogs.value = []
    me.value = null
  } finally {
    isLoading.value = false
  }
}

onMounted(loadLogs)

defineExpose({ loadLogs })

const summary = computed(() => {
  const battles = battleLogs.value.length

  const wins = battleLogs.value.filter((battle) => battle.victory === true).length

  const losses = battles - wins

  const winRate = battles > 0 ? Math.round((wins / battles) * 100) : 0

  return {
    battles,
    wins,
    losses,
    winRate,
  }
})

const winRateClass = computed(() => {
  if (summary.value.winRate >= 60) return 'text-green-400'
  if (summary.value.winRate <= 40) return 'text-red-400'

  return 'text-orange-400'
})

function onClose() {
  emit('close')
}
</script>

<template>
  <div
    class="font-inter flex max-h-[90vh] min-h-0 w-full flex-1 flex-col overflow-hidden rounded-xl border-b border-(--border) bg-(--kots-blocks-color) text-white shadow-md shadow-black/20"
    role="dialog"
    aria-modal="true"
    aria-labelledby="battle-logs-title"
  >
    <div class="px-4 pb-1 pt-4 sm:px-6 md:px-8 md:pb-2 md:pt-5">
      <div class="flex items-start justify-end gap-4">
        <button
          type="button"
          class="rounded-full px-2 text-lg leading-none text-zinc-400 transition hover:text-white"
          aria-label="Close battle logs"
          @click="onClose"
        >
          ×
        </button>
      </div>
    </div>

    <div class="min-h-0 flex-1 overflow-y-auto pb-8 md:pb-10">
      <div class="px-4 sm:px-6 md:px-8">
        <div
          class="grid grid-cols-2 justify-between gap-4 rounded-lg bg-white/[0.02] p-3 sm:grid-cols-4 sm:p-4"
        >
          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <BoxingGlove class="h-5 w-5 shrink-0 text-zinc-400" />

            <div class="min-w-0">
              <p class="text-body text-xs font-medium text-zinc-400">Battles</p>

              <p class="mt-1 text-sm font-medium leading-none text-white">
                {{ summary.battles }}
              </p>
            </div>
          </div>

          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <TriangleUp class="h-5 w-5 shrink-0" />

            <div class="min-w-0">
              <p class="text-body text-xs font-medium text-zinc-400">Wins</p>

              <p class="mt-1 text-sm font-medium leading-none text-white">
                {{ summary.wins }}
              </p>
            </div>
          </div>

          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <TriangleDown class="h-5 w-5 shrink-0" />

            <div class="min-w-0">
              <p class="text-body text-xs font-medium text-zinc-400">Losses</p>

              <p class="mt-1 text-sm font-medium leading-none text-white">
                {{ summary.losses }}
              </p>
            </div>
          </div>

          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <div
              class="grid h-5 w-5 shrink-0 place-items-center rounded-full border border-current text-[10px] font-medium"
              :class="winRateClass"
            >
              %
            </div>

            <div class="min-w-0">
              <p class="text-body text-xs font-medium text-zinc-400">Win rate</p>

              <p class="mt-1 text-sm font-medium leading-none" :class="winRateClass">
                {{ summary.winRate }}%
              </p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="p-8 text-center text-sm text-zinc-400">
        Loading battle logs...
      </div>

      <div v-else-if="loadError" class="p-8 text-center">
        <p class="text-sm text-red-400">
          {{ loadError }}
        </p>

        <button
          type="button"
          class="mt-3 rounded-md border border-zinc-600 px-3 py-1.5 text-sm text-white hover:bg-white/5"
          @click="loadLogs"
        >
          Try again
        </button>
      </div>

      <div v-else-if="battleLogs.length === 0" class="p-8 text-center text-sm text-zinc-400">
        No battle logs found.
      </div>

      <ul v-else class="mt-4 w-full">
        <li v-for="log in battleLogs" :key="log.combat_id">
          <BattleLogsCard v-bind="log" :me="me" />
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";

.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #333;
}
</style>
