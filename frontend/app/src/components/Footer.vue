<script setup>
import { RouterLink } from 'vue-router'

const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="font-inter bg-[#171715] text-white">
    <div
      class="mx-auto flex w-full max-w-[1240px] flex-col items-center justify-between gap-5 px-6 py-8 sm:flex-row sm:px-8 lg:px-12 xl:px-16"
    >
      <div class="text-center sm:text-left">
        <RouterLink
          to="/"
          class="text-lg font-semibold tracking-[-0.03em] text-white transition hover:text-cyan-200"
        >
          KingOfSleep
        </RouterLink>

        <p class="mt-1 text-xs text-white/40">© {{ currentYear }} KingOfTheSleep</p>
      </div>

      <nav aria-label="Legal links" class="flex items-center gap-5 text-sm">
        <RouterLink
          to="/privacy"
          class="text-white/55 transition hover:text-cyan-200 focus-visible:text-cyan-200"
        >
          Privacy Policy
        </RouterLink>

        <RouterLink
          to="/terms"
          class="text-white/55 transition hover:text-cyan-200 focus-visible:text-cyan-200"
        >
          Terms of Service
        </RouterLink>
      </nav>
    </div>
  </footer>
</template>
