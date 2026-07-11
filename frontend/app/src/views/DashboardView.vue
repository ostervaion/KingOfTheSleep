<script setup>
import NextBattle from '@/components/dashboard/NextBattle.vue'
import Ranking from '@/components/dashboard/Ranking.vue'
import Protocols from '@/components/dashboard/Protocols.vue'
import ProtocolsImpact from '@/components/dashboard/ProtocolImpact.vue'
import SleepScore from '@/components/dashboard/SleepScore.vue'
import Profile from '@/components/dashboard/Profile.vue'
import TodayStats from '@/components/dashboard/TodayStats.vue'
import Lobby from '@/components/dashboard/Lobby.vue'
import { useAppStore } from '@/stores/app'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '@/api/api'
import SleepDataForm from '@/components/SleepDataForm.vue'

const dashboard = ref(null)

const appStore = useAppStore()

async function fetchDashboard() {
  try {
    const response = await api.get('/dashboard')
    dashboard.value = {
      ...response.data,
      ranking: Array.isArray(response.data?.ranking) ? response.data.ranking : [],
    }
  } catch (error) {
    console.error('Error cargando dashboard:', error)
  }
}

let intervalId = null

onMounted(() => {
  fetchDashboard()
  appStore.onDashboard = true
  intervalId = setInterval(fetchDashboard, 30000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})
</script>

<template>
  <div
    class="h-[calc(100dvh-64px)] text-(--text) mt-5 px-4 py-4 sm:px-6 lg:px-8 overflow-hidden flex flex-col gap-3"
  >
    <NextBattle :next-battle="dashboard?.nextBattle" />

    <div
      class="mx-auto grid w-full flex-1 min-h-0 gap-4 lg:grid-cols-[1fr_1.2fr_1.2fr] items-stretch"
    >
      <section class="flex flex-col gap-4 min-h-0">
      <SleepDataForm v-if="!dashboard?.lobby" @saved="fetchDashboard" />
        <Lobby v-else/>
        <TodayStats />
      </section>

      <section class="flex flex-col gap-4 min-h-0">
        <Ranking :ranking-data="dashboard?.ranking || []" />
        <Protocols />
      </section>

      <section class="flex flex-col gap-4 min-h-0">
        <Profile />
        <SleepScore :sleep-score="dashboard?.sleepScore" />
        <ProtocolsImpact :protocol-impacts="dashboard?.protocolImpacts || []" />
      </section>
    </div>
  </div>
</template>
