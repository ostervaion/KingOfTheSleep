<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import api from '@/api/api'
import Chat from '@/components/Chat.vue'

const checkingAccess = ref(true)
const isAdmin = ref(false)
const users = ref([])
const selectedUser = ref(null)
const editingUser = ref(null)
const editError = ref('')
const editLoading = ref(false)
const battleNextTime = ref(null)
const battleInfo = ref(null)
const battleQueue = ref([])
const newBattleMinutes = ref(5)
const newIntervalMinutes = ref(120)
const battleLoading = ref(false)
const intervalLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const refreshTimer = ref(null)

const editForm = ref({
  username: '',
  email: '',
  password: '',
  role: 'user',
  active: true,
})

const timeDisplay = computed(() => {
  if (!battleNextTime.value) return 'Loading...'

  const { hours, minutes, seconds } = battleNextTime.value
  return `${hours}h ${minutes}m ${seconds}s`
})

const nextBattleFormatted = computed(() => {
  if (!battleNextTime.value?.next_battle_time) return '--'

  return new Date(battleNextTime.value.next_battle_time).toLocaleString('en-GB')
})

async function checkAdminAccess() {
  try {
    const { data } = await api.get('/me')
    isAdmin.value = data.role === 'admin'
  } catch (error) {
    console.error(error)
    isAdmin.value = false
  } finally {
    checkingAccess.value = false
  }
}

async function loadUsers() {
  try {
    const { data } = await api.get('/all_users')
    users.value = Array.isArray(data) ? data : []
  } catch (error) {
    console.error(error)
  }
}

async function deleteUser(username) {
  try {
    await api.delete(`/users/${username}`)
    await loadUsers()
  } catch (error) {
    console.error(error)
  }
}

function openEditUser(user) {
  editingUser.value = user
  editForm.value = {
    username: user.username || '',
    email: user.email || '',
    password: '',
    role: user.role || 'user',
    active: user.active ?? true,
  }
  editError.value = ''
}

function closeEditUser() {
  editingUser.value = null
  editError.value = ''
}

async function saveEditUser() {
  if (!editingUser.value) return

  editLoading.value = true
  editError.value = ''

  const payload = {
    username: editForm.value.username,
    email: editForm.value.email,
    role: editForm.value.role,
    active: editForm.value.active,
  }

  if (editForm.value.password) {
    payload.password = editForm.value.password
  }

  try {
    await api.patch(`/admin/users/${editingUser.value.username}`, payload)
    await loadUsers()
    closeEditUser()
  } catch (error) {
    editError.value = error.response?.data?.detail || 'Could not save the changes.'
    console.error(error)
  } finally {
    editLoading.value = false
  }
}

async function fetchBattleInfo() {
  try {
    const [timeResponse, infoResponse, queueResponse] = await Promise.all([
      api.get('/battles/time-until-next'),
      api.get('/battles/info'),
      api.get('/battles/queue'),
    ])

    battleNextTime.value = timeResponse.data
    battleInfo.value = infoResponse.data
    battleQueue.value = queueResponse.data.battles || []
  } catch (error) {
    console.error('Could not load battle information:', error)
  }
}

async function scheduleExtraBattle() {
  if (newBattleMinutes.value <= 0) {
    errorMessage.value = 'Minutes must be greater than 0.'
    return
  }

  battleLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await api.post('/admin/battles/schedule-extra', {
      minutes_from_now: newBattleMinutes.value,
    })

    successMessage.value = `Battle scheduled in ${newBattleMinutes.value} minutes.`
    newBattleMinutes.value = 5
    await fetchBattleInfo()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Could not schedule the battle.'
    console.error(error)
  } finally {
    battleLoading.value = false
  }
}

