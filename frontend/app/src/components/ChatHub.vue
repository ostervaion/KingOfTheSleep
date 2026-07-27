<script setup>
import { ref, computed, onMounted } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
import api from '@/api/api'
import Chat from './Chat.vue'

const emit = defineEmits(['close'])

const view = ref({ type: 'list' })
const activeTab = ref('chat')

const { conversations, onlineUsers, unreadGlobal, myUsername } = useWebSocket()

const friends = ref([])
const friendsLoading = ref(false)
const friendsError = ref(false)

const sortedFriends = computed(() => {
  return [...friends.value].sort((a, b) => {
    const aOnline = onlineUsers.value.has(a) ? 1 : 0
    const bOnline = onlineUsers.value.has(b) ? 1 : 0
    return bOnline - aOnline
  })
})

async function loadFriends() {
  if (friendsLoading.value) return

  friendsLoading.value = true
  friendsError.value = false

  try {
    const { data } = await api.get('/friends')

    friends.value = Array.isArray(data) ? data : []

    console.log('Amigos actualizados:', friends.value)
  } catch (err) {
    friendsError.value = true
    console.error('Error cargando amigos:', err)
  } finally {
    friendsLoading.value = false
  }
}

async function selectTab(tab) {
  activeTab.value = tab

  if (tab === 'friends') {
    await loadFriends()
  }
}

function openGlobal() {
  view.value = { type: 'global' }
}

function openPrivate(username) {
  view.value = { type: 'private', username }
}

async function backToList() {
  view.value = { type: 'list' }

  if (activeTab.value === 'friends') {
    await loadFriends()
  }
}

onMounted(() => {
  loadFriends()
})
</script>

<template>
  <!-- Listado: chat global + conversaciones -->
  <div
    v-if="view.type === 'list'"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
  >
    <div
      class="font-inter flex max-h-[90vh] min-h-0 w-full max-w-md flex-col overflow-hidden rounded-xl border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20"
    >
      <div
        class="flex items-center justify-between  px-4 py-4 sm:px-6"
      >
        <p class="text-sm font-medium text-white">Messages</p>
        <button
          @click="emit('close')"
          class="rounded-full px-2 text-lg leading-none text-neutral-400 transition hover:text-white"
        >
          ✕
        </button>
      </div>

      <!-- Pestañas -->
      <div class="flex border-b border-white/10 px-4 sm:px-6">
        <button
          @click="selectTab('chat')"
          :class="[
            'relative flex-1 py-2.5 text-xs font-medium transition',
            activeTab === 'chat' ? 'text-cyan-200' : 'text-neutral-500 hover:text-white',
          ]"
        >
          Chat
          <span
            v-if="activeTab === 'chat'"
            class="absolute bottom-0 left-1/2 h-0.5 w-10 -translate-x-1/2 rounded-full bg-cyan-200"
          ></span>
        </button>
        <button
          @click="selectTab('friends')"
          :class="[
            'relative flex-1 py-2.5 text-xs font-medium transition',
            activeTab === 'friends' ? 'text-cyan-200' : 'text-neutral-500 hover:text-white',
          ]"
        >
          Friends
          <span
            v-if="activeTab === 'friends'"
            class="absolute bottom-0 left-1/2 h-0.5 w-10 -translate-x-1/2 rounded-full bg-cyan-200"
          ></span>
        </button>
      </div>

      <div v-if="activeTab === 'chat'" class="min-h-0 max-h-[70vh] overflow-y-auto">
        <!-- Entrada al chat global -->
        <button
          @click="openGlobal"
          class="flex w-full items-center gap-3 border-b border-white/5 px-4 py-3 text-left transition hover:bg-white/[0.03] sm:px-6"
        >
          <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-(--kots-background-color) text-lg">
            🌐
          </div>
          <div class="min-w-0 flex-1 text-left">
            <p class="text-sm font-medium leading-none text-white">Chat global</p>
            <p class="mt-1 text-xs text-neutral-400">All users</p>
          </div>
          <span
            v-if="unreadGlobal > 0"
            class="flex h-5 min-w-[20px] items-center justify-center rounded-full bg-cyan-200 px-1.5 text-[10px] font-semibold text-[#171715]"
          >
            {{ unreadGlobal }}
          </span>
        </button>

        <!-- Conversaciones privadas -->
        <p v-if="conversations.length === 0" class="py-8 text-center text-sm text-neutral-500">
          No conversations...
        </p>

        <button
          v-for="conv in conversations"
          :key="conv.username"
          @click="openPrivate(conv.username)"
          class="flex w-full items-center gap-3 border-b border-white/5 px-4 py-3 transition hover:bg-white/[0.03] sm:px-6"
        >
          <div class="relative shrink-0">
            <div
              class="flex h-9 w-9 items-center justify-center rounded-full bg-(--kots-background-color) text-sm font-semibold text-cyan-200"
            >
              {{ conv.username[0].toUpperCase() }}
            </div>
            <span
              :class="[
                'absolute -bottom-0.5 -right-0.5 h-2.5 w-2.5 rounded-full border-2 border-[var(--kots-blocks-color)]',
                onlineUsers.has(conv.username) ? 'bg-green-500' : 'bg-red-400',
              ]"
            ></span>
          </div>
          <div class="min-w-0 flex-1 text-left">
            <p class="text-sm font-medium leading-none text-white">{{ conv.username }}</p>
            <p class="mt-1 truncate text-xs text-neutral-500">
              {{ conv.lastMessage.from === myUsername ? 'Tú: ' : '' }}{{ conv.lastMessage.text }}
            </p>
          </div>
          <span
            v-if="conv.unread > 0"
            class="flex h-5 min-w-[20px] items-center justify-center rounded-full bg-cyan-200 px-1.5 text-[10px] font-semibold text-[#171715]"
          >
            {{ conv.unread }}
          </span>
        </button>
      </div>

