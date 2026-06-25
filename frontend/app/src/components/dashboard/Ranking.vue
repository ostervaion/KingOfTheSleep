<script setup>
import example from '@/assets/example.jpg'
import { ref, onMounted } from 'vue'
import RankingUser from '@/components/dashboard/rankingUsers.vue'

const selectedRanking = ref('today')
var usersRanking = ref([])

onMounted(() => {
  loadUsers()
})

function loadUsers() {
  usersRanking.value = [
    {
      ranking: '1',
      name: 'Martin',
      points: '2500',
      posChange: '3',
    },
    {
      ranking: '1',
      name: 'Martin',
      points: '2500',
      posChange: '3',
    },
    {
      ranking: '1',
      name: 'Martin',
      points: '2500',
      posChange: '4',
    },
  ]
  ///llamar a funcion back para tener todos los usaurios y sus datos en descendiente por punto
}

function updateButtonColor(ranking) {
  selectedRanking.value = ranking
}

function buttonClass(ranking) {
  return {
    clickedButton: selectedRanking.value === ranking,
    unclickedButton: selectedRanking.value !== ranking,
  }
}
</script>

<template>
  <div
    class="font-inter flex flex-col flex-1 min-h-0 overflow-hidden rounded-xl bg-(--kots-blocks-color) border-b border-[color:var(--border)] shadow-md shadow-black/20"
  >
    <div class="px-6 pb-4 pt-4">
      <div class="flex items-center justify-between">
        <h2 class="text-base font-medium text-heading">Rankings</h2>

        <div class="flex rounded-full bg-(--kots-background-color) p-1">
          <button
            class="rounded-full bg-(--kots-blocks-color) px-4 py-1.5 text-xs font-medium text-white transition"
          >
            today
          </button>

          <button class="rounded-full px-4 py-1.5 text-xs text-body transition hover:text-heading">
            week
          </button>

          <button class="rounded-full px-4 py-1.5 text-xs text-body transition hover:text-heading">
            global
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-[40px_1fr_100px_100px] px-6 pb-2 text-xs text-body">
      <div>#</div>
      <div>player</div>
      <div class="text-right">points</div>
      <div class="text-right">change</div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-sm text-heading">1</div>

            <div class="flex items-center gap-3">
              <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
              <span class="text-sm text-heading">DreamWalker</span>
            </div>

            <div class="text-right text-sm text-heading">2,560</div>

            <div class="text-right text-sm font-medium text-green-400">↑ 85</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-sm text-heading">2</div>

            <div class="flex items-center gap-3">
              <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">2,340</div>

            <div class="text-right text-sm font-medium text-green-400">↑ 35</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-sm text-heading">3</div>

            <div class="flex items-center gap-3">
              <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
              <span class="text-sm text-heading">RestLord</span>
            </div>

            <div class="text-right text-sm text-heading">2,180</div>

            <div class="text-right text-sm font-medium text-green-400">↑ 12</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-sm text-heading">4</div>

            <div class="flex items-center gap-3">
              <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
              <span class="text-sm text-yellow-400">KingMoon (You)</span>
            </div>

            <div class="text-right text-sm text-heading">2,120</div>

            <div class="text-right text-sm font-medium text-green-400">↑ 42</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-sm text-heading">5</div>

            <div class="flex items-center gap-3">
              <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
              <span class="text-sm text-heading">Zenith</span>
            </div>

            <div class="text-right text-sm text-heading">1,980</div>

            <div class="text-right text-sm font-medium text-red-400">↓ 5</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-sm text-heading">6</div>

            <div class="flex items-center gap-3">
              <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
              <span class="text-sm text-heading">MoonSleeper</span>
            </div>

            <div class="text-right text-sm text-heading">1,850</div>

            <div class="text-right text-sm font-medium text-red-400">↓ 3</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-sm text-heading">7</div>

            <div class="flex items-center gap-3">
              <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
              <span class="text-sm text-heading">DeepRest</span>
            </div>

            <div class="text-right text-sm text-heading">1,790</div>

            <div class="text-right text-sm font-medium text-green-400">↑ 7</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-sm text-heading">8</div>

            <div class="flex items-center gap-3">
              <img class="h-8 w-8 rounded-full object-cover" :src="example" alt="" />
              <span class="text-sm text-heading">NightOwl</span>
            </div>

            <div class="text-right text-sm text-heading">1,720</div>

            <div class="text-right text-sm font-medium text-red-400">↓ 8</div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";

.clickedButton {
  @apply rounded-full px-3 py-1.5 text-xs font-medium text-white transition;
  background-color: var(--kots-blocks-color);
}

.unclickedButton {
  @apply rounded-full px-3 py-1.5 text-xs font-medium text-white transition;
  background-color: var(--kots-background-color);
}

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
