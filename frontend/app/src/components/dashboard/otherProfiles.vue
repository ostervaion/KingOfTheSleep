<script setup>
import { ref } from 'vue'
import Chat from '@/components/Chat.vue'

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

// 2. Creamos la variable reactiva para controlar el chat abierto
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
  <Chat 
    v-if="selectedUser" 
    :to_user="selectedUser" 
    @close="selectedUser = null" 
  />

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

    <div class="flex-1 min-h-0 overflow-y-auto px-5 pb-5 sm:px-6">
      <div class="rounded-lg p-5">
        <div class="flex flex-col items-center text-center">
          <div
            class="flex h-24 w-24 items-center justify-center overflow-hidden rounded-full border border-white/10 bg-[var(--kots-background-color)] shadow-md shadow-black/30 sm:h-28 sm:w-28"
          >
            <img
              v-if="user.profilePicture"
              :src="user.profilePicture"
              alt="User profile picture"
              class="h-full w-full object-cover"
            />

            <span
              v-else
              class="text-3xl font-semibold uppercase text-cyan-200"
            >
              {{ user.username?.charAt(0) || '?' }}
            </span>
          </div>

          <h3 class="mt-4 text-xl font-semibold leading-tight text-white">
            {{ user.username }}
          </h3>
        </div>

        <div class="my-5 border-t border-white/10"></div>

        <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div class="rounded-lg bg-[var(--kots-background-color)] px-4 py-3 text-center">
            <p class="text-xs font-medium text-body text-neutral-400">
              Rank
            </p>
            <p class="mt-1 text-xl font-light text-white">
              #{{ user.rank }}
            </p>
          </div>

          <div class="rounded-lg bg-[var(--kots-background-color)] px-4 py-3 text-center">
            <p class="text-xs font-medium text-body text-neutral-400">
              Level
            </p>
            <p class="mt-1 text-xl font-light text-white">
              {{ user.level }}
            </p>
          </div>

          <div class="rounded-lg bg-[var(--kots-background-color)] px-4 py-3 text-center">
            <p class="text-xs font-medium text-body text-neutral-400">
              Points
            </p>
            <p class="mt-1 text-xl font-light text-white">
              {{ user.points }}
            </p>
          </div>
        </div>

        <button
          @click="onChat"
          class="mt-5 w-full rounded-md bg-cyan-200 px-4 py-2.5 text-xs font-semibold text-[#171715] transition hover:bg-cyan-50"
        >
          Chat with {{ user.username }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";

.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #333;
}
</style>