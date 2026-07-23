<script setup>
import { ref, watch, toRef } from 'vue'
import RankingUser from '@/components/dashboard/rankingUsers.vue'

const props = defineProps({
  rankingData: {
    type: Array,
    default: () => [],
  },
})

const selectedRanking = ref('today')
const usersRanking = ref([])

watch(
  () => props.rankingData,
  (value) => {
    usersRanking.value = value || []
  },
  { immediate: true },
)

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
        <div class="border border-cyan-200 rounded-md px-1.5 py-0.5 text-gray-800 leading-none">
          <h2 class="text-cyan-200 text-xs font-medium text-heading">Rankings</h2>
        </div>
        <div class="flex rounded-full bg-(--kots-background-color) px-1.25 py-0.75">
          <button :class="buttonClass('today')" @click="updateButtonColor('today')">today</button>

          <button :class="buttonClass('week')" @click="updateButtonColor('week')">week</button>

          <button :class="buttonClass('global')" @click="updateButtonColor('global')">
            global
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-[40px_1fr_100px_100px] px-6 pb-2 text-xs text-body text-zinc-400">
      <div>#</div>
      <div>player</div>
      <div class="text-right">points</div>
      <div class="text-right">change</div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul>
        <rankingUser
          v-for="user in usersRanking"
          :key="user.name"
          :ranking="user.ranking"
          :name="user.name"
          :points="user.points"
          :pos-change="user.posChange"
          :trend="user.trend"
        />
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
