<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/api/api'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const props = defineProps({
  email: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['back', 'login'])

const username = ref('')
const email = ref(props.email)
const password = ref('')
const acceptedTerms = ref(false)

const message = ref('')
const loading = ref(false)

async function register() {
  if (loading.value) return

  message.value = ''

  if (username.value.trim().length < 5) {
    message.value = '// username must be at least 5 characters long'
    return
  }

  if (password.value.length < 8) {
    message.value = '// password must be at least 8 characters long'
    return
  }

  if (!acceptedTerms.value) {
    message.value = '// you must accept the Terms of Service and Privacy Policy'
    return
  }

  loading.value = true

  try {
    await api.post('/register', {
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value,
    })

    message.value = '// user registered successfully'
    auth.setTutorial()
    emit('login')
  } catch (error) {
    message.value = `// ${error.response?.data?.detail || 'registration failed'}`
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form class="space-y-5" @submit.prevent="register">
    <div>
      <span class="mb-3 block text-[10px] uppercase tracking-[4px] text-(--accent)">
        Register
      </span>

      <div class="space-y-4">
        <label class="block text-[10px] uppercase tracking-[2px] text-(--muted)">
          Username

          <input
            v-model.trim="username"
            type="text"
            required
            minlength="5"
            autocomplete="username"
            placeholder="username_"
            class="mt-2 w-full rounded-2xl border border-(--border) bg-(--surface-soft) px-4 py-3 text-sm text-(--text) outline-none placeholder:text-(--muted) transition-colors duration-150 focus:border-(--accent)"
          />

          <span class="mt-1 block text-[10px] normal-case tracking-normal text-(--muted)">
            At least 5 characters
          </span>
        </label>

        <label class="block text-[10px] uppercase tracking-[2px] text-(--muted)">
          Email

          <input
            v-model.trim="email"
            type="email"
            required
            autocomplete="email"
            placeholder="email@example.com"
            class="mt-2 w-full rounded-2xl border border-(--border) bg-(--surface-soft) px-4 py-3 text-sm text-(--text) outline-none placeholder:text-(--muted) transition-colors duration-150 focus:border-(--accent)"
          />
        </label>

        <label class="block text-[10px] uppercase tracking-[2px] text-(--muted)">
          Password

          <input
            v-model="password"
            type="password"
            required
            minlength="8"
            autocomplete="new-password"
            placeholder="••••••••"
            class="mt-2 w-full rounded-2xl border border-(--border) bg-(--surface-soft) px-4 py-3 text-sm text-(--text) outline-none placeholder:text-(--muted) transition-colors duration-150 focus:border-(--accent)"
          />

          <span class="mt-1 block text-[10px] normal-case tracking-normal text-(--muted)">
            At least 8 characters
          </span>
        </label>
      </div>
    </div>

    <div class="rounded-2xl border border-(--border) bg-(--surface-soft) p-4">
      <div class="flex items-start gap-3">
        <input
          id="accept-legal"
          v-model="acceptedTerms"
          type="checkbox"
          required
          class="mt-1 h-4 w-4 shrink-0 cursor-pointer accent-(--accent)"
        />

        <label for="accept-legal" class="cursor-pointer text-xs leading-5 text-(--muted)">
          I have read and accept the

          <RouterLink
            to="/terms"
            target="_blank"
            class="font-semibold text-(--accent) underline hover:text-(--button-hover)"
            @click.stop
          >
            Terms of Service
          </RouterLink>

          and the

          <RouterLink
            to="/privacy"
            target="_blank"
            class="font-semibold text-(--accent) underline hover:text-(--button-hover)"
            @click.stop
          >
            Privacy Policy
          </RouterLink>.
        </label>
      </div>
    </div>

    <button
      type="submit"
      :disabled="loading || !acceptedTerms"
      class="w-full rounded-2xl border border-(--accent) bg-(--surface-soft) px-4 py-3 text-sm font-semibold uppercase tracking-[2px] text-(--accent) transition-colors duration-150 hover:bg-(--surface) disabled:cursor-not-allowed disabled:opacity-40"
    >
      {{
        loading
          ? '// registering...'
          : acceptedTerms
            ? '▶ Register'
            : 'Accept terms to register'
      }}
    </button>

    <p
      v-if="message"
      role="status"
      class="text-sm tracking-[1px] text-(--muted)"
    >
      {{ message }}
    </p>

    <button
      type="button"
      class="text-(--accent) underline hover:text-(--button-hover)"
      @click="emit('back')"
    >
      Back
    </button>
  </form>
</template>