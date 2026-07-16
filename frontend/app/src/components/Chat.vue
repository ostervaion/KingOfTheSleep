<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket' // Importamos el nuevo composable unificado

const emit = defineEmits(['close'])
const props = defineProps({
  to_user: {
    type: String,
    required: true,
  },
})

const { chatMessages, isConnected, isAuthenticated, sendPayload, onlineUsers } = useWebSocket()

const isTargetOnline = computed(() => onlineUsers.value.has(props.to_user))

const messageText = ref('')
const messagesContainer = ref(null)

const conversationMessages = computed(() => {
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

  sendPayload('chat:message', {
    to: props.to_user,
    text: messageText.value.trim(),
  })

  messageText.value = ''

  scrollToBottom()
}

onMounted(() => {
  scrollToBottom()
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
            {{ props.to_user[0].toUpperCase() }}
          </div>
          <div>
            <p class="text-sm font-medium text-[#e8e8f0] leading-none">{{ props.to_user }}</p>
            <p class="text-xs mt-1 flex items-center gap-1.5">
              <span
                :class="['w-2 h-2 rounded-full', isTargetOnline ? 'bg-[#4caf50]' : 'bg-[#f44336]']"
              ></span>
              <span class="text-[#555]">{{ isTargetOnline ? 'Conectado' : 'Desconectado' }}</span>
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
          Esperando mensajes...
        </p>

        <!-- Iteramos sobre los mensajes filtrados para esta conversación -->
        <div
          v-for="(msg, index) in conversationMessages"
          :key="index"
          :class="['flex', msg.from === props.to_user ? 'justify-start' : 'justify-end']"
        >
          <div
            :class="[
              'max-w-[75%] px-3 py-2',
              msg.from === props.to_user
                ? 'bg-[#25252e] rounded-tl rounded-tr-xl rounded-br-xl rounded-bl-xl'
                : 'bg-[#2d2d4a] rounded-tl-xl rounded-tr rounded-br-xl rounded-bl-xl',
            ]"
          >
            <p
              :class="[
                'text-[10px] mb-1',
                msg.from === props.to_user ? 'text-[#555]' : 'text-[#8888aa] text-right',
              ]"
            >
              {{ msg.from === props.to_user ? msg.from : 'tú' }}
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
            isConnected && isAuthenticated ? 'Escribe un mensaje...' : 'Conectando al servidor...'
          "
          @keyup.enter="handleSend"
        />
        <button
          @click="handleSend"
          :disabled="!isConnected || !isAuthenticated"
          class="bg-[#3d3d7a] hover:bg-[#4a4a99] disabled:bg-[#252535] disabled:text-[#555] px-4 py-2 rounded-lg text-[#aaaaee] text-sm font-medium transition-colors"
        >
          ➤
        </button>
      </div>
    </div>
  </div>
</template>
