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
  const button = event.currentTarget.querySelector('button[type="submit"]') || event.currentTarget

  loading.value = true
  mensaje.value = ''

  try {
    await auth.login(user.value, password.value)
    mensaje.value = '// acceso concedido'
    await router.push('/admin')
  } catch (error) {
    mensaje.value = '// datos incorrectos'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form class="space-y-5" @submit.prevent="login">
    <div>
      <span class="block text-[10px] tracking-[4px] uppercase text-(--accent) mb-3">Login</span>
      <div class="space-y-4">
        <label class="block text-[10px] tracking-[2px] uppercase text-(--muted)">
          Usuario
          <input
            v-model="user"
            type="text"
            autocomplete="off"
            placeholder="usuario_"
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
      {{ loading ? '// conectando...' : '▶ Entrar' }}
    </button>

    <p v-if="mensaje" class="text-sm tracking-[1px] text-(--muted)">
      {{ mensaje }}
    </p>
  </form>
</template>
