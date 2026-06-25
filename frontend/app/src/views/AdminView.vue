<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import Chat from '@/components/Chat.vue'

const usuarios = ref([])
const selectedUser = ref(null)

async function loadUsers() {
  try {
    const response = await api.get('/all_users')
    usuarios.value = response.data
  } catch (error) {
    console.error(error)
  }
}

async function deteleUser(username) {
  try {
    await api.delete(`/users/${username}`)
    await loadUsers()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<template>
  <div class="min-h-full px-4 py-8 sm:px-6 md:px-8">
    <Chat v-if="selectedUser" :to_user="selectedUser" @close="selectedUser = null" />
    <div
      class="relative w-full bg-[#111] border-2 border-[#1a1a1a] outline outline-1 outline-[#2a2a2a] px-6 py-8 sm:px-8 font-mono"
    >
      <span
        class="absolute top-[-2px] left-[-2px] w-3 h-3 border-t-2 border-l-2 border-[#9d6fe8]"
      />
      <span
        class="absolute top-[-2px] right-[-2px] w-3 h-3 border-t-2 border-r-2 border-[#9d6fe8]"
      />
      <span
        class="absolute bottom-[-2px] left-[-2px] w-3 h-3 border-b-2 border-l-2 border-[#9d6fe8]"
      />
      <span
        class="absolute bottom-[-2px] right-[-2px] w-3 h-3 border-b-2 border-r-2 border-[#9d6fe8]"
      />
      <h2
        class="text-[#9d6fe8] text-xs sm:text-sm tracking-[4px] uppercase font-normal mb-6 before:content-['[_'] after:content-['_]']"
      >
        Usuarios
      </h2>
      <div class="overflow-x-auto">
        <table class="w-full border-collapse text-xs sm:text-sm">
          <thead>
            <tr class="border-b-2 border-[#9d6fe8]/30 text-left">
              <th
                class="px-4 py-3 text-[10px] tracking-[2px] uppercase text-[#444] font-normal w-12"
              >
                #
              </th>
              <th class="px-4 py-3 text-[10px] tracking-[2px] uppercase text-[#444] font-normal">
                Username
              </th>
              <th
                class="px-4 py-3 text-[10px] tracking-[2px] uppercase text-[#444] font-normal w-36"
              >
                Acción
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(usuario, index) in usuarios"
              :key="usuario.id || usuario.username"
              class="border-b border-[#1a1a1a] hover:bg-[#9d6fe8]/[0.04] transition-colors duration-100 group"
            >
              <td class="px-4 py-3 text-[#333]">{{ index + 1 }}</td>
              <td
                class="px-4 py-3 text-gray-400 group-hover:text-gray-200 transition-colors duration-100"
              >
                <span class="text-[#9d6fe8]/40 mr-2 text-[10px]">▶</span>
                {{ usuario.username }}
              </td>
              <td class="px-4 py-3 flex gap-2">
                <button
                  class="bg-[#0a0a0a] border border-[#9d6fe8]/50 text-[#9d6fe8] text-[10px] tracking-[2px] uppercase px-3 py-1.5 hover:bg-[#9d6fe8]/[0.1] hover:border-[#9d6fe8] active:scale-95 transition-all duration-150 cursor-pointer"
                  @click="selectedUser = usuario.username"
                >
                  ▶ Chat
                </button>
                <button
                  class="bg-[#0a0a0a] border border-red-900/50 text-red-500/70 text-[10px] tracking-[2px] uppercase px-3 py-1.5 hover:bg-red-950/40 hover:border-red-500/70 hover:text-red-400 active:scale-95 transition-all duration-150 cursor-pointer"
                  @click="deteleUser(usuario.username)"
                >
                  ✕ Del
                </button>
              </td>
            </tr>
            <tr v-if="usuarios.length === 0">
              <td
                colspan="3"
                class="px-4 py-8 text-center text-[#333] tracking-[2px] uppercase text-[11px]"
              >
                // sin usuarios
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mt-6 pt-4 border-t border-[#1a1a1a] flex items-center justify-between">
        <span class="text-[10px] text-[#2a2a2a] tracking-[2px] uppercase">
          total: {{ usuarios.length }}
        </span>
        <button
          class="text-[10px] tracking-[2px] uppercase text-[#444] hover:text-[#9d6fe8] transition-colors duration-150 cursor-pointer"
          @click="loadUsers"
        >
          ↺ Recargar
        </button>
      </div>
    </div>
  </div>
</template>
