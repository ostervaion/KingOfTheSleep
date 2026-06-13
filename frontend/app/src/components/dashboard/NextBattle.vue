<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const initialSeconds = 2000
const nextBattleSeconds = ref(initialSeconds)
let countdownInterval = null

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

onMounted(() => {
  countdownInterval = window.setInterval(() => {
    if (nextBattleSeconds.value > 0) {
      nextBattleSeconds.value -= 1
    } else {
      window.clearInterval(countdownInterval)
    }
  }, 1000)
})

onUnmounted(() => {
  if (countdownInterval) {
    window.clearInterval(countdownInterval)
  }
})
</script>

<template>
  <div class="flex items-center justify-between bg-(--surface) border border-(--border) p-4 rounded-xl">
    <div class="flex items-center gap-2">
      <span class="text-4xl text-yellow-400">#4</span>
      <div>
        current ranking <span class="text-xl text-green-400 ml-2">↑42</span> since last battle
      </div>
    </div>
    <div class="flex items-center gap-2">
      <span class="inline-flex items-center text-sm font-bold bg-yellow-400 rounded-md px-2 py-2 text-gray-800 leading-none">NEXT BATTLE IN</span>
      <span class="text-2xl">{{ formatTime(nextBattleSeconds) }}</span>
    </div>
    <div class="flex items-center">
      DAY ENDS IN <span class="text-2xl ml-2 mr-2">15:12:34</span> until daily reset
    </div>
  </div>
</template>
