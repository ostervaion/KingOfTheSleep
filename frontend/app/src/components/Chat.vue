<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'

const emit = defineEmits(['close'])
const props = defineProps({
  scope: {
    type: String,
    default: 'private',
  },
  to_user: {
    type: String,
    default: null,
  },
})

const isGlobal = computed(() => props.scope === 'global')

const {
  chatMessages,
  globalMessages,
  isConnected,
  isAuthenticated,
  sendPayload,
  onlineUsers,
  myUsername,
  setActiveChat,
} = useWebSocket()

const isTargetOnline = computed(() => !isGlobal.value && onlineUsers.value.has(props.to_user))

const messageText = ref('')
const messagesContainer = ref(null)

const conversationMessages = computed(() => {
  if (isGlobal.value) return globalMessages.value
  return chatMessages.value.filter((msg) => msg.from === props.to_user || msg.to === props.to_user)
})

async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function handleSend() {
  if (!isConnected.value || !isAuthenticated.value) {
    console.warn('El chat no está listo o no estás autenticado')
    return
  }
  if (!messageText.value.trim()) return

  if (isGlobal.value) {
    sendPayload('chat:global', {
      text: messageText.value.trim(),
    })
  } else {
    sendPayload('chat:message', {
      to: props.to_user,
      text: messageText.value.trim(),
    })
  }

  messageText.value = ''

  scrollToBottom()
}

onMounted(() => {
  setActiveChat(isGlobal.value ? 'global' : props.to_user)
  scrollToBottom()
})

onUnmounted(() => {
  setActiveChat(null)
})
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
    <div
      class="font-inter flex max-h-[90vh] w-full max-w-md flex-col overflow-hidden rounded-xl border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20"
    >
      <div class="flex items-center justify-between border-b border-white/10 px-4 py-4 sm:px-6">
        <div class="flex items-center gap-3">
          <div
            class="flex h-8 w-8 items-center justify-center rounded-full bg-(--kots-background-color) text-sm font-semibold text-cyan-200"
          >
            {{ isGlobal ? '🌐' : props.to_user[0].toUpperCase() }}
          </div>
          <div>
            <p class="text-sm font-medium leading-none text-white">
              {{ isGlobal ? 'Chat global' : props.to_user }}
            </p>
            <p v-if="isGlobal" class="mt-1 text-xs text-neutral-400">All users</p>
            <p v-else class="mt-1 flex items-center gap-1.5 text-xs">
              <span
                :class="['h-2 w-2 rounded-full', isTargetOnline ? 'bg-green-500' : 'bg-red-400']"
              ></span>
              <span class="text-neutral-400">{{
                isTargetOnline ? 'Conected' : 'Disconected'
              }}</span>
            </p>
          </div>
        </div>

        <button
          @click="emit('close')"
          class="rounded-full px-2 text-lg leading-none text-neutral-400 transition hover:text-white"
        >
          ✕
        </button>
      </div>

      <!-- Messages -->
      <div
        ref="messagesContainer"
        class="flex h-72 flex-col gap-2 overflow-y-auto px-4 py-4 sm:px-6"
      >
        <p
          v-if="conversationMessages.length === 0"
          class="mt-8 text-center text-sm text-neutral-500"
        >
          Waiting messages...
        </p>

        <!-- Iteramos sobre los mensajes filtrados para esta conversación -->
        <div
          v-for="(msg, index) in conversationMessages"
          :key="index"
          :class="['flex', msg.from === myUsername ? 'justify-end' : 'justify-start']"
        >
          <div
            :class="[
              'max-w-[75%] px-3 py-2 text-sm shadow-sm shadow-black/10',
              msg.from === myUsername
                ? 'rounded-bl-xl rounded-br-xl rounded-tl-xl rounded-tr bg-cyan-200 text-[#171715]'
                : 'rounded-bl-xl rounded-br-xl rounded-tl rounded-tr-xl bg-(--kots-background-color) text-white',
            ]"
          >
            <p
              :class="[
                'mb-1 text-[10px]',
                msg.from === myUsername ? 'text-right text-[#171715]/60' : 'text-neutral-400',
              ]"
            >
              {{ msg.from === myUsername ? 'tú' : msg.from }}
            </p>
            <p class="text-sm">{{ msg.text }}</p>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="flex gap-2 border-t border-white/10 px-4 py-4 sm:px-6">
        <input
          v-model="messageText"
          type="text"
          :disabled="!isConnected || !isAuthenticated"
          class="min-w-0 flex-1 rounded-lg border border-transparent bg-[var(--kots-background-color)] px-3 py-2.5 text-sm text-white outline-none transition placeholder:text-neutral-600 focus:border-cyan-200/60 disabled:cursor-not-allowed disabled:opacity-50"
          :placeholder="isConnected && isAuthenticated ? 'Write a message...' : 'Conecting...'"
          @keyup.enter="handleSend"
        />
        <button
          @click="handleSend"
          :disabled="!isTargetOnline || !isAuthenticated || props.to_user == myUsername"
          class="rounded-md bg-cyan-200 px-4 py-2 text-sm font-medium text-[#171715] transition hover:bg-cyan-100 disabled:cursor-not-allowed disabled:bg-(--kots-background-color) disabled:text-neutral-600"
        >
          ➤
        </button>
      </div>
    </div>
  </div>
</template>
