<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
</script>

<template>
  <div class="flex items-center justify-between bg-(--surface) border border-(--border) p-4 rounded-xl">
    <div class="flex items-center gap-2">
      <span class="text-4xl text-yellow-400">#4</span>
      <div>
        current ranking <span class="text-xl text-green-400 ml-2">↑42</span> since last battle
      </div>
    </div>
    <div class="flex items-center gap-2">
      <span class="inline-flex items-center text-sm font-bold bg-yellow-400 rounded-md px-2 py-2  text-gray-800 leading-none">NEXT BATTLE IN</span>
      <span class="text-2xl">00:28:47</span>
    </div>
    <div class="flex items-center">
      DAY ENDS IN <span class="text-2xl ml-2 mr-2">15:12:34 </span> until daily reset
    </div>
  </div>
</template>
