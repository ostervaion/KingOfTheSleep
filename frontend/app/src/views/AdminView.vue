<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api/api'
import Chat from '@/components/Chat.vue'
import SleepDataForm from '@/components/SleepDataForm.vue'

// ===== USUARIOS =====
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

// ===== BATALLAS =====
const battleNextTime = ref(null)
const battleInfo = ref(null)
const battleQueue = ref([])
const newBattleMinutes = ref(5)
const newIntervalMinutes = ref(120)
const loading = ref(false)
const loadingInterval = ref(false)
const errorMsg = ref('')
const successMsg = ref('')
const autoRefreshInterval = ref(null)

// Formato de tiempo formateado
const timeDisplay = computed(() => {
  if (!battleNextTime.value) return 'Cargando...'
  const data = battleNextTime.value
  return `${data.hours}h ${data.minutes}m ${data.seconds}s`
})

const nextBattleFormatted = computed(() => {
  if (!battleNextTime.value) return '--'
  return new Date(battleNextTime.value.next_battle_time).toLocaleString('es-ES')
})

async function fetchBattleInfo() {
  try {
    const [timeResponse, infoResponse, queueResponse] = await Promise.all([
      api.get('/battles/time-until-next'),
      api.get('/battles/info'),
      api.get('/battles/queue')
    ])
    
    battleNextTime.value = timeResponse.data
    battleInfo.value = infoResponse.data
    battleQueue.value = queueResponse.data.battles || []
  } catch (error) {
    console.error('Error fetching battle info:', error)
  }
}

