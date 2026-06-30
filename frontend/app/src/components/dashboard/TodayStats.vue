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
    <div class="px-6 pb-4 pt-5">
      <div class="flex items-center justify-between">
        <div class="border border-cyan-100 rounded-md px-2 py-0.5 text-gray-800 leading-none">
          <h2 class="text-cyan-100 text-sm font-medium text-heading">Today's Stats</h2>
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
          <p class="text-center text-xs font-medium text-body">battles</p>
          <p class="text-center mb-2 text-xl font-light text-white">18</p>
        </div>
        <div class="pt-3 items-center">
          <TriangleUp class="text-center -mt-0.5 w-6.5 h-6.5 mb-0.5" />
          <p class="text-center text-xs font-medium text-body">wins</p>
          <p class="text-center mb-2 text-xl font-light text-white">14</p>
        </div>
        <div class="pt-3 items-center">
          <TriangleDown class="text-center -mt-0.5 w-6.5 h-6.5 mb-0.5" />
          <p class="text-center text-xs font-medium text-body">looses</p>
          <p class="text-center mb-2 text-xl font-light text-white">4</p>
        </div>
        <div class="pt-3 items-center">
          <p class="text-center text-xs font-medium text-body mb-0.5">win rate</p>
          <p class="text-center mb-2 text-xl font-light text-green-400">% 70</p>
        </div>
      </div>
    </div>
  </div>
<Teleport to="body">
  <dialog
    ref="dialog"
    class="bg-(--kots-blocks-color) m-auto h-[620px] w-1/2 max-w-[90vw] rounded-xl border-none p-0"
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
