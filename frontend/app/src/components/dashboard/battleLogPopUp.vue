<script setup>
import { computed, onMounted, ref } from 'vue'
import BattleLogsCard from '@/components/dashboard/battleLogsCard.vue'
import BoxingGlove from '@/assets/boxing-glove.svg'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'
import api from '@/api/api'
const emit = defineEmits(['close'])

const battleLogs = ref([])
const isLoading = ref(false)

//onMounted(loadLogs)

async function loadLogs() {
  isLoading.value = true
  try {
    const response = await api.get('/battleData')
    console.log(response.data)
    battleLogs.value = response.data // adjust to your real response shape
  } catch (error) {
    console.error('Error cargando battle logs:', error)
  } finally {
    isLoading.value = false
  }
}
/*
  battleLogs.value = [
    {
      victory: true,
      enemy_user_name: 'Enemy 1',
      enemy_avatar: '',
      enemy_stats: {
        timeInBed: 6,
        awakeTime: 1,
        lightSleep: 2,
        slowWave: 1,
        rem: 2,
        disturbance: 0,
        baseline: 0,
        debt: 1,
        strain: 2,
        respiratoryRate: 16,
        performance: 80,
        consistency: 85,
        efficiency: 90,
      },
      enemy_protocol: [],
    },
    {
      victory: false,
      enemy_user_name: 'Enemy 2',
      enemy_avatar: '',
      enemy_stats: {
        timeInBed: 6,
        awakeTime: 1,
        lightSleep: 2,
        slowWave: 1,
        rem: 2,
        disturbance: 0,
        baseline: 0,
        debt: 1,
        strain: 2,
        respiratoryRate: 16,
        performance: 80,
        consistency: 85,
        efficiency: 90,
      },
      enemy_protocol: [],
    },
    {
      victory: true,
      enemy_user_name: 'Enemy 3',
      enemy_avatar: '',
      enemy_stats: {
        timeInBed: 7,
        awakeTime: 1,
        lightSleep: 3,
        slowWave: 2,
        rem: 2,
        disturbance: 1,
        baseline: 1,
        debt: 1,
        strain: 3,
        respiratoryRate: 17,
        performance: 84,
        consistency: 82,
        efficiency: 88,
      },
      enemy_protocol: ['kaka', 'culo', 'pedo', 'pis'],
    },
  ]
*/
defineExpose({ loadLogs })

/*
const props = defineProps({
  summary: {
    type: Object,
    default: () => ({ battles: 0, wins: 0, losses: 0, winRate: 0 }),
  },
})

const winRateColor = computed(() => {
  if (props.summary.winRate >= 60) return 'text-green-400'
  if (props.summary.winRate <= 40) return 'text-red-400'
  return 'text-orange-400'
  */
const summary = computed(() => {
  const battles = 18
  const wins = 14
  const losses = 4
  const winRate = 70

  return {
    battles,
    wins,
    losses,
    winRate,
  }
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
              class="grid h-5 w-5 shrink-0 place-items-center rounded-full border border-green-500/60 text-[10px] font-medium text-green-400"
            >
              %
            </div>

            <div class="min-w-0">
              <p class="text-body text-xs font-medium text-zinc-400">Win rate</p>

              <p class="mt-1 text-sm font-medium leading-none text-green-400">
                {{ summary.winRate }}%
              </p>
            </div>
          </div>
        </div>
      </div>

<!--    <ul class="mt-4">
        <BattleLogsCard
          v-for="log in battleLogs.battles"
          :key="log.combat_id"
          v-bind="log"
          :me="battleLogs.me"
        />
-->
      <ul class="mt-4 w-full">
        <BattleLogsCard v-for="log in battleLogs" :key="log.enemy_user_name" v-bind="log" />
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