async function scheduleExtraBattle() {
  if (newBattleMinutes.value <= 0) {
    errorMsg.value = 'Los minutos deben ser mayor a 0'
    return
  }
  
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''
  
  try {
    const response = await api.post('/admin/battles/schedule-extra', {
      minutes_from_now: newBattleMinutes.value
    })
    
    successMsg.value = `✓ Batalla programada en ${newBattleMinutes.value} minutos`
    newBattleMinutes.value = 5
    
    // Recargar información
    await new Promise(resolve => setTimeout(resolve, 500))
    await fetchBattleInfo()
  } catch (error) {
    errorMsg.value = error.response?.data?.detail || 'Error al programar batalla'
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function changeBattleInterval() {
  if (newIntervalMinutes.value <= 0) {
    errorMsg.value = 'El intervalo debe ser mayor a 0'
    return
  }
  
  loadingInterval.value = true
  errorMsg.value = ''
  successMsg.value = ''
  
  try {
    const response = await api.post('/admin/battles/set-interval', {
      interval_minutes: newIntervalMinutes.value
    })
    
    successMsg.value = `✓ Intervalo actualizado a ${newIntervalMinutes.value} minutos`
    
    // Recargar información
    await new Promise(resolve => setTimeout(resolve, 500))
    await fetchBattleInfo()
  } catch (error) {
    errorMsg.value = error.response?.data?.detail || 'Error al cambiar intervalo'
    console.error(error)
  } finally {
    loadingInterval.value = false
  }
}

// Auto-refresh cada 5 segundos
function startAutoRefresh() {
  if (autoRefreshInterval.value) return
  autoRefreshInterval.value = setInterval(fetchBattleInfo, 5000)
}

function stopAutoRefresh() {
  if (autoRefreshInterval.value) {
    clearInterval(autoRefreshInterval.value)
    autoRefreshInterval.value = null
  }
}

onMounted(() => {
  loadUsers()
  fetchBattleInfo()
  startAutoRefresh()
})

// Cleanup on unmount
import { onUnmounted } from 'vue'
onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<template>
  <SleepDataForm />
  <div class="min-h-full px-4 py-8 sm:px-6 md:px-8 space-y-6">
    <Chat v-if="selectedUser" :to_user="selectedUser" @close="selectedUser = null" />
    
    <!-- ===== PANEL DE BATALLAS ===== -->
    <div
      class="relative w-full bg-[#111] border-2 border-[#1a1a1a] outline outline-1 outline-[#2a2a2a] px-6 py-8 sm:px-8 font-mono"
    >
      <span class="absolute top-[-2px] left-[-2px] w-3 h-3 border-t-2 border-l-2 border-[#ff6b6b]" />
      <span class="absolute top-[-2px] right-[-2px] w-3 h-3 border-t-2 border-r-2 border-[#ff6b6b]" />
      <span class="absolute bottom-[-2px] left-[-2px] w-3 h-3 border-b-2 border-l-2 border-[#ff6b6b]" />
      <span class="absolute bottom-[-2px] right-[-2px] w-3 h-3 border-b-2 border-r-2 border-[#ff6b6b]" />
      
      <h2 class="text-[#ff6b6b] text-xs sm:text-sm tracking-[4px] uppercase font-normal mb-6 before:content-['[_'] after:content-['_]']">
        ⚔️ Control de Batallas
      </h2>

      <!-- Mostrar mensajes de error/éxito -->
      <div v-if="errorMsg" class="mb-4 p-3 bg-red-950/40 border border-red-500/50 text-red-400 text-xs rounded">
        {{ errorMsg }}
      </div>
      <div v-if="successMsg" class="mb-4 p-3 bg-green-950/40 border border-green-500/50 text-green-400 text-xs rounded">
        {{ successMsg }}
      </div>

      <!-- Estado Actual -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <!-- Próxima Batalla -->
        <div class="bg-[#0a0a0a] border border-[#1a1a1a] p-4 rounded">
          <div class="text-[#ff6b6b] text-[10px] tracking-[2px] uppercase mb-2">⏰ Próxima Batalla</div>
          <div class="text-[#9d6fe8] text-lg font-mono mb-1">{{ timeDisplay }}</div>
          <div class="text-[#666] text-[10px]">{{ nextBattleFormatted }}</div>
        </div>

        <!-- Configuración Actual -->
        <div class="bg-[#0a0a0a] border border-[#1a1a1a] p-4 rounded">
          <div class="text-[#ff6b6b] text-[10px] tracking-[2px] uppercase mb-2">⚙️ Configuración</div>
          <div class="text-gray-400 text-[12px] space-y-1">
            <div>Intervalo: <span class="text-[#9d6fe8]">{{ battleInfo?.interval_minutes ?? '--' }} min</span></div>
            <div>Verificación: <span class="text-[#9d6fe8]">{{ battleInfo?.check_interval_seconds ?? '--' }} seg</span></div>
          </div>
        </div>
      </div>

      <!-- Acciones -->
      <div class="space-y-4">
        <!-- Programar Batalla Adicional -->
        <div class="border-t border-[#1a1a1a] pt-4">
          <h3 class="text-[#9d6fe8] text-[10px] tracking-[2px] uppercase mb-3">📅 Programar Batalla Adicional</h3>
          <div class="flex flex-col sm:flex-row gap-2">
            <input
              v-model.number="newBattleMinutes"
              type="number"
              min="1"
              max="10080"
              placeholder="Minutos desde ahora"
              class="flex-1 bg-[#0a0a0a] border border-[#1a1a1a] text-[#9d6fe8] px-3 py-2 text-sm rounded placeholder-[#333] focus:border-[#9d6fe8] outline-none"
            />
            <button
              @click="scheduleExtraBattle"
              :disabled="loading"
              class="bg-[#ff6b6b]/10 border border-[#ff6b6b]/50 text-[#ff6b6b] text-[11px] tracking-[2px] uppercase px-4 py-2 rounded hover:bg-[#ff6b6b]/20 hover:border-[#ff6b6b] active:scale-95 transition-all duration-150 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? '⏳ Programando...' : '▶ Programar' }}
            </button>
          </div>
        </div>

        <!-- Cambiar Intervalo -->
        <div class="border-t border-[#1a1a1a] pt-4">
          <h3 class="text-[#9d6fe8] text-[10px] tracking-[2px] uppercase mb-3">🔄 Cambiar Intervalo de Batallas</h3>
          <div class="flex flex-col sm:flex-row gap-2">
            <input
              v-model.number="newIntervalMinutes"
              type="number"
              min="1"
              max="10080"
              placeholder="Minutos entre batallas"
              class="flex-1 bg-[#0a0a0a] border border-[#1a1a1a] text-[#9d6fe8] px-3 py-2 text-sm rounded placeholder-[#333] focus:border-[#9d6fe8] outline-none"
            />
            <button
              @click="changeBattleInterval"
              :disabled="loadingInterval"
              class="bg-[#9d6fe8]/10 border border-[#9d6fe8]/50 text-[#9d6fe8] text-[11px] tracking-[2px] uppercase px-4 py-2 rounded hover:bg-[#9d6fe8]/20 hover:border-[#9d6fe8] active:scale-95 transition-all duration-150 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loadingInterval ? '⏳ Actualizando...' : '▶ Actualizar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Cola de Batallas (Debug) -->
      <div class="border-t border-[#1a1a1a] pt-4 mt-4">
        <h3 class="text-[#666] text-[10px] tracking-[2px] uppercase mb-3">📋 Cola de Batallas (Debug)</h3>
        <div class="overflow-x-auto">
          <table class="w-full border-collapse text-[10px]" v-if="battleQueue.length > 0">
            <thead>
              <tr class="border-b border-[#1a1a1a]">
                <th class="px-2 py-2 text-left text-[#444]">ID</th>
                <th class="px-2 py-2 text-left text-[#444]">Hora</th>
                <th class="px-2 py-2 text-left text-[#444]">Tipo</th>
                <th class="px-2 py-2 text-left text-[#444]">Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="battle in battleQueue"
                :key="battle.id"
                class="border-b border-[#1a1a1a] hover:bg-[#9d6fe8]/[0.04]"
              >
                <td class="px-2 py-2 text-[#666]">#{{ battle.id }}</td>
                <td class="px-2 py-2 text-[#9d6fe8] font-mono text-[9px]">
                  {{ new Date(battle.scheduled_time).toLocaleTimeString('es-ES') }}
                </td>
                <td class="px-2 py-2">
                  <span v-if="battle.is_recurring" class="text-[#ffb700]">🔄 Recurrente</span>
                  <span v-else class="text-[#ff6b6b]">⏱️ Única</span>
                </td>
                <td class="px-2 py-2">
                  <span v-if="battle.executed" class="text-green-500">✓ Ejecutada</span>
                  <span v-else class="text-yellow-500">⏳ Pendiente</span>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="text-[#333] text-[10px] text-center py-4">
            // sin batallas programadas
          </div>
        </div>
      </div>

      <div class="mt-4 pt-4 border-t border-[#1a1a1a] flex items-center justify-between">
        <span class="text-[10px] text-[#2a2a2a] tracking-[2px] uppercase">
          batallas en cola: {{ battleQueue.length }}
        </span>
        <button
          @click="fetchBattleInfo"
          class="text-[10px] tracking-[2px] uppercase text-[#444] hover:text-[#ff6b6b] transition-colors duration-150 cursor-pointer"
        >
          ↺ Recargar
        </button>
      </div>
    </div>

    <!-- ===== PANEL DE USUARIOS ===== -->
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
