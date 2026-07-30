<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/api'
import example from '@/assets/example.jpg'

const authStore = useAuthStore()
const router = useRouter()

const emit = defineEmits(['close', 'save', 'delete-account', 'avatar-updated', 'profile-updated'])

const user = ref(null)
const isLoadingUser = ref(false)
const loadUserError = ref('')
const form = ref({
  email: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const isSaving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)
const showDeleteConfirm = ref(false)
const isDeleting = ref(false)
const deleteError = ref('')
const fileInput = ref(null)
const previewSrc = ref(example)
const isUploading = ref(false)
const uploadError = ref('')

const ALLOWED_EXTENSIONS = new Set(['jpg', 'jpeg', 'png', 'webp', 'gif'])

const MAX_FILE_SIZE_MB = 5

function resolveAvatarSrc(avatarPath) {
  if (!avatarPath) {
    return example
  }

  if (
    avatarPath.startsWith('http://') ||
    avatarPath.startsWith('https://') ||
    avatarPath.startsWith('/api/')
  ) {
    return avatarPath
  }

  if (avatarPath.startsWith('/')) {
    return `/api${avatarPath}`
  }

  return `/api/${avatarPath}`
}

async function loadUser() {
  isLoadingUser.value = true
  loadUserError.value = ''

  try {
    const response = await api.get('/me')
    const fetchedUser = response.data

    user.value = fetchedUser
    form.value.email = fetchedUser?.email ?? ''

    const avatarPath = fetchedUser?.avatar_path ?? fetchedUser?.avatar_url ?? null

    previewSrc.value = resolveAvatarSrc(avatarPath)
  } catch (error) {
    console.error('Error cargando usuario:', error.response?.data ?? error)

    loadUserError.value = error.response?.data?.detail || 'Failed to load user information'
  } finally {
    isLoadingUser.value = false
  }
}

onMounted(() => {
  loadUser()
})

function onClose() {
  emit('close')
}

function onChangePicture() {
  uploadError.value = ''
  fileInput.value?.click()
}

async function onFileSelected(event) {
  const file = event.target.files?.[0]

  if (!file) return

  uploadError.value = ''

  const extension = file.name.split('.').pop()?.toLowerCase() ?? ''

  if (!ALLOWED_EXTENSIONS.has(extension)) {
    uploadError.value = 'Only image files are allowed (jpg, jpeg, png, webp, gif)'

    event.target.value = ''
    return
  }

  if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
    uploadError.value = `File is too large (max ${MAX_FILE_SIZE_MB}MB)`

    event.target.value = ''
    return
  }

  const previousPreview = previewSrc.value
  const localPreview = URL.createObjectURL(file)

  previewSrc.value = localPreview

  const formData = new FormData()
  formData.append('file', file)

  isUploading.value = true

  try {
    const response = await api.post('/profile/avatar', formData)

    const avatarPath = response.data?.avatar_path ?? response.data?.avatar_url

    if (!avatarPath) {
      throw new Error('The server did not return an avatar path')
    }

    const avatarSrc = resolveAvatarSrc(avatarPath)

    previewSrc.value = avatarSrc

    if (user.value) {
      user.value.avatar_path = avatarPath
    }

    emit('avatar-updated', avatarSrc)
  } catch (error) {
    console.error('Error subiendo avatar:', error.response?.data ?? error)

    uploadError.value = error.response?.data?.detail || error.message || 'Failed to upload image'

    previewSrc.value = previousPreview
  } finally {
    isUploading.value = false
    URL.revokeObjectURL(localPreview)
    event.target.value = ''
  }
}

function onDeleteAccount() {
  deleteError.value = ''
  showDeleteConfirm.value = true
}

function cancelDeleteAccount() {
  if (isDeleting.value) return

  deleteError.value = ''
  showDeleteConfirm.value = false
}

async function confirmDeleteAccount() {
  const username = user.value?.username

  if (!username) {
    deleteError.value = 'The username could not be loaded'
    return
  }

  isDeleting.value = true
  deleteError.value = ''

  try {
    await api.delete(`/users/${encodeURIComponent(username)}`)

    emit('delete-account', username)

    authStore.logout()
    await router.push('/')
  } catch (error) {
    console.error('Error eliminando cuenta:', error.response?.data ?? error)

    deleteError.value = error.response?.data?.detail || 'Failed to delete account'
  } finally {
    isDeleting.value = false
  }
}

