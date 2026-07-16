<script setup>
import { ref } from 'vue'
import { useDraggable } from '@vueuse/core'
import Chat from '@/components/dashboard/profileSettings.vue'
import ChatIcon from '@/assets/chat-icon.svg'

const button = ref(null)
const dragged = ref(false)
const dialog = ref(null)

let startPosition

const { style } = useDraggable(button, {
  containerElement: document.documentElement,

  initialValue: {
    x: window.innerWidth - 72,
    y: window.innerHeight - 72,
  },

  onStart(position) {
    dragged.value = false
    startPosition = position
  },

  onMove(position) {
    dragged.value = Math.hypot(position.x - startPosition.x, position.y - startPosition.y) > 5
  },
})

function handleClick() {
  if (dragged.value) {
    dragged.value = false
    return
  }
  dialog.value.showModal()
}

function closeDialog() {
  dialog.value.close()
}
</script>

<template>
  <button
    ref="button"
    :style="style"
    class="font-inter flex items-center justify-center bg-(--kots-blocks-color) border-b border-[color:var(--border)] shadow-md shadow-black/20 fixed z-50 h-14 w-14 touch-none rounded-full"
    @click="handleClick"
  >
  <ChatIcon class="h-7 w-auto text-cyan-200 " />
  </button>

    <Teleport to="body">
    <dialog
      ref="dialog"
      class="m-auto h-[90vh] w-[96vw] sm:w-[90vw] md:w-[500px] lg:w-[700px] max-w-[96vw] rounded-xl border-none bg-transparent p-0"
    >
      <Chat @close="closeDialog" />
    </dialog>
  </Teleport>
  
</template>
