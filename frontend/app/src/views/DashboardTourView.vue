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
import { ref, nextTick, onMounted } from 'vue'
import { startDashboardTour } from '@/tours/dashboardTour'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const dashboard = ref({
  nextBattle: {
    currentRanking: 4,
    seconds: 1232,
    endDay: 38794,
    deltaRanking: 3,
  },

  sleepScore: {
    labels: ['THU', 'FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED'],
    scores: [76, 81, 79, 84, 80, 86, 82],
  },

  ranking: [
    {
      ranking: '1',
      user_id: 36,
      name: 'stormowl36',
      avatar_path: null,
      points: '1649',
      posChange: '3',
      trend: 'up',
    },
    {
      ranking: '2',
      user_id: 34,
      name: 'echowolf34',
      avatar_path: null,
      points: '1645',
      posChange: '1',
      trend: 'up',
    },
    {
      ranking: '3',
      user_id: 30,
      name: 'auroramystic30',
      avatar_path: null,
      points: '1640',
      posChange: '2',
      trend: 'down',
    },
    {
      ranking: '4',
      user_id: 48,
      name: 'Martin',
      avatar_path: null,
      points: '1618',
      posChange: '3',
      trend: 'up',
    },
    {
      ranking: '5',
      user_id: 37,
      name: 'velvettiger37',
      avatar_path: null,
      points: '1617',
      posChange: '1',
      trend: 'down',
    },
    {
      ranking: '6',
      user_id: 39,
      name: 'novashadow39',
      avatar_path: null,
      points: '1565',
      posChange: '4',
      trend: 'up',
    },
    {
      ranking: '7',
      user_id: 32,
      name: 'lunartiger32',
      avatar_path: null,
      points: '1549',
      posChange: '2',
      trend: 'up',
    },
    {
      ranking: '8',
      user_id: 25,
      name: 'novanova25',
      avatar_path: null,
      points: '1511',
      posChange: '1',
      trend: 'same',
    },
    {
      ranking: '9',
      user_id: 21,
      name: 'novawolf21',
      avatar_path: null,
      points: '1509',
      posChange: '2',
      trend: 'down',
    },
    {
      ranking: '10',
      user_id: 31,
      name: 'pixelmystic31',
      avatar_path: null,
      points: '1505',
      posChange: '4',
      trend: 'up',
    },
  ],

  protocolImpacts: [
    {
      id: 1,
      name: 'Temperature Cycling',
      percentage: 18,
      daysUsed: 12,
    },
    {
      id: 2,
      name: 'Magnesium Intake',
      percentage: 12,
      daysUsed: 18,
    },
    {
      id: 3,
      name: 'Light Management',
      percentage: 8,
      daysUsed: 15,
    },
    {
      id: 4,
      name: 'Late Caffeine',
      percentage: -14,
      daysUsed: 6,
    },
    {
      id: 5,
      name: 'Stimulant Control',
      percentage: -7,
      daysUsed: 9,
    },
  ],

  lobby: true,

  todayStats: {
    wins: 3,
    losses: 2,
  },

  protocols: {
    winner_protocols: [
      {
        ranking: 1,
        protocol: 'Melatonin Intake',
        usage: 190,
        winrate: 0.5263157894736842,
      },
      {
        ranking: 2,
        protocol: 'Magnesium Intake',
        usage: 165,
        winrate: 0.49696969696969695,
      },
      {
        ranking: 3,
        protocol: 'Sunlight Maxing',
        usage: 154,
        winrate: 0.4935064935064935,
      },
      {
        ranking: 4,
        protocol: 'Light Management',
        usage: 132,
        winrate: 0.48484848484848486,
      },
      {
        ranking: 5,
        protocol: 'Temperature Cycling',
        usage: 140,
        winrate: 0.4714285714285714,
      },
    ],
    loser_protocols: [
      {
        ranking: 1,
        protocol: 'Stimulant Control',
        usage: 91,
        winrate: 0.4175824175824176,
      },
      {
        ranking: 2,
        protocol: 'Caffeine Minimum',
        usage: 83,
        winrate: 0.46987951807228917,
      },
      {
        ranking: 3,
        protocol: 'Temperature Cycling',
        usage: 140,
        winrate: 0.4714285714285714,
      },
      {
        ranking: 4,
        protocol: 'Light Management',
        usage: 132,
        winrate: 0.48484848484848486,
      },
      {
        ranking: 5,
        protocol: 'Sunlight Maxing',
        usage: 154,
        winrate: 0.4935064935064935,
      },
    ],
  },

  profile: {
    rank: 4432,
    level: 42,
    xp: 18450,
    nextxp: 25000,
    todaysSleepScore: 82,
  },
})

