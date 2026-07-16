<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAppStore } from '@/stores/app'

const mobileMenuOpen = ref(false)
const appStore = useAppStore()
</script>

<template>
  <div class="min-h-screen bg-[var(--kots-background-color)] font-mono flex flex-col">
    <!-- Navbar horizontal -->
    <header
      v-if="!appStore.onDashboard"
      class="bg-[var(--web-bg)] border-b border-[color:var(--border)]"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo izquierda -->
          <div class="flex-shrink-0">
            <img src="/KOTS_logo.png" alt="King of the Sleep" class="h-10 w-auto" />
          </div>

          <!-- Menú desktop -->
          <nav class="hidden md:flex items-center gap-8">
            <RouterLink
              to="/login"
              class="text-xs tracking-[2px] uppercase text-[color:var(--muted)] hover:text-[color:var(--accent)] transition-colors duration-150 pb-0.5 border-b-2 border-transparent hover:border-[color:var(--accent)]"
              active-class="!text-[color:var(--accent)] !border-[color:var(--accent)]"
            >
              Login
            </RouterLink>

            <RouterLink
              to="/register"
              class="text-xs tracking-[2px] uppercase text-[color:var(--muted)] hover:text-[color:var(--accent)] transition-colors duration-150 pb-0.5 border-b-2 border-transparent hover:border-[color:var(--accent)]"
              active-class="!text-[color:var(--accent)] !border-[color:var(--accent)]"
            >
              Register
            </RouterLink>
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
        <nav class="flex flex-col gap-1 px-4 py-3">
          <RouterLink
            to="/login"
            class="px-3 py-2 text-xs tracking-[2px] uppercase text-[color:var(--muted)] hover:text-[color:var(--accent)] hover:bg-[color:var(--accent-soft)]/10 transition-all duration-150 rounded border-l-2 border-transparent hover:border-[color:var(--accent)]"
            active-class="!text-[color:var(--accent)] !border-[color:var(--accent)] bg-[color:var(--accent)]/10"
            @click="mobileMenuOpen = false"
          >
            Login
          </RouterLink>

          <RouterLink
            to="/register"
            class="px-3 py-2 text-xs tracking-[2px] uppercase text-[color:var(--muted)] hover:text-[color:var(--accent)] hover:bg-[color:var(--accent-soft)]/10 transition-all duration-150 rounded border-l-2 border-transparent hover:border-[color:var(--accent)]"
            active-class="!text-[color:var(--accent)] !border-[color:var(--accent)] bg-[color:var(--accent)]/10"
            @click="mobileMenuOpen = false"
          >
            Register
          </RouterLink>
        </nav>
      </div>
    </header>

    <main class="flex-1 mx-auto w-full">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.router-link-exact-active {
  color: var(--accent);
}
</style>