async function onSaveChanges() {
  saveError.value = ''
  saveSuccess.value = false

  if (!user.value) {
    saveError.value = 'User information is not loaded'
    return
  }

  const wantsPasswordChange = Boolean(form.value.newPassword) || Boolean(form.value.confirmPassword)

  if (wantsPasswordChange) {
    if (!form.value.currentPassword) {
      saveError.value = 'Enter your current password to set a new one'
      return
    }

    if (form.value.newPassword !== form.value.confirmPassword) {
      saveError.value = 'New password and confirmation do not match'
      return
    }

    if (form.value.newPassword.length < 8) {
      saveError.value = 'New password must be at least 8 characters'
      return
    }
  }

  const originalEmail = user.value.email ?? ''
  const newEmail = form.value.email.trim()

  const payload = {}

  if (newEmail !== originalEmail) {
    payload.email = newEmail
  }

  if (wantsPasswordChange) {
    payload.current_password = form.value.currentPassword

    payload.new_password = form.value.newPassword
  }

  // No hay nada que modificar
  if (Object.keys(payload).length === 0) {
    saveSuccess.value = true
    return
  }

  isSaving.value = true

  try {
    const response = await api.patch('/profile', payload)

    const updatedUser = response.data?.user ?? response.data

    user.value = {
      ...user.value,
      ...updatedUser,
      email: updatedUser?.email ?? newEmail,
    }

    form.value.email = user.value.email ?? ''

    form.value.currentPassword = ''
    form.value.newPassword = ''
    form.value.confirmPassword = ''

    saveSuccess.value = true

    emit('profile-updated', user.value)
    emit('save', user.value)
  } catch (error) {
    console.error('Error guardando perfil:', error.response?.status, error.response?.data ?? error)

    saveError.value = error.response?.data?.detail || 'Failed to save changes'
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div
    class="font-inter flex max-h-[98vh] w-full flex-col overflow-hidden rounded-xl border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20"
  >
    <!-- Cabecera -->
    <div class="px-4 pb-1 pt-4 sm:px-6 md:px-8 md:pb-2 md:pt-5">
      <div class="flex items-start justify-end gap-4">
        <button
          type="button"
          aria-label="Close"
          class="rounded-full px-2 text-lg leading-none text-neutral-400 transition hover:text-white"
          @click="onClose"
        >
          ×
        </button>
      </div>
    </div>

    <!-- Contenido -->
    <div class="min-h-0 flex-1 overflow-y-auto px-4 pb-8 sm:px-6 md:px-8 md:pb-10">
      <template v-if="!showDeleteConfirm">
        <p v-if="loadUserError" class="mb-4 text-xs text-red-400">
          {{ loadUserError }}
        </p>

        <!-- Avatar -->
        <div
          class="flex flex-col items-center gap-4 sm:flex-row sm:items-center sm:justify-between"
        >
          <div class="flex flex-col items-center gap-3 sm:flex-row sm:items-center">
            <div class="relative h-24 w-24 sm:h-28 sm:w-28">
              <img
                :src="previewSrc"
                alt="Profile picture"
                class="h-24 w-24 rounded-full border border-white/10 object-cover shadow-md shadow-black/30 sm:h-28 sm:w-28"
                :class="{
                  'opacity-50': isUploading || isLoadingUser,
                }"
              />

              <div
                v-if="isUploading || isLoadingUser"
                class="absolute inset-0 flex items-center justify-center"
              >
                <div
                  class="h-5 w-5 animate-spin rounded-full border-2 border-white/30 border-t-white"
                ></div>
              </div>
            </div>

            <div class="text-center sm:text-left">
              <p class="text-sm font-medium text-white">Profile Picture</p>

              <p class="mt-1 max-w-[260px] text-xs leading-relaxed text-neutral-400">
                Upload a new avatar for your profile.
              </p>

              <p v-if="uploadError" class="mt-1 text-xs text-red-400">
                {{ uploadError }}
              </p>
            </div>
          </div>

          <div class="flex w-full flex-col gap-2 sm:w-auto sm:flex-row">
            <input
              ref="fileInput"
              type="file"
              accept=".jpg,.jpeg,.png,.webp,.gif,image/*"
              class="hidden"
              @change="onFileSelected"
            />

            <button
              type="button"
              :disabled="isUploading || isLoadingUser"
              class="rounded-md bg-(--kots-background-color) px-3 py-2 text-xs font-medium text-white transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
              @click="onChangePicture"
            >
              {{ isUploading ? 'Uploading...' : 'Change Picture' }}
            </button>
          </div>
        </div>

        <!-- Formulario -->
        <form class=" mt-6 space-y-4" @submit.prevent="onSaveChanges">
          <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
            <label class="block">
              <span class="mb-1.5 block text-xs font-medium text-neutral-400"> Username </span>

              <input
                :value="user?.username ?? ''"
                disabled
                type="text"
                class="w-full cursor-not-allowed rounded-lg border border-white/5 bg-black/25 px-3 py-2.5 text-sm text-neutral-500 outline-none"
                :placeholder="isLoadingUser ? 'Loading...' : 'Username'"
              />
            </label>

            <label class="block">
              <span class="mb-1.5 block text-xs font-medium text-neutral-400"> Email </span>

              <input
                v-model.trim="form.email"
                :disabled="isLoadingUser"
                type="email"
                autocomplete="email"
                class="inputField disabled:cursor-not-allowed disabled:opacity-50"
                placeholder="email@example.com"
              />
            </label>
          </div>

          <!-- Contraseña -->
          <div class="rounded-lg bg-white/[0.02] p-3 sm:p-4">
            <p class="mb-3 text-sm font-medium text-white">Change Password</p>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
              <label class="block">
                <span class="mb-1.5 block text-xs font-medium text-neutral-400">
                  Current Password
                </span>

                <input
                  v-model="form.currentPassword"
                  type="password"
                  autocomplete="current-password"
                  class="inputField"
                  placeholder="••••••••"
                />
              </label>

              <label class="block">
                <span class="mb-1.5 block text-xs font-medium text-neutral-400">
                  New Password
                </span>

                <input
                  v-model="form.newPassword"
                  type="password"
                  autocomplete="new-password"
                  class="inputField"
                  placeholder="••••••••"
                />
              </label>

              <label class="block">
                <span class="mb-1.5 block text-xs font-medium text-neutral-400">
                  Confirm Password
                </span>

                <input
                  v-model="form.confirmPassword"
                  type="password"
                  autocomplete="new-password"
                  class="inputField"
                  placeholder="••••••••"
                />
              </label>
            </div>
          </div>

          <p v-if="saveError" class="text-xs text-red-400">
            {{ saveError }}
          </p>

          <p v-if="saveSuccess" class="text-xs text-green-400 text-end">Changes saved successfully</p>
        </form>
      </template>

      <!-- Confirmación de borrado -->
      <div v-else class="flex flex-col items-center gap-4 px-2 py-6 text-center sm:py-10">
        <img
          src="/DeleteAccount.png"
          alt="Sorry to see you go"
          class="h-40 w-40 object-cover opacity-80 sm:h-60 sm:w-60"
        />

        <h3 class="text-base font-semibold text-white sm:text-lg">We're sorry to see you go</h3>

        <p class="max-w-sm text-sm leading-relaxed text-neutral-400">
          Deleting your account is
          <span class="font-semibold text-red-400"> permanent and irreversible </span>. All your
          data, progress, and history will be lost and cannot be recovered.
        </p>

        <p v-if="deleteError" class="max-w-sm text-xs text-red-400">
          {{ deleteError }}
        </p>

        <div class="mt-2 flex w-full max-w-xs flex-col gap-2 sm:flex-row">
          <button
            type="button"
            :disabled="isDeleting"
            class="flex-1 rounded-md bg-(--kots-background-color) px-4 py-2 text-xs font-medium text-white transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
            @click="cancelDeleteAccount"
          >
            Cancel
          </button>

          <button
            type="button"
            :disabled="isDeleting"
            class="flex-1 rounded-md bg-red-950/50 px-4 py-2 text-xs font-medium text-red-300 transition hover:bg-red-950/70 disabled:cursor-not-allowed disabled:opacity-50"
            @click="confirmDeleteAccount"
          >
            {{ isDeleting ? 'Deleting...' : 'Yes, delete my account' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Botones inferiores -->
    <div
      v-if="!showDeleteConfirm"
      class="flex flex-col-reverse gap-2 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 md:px-8"
    >
      <button
        type="button"
        class="rounded-md px-3 py-2 text-xs font-medium text-red-400 transition hover:bg-red-950/20"
        @click="onDeleteAccount"
      >
        Delete Account
      </button>

      <button
        type="button"
        :disabled="isSaving || isLoadingUser"
        class="rounded-md px-4 py-2 text-xs font-medium text-white transition disabled:cursor-not-allowed disabled:opacity-50"
        @click="onSaveChanges"
      >
        {{ isSaving ? 'Saving...' : 'Save Changes' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";

.inputField {
  @apply w-full rounded-lg border border-transparent bg-[var(--kots-background-color)] px-3 py-2.5 text-sm text-white outline-none transition placeholder:text-neutral-600 focus:border-cyan-200/60;
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
