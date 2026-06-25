<script setup>
import NextBattle from '@/components/dashboard/NextBattle.vue'
import Ranking from '@/components/dashboard/Ranking.vue'
import Protocols from '@/components/dashboard/Protocols.vue'
import ProtocolsImpact from '@/components/dashboard/ProtocolImpact.vue'
import SleepScore from '@/components/dashboard/SleepScore.vue'
import Profile from '@/components/dashboard/Profile.vue'
import TodayStats from '@/components/dashboard/TodayStats.vue'
import Lobby from '@/components/dashboard/Lobby.vue'

const nextBattle = {
  currentRanking: 12,
  seconds: 999999,
  endDay: 1234,
  deltaRanking: 34,
}
import { ref, onMounted } from 'vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

onMounted(() => {
  appStore.onDashboard = true
})
</script>

<template>
  <div
    class="h-[calc(100dvh-64px)] text-(--text) mt-5 px-4 py-4 sm:px-6 lg:px-8 overflow-hidden flex flex-col gap-3"
  >
    <NextBattle :nextBattle="nextBattle" />

    <div
      class="mx-auto grid w-full flex-1 min-h-0 gap-4 lg:grid-cols-[1fr_1.2fr_1.2fr] items-stretch"
    >
      <section class="flex flex-col gap-4 min-h-0">
        <Lobby />
        <TodayStats />
      </section>

      <section class="flex flex-col gap-4 min-h-0">
        <Ranking />
        <Protocols />
      </section>

      <section class="flex flex-col gap-4 min-h-0">
        <Profile />
        <SleepScore />
        <ProtocolsImpact />
      </section>
    </div>
  </div>
</template>
