<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const mobileMenuOpen = ref(false)
const authStore = useAuthStore()
</script>

<template>
  <!-- Navbar horizontal -->
  <header class="bg-[var(--web-bg)] border-b border-[color:var(--border)]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo izquierda -->
        <div class="flex-shrink-0">
          <img src="/KOTS_logo.png" alt="King of the Sleep" class="h-10 w-auto" />
        </div>

        <nav class="hidden md:flex items-center gap-8">
          <button
            type="button"
            class="flex h-8 cursor-pointer w-full items-center justify-center gap-3 rounded-lg bg-[#FACC15] px-5 text-base font-semibold text-[#171715] transition hover:brightness-105"
            @click="authStore.setAuthMode('login')"
          >
            Login
          </button>
        </nav>

        <button
          class="md:hidden text-[color:var(--accent)] text-2xl leading-none hover:text-[color:var(--accent)]/80 transition-colors"
          @click="mobileMenuOpen = !mobileMenuOpen"
          aria-label="Toggle menu"
        >
          {{ mobileMenuOpen ? '✕' : '☰' }}
        </button>
      </div>
    </div>

    <div
      v-if="mobileMenuOpen"
      class="md:hidden bg-[color:var(--surface-soft)] border-t border-[color:var(--border)]"
    >
      <nav class="hidden md:flex items-center gap-8">
        <button
          type="button"
          class="text-xs tracking-[2px] uppercase text-[color:var(--muted)] hover:text-[color:var(--accent)] transition-colors duration-150 pb-0.5 border-b-2 border-transparent hover:border-[color:var(--accent)]"
          :class="{
            '!text-[color:var(--accent)] !border-[color:var(--accent)]':
              authStore.authMode === 'login',
          }"
          @click="authStore.setAuthMode('login')"
        >
          Login
        </button>

        <button
          type="button"
          class="text-xs tracking-[2px] uppercase text-[color:var(--muted)] hover:text-[color:var(--accent)] transition-colors duration-150 pb-0.5 border-b-2 border-transparent hover:border-[color:var(--accent)]"
          :class="{
            '!text-[color:var(--accent)] !border-[color:var(--accent)]':
              authStore.authMode === 'register',
          }"
          @click="authStore.setAuthMode('register')"
        >
          Register
        </button>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.router-link-exact-active {
  color: var(--accent);
}
</style>
