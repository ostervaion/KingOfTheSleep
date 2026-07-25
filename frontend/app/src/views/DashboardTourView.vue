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
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { startDashboardTour } from '@/tours/dashboardTour'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import WelcomePopup from '@/components/dashboard/welcomePopup.vue'

const router = useRouter()
const auth = useAuthStore()
const dashboard = ref(null)
const dialog = ref(null)

const showSleepFormTour = ref(false)

async function showSleepForm() {
  showSleepFormTour.value = true
  await nextTick()
}

function openDialog() {
  dialog.value?.showModal()
}

async function closeDialog() {
  dialog.value?.close()

  await auth.removeTutorial()

  await router.replace({
    name: 'dashboard',
  })
}

onMounted(async () => {
  await nextTick()

  startDashboardTour(showSleepForm, async () => {
    await nextTick()
    openDialog()
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
  <div
    class="relative flex h-dvh flex-col overflow-hidden text-(--text) lg:hidden"
  >
    <!-- Always visible top bar -->
    <div
      id="next-battle-mobile"
      class="shrink-0 px-4 pt-4"
    >
      <NextBattle
        :next-battle="dashboard?.nextBattle"
        class="w-full"
      />
    </div>

    <!-- Horizontal pages -->
    <div
      ref="mobileScroller"
      class="no-scrollbar flex min-h-0 w-full flex-1 snap-x snap-mandatory overflow-x-auto overflow-y-hidden scroll-smooth"
      @scroll="updateActiveMobilePage"
    >
      <!-- Page 1: Lobby/Sleep form + TodayStats -->
      <section
        class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6"
      >
        <div class="grid h-full min-h-0 grid-rows-[1fr_auto] gap-4">
          <Battle
            v-if="!showSleepFormTour"
            id="battle-mobile"
            class="h-full min-h-0"
            :lobby="dashboard?.lobby"
          />

          <SleepDataForm
            v-else
            id="sleep-form-mobile"
            class="h-full min-h-0"
            @saved="fetchDashboard"
          />

          <div id="today-stats-mobile">
            <TodayStats class="min-h-0" />
          </div>
        </div>
      </section>

      <!-- Page 2: Ranking -->
      <section
        class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6"
      >
        <Ranking
          id="ranking-mobile"
          :ranking-data="dashboard?.ranking || []"
          class="h-full min-h-0"
        />
      </section>

      <!-- Page 3: Protocols -->
      <section
        class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6"
      >
        <Protocols
          id="protocols-mobile"
          class="h-full min-h-0"
        />
      </section>

      <!-- Page 4: Profile + SleepScore -->
      <section
        class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6"
      >
        <div class="grid h-full min-h-0 grid-rows-2 gap-4">
          <div id="profile-mobile">
            <Profile class="h-full min-h-0" />
          </div>

          <SleepScore
            id="sleep-score-mobile"
            :sleep-score="dashboard?.sleepScore"
            class="h-full min-h-0"
          />
        </div>
      </section>

      <!-- Page 5: Protocol Impact -->
      <section
        class="h-full min-w-full snap-start snap-always px-4 py-4 pb-6"
      >
        <ProtocolsImpact
          id="protocol-impact-mobile"
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
        :class="
          activeMobilePage === index - 1
            ? 'w-6 bg-cyan-200'
            : 'w-2 bg-white/40'
        "
      />
    </div>
  </div>

  <!-- PARA ORDENADOR -->
  <div
    class="mt-5 hidden h-[calc(100dvh-64px)] flex-col gap-3 overflow-hidden px-8 py-4 text-(--text) lg:flex"
  >
    <NextBattle
      id="next-battle"
      :next-battle="dashboard?.nextBattle"
    />

    <div
      class="mx-auto grid min-h-0 min-w-0 w-full flex-1 items-stretch gap-4 lg:grid-cols-[1fr_1.2fr_1.2fr]"
    >
      <section class="flex min-h-0 flex-col gap-4">
        <Battle
          v-if="!showSleepFormTour"
          id="battle"
          class="min-h-0 flex-1"
          :lobby="dashboard?.lobby"
        />

        <SleepDataForm
          v-else
          id="sleep-form"
          class="min-h-0 flex-1"
          @saved="fetchDashboard"
        />

        <div
          id="today-stats"
          class="shrink-0"
        >
          <TodayStats />
        </div>
      </section>

      <section class="flex min-h-0 flex-col gap-4">
        <Ranking
          id="ranking"
          :ranking-data="dashboard?.ranking || []"
        />

        <Protocols id="protocols" />
      </section>

      <section class="flex min-h-0 min-w-0 flex-col gap-4">
        <div id="user-profile">
          <Profile />
        </div>

        <SleepScore
          id="sleep-score"
          :sleep-score="dashboard?.sleepScore"
        />

        <ProtocolsImpact id="protocol-impact" />
      </section>
    </div>
  </div>
  <ChatButton />
    <Teleport to="body">
    <dialog
      ref="dialog"
      class="m-auto lg:w-[50vw] max-w-5xl overflow-y-auto rounded-xl border-none bg-transparent p-0 backdrop:bg-black/60 sm:w-[90vw]"
    >
      <WelcomePopup @close="closeDialog" />
    </dialog>
  </Teleport>
</template>