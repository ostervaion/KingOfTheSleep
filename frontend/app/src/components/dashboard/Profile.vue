<script setup>
import { ref, computed, markRaw, watchEffect } from 'vue'
import LogOut from '@/components/dashboard/logOut.vue'
import ProfileSettings from '@/components/dashboard/profileSettings.vue'
import TutorialCompletedIcon from '@/assets/tutorial-completed-v2.svg'
import FirstVictoryFightIcon from '@/assets/achievement-v2.svg'
import First100PointsIcon from '@/assets/first-100-points-v2.svg'

const props = defineProps({
  experience: {
    type: String,
    default: '0',
  },

  sleepScore: {
    type: Object,
    default: () => ({
      labels: [],
      scores: [],
    }),
  },

  nextBattle: {
    type: Object,
    default: () => ({
      currentRanking: 0,
      seconds: 0,
      endDay: 0,
      deltaRanking: 0,
    }),
  },
})

const achievements = ref({
  tutorialCompleted: {
    unlocked: true,
    icon: markRaw(TutorialCompletedIcon),
  },

  firstSleepFight: {
    unlocked: false,
    icon: markRaw(FirstVictoryFightIcon),
  },

  first100Points: {
    unlocked: false,
    icon: markRaw(First100PointsIcon),
  },
})

const XP_BASE = 100

const totalExperience = computed(() => {
  return Math.max(0, Number(props.experience) || 0)
})

const level = computed(() => {
  return Math.floor(Math.log2(totalExperience.value / XP_BASE + 1)) + 1
})

const currentLevelXP = computed(() => {
  return XP_BASE * (2 ** (level.value - 1) - 1)
})

const nextLevelXP = computed(() => {
  return XP_BASE * (2 ** level.value - 1)
})

const xpProgress = computed(() => {
  const earnedThisLevel = totalExperience.value - currentLevelXP.value

  const requiredThisLevel = nextLevelXP.value - currentLevelXP.value

  if (requiredThisLevel <= 0) {
    return 0
  }

  const progress = (earnedThisLevel / requiredThisLevel) * 100

  return Math.min(100, Math.max(0, progress))
})

const sleepScoreValue = computed(() => {
  const scores = props.sleepScore?.scores ?? []

  if (!Array.isArray(scores) || scores.length === 0) {
    return 0
  }

  return Math.round(Number(scores.at(-1)) || 0)
})

const usersData = computed(() => ({
  rank: props.nextBattle.currentRanking,
  level: level.value,
  currentxp: totalExperience.value,
  nextxp: nextLevelXP.value,
  todaysSleepScore: sleepScoreValue.value,
}))

watchEffect(() => {
  achievements.value.firstSleepFight.unlocked = totalExperience.value > 0

  achievements.value.first100Points.unlocked = totalExperience.value >= 100
})

const dialog = ref(null)
const dialog_settings = ref(null)

function openDialog() {
  dialog.value?.showModal()
}

function closeDialog() {
  dialog.value?.close()
}

function openDialogSettings() {
  dialog_settings.value?.showModal()
}

function closeDialogSettings() {
  dialog_settings.value?.close()
}
</script>
<template>
  <div
    class="font-inter flex flex-col h-full flex-2 min-h-0 overflow-hidden rounded-xl bg-(--kots-blocks-color) border-b border-[color:var(--border)] shadow-md shadow-black/20"
  >
    <div class="px-6 pt-3">
      <div class="flex items-center justify-between">
        <div class="border border-cyan-200 rounded-md px-1.5 py-0.5 leading-none">
          <h2 class="text-cyan-200 text-xs font-medium text-heading">Profile</h2>
        </div>
        <div class="flex rounded-full px-1.25 text-right">
          <div class="flex rounded-full px-1.25 py-0.75 bg-(--kots-background-color) m-2">
            <button
              @click="openDialogSettings"
              class="p5 px-2 py-0.5 leading-none text-xs font-medium text-white text-heading"
            >
              settings
            </button>
          </div>

          <div
            class="flex border border-red-950 rounded-full px-1.25 py-0.75 bg-(--kots-background-color) m-2"
          >
            <button
              @click="openDialog"
              class="p5 px-2 py-0.5 leading-none text-xs font-medium text-red-800 text-heading"
            >
              log out
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="flex-1 min-h-0 flex justify-between gap-4 px-6 py-5 min-w-0">
      <div class="min-w-0 flex-1">
        <div class="flex justify-items-start">
          <div class="pr-7">
            <p class="text-xs font-medium tracking-wide text-body text-zinc-400">rank</p>
            <p class="mb-4 text-xl font-light leading-tight text-white">{{ usersData.rank }}</p>
          </div>
          <div>
            <p class="text-xs font-medium tracking-wide text-body text-zinc-400">achievements</p>

            <div class="mt-1 flex items-center gap-2">
              <div v-for="(achievement, name) in achievements" :key="name">
                <div
                  v-if="achievement.unlocked"
                  class="flex h-5 w-5 shrink-0 items-center justify-center overflow-hidden"
                >
                  <component :is="achievement.icon" class="h-full w-full object-contain" />
                </div>
              </div>
            </div>
          </div>
        </div>
        <p class="text-xs font-medium % tracking-wide text-body text-zinc-400">level</p>
        <p class="mb-2 text-xl font-light leading-tight text-white">{{ usersData.level }}</p>

        <div class="mb-2 h-1.5 w-full overflow-hidden rounded-full bg-neutral-800">
          <div
            class="h-full rounded-full bg-yellow-400 transition-all duration-500"
            :style="{ width: `${xpProgress}%` }"
          ></div>
        </div>

        <p class="text-xs font-light text-neutral-300">
          {{ usersData.currentxp }} / {{ usersData.nextxp }} xp
        </p>
      </div>

      <div class="relative size-24 lg:size-32 shrink-0">
        <svg class="size-full -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="42" fill="none" stroke-width="6" class="stroke-neutral-800" />

          <circle
            cx="50"
            cy="50"
            r="42"
            fill="none"
            stroke-width="6"
            stroke-linecap="round"
            :stroke-dasharray="2 * Math.PI * 42"
            :stroke-dashoffset="2 * Math.PI * 42 * (1 - Number(usersData.todaysSleepScore) / 100)"
            :class="usersData.todaysSleepScore >= 80 ? 'stroke-green-500' : 'stroke-red-400'"
          />
        </svg>

        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <div
            class="text-4xl font-bold leading-none"
            :class="usersData.todaysSleepScore >= 80 ? 'text-green-500' : 'text-red-400'"
          >
            {{ usersData.todaysSleepScore }}
          </div>
          <div class="text-base font-light leading-none text-white">/100</div>
        </div>
      </div>
    </div>
    <Teleport to="body">
      <dialog
        ref="dialog"
        class="m-auto w-[400px] max-w-[90vw] rounded-xl border-none bg-transparent"
      >
        <LogOut @close="closeDialog" />
      </dialog>

      <!-- profile settings button -->
      <dialog
        ref="dialog_settings"
        class="m-auto w-[720px] max-w-[94vw] rounded-xl border-none bg-transparent p-0"
      >
        <ProfileSettings @close="closeDialogSettings" />
      </dialog>
    </Teleport>
  </div>
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
