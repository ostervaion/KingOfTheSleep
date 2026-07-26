<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BoxingGlove from '@/assets/boxing-glove.svg'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'
import BattleLog from '@/components/dashboard/battleLogPopUp.vue'

const dialog = ref(null)

function openDialog() {
  dialog.value.showModal()
}

function closeDialog() {
  dialog.value.close()
}
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
        <div
          class="grid grid-cols-4 justify-between gap-1 rounded-lg py-3  sm:py-6"
        >
          <div class="justify-center">
            <p class="text-body text-center text-xs font-medium text-zinc-400 pb-1">Battles</p>
          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <BoxingGlove class="h-7 w-7  shrink-0" />
            <div class="min-w-0">
              <p class="mt-1 text-xl font-normal leading-none text-white">
               18
              </p>
            </div>
          </div>
          </div>

          <div class="justify-center">
            <p class="text-body text-center text-xs font-medium text-zinc-400 pb-1">Wins</p>
          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <TriangleUp class="h-7 w-7  shrink-0" />
            <div class="min-w-0">
              <p class="mt-1 text-xl font-normal leading-none text-white">
               10
              </p>
            </div>
          </div>
          </div>

          <div class="justify-center">
            <p class="text-body text-center text-xs font-medium text-zinc-400 pb-1">Losses</p>
          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <TriangleDown class="h-7 w-7  shrink-0" />
            <div class="min-w-0">
              <p class="mt-1 text-xl font-normal leading-none text-white">
               8
              </p>
            </div>
          </div>
          </div>

                    <div class="justify-center">
            <p class="text-body text-center text-xs font-medium text-zinc-400 pb-1">Win rate</p>
          <div class="flex min-w-0 items-center justify-center gap-2.5">
            <div
              class="grid h-7 w-7 shrink-0 place-items-center rounded-full border-2 border-green-400 text-l font-semibold text-green-400"
            >
              %
            </div>
              <div class="min-w-0">
              <p class="mt-1 text-xl font-medium leading-none text-green-400">
               70
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
      class="m-auto lg:w-[50vw] max-w-5xl overflow-y-auto rounded-xl border-none bg-transparent p-0 backdrop:bg-black/60 sm:w-[90vw]"
    >
      <BattleLog @close="closeDialog" />
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
