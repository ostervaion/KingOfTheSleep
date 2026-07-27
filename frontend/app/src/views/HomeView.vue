<script setup>
import { ref } from 'vue'
import LoginPanel from '@/components/LoginPanel.vue'
import AppFooter from '@/components/Footer.vue'
import RegisterPanel from '@/components/RegisterPanel.vue'
import placeholderImage from '@/assets/placeholder-7.png'
import ArenaImage from '@/assets/ArenaImage.png'
import SleepScoreImage from '@/assets/SleepScoreImage.png'
import ProfileImage from '@/assets/ProfileImage.png'
import RankingsImage from '@/assets/RankingsImage.png'
import ProtocolsImage from '@/assets/ProtocolsImage.png'
import ChatImage from '@/assets/ChatImage.png'
import DashboardImage from '@/assets/DashboardImage.png'
import Menu from '@/components/Menu.vue'
import { useAuthStore } from '@/stores/auth'
const appStore = useAuthStore()
const homeEmail = ref('')

function submitJoin() {
  appStore.setAuthMode('register')
}

function openRegistration() {
  appStore.setAuthMode('register')
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <Menu />
  <div class="font-inter min-h-screen overflow-hidden bg-(--kots-blocks-color) text-white">
    <div
      class="mx-auto w-full max-w-[1240px] px-6 pb-8 pt-6 sm:px-8 lg:px-12 lg:pb-12 lg:pt-8 xl:px-16"
    >
<!-- HERO -->
<section
  class="grid items-center gap-12 py-12 sm:py-16 lg:min-h-[620px] lg:grid-cols-[0.92fr_1.08fr] lg:gap-16 lg:py-20"
>
  <!-- Hero content -->
  <div class="mx-auto w-full max-w-[560px] lg:mx-0">
    <h1
      class="text-center text-5xl font-semibold leading-[0.95] tracking-[-0.06em] sm:text-7xl sm:leading-[0.95] lg:text-left"
    >
      Enter the arena and
      <span class="text-yellow-400">master your sleep.</span>
    </h1>

    <p
      class="mx-auto mt-6 max-w-[520px] text-balance text-center text-base leading-6 text-zinc-400 sm:text-lg sm:leading-7 lg:mx-0 lg:text-left"
    >
      Maximize your sleep quality with a competitive auto-battle game powered by your real sleep
      data.
    </p>

    <!-- Authentication form -->
    <div
      class="mt-8 rounded-xl bg-(--kots-blocks-color) p-3 sm:mt-10 sm:p-5"
    >
      <template v-if="appStore.authMode === 'default'">
        <form class="space-y-3" @submit.prevent="submitJoin">
          <div class="flex flex-col gap-2 sm:flex-row">
            <input
              v-model="homeEmail"
              type="email"
              required
              placeholder="Type your email here..."
              class="h-11 w-full rounded-lg border border-white/10 bg-(--kots-background-color) px-4 text-sm text-white outline-none transition placeholder:text-white/35 hover:border-white/20 focus:border-cyan-200 focus:ring-1 focus:ring-cyan-200/30 sm:w-3/4"
            />

            <button
              type="submit"
              class="flex h-11 w-full cursor-pointer items-center justify-center gap-3 rounded-lg border-none bg-cyan-200 px-5 text-sm font-semibold text-[#171715] transition hover:bg-cyan-100 sm:w-1/4"
            >
              Join
              <span aria-hidden="true">→</span>
            </button>
          </div>

          <button
            type="button"
            class="w-full cursor-pointer rounded-lg px-3 text-center text-xs text-zinc-400 transition hover:text-cyan-200"
            @click="appStore.setAuthMode('login')"
          >
            If you already have an account, we'll log you in
          </button>
        </form>
      </template>

      <div v-else class="relative rounded-lg">
        <button
          type="button"
          class="mb-4 cursor-pointer rounded-lg px-3 py-2 text-xs font-medium text-white/55 transition hover:bg-white/5 hover:text-cyan-200"
          @click="appStore.setAuthMode('default')"
        >
          ← Back
        </button>

        <LoginPanel v-if="appStore.authMode === 'login'" />

        <RegisterPanel
          v-else
          :email="homeEmail"
          @back="appStore.setAuthMode('default')"
          @login="appStore.setAuthMode('login')"
        />
      </div>
    </div>
  </div>

  <!-- Dashboard preview -->
  <div class="flex w-full items-center justify-center">
    <div
      class="relative w-full overflow-hidden rounded-2xl bg-[#171715] shadow-xl shadow-black/20"
    >
      <img
        :src="DashboardImage"
        alt="King Of The Sleep dashboard preview"
        class="aspect-[16/10] w-full object-cover"
      />
    </div>
  </div>
</section>

            <!-- GAME INTRODUCTION -->
      <section class="py-16 sm:py-20 lg:py-10">
        <div class="mx-auto max-w-[820px] text-center">
          <div class="flex justify-center">
            <div class="rounded-lg border border-cyan-200 px-2 py-0.5 leading-none">
              <span class="text-sm font-medium text-cyan-200">The game</span>
            </div>
          </div>

          <h2
            class="mx-auto mt-6 max-w-[700px] text-3xl font-semibold leading-thigh tracking-[-0.045em] sm:text-4xl lg:text-5xl"
          >
          <span> Your real life sleep determines how your avatar performs in the arena.</span>
          </h2>

      <p class="mx-auto mt-4 max-w-[760px] text-sm leading-7 text-white/60 sm:text-base">
        King Of Sleep turns your real sleep data into the performance of your avatar in a
            competitive auto-battle game. Every day, up to 100 players enter the same arena, fight
            automatically, and climb the rankings based on how well they slept.
          </p>

          <p class="mx-auto mt-4 max-w-[760px] text-sm leading-7 text-white/60 sm:text-base">
            Sleep duration, efficiency, consistency, REM, and deep sleep determine each battle. As the
            day progresses, players can explore the lobby, challenge rivals, compare sleep protocols,
            and discover which habits produce the best results.
          </p>
        </div>
      </section>

      <section class="py-16 sm:py-20 lg:py-8">

        <div class="grid gap-3 md:grid-cols-12 md:auto-rows-[230px]">
          <article
            class="relative min-h-[520px] overflow-hidden rounded-2xl bg-[#1B1B19] md:col-span-5 md:row-span-2 md:min-h-0"
          >
            <div class="relative z-10 max-w-[230px] p-6 lg:p-7">
              <h2 class="text-3xl font-semibold leading-[0.98] tracking-[-0.045em]">
                Enter the<br />Sleep Arena
              </h2>
              <p class="mt-5 text-sm leading-6 text-white/55">
                King Of The Sleep turns sleep improvement into something you can see, feel, and
                compete with.
              </p>
            </div>
            <img
              :src="ArenaImage"
              alt="Arena placeholder"
              class="absolute bottom-0 right-0 h-[72%] w-[68%] rounded-tl-2xl object-cover"
            />
          </article>

          <article
            class="min-h-[260px] overflow-hidden rounded-2xl bg-[#1B1B19] p-6 md:col-span-7 md:min-h-0"
          >
            <div class="grid h-full gap-5 sm:grid-cols-[0.85fr_1.45fr] sm:items-center">
              <div>
                <h2 class="text-2xl font-semibold leading-[0.98] tracking-[-0.04em]">
                  Better Sleep<br />Becomes Rewarding
                </h2>
                <p class="mt-4 text-sm leading-6 text-white/55">
                  See your progress, rank, level, and recovery score so better nights stop feeling
                  invisible.
                </p>
              </div>
              <img
                :src="ProfileImage"
                alt="Profile section placeholder"
                class="h-full min-h-[130px] w-full rounded-xl object-contain"
              />
            </div>
          </article>

          <article
            class="flex min-h-[260px] flex-col overflow-hidden rounded-2xl bg-[#1B1B19] p-6 md:col-span-3 md:min-h-0"
          >
            <h2 class="text-xl font-semibold leading-[1] tracking-[-0.035em]">
              Consistency<br />Becomes a Game
            </h2>
            <p class="mt-3 text-xs leading-5 text-white/50">
              Daily battles, rankings, and weekly seasons give you a reason to keep showing up.
            </p>
            <img
              :src="SleepScoreImage"
              alt="Sleep score placeholder"
              class="mt-auto h-[108px] w-full rounded-lg object-cover"
            />
          </article>

          <article
            class="flex min-h-[260px] flex-col overflow-hidden rounded-2xl bg-[#1B1B19] p-6 md:col-span-4 md:min-h-0"
          >
            <h2 class="text-xl font-semibold leading-[1] tracking-[-0.035em]">
              Your Routine<br />Becomes a Strategy
            </h2>
            <p class="mt-3 text-xs leading-5 text-white/50">
              Refine your habits, learn from top players, and discover what helps you recover
              better.
            </p>
            <img
              :src="ProtocolsImage"
              alt="Protocols ranking placeholder"
              class="h-[108px] w-full rounded-lg object-cover object-top"
            />
          </article>

          <article class="min-h-[230px] rounded-2xl bg-[#1B1B19] p-6 md:col-span-3 md:min-h-0">
            <h2 class="text-xl font-semibold leading-[1] tracking-[-0.035em]">
              Tomorrow's Battle Gives<br />Tonight a Purpose
            </h2>
            <p class="mt-4 text-xs leading-5 text-white/50">
              Every upcoming battle gives you a clear reason to care about recovery, consistency,
              and sleep quality before bed.
            </p>
          </article>

          <article
            class="min-h-[230px] overflow-hidden rounded-2xl bg-[#1B1B19] p-4 md:col-span-3 md:min-h-0"
          >
            <img
              :src="RankingsImage"
              alt="Rankings placeholder"
              class="h-full min-h-[145px] w-full rounded-xl object-cover"
            />
          </article>

          <article
            class="min-h-[260px] overflow-hidden rounded-2xl bg-[#1B1B19] p-5 md:col-span-4 md:min-h-0"
          >
            <div class="grid h-full gap-4 sm:grid-cols-[0.8fr_1.2fr]">
              <div>
                <h2 class="text-xl font-semibold leading-[1] tracking-[-0.035em]">
                  Learn from<br />the Arena
                </h2>
                <p class="mt-3 text-[11px] leading-5 text-white/50">
                  Chat with the player community or message rivals directly about routines,
                  protocols, and strategies.
                </p>
              </div>
              <img
                :src="ChatImage"
                alt="Community chat placeholder"
                class="h-full min-h-[130px] w-full rounded-xl object-cover"
              />
            </div>
          </article>

          <button
            type="button"
            class="group flex min-h-[230px] items-end justify-between rounded-2xl bg-yellow-500 p-6 text-left text-[#171715] transition  md:col-span-2 md:min-h-0"
            @click="openRegistration"
          >
            <span class="text-base font-bold uppercase tracking-[-0.02em]">Join the arena</span>
            <span class="text-2xl transition group-hover:translate-x-1" aria-hidden="true">→</span>
          </button>
        </div>
      </section>
      <!-- HOW IT WORKS -->
      <section class="py-16 sm:py-20 lg:py-24">
        <!-- Section heading -->
        <div class="mx-auto max-w-[680px] text-center">
          <div class="flex justify-center">
            <div class="rounded-lg border border-cyan-200 px-2 py-1 leading-none">
              <span class="text-sm font-medium text-cyan-200">How it works</span>
            </div>
          </div>

          <h2
            class="mt-6 text-3xl font-semibold tracking-[-0.045em] text-white sm:text-4xl"
          >
            Sleep, compete, and improve.
          </h2>

          <p class="mx-auto mt-4 max-w-[560px] text-sm leading-6 text-white/50 sm:text-base">
            Your sleep data powers your avatar, determines your results, and helps you discover which
            habits improve your recovery.
          </p>
        </div>

        <!-- Steps -->
<!-- Steps -->
<div class="mx-auto mt-12 grid max-w-[1050px] gap-4 sm:grid-cols-2 lg:mt-16 lg:grid-cols-5">
  <!-- Step 1 -->
  <article class="relative flex flex-col rounded-2xl bg-[#1B1B19] p-5">
    <div class="flex items-center justify-between">
      <span
        class="grid h-10 w-10 place-items-center rounded-full border border-yellow-400 text-sm font-semibold text-yellow-400"
      >
        1
      </span>

      <span class="text-xs font-medium uppercase text-zinc-400">
        Tonight
      </span>
    </div>

    <div class="mt-auto pt-6 align-top">
      <h3 class="text-lg font-semibold tracking-[-0.025em]">
        Track your daily sleep
      </h3>

      <p class="mt-2 text-sm leading-5 text-white/50">
        Use your preferred device to measure your sleep data.
      </p>
    </div>
  </article>

  <!-- Step 2 -->
  <article class="relative flex flex-col rounded-2xl bg-[#1B1B19] p-5">
    <div class="flex items-center justify-between">
      <span
        class="grid h-10 w-10 place-items-center rounded-full border border-yellow-400 text-sm font-semibold text-yellow-400"
      >
        2
      </span>

      <span class="text-xs font-medium uppercase text-zinc-400">
        Tomorrow
      </span>
    </div>

    <div class="mt-auto pt-6 align-top">
      <h3 class="text-lg font-semibold tracking-[-0.025em]">
        Enter tomorrow's battle
      </h3>

      <p class="mt-2 text-sm leading-5 text-white/50">
        Your avatar enters the arena based on how well you slept.
      </p>
    </div>
  </article>

  <!-- Step 3 -->
  <article class="relative flex flex-col rounded-2xl bg-[#1B1B19] p-5">
    <div class="flex items-center justify-between">
      <span
        class="grid h-10 w-10 place-items-center rounded-full border border-yellow-400 text-sm font-semibold text-yellow-400"
      >
        3
      </span>

      <span class="text-xs font-medium uppercase text-zinc-400">
        Compete
      </span>
    </div>

    <div class="mt-auto pt-6 align-top">
      <h3 class="text-lg font-semibold tracking-[-0.025em]">
        Earn points and climb
      </h3>

      <p class="mt-2 text-sm leading-5 text-white/50">
        Win automatic battles, earn points, and rise through the rankings.
      </p>
    </div>
  </article>

  <!-- Step 4 -->
  <article class="relative flex flex-col rounded-2xl bg-[#1B1B19] p-5">
    <div class="flex items-center justify-between">
      <span
        class="grid h-10 w-10 place-items-center rounded-full border border-yellow-400 text-sm font-semibold text-yellow-400"
      >
        4
      </span>

      <span class="text-xs font-medium uppercase text-zinc-400">
        Adapt
      </span>
    </div>

    <div class="mt-auto pt-6 align-top">
      <h3 class="text-lg font-semibold tracking-[-0.025em]">
        Refine your protocol
      </h3>

      <p class="mt-2 text-sm leading-5 text-white/50">
        Test new habits, adjust your routine, and improve your recovery.
      </p>
    </div>
  </article>

  <!-- Step 5 -->
  <article
    class="relative flex flex-col rounded-2xl bg-[#1B1B19] p-5 sm:col-span-2 lg:col-span-1"
  >
    <div class="flex items-center justify-between">
      <span
        class="grid h-10 w-10 place-items-center rounded-full border border-yellow-400 text-sm font-semibold text-yellow-400"
      >
        5
      </span>

      <span class="text-xs font-medium uppercase text-zinc-400">
        Improve
      </span>
    </div>

    <div class="mt-auto pt-6 align-top">
      <h3 class="text-lg font-semibold tracking-[-0.025em]">
        Learn from the arena
      </h3>

      <p class="mt-2 text-sm leading-5 text-white/50">
        Explore other strategies, learn from players, and keep improving.
      </p>
    </div>
  </article>
</div>
      </section>

   
      <!-- DASHBOARD -->
      <section class=" py-16 sm:py-20 lg:py-24">
        <div class="flex justify-center">
          <div class="rounded-lg border border-cyan-200 px-2 py-0.5 text-gray-800 leading-none">
             <span class="text-sm font-medium text-cyan-200">Dashboard</span>
          </div>
        </div>

        <p
          class="mx-auto mt-6 max-w-[680px] text-center text-base leading-7 text-white/55 sm:text-lg sm:leading-8"
        >
          See how your sleep, battles, protocols, and rankings connect in one place so you always
          know what helped, what changed, and what to improve next.
        </p>

        <div class="mt-10 overflow-hidden p-3 sm:mt-12 sm:p-4 lg:p-5">
          <img
            :src="DashboardImage"
            alt="Dashboard placeholder"
            class="aspect-[16/9] w-full rounded-xl object-contain"
          />
        </div>
      </section>
    </div>
  </div>
  <AppFooter />
</template>

<style scoped>
@reference "@/assets/main.css";

</style>
