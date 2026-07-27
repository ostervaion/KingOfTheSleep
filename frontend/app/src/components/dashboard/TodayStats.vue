<script setup>
import { ref, computed } from 'vue'
import BoxingGlove from '@/assets/boxing-glove.svg'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'
import BattleLog from '@/components/dashboard/battleLogPopUp.vue'

const dialog = ref(null)
const battleLogRef = ref(null)

const props = defineProps({
  todayStats: {
    type: Object,
    default: () => ({
      wins: 0,
      losses: 0,
    }),
  },
})

const summary = computed(() => {
  const wins = Number(props.todayStats?.wins ?? 0)
  const losses = Number(props.todayStats?.losses ?? 0)
  const battles = wins + losses

  const winRate =
    battles > 0
      ? Math.round((wins / battles) * 100)
      : 0

  return {
    battles,
    wins,
    losses,
    winRate,
  }
})

const winRateColor = computed(() => {
  if (summary.value.winRate >= 60) {
    return 'text-green-400 border-green-400'
  }

  if (summary.value.winRate <= 40) {
    return 'text-red-400 border-red-400'
  }

  return 'text-orange-400 border-orange-400'
})

async function openDialog() {
  dialog.value?.showModal()
  await battleLogRef.value?.loadLogs()
}

function closeDialog() {
  dialog.value?.close()
}
</script>

<template>
  <div
    class="font-inter flex min-h-0 flex-2 flex-col overflow-hidden rounded-xl border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20"
  >
    <div class="px-6 pb-4 pt-5.5">
      <div class="flex items-center justify-between">
        <div
          class="rounded-md border border-cyan-200 px-1.5 py-0.5 leading-none text-gray-800"
        >
          <h2 class="text-heading text-xs font-medium text-cyan-200">
            Today's Stats
          </h2>
        </div>

        <div class="flex rounded-full px-1.25 text-right">
          <div
            class="flex rounded-full bg-(--kots-background-color) px-1.25 py-0.75"
          >
            <button
              type="button"
              class="px-2 py-1 text-xs font-medium leading-none text-white"
              @click="openDialog"
            >
              See all
            </button>
          </div>
        </div>
      </div>

      <div
        class="grid grid-cols-4 justify-between gap-1 rounded-lg py-3 sm:py-6"
      >
        <!-- Battles -->
        <div class="justify-center">
          <p
            class="pb-1 text-center text-xs font-medium text-zinc-400"
          >
            Battles
          </p>

          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <BoxingGlove class="h-7 w-7 shrink-0" />

            <div class="min-w-0">
              <p class="mt-1 text-xl font-normal leading-none text-white">
                {{ summary.battles }}
              </p>
            </div>
          </div>
        </div>

        <!-- Wins -->
        <div class="justify-center">
          <p
            class="pb-1 text-center text-xs font-medium text-zinc-400"
          >
            Wins
          </p>

          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <TriangleUp class="h-7 w-7 shrink-0" />

            <div class="min-w-0">
              <p class="mt-1 text-xl font-normal leading-none text-white">
                {{ summary.wins }}
              </p>
            </div>
          </div>
        </div>

        <!-- Losses -->
        <div class="justify-center">
          <p
            class="pb-1 text-center text-xs font-medium text-zinc-400"
          >
            Losses
          </p>

          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <TriangleDown class="h-7 w-7 shrink-0" />

            <div class="min-w-0">
              <p class="mt-1 text-xl font-normal leading-none text-white">
                {{ summary.losses }}
              </p>
            </div>
          </div>
        </div>

        <!-- Win rate -->
        <div class="justify-center">
          <p
            class="pb-1 text-center text-xs font-medium text-zinc-400"
          >
            Win rate
          </p>

          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <div
              class="grid h-7 w-7 shrink-0 place-items-center rounded-full border-2 text-lg font-semibold"
              :class="winRateColor"
            >
              %
            </div>

            <div class="min-w-0">
              <p
                class="mt-1 text-xl font-medium leading-none"
                :class="winRateColor"
              >
                {{ summary.winRate }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <Teleport to="body">
    <dialog
      ref="dialog"
      class="m-auto max-w-5xl overflow-y-auto rounded-xl border-none bg-transparent p-0 backdrop:bg-black/60 sm:w-[90vw] lg:w-[50vw]"
    >
      <BattleLog
        ref="battleLogRef"
        :summary="summary"
        @close="closeDialog"
      />
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