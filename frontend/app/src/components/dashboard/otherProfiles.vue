<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import Chat from '@/components/Chat.vue'
import ChatIcon from '@/assets/chat-icon_white.svg'
import api from '@/api/api'

const emit = defineEmits(['close', 'chat'])

const props = defineProps({
  user: {
    type: Object,
    default: () => ({
      username: 'Enemy Player',
      profilePicture: '',
      rank: '4,432',
      level: '42',
      points: '2,500',
    }),
  },
})

const selectedUser = ref(null)

const friendStatus = ref('checking')

const friendButtonLabel = computed(() => {
  const labels = {
    checking: 'Checking friendship...',
    notFriend: 'Add as friend',
    adding: 'Adding...',
    friend: 'Delete friend',
    deleting: 'Deleting...',
    addError: 'Retry adding friend',
    deleteError: 'Retry deleting friend',
  }

  return labels[friendStatus.value]
})

const friendButtonDisabled = computed(() => {
  return ['checking', 'adding', 'deleting'].includes(friendStatus.value)
})

function onClose() {
  emit('close')
}

function onChat() {
  selectedUser.value = props.user.username
  emit('chat', props.user)
}

function getEncodedUsername() {
  return encodeURIComponent(props.user.username)
}

async function checkFriendship() {
  if (!props.user?.username) {
    friendStatus.value = 'notFriend'
    return
  }

  friendStatus.value = 'checking'

  try {
    const { data } = await api.get('/friends')

    const usernames = Array.isArray(data)
      ? data.map((friend) => (typeof friend === 'string' ? friend : friend.username))
      : []

    friendStatus.value = usernames.includes(props.user.username) ? 'friend' : 'notFriend'
  } catch (err) {
    console.error('No se pudo comprobar la lista de amigos:', err)

    friendStatus.value = 'notFriend'
  }
}

async function addFriend() {
  friendStatus.value = 'adding'

  try {
    await api.post(`/friends/${getEncodedUsername()}`)
    friendStatus.value = 'friend'
  } catch (err) {
    const detail = err.response?.data?.detail

    if (err.response?.status === 400 && detail === 'Ya sois amigos') {
      friendStatus.value = 'friend'
      return
    }

    friendStatus.value = 'addError'
    console.error('Error al añadir amigo:', err)
  }
}

async function deleteFriend() {
  friendStatus.value = 'deleting'

  try {
    await api.delete(`/friends/${getEncodedUsername()}`)

    friendStatus.value = 'notFriend'
  } catch (err) {
    const detail = err.response?.data?.detail

    if (err.response?.status === 404 && detail === 'No sois amigos') {
      friendStatus.value = 'notFriend'
      return
    }

    friendStatus.value = 'deleteError'
    console.error('Error al eliminar amigo:', err)
  }
}

async function toggleFriend() {
  if (friendButtonDisabled.value) return

  if (friendStatus.value === 'friend' || friendStatus.value === 'deleteError') {
    await deleteFriend()
    return
  }

  await addFriend()
}

onMounted(() => {
  checkFriendship()
})

watch(
  () => props.user.username,
  () => {
    selectedUser.value = null
    checkFriendship()
  },
)
</script>

<template>
  <Chat v-if="selectedUser" :to_user="selectedUser" @close="selectedUser = null" />

  <div
    class="font-inter flex max-h-[90vh] w-full flex-col overflow-hidden rounded-xl border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20"
  >
    <div class="px-5 pb-3 pt-4 sm:px-6">
      <div class="flex items-start justify-end gap-4">
        <button
          type="button"
          class="rounded-full px-2 text-lg leading-none text-neutral-400 transition hover:text-white"
          aria-label="Close"
          @click="onClose"
        >
          ×
        </button>
      </div>
    </div>

    <div class="min-h-0 flex-1 overflow-y-auto px-5 pb-5 sm:px-6">
      <div class="rounded-lg p-5">
        <div class="flex items-center gap-4">
          <div
            class="flex h-24 w-24 items-center justify-center overflow-hidden rounded-full bg-[var(--kots-background-color)] sm:h-28 sm:w-28"
          >
            <img
              v-if="user.profilePicture"
              :src="user.profilePicture"
              alt="User profile picture"
              class="h-full w-full object-cover"
            />

            <div v-else class="text-3xl font-semibold uppercase text-cyan-200">
              {{ user.username?.charAt(0) || '?' }}
            </div>
          </div>

          <h3 class="mt-4 text-xl font-semibold leading-tight text-white">
            {{ user.username }}
          </h3>
        </div>

        <div class="my-5"></div>

        <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
          <div class="rounded-lg bg-[var(--kots-background-color)] px-4 py-3 text-center">
            <p class="text-xs font-medium text-neutral-400">Rank</p>

            <p class="mt-1 text-xl font-light text-white">#{{ user.rank }}</p>
          </div>

          <div class="rounded-lg bg-[var(--kots-background-color)] px-4 py-3 text-center">
            <p class="text-xs font-medium text-neutral-400">Level</p>

            <p class="mt-1 text-xl font-light text-white">
              {{ user.level }}
            </p>
          </div>

          <div class="rounded-lg bg-[var(--kots-background-color)] px-4 py-3 text-center">
            <p class="text-xs font-medium text-neutral-400">Points</p>

            <p class="mt-1 text-xl font-light text-white">
              {{ user.points }}
            </p>
          </div>
        </div>

        <div class="mt-5 flex items-center justify-end gap-2 ">
        <button type="button" :disabled="friendButtonDisabled" :class="[
          'flex h-full w-full items-center justify-center  rounded-md px-4 py-2.5 text-xs font-semibold transition',
          friendStatus === 'friend' || friendStatus === 'deleting'
            ? 'bg-red-300 text-[#171715] hover:bg-red-200'
            : friendStatus === 'deleteError' ||
              friendStatus === 'addError'
              ? 'bg-amber-200 text-[#171715] hover:bg-amber-100'
              : 'bg-cyan-200 text-[#171715] hover:bg-cyan-50',
          friendButtonDisabled
            ? 'cursor-not-allowed opacity-60'
            : 'cursor-pointer',
        ]" @click="toggleFriend">
          {{ friendButtonLabel }}
        </button>
                  <button type="button"
            class="flex items-center justify-center gap-2 rounded-md bg-cyan-200 px-4 py-2.5 text-xs font-semibold text-[#171715] transition hover:bg-cyan-50"
            @click="onChat">
            <ChatIcon class="h-4 w-4 shrink-0" />

            <span>
              Chat 
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
