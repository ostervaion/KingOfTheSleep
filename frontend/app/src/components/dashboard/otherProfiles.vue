<script setup>
import { ref } from 'vue'
import Chat from '@/components/Chat.vue'
import ChatIcon from '@/assets/chat-icon_white.svg'

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

function onClose() {
  emit('close')
}

function onChat() {
  selectedUser.value = props.user.username
  emit('chat', props.user)
}
</script>

<template>
  <Chat v-if="selectedUser" :to_user="selectedUser" @close="selectedUser = null" />

  <div
    class="font-inter flex max-h-[90vh] w-full flex-col overflow-hidden rounded-xl bg-(--kots-blocks-color) border-b border-[color:var(--border)] shadow-md shadow-black/20"
  >
    <div class="px-5 pb-3 pt-4 sm:px-6">
      <div class="flex items-start justify-end gap-4">
        <button
          @click="onClose"
          class="rounded-full px-2 text-lg leading-none text-neutral-400 transition hover:text-white"
        >
          ×
        </button>
      </div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto px-5 pb-5 sm:px-6 ">
      <div class="rounded-lg p-5">
        <div class="flex items-center gap-4">
          <div
            class="h-24 w-24 items-center justify-center overflow-hidden rounded-full  bg-[var(--kots-background-color)]  sm:h-28 sm:w-28"
          >
            <img
              v-if="user.profilePicture"
              :src="user.profilePicture"
              alt="User profile picture"
              class="h-full w-full object-cover"
            />

            <div v-else class="text-3xl font-semibold uppercase text-cyan-200 ">
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
            <p class="text-xs font-medium text-body text-neutral-400">Rank</p>
            <p class="mt-1 text-xl font-light text-white">#{{ user.rank }}</p>
          </div>

          <div class="rounded-lg bg-[var(--kots-background-color)] px-4 py-3 text-center">
            <p class="text-xs font-medium text-body text-neutral-400">Level</p>
            <p class="mt-1 text-xl font-light text-white">
              {{ user.level }}
            </p>
          </div>

          <div class="rounded-lg bg-[var(--kots-background-color)] px-4 py-3 text-center">
            <p class="text-xs font-medium text-body text-neutral-400">Points</p>
            <p class="mt-1 text-xl font-light text-white">
              {{ user.points }}
            </p>
          </div>
        </div>
        <div class="flex justify-end items-center">
        <button
          @click="onChat"
          class="mt-5 flex items-center justify-center gap-2 rounded-full bg-cyan-200 px-4 py-2.5 text-xs font-semibold text-[#171715] transition hover:bg-cyan-50"
        >
          <ChatIcon class="h-5 w-5 shrink-0" />
          <span>Chat with {{ user.username }}</span>
        </button>
        </div>
      </div>
    </div>
  </div>
</template>
