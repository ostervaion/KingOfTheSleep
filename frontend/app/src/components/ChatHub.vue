<script setup>
import { ref, computed } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
import api from '@/api/api'
import Chat from './Chat.vue'

const emit = defineEmits(['close'])

// view: { type: 'list' } | { type: 'global' } | { type: 'private', username }
const view = ref({ type: 'list' })

// tab: 'chat' | 'friends'
const activeTab = ref('chat')

const { conversations, onlineUsers, unreadGlobal, myUsername } = useWebSocket()

const friends = ref([])
const friendsLoading = ref(false)
const friendsError = ref(false)

// Amigos online primero
const sortedFriends = computed(() => {
  return [...friends.value].sort((a, b) => {
    const aOnline = onlineUsers.value.has(a) ? 1 : 0
    const bOnline = onlineUsers.value.has(b) ? 1 : 0
    return bOnline - aOnline
  })
})

async function loadFriends() {
  friendsLoading.value = true
  friendsError.value = false
  try {
    const { data } = await api.get('/friends')
    friends.value = data
  } catch (err) {
    friendsError.value = true
    console.error('Error cargando amigos:', err)
  } finally {
    friendsLoading.value = false
  }
}

function selectTab(tab) {
  activeTab.value = tab
  if (tab === 'friends') {
    loadFriends()
  }
}

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

      <!-- Pestañas -->
      <div class="flex border-b border-[#2a2a2f] bg-[#16161a]">
        <button
          @click="selectTab('chat')"
          :class="[
            'flex-1 py-2.5 text-xs font-semibold transition-colors relative',
            activeTab === 'chat' ? 'text-[#e8e8f0]' : 'text-[#666] hover:text-[#999]',
          ]"
        >
          Chat
          <span
            v-if="activeTab === 'chat'"
            class="absolute bottom-0 left-1/2 -translate-x-1/2 h-0.5 w-10 bg-[#5555dd] rounded-full"
          ></span>
        </button>
        <button
          @click="selectTab('friends')"
          :class="[
            'flex-1 py-2.5 text-xs font-semibold transition-colors relative',
            activeTab === 'friends' ? 'text-[#e8e8f0]' : 'text-[#666] hover:text-[#999]',
          ]"
        >
          Friends
          <span
            v-if="activeTab === 'friends'"
            class="absolute bottom-0 left-1/2 -translate-x-1/2 h-0.5 w-10 bg-[#5555dd] rounded-full"
          ></span>
        </button>
      </div>

      <div v-if="activeTab === 'chat'" class="max-h-[70vh] overflow-y-auto">
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
            <p class="text-xs text-[#555] mt-1">All users</p>
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
          No conversations...
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

      <!-- Pestaña Amigos -->
      <div v-else class="max-h-[70vh] overflow-y-auto">
        <p v-if="friendsLoading" class="text-sm text-[#555] text-center py-8">Cargando amigos...</p>

        <p v-else-if="friendsError" class="text-sm text-[#e8455a] text-center py-8">
          Failed to load friends.
        </p>

        <p v-else-if="friends.length === 0" class="text-sm text-[#555] text-center py-8">
          No friends
        </p>

        <button
          v-for="username in sortedFriends"
          :key="username"
          @click="openPrivate(username)"
          class="w-full flex items-center gap-3 px-5 py-3 hover:bg-[#20202a] transition-colors border-b border-[#232329]"
        >
          <div class="relative shrink-0">
            <div
              class="w-9 h-9 rounded-full bg-[#2a2a3a] flex items-center justify-center text-[#8888cc] text-sm font-semibold"
            >
              {{ username[0].toUpperCase() }}
            </div>
            <span
              :class="[
                'absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full border-2 border-[#1a1a1f]',
                onlineUsers.has(username) ? 'bg-[#4caf50]' : 'bg-[#f44336]',
              ]"
            ></span>
          </div>
          <div class="flex-1 text-left min-w-0">
            <p class="text-sm text-[#e8e8f0] font-medium leading-none">{{ username }}</p>
            <p
              class="text-xs mt-1"
              :class="onlineUsers.has(username) ? 'text-[#4caf50]' : 'text-[#666]'"
            >
              {{ onlineUsers.has(username) ? 'Conected' : 'Disconected' }}
            </p>
          </div>
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
