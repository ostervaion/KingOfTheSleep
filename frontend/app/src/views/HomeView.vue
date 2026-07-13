<script setup>
import { ref } from 'vue'
import LoginPanel from '@/components/LoginPanel.vue'
import RegisterPanel from '@/components/RegisterPanel.vue'
import placeholderImage from '@/assets/placeholder-7.png'
import ArenaImage from '@/assets/ArenaImage.png'
import SleepScoreImage from '@/assets/SleepScoreImage.png'
import ProfileImage from '@/assets/ProfileImage.png'
import RankingsImage from '@/assets/RankingsImage.png'
import ProtocolsImage from '@/assets/ProtocolsImage.png'
import ChatImage from '@/assets/ChatImage.png'
import DashboardImage from '@/assets/DashboardImage.png'

const mode = ref('default')
const homeEmail = ref('')

const benefits = [
  'Gamify your sleep',
  'Track and improve consistency',
  'Compete and climb the ranks',
]

const steps = [
  {
    number: '1',
    title: 'Track your sleep',
    text: 'Use your prefered device to measure your sleep data',
    side: 'right',
  },
  {
    number: '2',
    title: "Enter tomorrow's battle",
    text: 'Your avatar fights in the arena the next day based on your sleep.',
    side: 'left',
  },
  {
    number: '3',
    title: 'Earn points and climb',
    text: 'Win battles, earn points, and rise in the rankings.',
    side: 'right',
  },
  {
    number: '4',
    title: 'Refine your protocol',
    text: 'Test habits, tweak your routine, and improve your recovery.',
    side: 'left',
  },
  {
    number: '5',
    title: 'Learn from the arena',
    text: 'See strategies, learn from other players, and get better.',
    side: 'right',
  },
]

function submitJoin() {
  mode.value = 'register'
}

