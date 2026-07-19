<script setup>
import { ref } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
import Chat from '@/components/Chat.vue'

const emit = defineEmits(['close'])

// view: { type: 'list' } | { type: 'global' } | { type: 'private', username }
const view = ref({ type: 'list' })

const { conversations, onlineUsers, unreadGlobal, myUsername } = useWebSocket()

function openGlobal() {
  view.value = { type: 'global' }
}

function openPrivate(username) {
  view.value = { type: 'private', username }
}

function backToList() {
  view.value = { type: 'list' }
}
</script>

<template>
  <!-- Listado: chat global + conversaciones -->
  <div
    v-if="view.type === 'list'"
    class="fixed inset-0 flex items-center justify-center bg-black/60 z-50"
  >
    <div
      class="w-full max-w-md bg-[#1a1a1f] border border-[#2a2a2f] rounded-2xl overflow-hidden shadow-2xl flex flex-col"
    >
      <div
        class="flex items-center justify-between px-5 py-3 bg-[#16161a] border-b border-[#2a2a2f]"
      >
        <p class="text-sm font-medium text-[#e8e8f0]">Mensajes</p>
        <button
          @click="emit('close')"
          class="text-[#555] hover:text-[#aaa] transition-colors text-lg"
        >
          ✕
        </button>
      </div>

      <div class="max-h-[70vh] overflow-y-auto">
        <!-- Entrada al chat global -->
        <button
          @click="openGlobal"
          class="w-full flex items-center gap-3 px-5 py-3 hover:bg-[#20202a] transition-colors border-b border-[#2a2a2f]"
        >
          <div class="w-9 h-9 rounded-full bg-[#2a2a3a] flex items-center justify-center text-lg">
            🌐
          </div>
          <div class="flex-1 text-left">
            <p class="text-sm text-[#e8e8f0] font-medium leading-none">Chat global</p>
            <p class="text-xs text-[#555] mt-1">Todos los usuarios</p>
          </div>
          <span
            v-if="unreadGlobal > 0"
            class="min-w-[20px] h-5 px-1.5 rounded-full bg-[#5555dd] text-[10px] text-white flex items-center justify-center font-semibold"
          >
            {{ unreadGlobal }}
          </span>
        </button>

        <!-- Conversaciones privadas -->
        <p v-if="conversations.length === 0" class="text-sm text-[#555] text-center py-8">
          Nadie te ha escrito todavía
        </p>

        <button
          v-for="conv in conversations"
          :key="conv.username"
          @click="openPrivate(conv.username)"
          class="w-full flex items-center gap-3 px-5 py-3 hover:bg-[#20202a] transition-colors border-b border-[#232329]"
        >
          <div class="relative shrink-0">
            <div
              class="w-9 h-9 rounded-full bg-[#2a2a3a] flex items-center justify-center text-[#8888cc] text-sm font-semibold"
            >
              {{ conv.username[0].toUpperCase() }}
            </div>
            <span
              :class="[
                'absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full border-2 border-[#1a1a1f]',
                onlineUsers.has(conv.username) ? 'bg-[#4caf50]' : 'bg-[#f44336]',
              ]"
            ></span>
          </div>
          <div class="flex-1 text-left min-w-0">
            <p class="text-sm text-[#e8e8f0] font-medium leading-none">{{ conv.username }}</p>
            <p class="text-xs text-[#666] mt-1 truncate">
              {{ conv.lastMessage.from === myUsername ? 'Tú: ' : '' }}{{ conv.lastMessage.text }}
            </p>
          </div>
          <span
            v-if="conv.unread > 0"
            class="min-w-[20px] h-5 px-1.5 rounded-full bg-[#5555dd] text-[10px] text-white flex items-center justify-center font-semibold"
          >
            {{ conv.unread }}
          </span>
        </button>
      </div>
    </div>
  </div>

  <!-- Chat abierto (global o privado). El cierre desde aquí vuelve al listado. -->
  <Chat
    v-else
    :scope="view.type"
    :to_user="view.type === 'private' ? view.username : null"
    @close="backToList"
  />
</template>
