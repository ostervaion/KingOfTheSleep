<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LogOut from '@/components/dashboard/logOut.vue'
import ProfileSettings from '@/components/dashboard/profileSettings.vue'
import TutorialCompletedIcon from '@/assets/tutorial-completed-v2.svg'
import FirstVictoryFightIcon from '@/assets/achievement-v2.svg'
import First100PointsIcon from '@/assets/first-100-points-v2.svg'

const achievements = ref({
  tutorialCompleted: {
    unlocked: true,
    icon: TutorialCompletedIcon,
  },
  firstSleepFight: {
    unlocked: true,
    icon: FirstVictoryFightIcon,
  },
  first100Points: {
    unlocked: true,
    icon: First100PointsIcon,
  },
})


var usersData = ref({
  rank: '',
  level: '',
  xp: '',
  nextxp: '',
  todaysSleepScore: '',
})




const dialog = ref(null)
const dialog_settings = ref(null)

function openDialog() {
  dialog.value.showModal()
}

function closeDialog() {
  dialog.value.close()
}

function openDialogSettings() {
  dialog_settings.value.showModal()
}

function closeDialogSettings() {
  dialog_settings.value.close()
}

onMounted(() => {
  loadUsersData()
})

function loadUsersData() {
  usersData.value = {
    rank: '4,432',
    level: '42',
    currentxp: '18,450',
    nextxp: '25,000',
    todaysSleepScore: '2',
  }
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
        <p class="mb-4 text-xl font-light leading-tight text-white">#{{ usersData.rank }}</p>
        </div>
<div>
  <p class="text-xs font-medium tracking-wide text-body text-zinc-400">
    achievements
  </p>

  <div class="mt-1 flex items-center gap-2">
    <div
      v-for="(achievement, name) in achievements"
      :key="name"
    >
      <div
        v-if="achievement.unlocked"
        class="flex h-5 w-5 shrink-0 items-center justify-center overflow-hidden"
      >
        <component
          :is="achievement.icon"
          class="h-full w-full object-contain"
        />
      </div>
    </div>
  </div>
</div>
        </div>
        <p class="text-xs font-medium % tracking-wide text-body text-zinc-400">level</p>
        <p class="mb-2 text-xl font-light leading-tight text-white">{{ usersData.level }}</p>

        <div class="mb-2 h-1.5 w-full overflow-hidden rounded-full bg-neutral-800">
          <div class="h-full w-[74%] rounded-full bg-yellow-400"></div>
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
            stroke-dasharray="264"
            stroke-dashoffset="47"
            class="stroke-green-500"
          />
        </svg>

        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <div class="text-4xl font-bold leading-none text-green-500">
            {{ usersData.todaysSleepScore }}
          </div>
          <div class="text-base font-light leading-none text-white">/100</div>
        </div>
      </div>
    </div>
  </div>

  <Teleport to="body">
    <!-- log out button -->
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
