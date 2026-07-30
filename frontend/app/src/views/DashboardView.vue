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
import SleepDataForm from '@/components/SleepDataForm.vue'
import { useWebSocket } from '@/composables/useWebSocket'
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/api'

const router = useRouter()
const auth = useAuthStore()

const dashboard = ref(null)
const { connect, disconnect, updateDashboard } = useWebSocket()

// Evita varias llamadas simultáneas a /dashboard.
let dashboardLoading = false
let dashboardRefreshQueued = false

async function fetchDashboard() {
  if (dashboardLoading) {
    dashboardRefreshQueued = true
    return
  }

  dashboardLoading = true

  try {
    const response = await api.get('/dashboard')

    dashboard.value = {
      ...response.data,
      ranking: Array.isArray(response.data?.ranking) ? response.data.ranking : [],
      protocols: {
        winner_protocols: Array.isArray(response.data?.protocols?.winner_protocols)
          ? response.data.protocols.winner_protocols
          : [],
        loser_protocols: Array.isArray(response.data?.protocols?.loser_protocols)
          ? response.data.protocols.loser_protocols
          : [],
      },
    }

    console.log('Dashboard updated')
  } catch (error) {
    console.error('Error cargando dashboard:', error)
  } finally {
    dashboardLoading = false

    // Si llegó otra actualización durante la petición, ejecuta solo una más.
    if (dashboardRefreshQueued) {
      dashboardRefreshQueued = false
      void fetchDashboard()
    }
  }
}

watch(updateDashboard, (shouldUpdate) => {
  if (!shouldUpdate) return

  // Se resetea antes de pedir los datos para no crear un bucle reactivo.
  updateDashboard.value = false
  void fetchDashboard()
})

const desktopMediaQuery = window.matchMedia('(min-width: 1024px)')
const isDesktop = ref(desktopMediaQuery.matches)

function handleDesktopChange(event) {
  isDesktop.value = event.matches
}

onMounted(async () => {
  desktopMediaQuery.addEventListener('change', handleDesktopChange)

  if (auth.tutorial) {
    await router.replace({
      name: 'dashboard-tour',
    })
    return
  }

  await fetchDashboard()
  connect()
})

onUnmounted(() => {
  desktopMediaQuery.removeEventListener('change', handleDesktopChange)
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
  <!-- Solo se monta la versión móvil/tablet cuando la pantalla es menor de lg. -->
  <div
    v-if="!isDesktop"
    class="relative flex h-dvh flex-col overflow-hidden text-(--text)"
  >
    <div id="next-battle-mobile" class="shrink-0 px-4 pt-4">
      <NextBattle :next-battle="dashboard?.nextBattle" class="w-full" />
    </div>

    <div
      ref="mobileScroller"
      class="no-scrollbar flex min-h-0 w-full flex-1 snap-x snap-mandatory overflow-x-auto overflow-y-hidden scroll-smooth"
      @scroll="updateActiveMobilePage"
    >
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <div class="grid h-full min-h-0 grid-rows-[1fr_auto] gap-4">
          <Battle
            id="battle-mobile"
            :lobby="dashboard?.lobby"
            class="h-full min-h-0"
          />

          <div id="today-stats-mobile">
            <TodayStats :today-stats="dashboard?.todayStats || []" class="min-h-0" />
          </div>
        </div>
      </section>

      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <Ranking
          id="ranking-mobile"
          :ranking-data="dashboard?.ranking || []"
          class="h-full min-h-0"
        />
      </section>

      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <Protocols
          id="protocols-mobile"
          :protocols-data="dashboard?.protocols"
          class="h-full min-h-0"
        />
      </section>

      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <div class="grid h-full min-h-0 grid-rows-2 gap-4">
          <div id="profile-mobile">
            <Profile
              :sleep-score="dashboard?.sleepScore"
              :next-battle="dashboard?.nextBattle"
              :experience="dashboard?.experience"
              class="h-full min-h-0"
            />
          </div>

          <SleepScore
            id="sleep-score-mobile"
            :sleep-score="dashboard?.sleepScore"
            class="h-full min-h-0"
          />
        </div>
      </section>

      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <ProtocolsImpact
          id="protocol-impact-mobile"
          :protocol-impacts="dashboard?.protocolImpacts || []"
          class="h-full min-h-0"
        />
      </section>
    </div>

    <div
      class="pointer-events-none absolute bottom-5 left-1/2 z-20 flex -translate-x-1/2 items-center gap-2 rounded-full px-3 py-0 pt-5"
    >
      <span
        v-for="index in mobilePages"
        :key="index"
        class="h-2 rounded-full transition-all duration-200"
        :class="activeMobilePage === index - 1 ? 'w-6 bg-cyan-200' : 'w-2 bg-white/40'"
      />
    </div>
  </div>

  <!-- Solo se monta la versión de escritorio cuando la pantalla es lg o superior. -->
  <div
    v-else
    class="mt-5 flex h-[calc(100dvh-64px)] flex-col gap-3 overflow-hidden px-8 py-4 text-(--text)"
  >
    <NextBattle id="next-battle" :next-battle="dashboard?.nextBattle" />

    <div
      class="mx-auto grid min-h-0 min-w-0 w-full flex-1 grid-cols-[1fr_1.2fr_1.2fr] items-stretch gap-4"
    >
      <section class="flex min-h-0 flex-col gap-4">
        <SleepDataForm
          v-if="!dashboard?.lobby"
          class="min-h-0 flex-1"
          @saved="fetchDashboard"
        />

        <div v-else id="battle" class="min-h-0 flex-1 overflow-hidden">
          <Battle class="h-full w-full" :lobby="dashboard.lobby" />
        </div>

        <div id="today-stats" class="shrink-0">
          <TodayStats :today-stats="dashboard?.todayStats || []" />
        </div>
      </section>

      <section class="flex min-h-0 flex-col gap-4">
        <Ranking id="ranking" :ranking-data="dashboard?.ranking || []" />
        <Protocols id="protocols" :protocols-data="dashboard?.protocols" />
      </section>

      <section class="flex min-h-0 min-w-0 flex-col gap-4">
        <div id="user-profile">
          <Profile
            :sleep-score="dashboard?.sleepScore"
            :next-battle="dashboard?.nextBattle"
            :experience="dashboard?.experience"
            class="h-full min-h-0"
          />
        </div>

        <SleepScore id="sleep-score" :sleep-score="dashboard?.sleepScore" />

        <ProtocolsImpact
          id="protocol-impact"
          :protocol-impacts="dashboard?.protocolImpacts || []"
        />
      </section>
    </div>
  </div>

  <ChatButton />
</template>