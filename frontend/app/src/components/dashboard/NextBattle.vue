<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  nextBattle: {
    type: Object,
    default: null,
  },
})

const nextBattleSeconds = ref(0)
const endDaySeconds = ref(0)

let countdownInterval = null

watch(
  () => props.nextBattle,
  (newNextBattle) => {
    if (!newNextBattle) return

    nextBattleSeconds.value = newNextBattle.seconds ?? 0
    endDaySeconds.value = newNextBattle.endDay ?? 0
  },
  { immediate: true },
)

const formatTime = (seconds) => {
  const totalSeconds = Math.max(0, Number(seconds) || 0)

  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const secs = totalSeconds % 60

  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

onMounted(() => {
  countdownInterval = window.setInterval(() => {
    nextBattleSeconds.value = Math.max(0, nextBattleSeconds.value - 1)
    endDaySeconds.value = Math.max(0, endDaySeconds.value - 1)
  }, 1000)
})

onUnmounted(() => {
  if (countdownInterval) {
    window.clearInterval(countdownInterval)
  }
})
</script>

<template>
  <div
    v-if="props.nextBattle"
    class="font-inter text-sm text-heading flex items-center justify-between bg-(--kots-blocks-color) p-4 rounded-full border-b border-[color:var(--border)]"
  >
    <div class="flex items-center gap-2">
      <span class="text-4xl text-yellow-400">
        {{ '#' + props.nextBattle.currentRanking }}
      </span>

      <div>
        current ranking
        <span class="text-xl text-green-400 ml-2">
          {{ props.nextBattle.deltaRanking }}
        </span>
        since last battle
      </div>
    </div>

    <div class="flex items-center gap-2">
      <span
        class="inline-flex items-center text-sm font-bold bg-yellow-400 rounded-md px-2 py-2 text-gray-800 leading-none"
      >
        NEXT BATTLE IN
      </span>

      <span class="text-2xl">
        {{ formatTime(nextBattleSeconds) }}
      </span>
    </div>

    <div class="flex items-center">
      DAY ENDS IN
      <span class="text-2xl ml-2 mr-2">
        {{ formatTime(endDaySeconds) }}
      </span>
      until daily reset
    </div>
  </div>

  <div
    v-else
    class="font-inter text-sm text-heading bg-(--kots-blocks-color) p-4 rounded-full border-b border-[color:var(--border)]"
  >
    Loading next battle...
  </div>
</template>