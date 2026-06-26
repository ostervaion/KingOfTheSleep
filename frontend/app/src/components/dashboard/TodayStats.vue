<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LambBattleIcon from '@/assets/lamb_battle.svg'
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
    class="font-inter text-base font-medium text-heading flex-1 min-h-0 bg-(--kots-blocks-color) rounded-xl p-6 overflow-auto"
  >
    Today's Stats
  </div>
  <Teleport to="body">
    <dialog ref="dialog" class="m-auto w-[500px] max-w-[90vw] rounded-xl border-none p-0">
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
