<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const user = ref('')
const password = ref('')
const mensaje = ref('')
const loading = ref(false)

async function login(event) {
  event.preventDefault()
  if (loading.value) return

  loading.value = true
  mensaje.value = ''

  try {
    await auth.login(user.value, password.value)
    mensaje.value = '// acceso concedido'
    await router.push('/dashboard')
  } catch (error) {
    mensaje.value = '// datos incorrectos'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form class="font-inter space-y-5" @submit.prevent="login">
    <div>
      <span class="mb-4 block text-xs font-semibold uppercase tracking-[0.18em] text-yellow-400"
        >Login</span
      >
      <div class="space-y-4">
        <label class="block text-xs font-medium tracking-wide text-[#A2A1A6]">
          Usuario
          <input
            v-model="user"
            type="text"
            autocomplete="off"
            placeholder="usuario_"
            class="mt-2 w-full rounded-lg border border-[color:var(--border)] bg-(--kots-background-color) px-4 py-3 text-sm text-white outline-none transition-colors duration-150 placeholder:text-[#6f6e73] focus:border-cyan-200 focus:ring-1 focus:ring-cyan-200"
          />
        </label>

        <label class="block text-xs font-medium tracking-wide text-[#A2A1A6]">
          Contraseña
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="mt-2 w-full rounded-lg border border-[color:var(--border)] bg-(--kots-background-color) px-4 py-3 text-sm text-white outline-none transition-colors duration-150 placeholder:text-[#6f6e73] focus:border-cyan-200 focus:ring-1 focus:ring-cyan-200"
          />
        </label>
      </div>
    </div>

    <button
      type="submit"
      :disabled="loading"
      class="w-full rounded-lg border-none bg-cyan-200 px-4 py-3 text-sm font-semibold uppercase tracking-wider text-[#171715] transition-colors duration-150 hover:bg-cyan-100 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {{ loading ? '// conectando...' : '▶ Entrar' }}
    </button>

    <p
      v-if="mensaje"
      class="rounded-lg border border-[color:var(--border)] bg-(--kots-background-color) px-3 py-2 text-xs tracking-wide text-[#A2A1A6]"
    >
      {{ mensaje }}
    </p>
  </form>
</template>