const showSleepFormTour = ref(false)

async function showSleepForm() {
  showSleepFormTour.value = true
  await nextTick()
}

onMounted(async () => {
  await nextTick()

  startDashboardTour(showSleepForm, async () => {
    await nextTick()
    auth.removeTutorial()
    await router.replace({
      name: 'dashboard',
    })
  })
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
    <div id="next-battle-mobile" class="shrink-0 px-4 pt-4">
      <NextBattle :next-battle="dashboard?.nextBattle" class="w-full" />
    </div>

    <!-- Horizontal pages -->
    <div
      ref="mobileScroller"
      class="no-scrollbar flex min-h-0 w-full flex-1 snap-x snap-mandatory overflow-x-auto overflow-y-hidden scroll-smooth"
      @scroll="updateActiveMobilePage"
    >
      <!-- Page 1: Lobby/Sleep form + TodayStats -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <div class="grid h-full min-h-0 grid-rows-[1fr_auto] gap-4">
         <!-- <Battle
            v-if="!showSleepFormTour"
            id="battle-mobile"
            class="h-full min-h-0"
            :lobby="dashboard?.lobby"
          /> -->

          <SleepDataForm  id="sleep-form-mobile" class="h-full min-h-0" />

          <div id="today-stats-mobile">
            <TodayStats :today-stats="dashboard?.todayStats || {}" class="min-h-0" />
          </div>
        </div>
      </section>

      <!-- Page 2: Ranking -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <Ranking
          id="ranking-mobile"
          :ranking-data="dashboard?.ranking || []"
          class="h-full min-h-0"
        />
      </section>

      <!-- Page 3: Protocols -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <Protocols
          id="protocols-mobile"
          :protocols-data="dashboard?.protocols"
          class="h-full min-h-0"
        />
      </section>

      <!-- Page 4: Profile + SleepScore -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <div class="grid h-full min-h-0 grid-rows-2 gap-4">
          <div id="profile-mobile">
            <Profile
              :sleep-score="dashboard?.sleepScore"
              :next-battle="dashboard?.nextBattle"
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

      <!-- Page 5: Protocol Impact -->
      <section class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6">
        <ProtocolsImpact
          id="protocol-impact-mobile"
          :protocol-impacts="dashboard?.protocolImpacts || []"
          class="h-full min-h-0"
        />
      </section>
    </div>

    <!-- Mobile dots -->
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

  <!-- PARA ORDENADOR -->
  <div
    class="mt-5 hidden h-[calc(100dvh-64px)] flex-col gap-3 overflow-hidden px-8 py-4 text-(--text) lg:flex"
  >
    <NextBattle id="next-battle" :next-battle="dashboard?.nextBattle" />

    <div
      class="mx-auto grid min-h-0 min-w-0 w-full flex-1 items-stretch gap-4 lg:grid-cols-[1fr_1.2fr_1.2fr]"
    >
      <section class="flex min-h-0 flex-col gap-4">
        <!-- <Battle
          v-if="!showSleepFormTour"
          id="battle"
          class="min-h-0 flex-1"
          :lobby="dashboard?.lobby"
        /> -->

        <SleepDataForm  id="sleep-form" class="min-h-0 flex-1" />

        <div id="today-stats" class="shrink-0">
          <TodayStats :today-stats="dashboard?.todayStats || {}" />
        </div>
      </section>

      <section class="flex min-h-0 flex-col gap-4">
        <Ranking id="ranking" :ranking-data="dashboard?.ranking || []" />

        <Protocols id="protocols" :protocols-data="dashboard?.protocols" />
      </section>

      <section class="flex min-h-0 min-w-0 flex-col gap-4">
        <div id="user-profile">
          <Profile :sleep-score="dashboard?.sleepScore" :next-battle="dashboard?.nextBattle" />
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
