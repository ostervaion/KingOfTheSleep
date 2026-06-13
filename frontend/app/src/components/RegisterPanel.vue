<script setup>
import { ref } from 'vue'
import api from '@/api/api'

const props = defineProps({
  email: {
    type: String,
    default: '',
  },
})
const emit = defineEmits(['back'])

const username = ref('')
const email = ref(props.email)
const password = ref('')
const mensaje = ref('')
const loading = ref(false)

async function register(event) {
  event.preventDefault()
  if (loading.value) return

  loading.value = true
  mensaje.value = ''

  try {
    await api.post('/register', {
      username: username.value,
      email: email.value,
      password: password.value,
    })
    mensaje.value = '// usuario registrado'
  } catch (error) {
    mensaje.value = `// ${error.response?.data?.detail || 'error al registrar'}`
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form class="space-y-5" @submit.prevent="register">
    <div>
      <span class="block text-[10px] tracking-[4px] uppercase text-(--accent) mb-3">Register</span>
      <div class="space-y-4">
        <label class="block text-[10px] tracking-[2px] uppercase text-(--muted)">
          Usuario
          <input
            v-model="username"
            type="text"
            autocomplete="off"
            placeholder="usuario_"
            class="mt-2 w-full rounded-2xl border border-(--border) bg-(--surface-soft) px-4 py-3 text-sm text-(--text) outline-none placeholder:text-(--muted) focus:border-(--accent) transition-colors duration-150"
          />
        </label>

        <label class="block text-[10px] tracking-[2px] uppercase text-(--muted)">
          Email
          <input
            v-model="email"
            type="email"
            autocomplete="off"
            placeholder="correo@dominio.com"
            class="mt-2 w-full rounded-2xl border border-(--border) bg-(--surface-soft) px-4 py-3 text-sm text-(--text) outline-none placeholder:text-(--muted) focus:border-(--accent) transition-colors duration-150"
          />
        </label>

        <label class="block text-[10px] tracking-[2px] uppercase text-(--muted)">
          Contraseña
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="mt-2 w-full rounded-2xl border border-(--border) bg-(--surface-soft) px-4 py-3 text-sm text-(--text) outline-none placeholder:text-(--muted) focus:border-(--accent) transition-colors duration-150"
          />
        </label>
      </div>
    </div>

    <button
      type="submit"
      :disabled="loading"
      class="w-full rounded-2xl border border-(--accent) bg-(--surface-soft) px-4 py-3 text-sm font-semibold uppercase tracking-[2px] text-(--accent) hover:bg-(--surface) transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {{ loading ? '// registrando...' : '▶ Registrarse' }}
    </button>

    <p v-if="mensaje" class="text-sm tracking-[1px] text-(--muted)">
      {{ mensaje }}
    </p>
    <button
      type="button"
      @click="emit('back')"
      class="text-(--accent) hover:text-(--button-hover) underline"
    >
      Back
    </button>
  </form>
</template>
