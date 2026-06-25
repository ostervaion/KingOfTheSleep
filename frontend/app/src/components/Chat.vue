<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const API_WS_URL = 'api/ws'
const emit = defineEmits(['close'])
const props = defineProps({
  to_user: {
    type: String,
    required: true,
  },
})

const ws = ref(null)
const messageText = ref('')
const messages = ref([])
const messagesContainer = ref(null)

async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function sendMessage() {
  if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
    console.warn('WebSocket no está conectado')
    return
  }
  if (!messageText.value.trim()) return

  ws.value.send(
    JSON.stringify({
      type: 'message',
      to: props.to_user,
      text: messageText.value.trim(),
    }),
  )
  messageText.value = ''
}

onMounted(() => {
  ws.value = new WebSocket(API_WS_URL)

  ws.value.onopen = () => {
    ws.value.send(
      JSON.stringify({
        type: 'auth',
        token: localStorage.getItem('token'),
        to: props.to_user,
      }),
    )
  }

  ws.value.onmessage = (event) => {
    try {
      const parsed = JSON.parse(event.data)
      messages.value.push(parsed)
    } catch {
      messages.value.push({ from: 'server', text: event.data })
    }
    scrollToBottom()
  }

  ws.value.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
})

onUnmounted(() => {
  ws.value?.close()
})
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black/60 z-50">
    <div
      class="w-full max-w-md bg-[#1a1a1f] border border-[#2a2a2f] rounded-2xl overflow-hidden shadow-2xl"
    >
      <button
        @click="emit('close')"
        class="ml-auto text-[#555] hover:text-[#aaa] transition-colors"
      >
        ✕
      </button>
      <div class="flex items-center gap-3 px-5 py-3 bg-[#16161a] border-b border-[#2a2a2f]">
        <div
          class="w-8 h-8 rounded-full bg-[#2a2a3a] flex items-center justify-center text-[#8888cc] text-sm"
        >
          {{ props.to_user[0].toUpperCase() }}
        </div>
        <div>
          <p class="text-sm font-medium text-[#e8e8f0] leading-none">{{ props.to_user }}</p>
          <p class="text-xs text-[#555] mt-0.5">chat</p>
        </div>
      </div>

      <!-- Messages -->
      <div
        ref="messagesContainer"
        class="h-72 overflow-y-auto flex flex-col gap-2 px-4 py-4 bg-[#1a1a1f]"
      >
        <p v-if="messages.length === 0" class="text-sm text-[#555] text-center mt-8">
          Esperando mensajes...
        </p>

        <div
          v-for="(msg, index) in messages"
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
          class="flex-1 bg-[#25252e] border border-[#333] rounded-lg px-3 py-2 text-sm text-[#e0e0e0] placeholder-[#555] outline-none focus:border-[#5555aa] transition-colors"
          placeholder="Escribe un mensaje..."
          @keyup.enter="sendMessage"
        />
        <button
          @click="sendMessage"
          class="bg-[#3d3d7a] hover:bg-[#4a4a99] px-4 py-2 rounded-lg text-[#aaaaee] text-sm transition-colors"
        >
          ➤
        </button>
      </div>
    </div>
  </div>
</template>
