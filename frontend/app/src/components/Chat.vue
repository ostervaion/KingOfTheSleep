<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket' // Importamos el nuevo composable unificado

const emit = defineEmits(['close'])
const props = defineProps({
  // Si scope es 'global' se ignora to_user y se usa el chat global
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
  // Avisamos al composable de qué chat estamos viendo, para que no cuente
  // como "no leídos" los mensajes de esta conversación mientras está abierta.
  setActiveChat(isGlobal.value ? 'global' : props.to_user)
  scrollToBottom()
})

onUnmounted(() => {
  setActiveChat(null)
})
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black/60 z-50">
    <div
      class="w-full max-w-md bg-[#1a1a1f] border border-[#2a2a2f] rounded-2xl overflow-hidden shadow-2xl"
    >
      <div
        class="flex items-center justify-between px-5 py-3 bg-[#16161a] border-b border-[#2a2a2f]"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-8 h-8 rounded-full bg-[#2a2a3a] flex items-center justify-center text-[#8888cc] text-sm font-semibold"
          >
            {{ isGlobal ? '🌐' : props.to_user[0].toUpperCase() }}
          </div>
          <div>
            <p class="text-sm font-medium text-[#e8e8f0] leading-none">
              {{ isGlobal ? 'Chat global' : props.to_user }}
            </p>
            <p v-if="isGlobal" class="text-xs mt-1 text-[#555]">All users</p>
            <p v-else class="text-xs mt-1 flex items-center gap-1.5">
              <span
                :class="['w-2 h-2 rounded-full', isTargetOnline ? 'bg-[#4caf50]' : 'bg-[#f44336]']"
              ></span>
              <span class="text-[#555]">{{ isTargetOnline ? 'Conected' : 'Disconected' }}</span>
            </p>
          </div>
        </div>

        <button
          @click="emit('close')"
          class="text-[#555] hover:text-[#aaa] transition-colors text-lg"
        >
          ✕
        </button>
      </div>

      <!-- Messages -->
      <div
        ref="messagesContainer"
        class="h-72 overflow-y-auto flex flex-col gap-2 px-4 py-4 bg-[#1a1a1f]"
      >
        <p v-if="conversationMessages.length === 0" class="text-sm text-[#555] text-center mt-8">
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
              'max-w-[75%] px-3 py-2',
              msg.from === myUsername
                ? 'bg-[#2d2d4a] rounded-tl-xl rounded-tr rounded-br-xl rounded-bl-xl'
                : 'bg-[#25252e] rounded-tl rounded-tr-xl rounded-br-xl rounded-bl-xl',
            ]"
          >
            <p
              :class="[
                'text-[10px] mb-1',
                msg.from === myUsername ? 'text-[#8888aa] text-right' : 'text-[#555]',
              ]"
            >
              {{ msg.from === myUsername ? 'tú' : msg.from }}
            </p>
            <p class="text-sm text-[#ddd]">{{ msg.text }}</p>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="flex gap-2 px-4 py-3 bg-[#16161a] border-t border-[#2a2a2f]">
        <input
          v-model="messageText"
          type="text"
          :disabled="!isConnected || !isAuthenticated"
          class="flex-1 bg-[#25252e] border border-[#333] rounded-lg px-3 py-2 text-sm text-[#e0e0e0] placeholder-[#555] outline-none focus:border-[#5555aa] disabled:opacity-50 transition-colors"
          :placeholder="
            isConnected && isAuthenticated ? 'Write a message...' : 'Conecting...'
          "
          @keyup.enter="handleSend"
        />
        <button
          @click="handleSend"
          :disabled="!isTargetOnline || !isAuthenticated || props.to_user == myUsername"
          class="bg-[#3d3d7a] hover:bg-[#4a4a99] disabled:bg-[#252535] disabled:text-[#555] px-4 py-2 rounded-lg text-[#aaaaee] text-sm font-medium transition-colors"
        >
          ➤
        </button>
      </div>
    </div>
  </div>
</template>
