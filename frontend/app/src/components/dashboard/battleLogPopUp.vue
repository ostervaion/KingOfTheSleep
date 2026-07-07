<script setup>
import { ref, onMounted } from 'vue'
import BattleLogsCard from '@/components/dashboard/battleLogsCard.vue'
import BoxingGlove from '@/assets/boxing-glove.svg'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'
import BattleLog from '@/components/dashboard/battleLogPopUp.vue'

const emit = defineEmits(['close'])

var battleLogs = ref([])

onMounted(() => {
  loadLogs()
})

function loadLogs() {
  battleLogs.value = [
    {
      victory: true,
      enemy_user_name: 'Enemy 1',
      enemy_avatar: '',
      enemy_stats: {
        timeInBed: 8,
        awakeTime: 1,
        lightSleep: 2,
        slowWave: 3,
        rem: 2,
        disturbance: 0,
        baseline: 8,
        debt: 0,
        strain: 1,
        nap: 0,
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
        timeInBed: 8,
        awakeTime: 1,
        lightSleep: 2,
        slowWave: 3,
        rem: 2,
        disturbance: 0,
        baseline: 8,
        debt: 0,
        strain: 1,
        nap: 0,
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
        timeInBed: 8,
        awakeTime: 1,
        lightSleep: 2,
        slowWave: 3,
        rem: 2,
        disturbance: 0,
        baseline: 8,
        debt: 0,
        strain: 1,
        nap: 0,
        respiratoryRate: 16,
        performance: 80,
        consistency: 85,
        efficiency: 90,
      },
      enemy_protocol: [],
    },
  ]
}

function onClose() {
  emit('close')
}
</script>

<template>
  <div
    class="font-inter flex h-full max-h-[90vh] flex-col overflow-hidden rounded-xl bg-(--kots-blocks-color) border-b border-[color:var(--border)] shadow-md shadow-black/20"
  >
    <div class="px-4 pb-4 pt-3 sm:px-6 md:px-8 md:pb-5 md:pt-4">
      <div class="flex justify-end">
        <button @click="onClose" class="text-white text-sm">X</button>
      </div>

      <div class="grid grid-cols-2 gap-3 pt-2 text-white sm:grid-cols-4 sm:px-5">
        <div class="pt-3 flex flex-col items-center">
          <BoxingGlove class="-mt-0.5 h-8 w-8 sm:h-10 sm:w-10" />
          <p class="text-center text-[10px] font-medium text-body sm:text-xs">battles</p>
          <p class="text-center mb-2 text-lg font-light text-white sm:text-xl">18</p>
        </div>

        <div class="pt-3 flex flex-col items-center">
          <TriangleUp class="-mt-0.5 h-8 w-8 sm:h-10 sm:w-10" />
          <p class="text-center text-[10px] font-medium text-body sm:text-xs">wins</p>
          <p class="text-center mb-2 text-lg font-light text-white sm:text-xl">14</p>
        </div>

        <div class="pt-3 flex flex-col items-center">
          <TriangleDown class="-mt-0.5 h-8 w-8 sm:h-10 sm:w-10" />
          <p class="text-center text-[10px] font-medium text-body sm:text-xs">looses</p>
          <p class="text-center mb-2 text-lg font-light text-white sm:text-xl">4</p>
        </div>

        <div class="pt-3 flex flex-col items-center justify-center">
          <p class="text-center text-[10px] font-medium text-body mb-0.5 sm:text-xs">win rate</p>
          <p class="text-center mb-2 text-lg font-light text-green-400 sm:text-xl">% 70</p>
        </div>
      </div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto snap-y">
      <ul class="space-y-4 px-2 pb-4">
        <BattleLogsCard
          v-for="logs in battleLogs"
          :key="logs.enemy_user_name"
          class="snap-start"
          v-bind="logs"
        />
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
