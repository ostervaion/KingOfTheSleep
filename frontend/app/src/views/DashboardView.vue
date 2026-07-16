<script setup>
import NextBattle from '@/components/dashboard/NextBattle.vue'
import Ranking from '@/components/dashboard/Ranking.vue'
import Protocols from '@/components/dashboard/Protocols.vue'
import ProtocolsImpact from '@/components/dashboard/ProtocolImpact.vue'
import SleepScore from '@/components/dashboard/SleepScore.vue'
import Profile from '@/components/dashboard/Profile.vue'
import TodayStats from '@/components/dashboard/TodayStats.vue'
import Battle from '@/components/dashboard/Battle.vue'
import ChatButton from '@/components/dashboard/ChatButton.vue'
import { useAppStore } from '@/stores/app'
import { useWebSocket } from '@/composables/useWebSocket'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '@/api/api'
import SleepDataForm from '@/components/SleepDataForm.vue'

const dashboard = ref(null)
const appStore = useAppStore()
const { connect, disconnect } = useWebSocket()

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
  connect()
})

onUnmounted(() => {
  clearInterval(intervalId)
  disconnect()
})

const mobileScroller = ref(null)
const activeMobilePage = ref(0)

const mobilePages = 5

function updateActiveMobilePage() {
  if (!mobileScroller.value) return

  const scrollLeft = mobileScroller.value.scrollLeft
  const pageWidth = mobileScroller.value.clientWidth

  activeMobilePage.value = Math.round(scrollLeft / pageWidth)
}
</script>

<template>
  <!-- PARA LA VERSIÓN MÓVIL O TABLET -->
  <div class="relative flex h-dvh flex-col overflow-hidden text-(--text) lg:hidden">
    <!-- Always visible top bar -->
    <div class="shrink-0 px-4 pt-4">
      <NextBattle :next-battle="dashboard?.nextBattle" class="w-full" />
    </div>

    <!-- Horizontal pages -->
    <div
      ref="mobileScroller"
      @scroll="updateActiveMobilePage"
      class="no-scrollbar flex min-h-0 flex-1 w-full snap-x snap-mandatory overflow-x-auto overflow-y-hidden scroll-smooth"
    >
      <!-- Page 1: Lobby + TodayStats -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <div class="grid h-full min-h-0 grid-rows-[1fr_auto] gap-4">
          <Battle class="h-full min-h-0" />
          <TodayStats class="min-h-0" />
        </div>
      </section>

      <!-- Page 2: Ranking -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <Ranking class="h-full min-h-0" />
      </section>

      <!-- Page 3: Protocols -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <Protocols class="h-full min-h-0" />
      </section>

      <!-- Page 4: Profile + SleepScore -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <div class="grid h-full min-h-0 grid-rows-2 gap-4">
          <Profile class="h-full min-h-0" />

          <SleepScore :sleep-score="dashboard?.sleepScore" class="h-full min-h-0" />
        </div>
      </section>

      <!-- Page 5: Protocol Impact -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <ProtocolsImpact class="h-full min-h-0" />
      </section>
    </div>

    <!-- Mobile dots -->
    <div
      class="pt-5 pointer-events-none absolute bottom-5 left-1/2 z-20 flex -translate-x-1/2 items-center gap-2 rounded-full px-3 py-0"
    >
      <span
        v-for="index in mobilePages"
        :key="index"
        class="h-2 rounded-full transition-all duration-200"
        :class="activeMobilePage === index - 1 ? 'w-6 bg-cyan-200' : 'w-2 bg-white/40'"
      />
    </div>
  </div>

  <!-- PARA ORDENADOR -->
  <div
    class="hidden h-[calc(100dvh-64px)] flex-col gap-3 overflow-hidden px-8 py-4 mt-5 text-(--text) lg:flex"
  >
    <NextBattle :next-battle="dashboard?.nextBattle" />

    <div
      class="mx-auto grid w-full flex-1 min-h-0 min-w-0 gap-4 items-stretch lg:grid-cols-[1fr_1.2fr_1.2fr]"
    >
      <section class="flex flex-col gap-4 min-h-0">
        <SleepDataForm v-if="!dashboard?.lobby" @saved="fetchDashboard" />
        <Battle v-else />
        <TodayStats />
      </section>

      <section class="flex flex-col gap-4 min-h-0">
        <Ranking :ranking-data="dashboard?.ranking || []" />
        <Protocols />
      </section>

      <section class="flex flex-col gap-4 min-h-0 min-w-0">
        <Profile />
        <SleepScore :sleep-score="dashboard?.sleepScore" />
        <ProtocolsImpact />
      </section>
    </div>
  </div>
  <ChatButton />
</template>