async function changeBattleInterval() {
  if (newIntervalMinutes.value <= 0) {
    errorMessage.value = 'The interval must be greater than 0.'
    return
  }

  intervalLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await api.post('/admin/battles/set-interval', {
      interval_minutes: newIntervalMinutes.value,
    })

    successMessage.value = `Battle interval updated to ${newIntervalMinutes.value} minutes.`
    await fetchBattleInfo()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Could not update the interval.'
    console.error(error)
  } finally {
    intervalLoading.value = false
  }
}

function startAutoRefresh() {
  if (refreshTimer.value) return
  refreshTimer.value = setInterval(fetchBattleInfo, 5000)
}

function stopAutoRefresh() {
  if (!refreshTimer.value) return
  clearInterval(refreshTimer.value)
  refreshTimer.value = null
}

onMounted(async () => {
  await checkAdminAccess()
  if (!isAdmin.value) return

  await Promise.all([loadUsers(), fetchBattleInfo()])
  startAutoRefresh()
})

onUnmounted(stopAutoRefresh)
</script>

<template>
  <div class="min-h-full bg-neutral-950 text-white">
    <div v-if="checkingAccess" class="flex min-h-[60vh] items-center justify-center px-4">
      <p class="text-sm text-neutral-400">Checking access...</p>
    </div>

    <div v-else-if="!isAdmin" class="flex min-h-[60vh] items-center justify-center px-4">
      <div
        class="w-full max-w-md rounded-lg border border-neutral-800 bg-neutral-900 p-8 text-center"
      >
        <h1 class="mb-2 text-lg font-semibold">Access denied</h1>
        <p class="text-sm text-neutral-400">This page is only available to administrators.</p>
      </div>
    </div>

    <main v-else class="mx-auto max-w-6xl space-y-6 px-4 py-8 sm:px-6">
      <Chat v-if="selectedUser" :to_user="selectedUser" @close="selectedUser = null" />

      <div
        v-if="editingUser"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4"
        @click.self="closeEditUser"
      >
        <div
          class="w-full max-w-md rounded-lg border border-neutral-800 bg-neutral-900 p-6 shadow-xl"
        >
          <h2 class="mb-5 text-lg font-semibold">Edit user</h2>

          <div
            v-if="editError"
            class="mb-4 rounded-md border border-red-900 bg-red-950/40 px-3 py-2 text-sm text-red-300"
          >
            {{ editError }}
          </div>

          <div class="space-y-4">
            <div>
              <label class="mb-1 block text-sm text-neutral-300">Username</label>
              <input
                v-model="editForm.username"
                type="text"
                class="w-full rounded-md border border-neutral-700 bg-neutral-950 px-3 py-2 text-sm text-white outline-none focus:border-neutral-400"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm text-neutral-300">Email</label>
              <input
                v-model="editForm.email"
                type="email"
                class="w-full rounded-md border border-neutral-700 bg-neutral-950 px-3 py-2 text-sm text-white outline-none focus:border-neutral-400"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm text-neutral-300">New password</label>
              <input
                v-model="editForm.password"
                type="password"
                placeholder="Leave blank to keep the current password"
                class="w-full rounded-md border border-neutral-700 bg-neutral-950 px-3 py-2 text-sm text-white outline-none placeholder:text-neutral-600 focus:border-neutral-400"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm text-neutral-300">Role</label>
              <select
                v-model="editForm.role"
                class="w-full rounded-md border border-neutral-700 bg-neutral-950 px-3 py-2 text-sm text-white outline-none focus:border-neutral-400"
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>

            <label class="flex items-center gap-2 text-sm text-neutral-300">
              <input v-model="editForm.active" type="checkbox" class="h-4 w-4" />
              Active account
            </label>
          </div>

          <div class="mt-6 flex gap-3">
            <button
              type="button"
              :disabled="editLoading"
              class="flex-1 rounded-md bg-white px-4 py-2 text-sm font-medium text-black hover:bg-neutral-200 disabled:cursor-not-allowed disabled:opacity-50"
              @click="saveEditUser"
            >
              {{ editLoading ? 'Saving...' : 'Save' }}
            </button>
            <button
              type="button"
              class="flex-1 rounded-md border border-neutral-700 px-4 py-2 text-sm text-white hover:bg-neutral-800"
              @click="closeEditUser"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>

      <section class="rounded-lg border border-neutral-800 bg-neutral-900 p-5 sm:p-6">
        <div class="mb-6 flex items-center justify-between gap-4">
          <div>
            <h1 class="text-xl font-semibold">Battle controls</h1>
            <p class="mt-1 text-sm text-neutral-400">Manage battle timing and review the queue.</p>
          </div>
          <button
            type="button"
            class="rounded-md border border-neutral-700 px-3 py-2 text-sm text-neutral-300 hover:bg-neutral-800 hover:text-white"
            @click="fetchBattleInfo"
          >
            Refresh
          </button>
        </div>

        <div
          v-if="errorMessage"
          class="mb-4 rounded-md border border-red-900 bg-red-950/40 px-3 py-2 text-sm text-red-300"
        >
          {{ errorMessage }}
        </div>

        <div
          v-if="successMessage"
          class="mb-4 rounded-md border border-green-900 bg-green-950/40 px-3 py-2 text-sm text-green-300"
        >
          {{ successMessage }}
        </div>

        <div class="mb-6 grid grid-cols-1 gap-4 md:grid-cols-2">
          <div class="rounded-md border border-neutral-800 bg-neutral-950 p-4">
            <p class="text-sm text-neutral-400">Next battle</p>
            <p class="mt-2 text-2xl font-semibold">{{ timeDisplay }}</p>
            <p class="mt-1 text-sm text-neutral-500">{{ nextBattleFormatted }}</p>
          </div>

          <div class="rounded-md border border-neutral-800 bg-neutral-950 p-4">
            <p class="text-sm text-neutral-400">Current settings</p>
            <div class="mt-2 space-y-1 text-sm">
              <p>
                Interval:
                <span class="text-neutral-300"
                  >{{ battleInfo?.interval_minutes ?? '--' }} minutes</span
                >
              </p>
              <p>
                Check frequency:
                <span class="text-neutral-300">
                  {{ battleInfo?.check_interval_seconds ?? '--' }} seconds
                </span>
              </p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <div class="rounded-md border border-neutral-800 p-4">
            <h2 class="mb-3 font-medium">Schedule an extra battle</h2>
            <div class="flex flex-col gap-2 sm:flex-row">
              <input
                v-model.number="newBattleMinutes"
                type="number"
                min="1"
                max="10080"
                placeholder="Minutes from now"
                class="min-w-0 flex-1 rounded-md border border-neutral-700 bg-neutral-950 px-3 py-2 text-sm text-white outline-none placeholder:text-neutral-600 focus:border-neutral-400"
              />
              <button
                type="button"
                :disabled="battleLoading"
                class="rounded-md bg-white px-4 py-2 text-sm font-medium text-black hover:bg-neutral-200 disabled:cursor-not-allowed disabled:opacity-50"
                @click="scheduleExtraBattle"
              >
                {{ battleLoading ? 'Scheduling...' : 'Schedule' }}
              </button>
            </div>
          </div>

          <div class="rounded-md border border-neutral-800 p-4">
            <h2 class="mb-3 font-medium">Change battle interval</h2>
            <div class="flex flex-col gap-2 sm:flex-row">
              <input
                v-model.number="newIntervalMinutes"
                type="number"
                min="1"
                max="10080"
                placeholder="Minutes between battles"
                class="min-w-0 flex-1 rounded-md border border-neutral-700 bg-neutral-950 px-3 py-2 text-sm text-white outline-none placeholder:text-neutral-600 focus:border-neutral-400"
              />
              <button
                type="button"
                :disabled="intervalLoading"
                class="rounded-md bg-white px-4 py-2 text-sm font-medium text-black hover:bg-neutral-200 disabled:cursor-not-allowed disabled:opacity-50"
                @click="changeBattleInterval"
              >
                {{ intervalLoading ? 'Updating...' : 'Update' }}
              </button>
            </div>
          </div>
        </div>

        <div class="mt-6 border-t border-neutral-800 pt-6">
          <div class="mb-3 flex items-center justify-between">
            <h2 class="font-medium">Battle queue</h2>
            <span class="text-sm text-neutral-500">{{ battleQueue.length }} queued</span>
          </div>

          <div class="overflow-x-auto">
            <table v-if="battleQueue.length" class="w-full min-w-[560px] text-left text-sm">
              <thead class="border-b border-neutral-800 text-neutral-500">
                <tr>
                  <th class="px-3 py-2 font-medium">ID</th>
                  <th class="px-3 py-2 font-medium">Time</th>
                  <th class="px-3 py-2 font-medium">Type</th>
                  <th class="px-3 py-2 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="battle in battleQueue"
                  :key="battle.id"
                  class="border-b border-neutral-800 last:border-0 hover:bg-neutral-800/50"
                >
                  <td class="px-3 py-3 text-neutral-400">#{{ battle.id }}</td>
                  <td class="px-3 py-3">
                    {{ new Date(battle.scheduled_time).toLocaleTimeString('en-GB') }}
                  </td>
                  <td class="px-3 py-3 text-neutral-300">
                    {{ battle.is_recurring ? 'Recurring' : 'One-time' }}
                  </td>
                  <td class="px-3 py-3">
                    <span :class="battle.executed ? 'text-green-400' : 'text-yellow-300'">
                      {{ battle.executed ? 'Completed' : 'Pending' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>

            <p v-else class="py-8 text-center text-sm text-neutral-500">No battles scheduled.</p>
          </div>
        </div>
      </section>

      <section class="rounded-lg border border-neutral-800 bg-neutral-900 p-5 sm:p-6">
        <div class="mb-5 flex items-center justify-between gap-4">
          <div>
            <h1 class="text-xl font-semibold">Users</h1>
            <p class="mt-1 text-sm text-neutral-400">Manage accounts and start admin chats.</p>
          </div>
          <button
            type="button"
            class="rounded-md border border-neutral-700 px-3 py-2 text-sm text-neutral-300 hover:bg-neutral-800 hover:text-white"
            @click="loadUsers"
          >
            Refresh
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full min-w-[560px] text-left text-sm">
            <thead class="border-b border-neutral-800 text-neutral-500">
              <tr>
                <th class="w-16 px-3 py-2 font-medium">#</th>
                <th class="px-3 py-2 font-medium">Username</th>
                <th class="px-3 py-2 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(user, index) in users"
                :key="user.id || user.username"
                class="border-b border-neutral-800 last:border-0 hover:bg-neutral-800/50"
              >
                <td class="px-3 py-3 text-neutral-500">{{ index + 1 }}</td>
                <td class="px-3 py-3 text-neutral-200">{{ user.username }}</td>
                <td class="px-3 py-3">
                  <div class="flex flex-wrap gap-2">
                    <button
                      type="button"
                      class="rounded-md border border-neutral-700 px-3 py-1.5 text-sm text-neutral-200 hover:bg-neutral-800"
                      @click="selectedUser = user.username"
                    >
                      Chat
                    </button>
                    <button
                      type="button"
                      class="rounded-md border border-neutral-700 px-3 py-1.5 text-sm text-neutral-200 hover:bg-neutral-800"
                      @click="openEditUser(user)"
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      class="rounded-md border border-red-900 px-3 py-1.5 text-sm text-red-300 hover:bg-red-950/40"
                      @click="deleteUser(user.username)"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="users.length === 0">
                <td colspan="3" class="px-3 py-8 text-center text-neutral-500">No users found.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <p class="mt-4 border-t border-neutral-800 pt-4 text-sm text-neutral-500">
          Total users: {{ users.length }}
        </p>
      </section>
    </main>
  </div>
</template>