function openRegistration() {
  mode.value = 'register'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div class="font-inter min-h-screen overflow-hidden bg-[#171715] text-white">
    <div class="mx-auto w-full max-w-[1240px] px-6 pb-8 pt-6 sm:px-8 lg:px-12 lg:pb-12 lg:pt-8 xl:px-16">
      <!-- HERO -->
      <section
        class="grid items-stretch gap-10 border-b border-white/10 pb-14 lg:grid-cols-[0.92fr_1.08fr] lg:gap-16 lg:pb-16"
      >
        <div class="flex flex-col justify-between lg:min-h-[550px]">
          <div>
            <h1
              class="mt-8 max-w-[520px] text-[clamp(3rem,5.2vw,5.25rem)] font-semibold leading-[0.98] tracking-[-0.06em]"
            >
              Enter the arena and <span class="text-cyan-200">master</span> your <span class="text-cyan-200">sleep</span>.
            </h1>

            <p class="mt-6 max-w-[470px] text-base leading-7 text-white/60 sm:text-lg sm:leading-8">
              Maximize your sleep quality with a competitive auto-battle game powered by your real sleep data.
            </p>
          </div>

          <div class="mt-10 grid max-w-[540px] gap-4 sm:grid-cols-3 lg:mt-12">
            <div v-for="benefit in benefits" :key="benefit" class="flex items-center gap-3">
              <img
                :src="placeholderImage"
                alt=""
                class="h-9 w-9 shrink-0 rounded-md  object-cover"
              />
              <p class="text-[11px] leading-4 text-white/65">{{ benefit }}</p>
            </div>
          </div>
        </div>

        <div class="rounded-2xl  bg-[#1B1B19] p-4 sm:p-5">
          <div class="relative overflow-hidden rounded-xl  bg-[#171715]">
            <img
              :src="placeholderImage"
              alt="Product preview placeholder"
              class="aspect-[16/10] w-full object-cover"
            />
            <button
              type="button"
              class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full border border-[#4ADE80] bg-[#171715]/90 px-5 py-3 text-xs font-semibold uppercase tracking-[0.18em] text-[#4ADE80]"
            >
              View demo
            </button>
          </div>

          <div class="mt-4 rounded-xl  bg-[#171715] p-3 sm:p-4">
            <template v-if="mode === 'default'">
              <form class="space-y-3" @submit.prevent="submitJoin">
                <input
                  v-model="homeEmail"
                  type="email"
                  required
                  placeholder="Type your email here..."
                  class="h-12 w-full rounded-lg  bg-[#1B1B19] px-4 text-sm text-white outline-none placeholder:text-white/35 focus:border-[#FACC15]"
                />
                <button
                  type="submit"
                  class="flex h-12 w-full items-center justify-center gap-3 rounded-lg bg-[#FACC15] px-5 text-base font-semibold text-[#171715] transition hover:brightness-105"
                >
                  Join <span aria-hidden="true">→</span>
                </button>
                <button
                  type="button"
                  class="mx-auto block text-xs text-white/45 transition hover:text-white/75"
                  @click="mode = 'login'"
                >
                  If you already have an account, we'll log you in
                </button>
              </form>
            </template>

            <div v-else class="relative">
              <button
                type="button"
                class="mb-4 text-xs font-medium text-[#FACC15]"
                @click="mode = 'default'"
              >
                ← Back
              </button>
              <LoginPanel v-if="mode === 'login'" />
              <RegisterPanel
                v-else
                :email="homeEmail"
                @back="mode = 'default'"
                @login="mode = 'login'"
              />
            </div>
          </div>
        </div>
      </section>

      <!-- HOW IT WORKS -->
      <section class="border-b border-white/10 py-16 sm:py-20 lg:py-24">
        <div class="flex justify-center">
          <div class="rounded-lg border border-cyan-200 px-2 text-gray-800 leading-none">
            <h2 class="text-heading text-xl  text-cyan-200">How it works</h2>
          </div>
        </div>

        <div class="relative mx-auto mt-10 max-w-[850px] sm:mt-14">
          <div
            class="absolute bottom-[6%] left-7 top-[6%] w-px bg-[#FACC15] md:left-1/2 md:-translate-x-1/2"
          ></div>

          <div
            v-for="step in steps"
            :key="step.number"
            class="relative grid min-h-[160px] grid-cols-[56px_1fr] items-center gap-5 py-3 md:grid-cols-[1fr_72px_1fr] md:gap-8"
          >
            <div v-if="step.side === 'left'" class="hidden items-center justify-end gap-5 text-right md:flex">
              <div class="max-w-[270px]">
                <h3 class="text-lg font-semibold tracking-[-0.025em]">{{ step.title }}</h3>
                <p class="mt-2 text-sm leading-6 text-white/50">{{ step.text }}</p>
              </div>
              <img
                :src="placeholderImage"
                alt=""
                class="h-[82px] w-[82px] shrink-0 rounded-xl  object-cover"
              />
            </div>
            <div v-else class="hidden md:block"></div>

            <div
              class="relative z-10 grid h-14 w-14 place-items-center justify-self-center rounded-full border-2 border-[#FACC15] bg-[#171715] text-xl font-semibold"
            >
              {{ step.number }}
            </div>

            <div v-if="step.side === 'right'" class="hidden items-center gap-5 md:flex">
              <img
                :src="placeholderImage"
                alt=""
                class="h-[82px] w-[82px] shrink-0 rounded-xl  object-cover"
              />
              <div class="max-w-[270px]">
                <h3 class="text-lg font-semibold tracking-[-0.025em]">{{ step.title }}</h3>
                <p class="mt-2 text-sm leading-6 text-white/50">{{ step.text }}</p>
              </div>
            </div>
            <div v-else class="hidden md:block"></div>

            <div class="flex items-center gap-4 md:hidden">
              <img
                :src="placeholderImage"
                alt=""
                class="h-14 w-14 shrink-0 rounded-lg  object-cover"
              />
              <div>
                <h3 class="text-base font-semibold">{{ step.title }}</h3>
                <p class="mt-1 text-sm leading-5 text-white/50">{{ step.text }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FEATURE GRID -->
      <section class="py-16 sm:py-20 lg:py-24">
        <div class="mb-10 flex justify-center sm:mb-12">
          <div class="rounded-lg border border-cyan-200 px-2 py-0.5 text-gray-800 leading-none">
            <h2 class="text-heading text-xl font-medium text-cyan-200">Why it works</h2>
          </div>
        </div>

        <div class="grid gap-3 md:grid-cols-12 md:auto-rows-[230px]">
          <article
            class="relative min-h-[520px] overflow-hidden rounded-2xl  bg-[#1B1B19] md:col-span-5 md:row-span-2 md:min-h-0"
          >
            <div class="relative z-10 max-w-[230px] p-6 lg:p-7">
              <h2 class="text-3xl font-semibold leading-[0.98] tracking-[-0.045em]">
                Enter the<br />Sleep Arena
              </h2>
              <p class="mt-5 text-sm leading-6 text-white/55">
                King Of The Sleep turns sleep improvement into something you can see, feel, and compete with.
              </p>
            </div>
            <img
              :src="ArenaImage"
              alt="Arena placeholder"
              class="absolute bottom-0 right-0 h-[72%] w-[68%] rounded-tl-2xl object-cover"
            />
          </article>

          <article class="min-h-[260px] overflow-hidden rounded-2xl bg-[#1B1B19] p-6 md:col-span-7 md:min-h-0">
            <div class="grid h-full gap-5 sm:grid-cols-[0.85fr_1.45fr] sm:items-center">
              <div>
                <h2 class="text-2xl font-semibold leading-[0.98] tracking-[-0.04em]">
                  Better Sleep<br />Becomes Rewarding
                </h2>
                <p class="mt-4 text-sm leading-6 text-white/55">
                  See your progress, rank, level, and recovery score so better nights stop feeling invisible.
                </p>
              </div>
              <img
                :src="ProfileImage"
                alt="Profile section placeholder"
                class="h-full min-h-[130px] w-full rounded-xl  object-contain"
              />
            </div>
          </article>

          <article class="flex min-h-[260px] flex-col overflow-hidden rounded-2xl bg-[#1B1B19] p-6 md:col-span-3 md:min-h-0">
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

          <article class="flex min-h-[260px] flex-col overflow-hidden rounded-2xl bg-[#1B1B19] p-6 md:col-span-4 md:min-h-0">
            <h2 class="text-xl font-semibold leading-[1] tracking-[-0.035em]">
              Your Routine<br />Becomes a Strategy
            </h2>
            <p class="mt-3 text-xs leading-5 text-white/50">
              Refine your habits, learn from top players, and discover what helps you recover better.
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
              Every upcoming battle gives you a clear reason to care about recovery, consistency, and sleep quality before bed.
            </p>
          </article>

          <article class="min-h-[230px] overflow-hidden rounded-2xl bg-[#1B1B19] p-4 md:col-span-3 md:min-h-0">
            <img
              :src="RankingsImage"
              alt="Rankings placeholder"
              class="h-full min-h-[145px] w-full rounded-xl  object-cover"
            />
          </article>

          <article class="min-h-[260px] overflow-hidden rounded-2xl bg-[#1B1B19] p-5 md:col-span-4 md:min-h-0">
            <div class="grid h-full gap-4 sm:grid-cols-[0.8fr_1.2fr]">
              <div>
                <h2 class="text-xl font-semibold leading-[1] tracking-[-0.035em]">
                  Learn from<br />the Arena
                </h2>
                <p class="mt-3 text-[11px] leading-5 text-white/50">
                  Chat with the player community or message rivals directly about routines, protocols, and strategies.
                </p>
              </div>
              <img
                :src="ChatImage"
                alt="Community chat placeholder"
                class="h-full min-h-[130px] w-full rounded-xl  object-cover"
              />
            </div>
          </article>

          <button
            type="button"
            class="group flex min-h-[230px] items-end justify-between rounded-2xl bg-[#FACC15] p-6 text-left text-[#171715] transition hover:brightness-105 md:col-span-2 md:min-h-0"
            @click="openRegistration"
          >
            <span class="text-base font-bold uppercase tracking-[-0.02em]">Join the arena</span>
            <span class="text-2xl transition group-hover:translate-x-1" aria-hidden="true">→</span>
          </button>
        </div>
      </section>

      <!-- DASHBOARD -->
      <section class="border-t border-white/10 py-16 sm:py-20 lg:py-24">
        <div class="flex justify-center">
          <div class="rounded-lg border border-cyan-200 px-2 py-0.5 text-gray-800 leading-none">
            <h2 class="text-heading text-xl font-medium text-cyan-200">Dashboard</h2>
          </div>
        </div>

        <p class="mx-auto mt-6 max-w-[680px] text-center text-base leading-7 text-white/55 sm:text-lg sm:leading-8">
See how your sleep, battles, protocols, and rankings connect in one place so you always know what helped, what changed, and what to improve next.        </p>

        <div class="mt-10 overflow-hidden  p-3 sm:mt-12 sm:p-4 lg:p-5">
          <img
            :src="DashboardImage"
            alt="Dashboard placeholder"
            class="aspect-[16/9] w-full rounded-xl object-contain"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";
</style>
