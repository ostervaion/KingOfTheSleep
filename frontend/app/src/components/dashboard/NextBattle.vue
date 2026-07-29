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
    class="font-inter relative flex min-w-0 items-center justify-between gap-2 rounded-full border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20 px-3 py-2 text-heading sm:gap-4 sm:px-4 sm:py-3 lg:p-4 lg:px-6"
  >
    <!-- Ranking -->
    <div class="flex min-w-0 shrink-0 items-center gap-1.5 sm:gap-2">
      <span class="text-2xl align-baseline leading-none text-yellow-400 sm:text-3xl lg:text-4xl">
        {{ '#' + props.nextBattle.currentRanking }}
      </span>

      <div class="hidden min-w-0 text-xs leading-tight sm:block lg:text-sm">
        <span class="hidden:xs align-baseline">current ranking</span>
      </div>
      <div>
        <div class="ml-1 hidden lg:inline">
          <span class="ml-2 text-xs text-green-400 lg:text-xl">
            ▲ {{ props.nextBattle.deltaRanking }}
            <span class="text-zinc-400 text-sm">since last battle</span>
          </span>
        </div>
      </div>
    </div>

    <!-- Next battle -->
    <div
      class="flex min-w-0 flex-1 items-center justify-center gap-1.5 sm:gap-2 lg:absolute lg:left-1/2 lg:top-1/2 lg:flex-none lg:-translate-x-1/2 lg:-translate-y-1/2"
    >
      <span
        class="hidden shrink-0 items-center rounded-md bg-yellow-400 px-2 py-1.5 text-[10px] font-bold leading-none text-gray-800 sm:inline-flex lg:text-sm"
      >
        NEXT BATTLE IN
      </span>

      <span
        class="inline-flex shrink-0 items-center rounded-md bg-yellow-400 px-1.5 py-1 text-[9px] font-bold leading-none text-gray-800 sm:hidden"
      >
        NEXT BATTLE IN
      </span>

      <span class="whitespace-nowrap text-lg leading-none sm:text-xl lg:text-2xl">
        {{ formatTime(nextBattleSeconds) }}
      </span>
    </div>

    <!-- Day ends -->
    <div class="hidden md:block min-w-0 shrink-0 items-center gap-1 text-right">
      <span class="whitespace-nowrap text-zinc-400 text-xs leading-none sm:text-xl lg:text-2xl">
        {{ formatTime(endDaySeconds) }}
      </span>

      <span class="hidden text-zinc-400 text-xs lg:inline"> until daily reset</span>
    </div>
  </div>
  <div
    v-else
    class="font-inter rounded-full border-b border-[color:var(--border)] bg-yellow-400 px-3 py-2 text-sm sm:px-4 sm:py-3 lg:p-4"
  >
    <div class="flex items-cente rounded-md justify-center">
      <span class="font-inter text-sm font-bold text-(--kots-blocks-color) animate-pulse">
        LOADING NEXT BATTLE
      </span>
    </div>
  </div>
</template>
