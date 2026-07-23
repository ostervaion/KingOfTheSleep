<script setup>
import { ref } from 'vue'
import { useDraggable } from '@vueuse/core'
import { useWebSocket } from '@/composables/useWebSocket'
import ChatHub from '@/components/ChatHub.vue'
import ChatIcon from '@/assets/chat-icon.svg'

const { totalUnread } = useWebSocket()

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
    <ChatIcon class="h-7 w-auto text-cyan-200" />
    <span
      v-if="totalUnread > 0"
      class="absolute -top-1 -right-1 min-w-[20px] h-5 px-1 rounded-full bg-[#e8455a] text-[11px] text-white flex items-center justify-center font-semibold border-2 border-[#0f0f12]"
    >
      {{ totalUnread > 9 ? '9+' : totalUnread }}
    </span>
  </button>

  <Teleport to="body">
    <dialog
      ref="dialog"
      class="m-auto h-[90vh] w-[96vw] sm:w-[90vw] md:w-[500px] lg:w-[700px] max-w-[96vw] rounded-xl border-none bg-transparent p-0"
    >
      <ChatHub @close="closeDialog" />
    </dialog>
  </Teleport>
</template>
