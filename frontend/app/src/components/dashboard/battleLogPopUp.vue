<script setup>
import { ref, onMounted } from 'vue'
import BattleLogsCard from '@/components/dashboard/battleLogsCard.vue'
import LambBattleIcon from '@/assets/lamb_battle.svg'

const emit = defineEmits(['close'])

var battleLogs = ref([])

onMounted(() => {
  loadLogs()
})

function loadLogs() {
  battleLogs.value = [
    {
      victory: true,
      enemy_user_name: 'Martin',
      enemy_avatar: '',
      enemy_stats: {
        battles: 0,
        wins: 0,
        losses: 0,
        winrate: 0,
        score: 0,
      },
      enemy_protocol: [],
    },
    {
      victory: false,
      enemy_user_name: 'Enemy 2',
      enemy_avatar: '',
      enemy_stats: {
        battles: 0,
        wins: 0,
        losses: 0,
        winrate: 0,
        score: 0,
      },
      enemy_protocol: [],
    },
    {
      victory: true,
      enemy_user_name: 'Enemy 3',
      enemy_avatar: '',
      enemy_stats: {
        battles: 0,
        wins: 0,
        losses: 0,
        winrate: 0,
        score: 0,
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
    class="font-inter flex flex-col flex-1 min-h-0 overflow-hidden rounded-xl bg-(--kots-blocks-color) border-b border-[color:var(--border)] shadow-md shadow-black/20"
  >
    <div class="px-6 pb-4 pt-4">
      <div class="flex items-center justify-between">
        <div class="border border-cyan-100 rounded-md px-2 py-0.5 text-gray-800 leading-none">
          <h2 class="text-cyan-100 text-sm font-medium text-heading">Today's Stats</h2>
        </div>
        <button @click="onClose" class="text-white text-sm">X</button>
      </div>
      <div class="pt-2 px-5 flex items-center justify-between">
        <div class="pt-3 items-center">
          <LambBattleIcon class="text-center -mt-0.5 w-10 h-10" />
          <p class="text-center text-xs font-medium text-body">battles</p>
          <p class="text-center mb-2 text-xl font-light text-white">18</p>
        </div>
        <div class="pt-3 items-center">
          <LambBattleIcon class="text-center -mt-0.5 w-10 h-10" />
          <p class="text-center text-xs font-medium text-body">wins</p>
          <p class="text-center mb-2 text-xl font-light text-white">14</p>
        </div>
        <div class="pt-3 items-center">
          <LambBattleIcon class="text-center -mt-0.5 w-10 h-10" />
          <p class="text-center text-xs font-medium text-body">looses</p>
          <p class="text-center mb-2 text-xl font-light text-white">4</p>
        </div>
        <div class="pt-3 items-center">
          <LambBattleIcon class="text-center -mt-0.5 w-10 h-10" />
          <p class="text-center text-xs font-medium text-body">win rate</p>
          <p class="text-center mb-2 text-xl font-light text-green-400">% 70</p>
        </div>
      </div>
    </div>
    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul>
        <BattleLogsCard
          v-for="logs in battleLogs"
          :key="logs.enemy_user_name"
          :victory="logs.victory"
          :enemy_user_name="logs.enemy_user_name"
          :enemy_avatar="logs.enemy_avatar"
          :enemy_stats="logs.enemy_stats"
          :enemy_protocol="logs.enemy_protocol"
        />
      </ul>
    </div>
  </div>
</template>

<style scoped></style>