<div v-else class="min-h-0 max-h-[70vh] overflow-y-auto">
  <p v-if="friendsLoading" class="py-8 text-center text-sm text-neutral-500">
    Loading friends...
  </p>

  <p v-else-if="friendsError" class="py-8 text-center text-sm text-red-400">
    Failed to load friends.
  </p>

  <p v-else-if="friends.length === 0" class="py-8 text-center text-sm text-neutral-500">
    No friends
  </p>

  <button
    v-for="username in sortedFriends"
    :key="username"
    @click="openPrivate(username)"
    class="flex w-full items-center gap-3 border-b border-white/5 px-4 py-3 transition hover:bg-white/[0.03] sm:px-6"
  >
    <div class="relative shrink-0">
      <div
        class="flex h-9 w-9 items-center justify-center rounded-full bg-(--kots-background-color) text-sm font-semibold text-cyan-200"
      >
        {{ username[0].toUpperCase() }}
      </div>

      <span
        :class="[
          'absolute -bottom-0.5 -right-0.5 h-2.5 w-2.5 rounded-full border-2 border-[var(--kots-blocks-color)]',
          onlineUsers.has(username) ? 'bg-green-500' : 'bg-red-400',
        ]"
      />
    </div>

    <div class="min-w-0 flex-1 text-left">
      <p class="text-sm font-medium leading-none text-white">
        {{ username }}
      </p>

      <p
        class="mt-1 text-xs"
        :class="onlineUsers.has(username) ? 'text-green-500' : 'text-neutral-500'"
      >
        {{ onlineUsers.has(username) ? 'Connected' : 'Disconnected' }}
      </p>
    </div>
  </button>

  <!-- Botón actualizar -->
  <div class="sticky bottom-0 border-t border-white/10 bg-(--kots-blocks-color) p-3 sm:px-6">
    <button
      type="button"
      :disabled="friendsLoading"
      @click="loadFriends"
      class="flex w-full items-center justify-center gap-2 rounded-md bg-(--kots-background-color) px-4 py-2.5 text-xs font-medium text-white transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
    >
      <span :class="{ 'animate-spin': friendsLoading }">↻</span>

      {{ friendsLoading ? 'Actualizando...' : 'Actualizar amigos' }}
    </button>
  </div>
  </div>
  </div>
</div>

  <Chat
    v-else
    :scope="view.type"
    :to_user="view.type === 'private' ? view.username : null"
    @close="backToList"
  />
</template>
