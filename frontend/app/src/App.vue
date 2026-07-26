<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-[var(--kots-background-color)] font-mono flex flex-col">
    <main class="flex-1 mx-auto w-full">
      <RouterView />
    </main>
  </div>
</template>
