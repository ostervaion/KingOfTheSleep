<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BoxingGlove from '@/assets/boxing-glove.svg'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'
import BattleLog from '@/components/dashboard/battleLogPopUp.vue'

const dialog = ref(null)
const battleLogRef = ref(null)

//function openDialog() {
//  dialog.value.showModal()
//}
async function openDialog() {
  dialog.value.showModal()
  battleLogRef.value?.loadLogs() // always refresh on open
}

function closeDialog() {
  dialog.value.close()
}

const props = defineProps({
  todayStats: {
    type: Object,
    default: () => ({ wins: 0, losses: 0 }),
  },
})

const summary = computed(() => {
  // Replace these fallback totals with API values when the full battle history is loaded.
  const battles = computed(() => props.todayStats.wins + props.todayStats.losses ?? 0)
  const wins = computed(() => props.todayStats.wins ?? 0)
  const losses = computed(() => props.todayStats.losses ?? 0)
  const winRate = computed(() => {
    const total = wins.value + losses.value
    if (total === 0) return 0
    return Math.round((wins.value / total) * 100)
  })

  return { battles, wins, losses, winRate }
})

const winRateColor = computed(() => {
  if (summary.winRate >= 60) return 'text-green-400'
  if (summary.winRate <= 40) return 'text-red-400'
  return 'text-orange-400'
})
</script>

<template>
  <div
    class="font-inter flex flex-col flex-2 min-h-0 overflow-hidden rounded-xl bg-(--kots-blocks-color) shadow-md shadow-black/20 border-b border-[color:var(--border)]"
  >
    <div class="px-6 pb-4 pt-5.5">
      <div class="flex items-center justify-between">
        <div class="border border-cyan-200 rounded-md px-1.5 py-0.5 text-gray-800 leading-none">
          <h2 class="text-cyan-200 text-xs font-medium text-heading">Today's Stats</h2>
        </div>
        <div class="flex rounded-full px-1.25 text-right">
          <div class="flex rounded-full px-1.25 py-0.75 bg-(--kots-background-color)">
            <button
              @click="openDialog"
              class="p5 px-2 py-1 leading-none text-xs font-medium text-white text-heading"
            >
              see all
            </button>
          </div>
        </div>
      </div>
      <div class="pt-2 px-5 flex items-center justify-between">
        <div class="pt-3 items-center">
          <BoxingGlove class="text-center -mt-0.5 w-6.5 h-6.5 mb-1" />
<!--          <p class="text-center text-xs font-medium text-body">battles</p>
          <p class="text-center mb-2 text-xl font-light text-white">{{ summary.battles }}</p>
        </div>
        <div class="pt-3 items-center">
          <TriangleUp class="text-center -mt-0.5 w-6.5 h-6.5 mb-0.5" />
          <p class="text-center text-xs font-medium text-body">wins</p>
          <p class="text-center mb-2 text-xl font-light text-white">{{ summary.wins }}</p>
        </div>
        <div class="pt-3 items-center">
          <TriangleDown class="text-center -mt-0.5 w-6.5 h-6.5 mb-0.5" />
          <p class="text-center text-xs font-medium text-body">looses</p>
          <p class="text-center mb-2 text-xl font-light text-white">{{ summary.losses }}</p>
        </div>
        <div class="pt-3 items-center">
          <p class="text-center text-xs font-medium text-body mb-0.5">win rate</p>
          <p class="text-center mb-2 text-xl font-light" :class="winRateColor">
            {{ summary.winRate }}%
          </p>
          -->
          <p class="text-center text-xs font-medium text-body text-zinc-400">battles</p>
          <p class="text-center mb-2 text-xl font-light text-white">18</p>
        </div>
        <div class="pt-3 items-center">
          <TriangleUp class="text-center -mt-0.5 w-6.5 h-6.5 mb-0.5" />
          <p class="text-center text-xs font-medium text-body text-zinc-400">wins</p>
          <p class="text-center mb-2 text-xl font-light text-white">14</p>
        </div>
        <div class="pt-3 items-center">
          <TriangleDown class="text-center -mt-0.5 w-6.5 h-6.5 mb-0.5" />
          <p class="text-center text-xs font-medium text-body text-zinc-400">looses</p>
          <p class="text-center mb-2 text-xl font-light text-white">4</p>
        </div>
        <div class="pt-3 items-center">
          <p class="text-center text-xs font-medium text-body mb-0.5 text-zinc-400">win rate</p>
          <p class="text-center mb-2 text-xl font-light text-green-400">% 70</p>
        </div>
      </div>
    </div>
  </div>
  <Teleport to="body">
    <dialog
      ref="dialog"
      class="m-auto lg:w-[50vw] max-w-5xl overflow-y-auto rounded-xl border-none bg-transparent p-0 backdrop:bg-black/60 sm:w-[90vw]"
    >
      <BattleLog ref="battleLogRef" :summary="summary" @close="closeDialog" />
    </dialog>
  </Teleport>
</template>

<style scoped>
dialog::backdrop {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(1px);
}

dialog {
  background: transparent;
  padding: 0;
  border: none;
}
</style>
