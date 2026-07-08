<script setup>
import { ref } from 'vue'
import example from '@/assets/example.jpg'

const emit = defineEmits(['close', 'save', 'delete-account', 'change-picture', 'delete-picture'])

const form = ref({
  username: 'matxi182',
  country: 'Spain',
  email: 'martin@example.com',
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

function onClose() {
  emit('close')
}

function onChangePicture() {
  emit('change-picture')
}

function onDeletePicture() {
  emit('delete-picture')
}

function onDeleteAccount() {
  emit('delete-account')
}

function onSaveChanges() {
  emit('save', form.value)
}
</script>

<template>
  <div
    class="font-inter flex max-h-[90vh] w-full flex-col overflow-hidden rounded-xl bg-(--kots-blocks-color) border-b border-[color:var(--border)] shadow-md shadow-black/20"
  >
    <div class="px-4 pb-4 pt-3 sm:px-6 md:px-8 md:pb-5 md:pt-4">
      <div class="flex items-start justify-end gap-4">
        <button
          @click="onClose"
          class="rounded-full px-2 text-lg leading-none text-neutral-400 transition hover:text-white"
        >
          ×
        </button>
      </div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto px-4 pb-4 sm:px-6 md:px-6 md:pb-6">
      <div class="rounded-lg  p-4 sm:p-5">
        <div class="flex flex-col items-center gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div class="flex flex-col items-center gap-3 sm:flex-row sm:items-center">
            <img
              :src="example"
              alt="Profile picture"
              class="h-24 w-24 rounded-full border border-white/10 object-cover shadow-md shadow-black/30 sm:h-28 sm:w-28"
            />

            <div class="text-center sm:text-left">
              <p class="text-sm font-medium text-white">Profile Picture</p>
              <p class="mt-1 max-w-[260px] text-xs leading-relaxed text-body text-neutral-400">
                Upload a new avatar or remove the current one from your profile.
              </p>
            </div>
          </div>

          <div class="flex w-full flex-col gap-2 sm:w-auto sm:flex-row">
            <button
              @click="onChangePicture"
              class="rounded-md bg-(--kots-background-color) px-3 py-2 text-xs font-medium text-white transition hover:bg-white/10"
            >
              Change Picture
            </button>

            <button
              @click="onDeletePicture"
              class="rounded-md  px-3 py-2 text-xs font-medium text-red-300 transition hover:bg-red-950/35"
            >
              Delete Picture
            </button>
          </div>
        </div>

        <div class="mb-5"></div>

        <form class="space-y-4" @submit.prevent="onSaveChanges">
          <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
            <label class="block">
              <span class="mb-1.5 block text-xs font-medium text-body text-neutral-400">Username</span>
              <input
                v-model="form.username"
                disabled
                type="text"
                class="w-full rounded-lg border border-white/5 bg-black/25 px-3 py-2.5 text-sm text-neutral-500 outline-none cursor-not-allowed"
              />
            </label>

            <label class="block">
              <span class="mb-1.5 block text-xs font-medium text-body text-neutral-400">Country</span>
              <input
                v-model="form.country"
                type="text"
                class="inputField"
                placeholder="Country"
              />
            </label>

            <label class="block md:col-span-2">
              <span class="mb-1.5 block text-xs font-medium text-body text-neutral-400">Email</span>
              <input
                v-model="form.email"
                type="email"
                class="inputField"
                placeholder="email@example.com"
              />
            </label>
          </div>

          <div class="rounded-lg bg-white/[0.02] p-3 sm:p-4">
            <p class="mb-3 text-sm font-medium text-white">Change Password</p>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
              <label class="block">
                <span class="mb-1.5 block text-xs font-medium text-body text-neutral-400">
                  Current Password
                </span>
                <input
                  v-model="form.currentPassword"
                  type="password"
                  class="inputField"
                  placeholder="••••••••"
                />
              </label>

              <label class="block">
                <span class="mb-1.5 block text-xs font-medium text-body text-neutral-400">
                  New Password
                </span>
                <input
                  v-model="form.newPassword"
                  type="password"
                  class="inputField"
                  placeholder="••••••••"
                />
              </label>

              <label class="block">
                <span class="mb-1.5 block text-xs font-medium text-body text-neutral-400">
                  Confirm Password
                </span>
                <input
                  v-model="form.confirmPassword"
                  type="password"
                  class="inputField"
                  placeholder="••••••••"
                />
              </label>
            </div>
          </div>
        </form>
      </div>
    </div>

    <div
      class="flex flex-col-reverse gap-2 border-t border-white/10 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 md:px-8"
    >
      <button
        @click="onDeleteAccount"
        class="rounded-md px-3 py-2 text-xs font-medium text-red-400 transition "
      >
        Delete Account
      </button>

      <button
        @click="onSaveChanges"
        class="rounded-md  px-4 py-2  text-xs font-medium  text-white transition"
      >
        Save Changes
      </button>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";

.inputField {
  @apply w-full rounded-lg border border-white/10 bg-[var(--kots-background-color)] px-3 py-2.5 text-sm text-white outline-none transition placeholder:text-neutral-600 focus:border-cyan-100/60;
}

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
