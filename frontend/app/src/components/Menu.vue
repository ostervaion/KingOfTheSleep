<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const mobileMenuOpen = ref(false)
const authStore = useAuthStore()
</script>

<template>
  <!-- Navbar horizontal -->
  <header class="font-inter bg-(--kots-blocks-color)">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="relative flex items-center justify-center h-16">
        <!-- Logo izquierda -->
        <div class="flex-shrink-0 justify-center">
          <img src="/KOTS_LOGO_2.png" alt="King of the Sleep" class="pt-4 h-16 w-auto" />
        </div>

        <nav class="hidden absolute right-0 md:flex items-center gap-8 justify-end">
          <button
            type="button"
            class="flex h-5 mt-4 cursor-pointer w-15 items-center justify-center gap-3 rounded-lg  hover:bg-yellow-400 hover:text-(--kots-background-color) px-4 text-xs font-semibold text-zinc-400 "
            @click="authStore.setAuthMode('login')"
          >
            Login
          </button>
        </nav>

        <button
          class="absolute right-0 md:hidden pt-4 text-yellow-400 text-2xl leading-none"
          @click="mobileMenuOpen = !mobileMenuOpen"
          aria-label="Toggle menu"
        >
          {{ mobileMenuOpen ? '✕' : '☰' }}
        </button>
      </div>
    </div>

    <div
      v-if="mobileMenuOpen"
      class="md:hidden bg-(--kots-background-color) border-t border-(--border) z-10"
    >
      <nav class="flex flex-col gap-2 px-4 py-4">
          <button
            type="button"
            class="flex h-5 cursor-pointer w-15 items-center justify-center gap-3 rounded-lg  hover:bg-yellow-400 hover:text-(--kots-background-color) px-4 text-xs font-semibold text-yellow-400 "
            @click="authStore.setAuthMode('login')"
          >
            Login
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
