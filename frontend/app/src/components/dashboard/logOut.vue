<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const emit = defineEmits(['close'])

const authStore = useAuthStore()
const router = useRouter()

function onLogout() {
  authStore.logout()
  emit('close')
  router.push('/')
}

function onClose() {
  emit('close')
}
</script>

<template>
  <div
    class="font-inter overflow-hidden rounded-xl border-2 border-red-950/50 bg-[var(--kots-blocks-color)] shadow-xl shadow-black/40"
  >
    <div class="px-6 py-5">
      <div class="mb-4 flex items-start justify-between gap-4">
        <div>
          <h2 class="text-base font-semibold text-white">Log out?</h2>

          <p class="mt-1 text-sm text-neutral-400">
            Are you sure you want to log out of your account?
          </p>
        </div>

        <button
          @click="onClose"
          class="rounded-full px-2 text-lg leading-none text-neutral-400 transition hover:text-white"
        >
          ×
        </button>
      </div>
      <div class="mt-6 flex justify-end gap-2">
        <button @click="onClose" class="px-2 py-0.5 text-xs font-medium leading-none text-white">
          cancel
        </button>
        <button @click="onLogout" class="px-2 py-0.5 text-xs font-medium leading-none text-red-900">
          log out
        </button>
      </div>
    </div>
  </div>
</template>
