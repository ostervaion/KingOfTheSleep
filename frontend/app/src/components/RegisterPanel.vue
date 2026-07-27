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

const mensaje = ref('')
const loading = ref(false)

async function register() {
  if (loading.value) return

  if (!acceptedTerms.value) {
    mensaje.value = '// debes aceptar los términos y la política de privacidad'
    return
  }

  loading.value = true
  mensaje.value = ''

  try {
    await api.post('/register', {
      username: username.value,
      email: email.value,
      password: password.value,
    })

    mensaje.value = '// usuario registrado'
    auth.setTutorial()
    emit('login')
  } catch (error) {
    mensaje.value = `// ${error.response?.data?.detail || 'error al registrar'}`
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form class="font-inter space-y-5" @submit.prevent="register">
    <div>
      <span class="mb-4 block text-xs font-semibold uppercase tracking-[0.18em] text-yellow-400">
        Register
      </span>

      <div class="space-y-4">
        <label class="block text-xs font-medium tracking-wide text-[#A2A1A6]">
          Usuario

          <input
            v-model.trim="username"
            type="text"
            required
            autocomplete="username"
            placeholder="usuario_"
            class="mt-2 w-full rounded-lg border border-[color:var(--border)] bg-(--kots-background-color) px-4 py-3 text-sm text-white outline-none transition-colors duration-150 placeholder:text-[#6f6e73] focus:border-cyan-200 focus:ring-1 focus:ring-cyan-200"
          />
        </label>

        <label class="block text-xs font-medium tracking-wide text-[#A2A1A6]">
          Email

          <input
            v-model.trim="email"
            type="email"
            required
            autocomplete="email"
            placeholder="correo@dominio.com"
            class="mt-2 w-full rounded-lg border border-[color:var(--border)] bg-(--kots-background-color) px-4 py-3 text-sm text-white outline-none transition-colors duration-150 placeholder:text-[#6f6e73] focus:border-cyan-200 focus:ring-1 focus:ring-cyan-200"
          />
        </label>

        <label class="block text-xs font-medium tracking-wide text-[#A2A1A6]">
          Contraseña

          <input
            v-model="password"
            type="password"
            required
            autocomplete="new-password"
            placeholder="••••••••"
            class="mt-2 w-full rounded-lg border border-[color:var(--border)] bg-(--kots-background-color) px-4 py-3 text-sm text-white outline-none transition-colors duration-150 placeholder:text-[#6f6e73] focus:border-cyan-200 focus:ring-1 focus:ring-cyan-200"
          />
        </label>
      </div>
    </div>

    <div class="rounded-lg border border-[color:var(--border)] bg-(--kots-background-color) p-4">
      <div class="flex items-start gap-3">
        <input
          id="accept-legal"
          v-model="acceptedTerms"
          type="checkbox"
          required
          class="mt-0.5 h-4 w-4 shrink-0 cursor-pointer rounded border-[color:var(--border)] accent-cyan-200"
        />

        <label for="accept-legal" class="cursor-pointer text-xs leading-5 text-[#A2A1A6]">
          I have read and accept the

          <RouterLink
            to="/terms"
            target="_blank"
            class="font-semibold text-cyan-200 underline decoration-cyan-200/50 underline-offset-2 transition-colors hover:text-cyan-100"
            @click.stop
          >
            Terms of Service
          </RouterLink>

          and the

          <RouterLink
            to="/privacy"
            target="_blank"
            class="font-semibold text-cyan-200 underline decoration-cyan-200/50 underline-offset-2 transition-colors hover:text-cyan-100"
            @click.stop
          >
            Privacy Policy </RouterLink
          >.
        </label>
      </div>
    </div>

    <button
      type="submit"
      :disabled="loading || !acceptedTerms"
      class="w-full rounded-lg border-none bg-cyan-200 px-4 py-3 text-sm font-semibold uppercase tracking-wider text-[#171715] transition-colors duration-150 hover:bg-cyan-100 disabled:cursor-not-allowed disabled:opacity-40"
    >
      {{
        loading ? '// registrando...' : acceptedTerms ? '▶ Registrarse' : 'Accept terms to register'
      }}
    </button>

    <p v-if="mensaje" role="status" class="rounded-lg border border-[color:var(--border)] bg-(--kots-background-color) px-3 py-2 text-xs tracking-wide text-[#A2A1A6]">
      {{ mensaje }}
    </p>

    <button
      type="button"
      class="text-xs font-semibold text-cyan-200 underline decoration-cyan-200/50 underline-offset-4 transition-colors hover:text-cyan-100"
      @click="emit('back')"
    >
      Back
    </button>
  </form>
</template>
