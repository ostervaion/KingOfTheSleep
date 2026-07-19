<script setup>
import { computed } from 'vue'
import { useCycleList } from '@vueuse/core'

import avatarOne from '@/assets/example.jpg'
import avatarTwo from '@/assets/example.jpg'
import avatarThree from '@/assets/example.jpg'
import avatarFour from '@/assets/example.jpg'
import avatarFive from '@/assets/example.jpg'

const emit = defineEmits('save')

const avatars = [
  {
    id: 'avatarOne',
    name: 'avatarOne',
    image: avatarOne,
  },
  {
    id: 'avatarTwo',
    name: 'avatarTwo',
    image: avatarTwo,
  },
  {
    id: 'avatarThree',
    name: 'avatarThree',
    image: avatarThree,
  },
  {
    id: 'avatarFour',
    name: 'avatarFour',
    image: avatarFour,
  },
  {
    id: 'Five',
    name: 'Five',
    image: avatarFive,
  }
]

const {
  state: selectedAvatar,
  index: selectedAvatarIndex,
  next,
  prev,
  go,
} = useCycleList(avatars, {
  initialValue: avatars[0],
})


function selectAvatar(index) {
  go(index)
}

</script>

<template>
  <div
    class="font-inter flex max-h-[90vh] w-full min-w-0 flex-col overflow-hidden rounded-xl border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20"
  >
      <div
        class="grid min-w-0 grid-cols-1 overflow-hidden rounded-xl bg-white/[0.015] lg:grid-cols-[minmax(0,0.78fr)_minmax(0,1.22fr)]"
      >
        <!-- Welcome section -->
        <section
          class="relative flex min-w-0 flex-col justify-between overflow-hidden px-5 py-7 sm:px-7 sm:py-8 lg:min-h-[570px] lg:px-8 lg:py-10"
        >
          <div
            aria-hidden="true"
            class="pointer-events-none absolute -bottom-28 right-0 h-64 w-64 rounded-full bg-green-400/[0.025] blur-3xl"
          ></div>

          <div class="relative z-10">
            <!-- Visual placeholder -->
            <h1
              class="max-w-md text-3xl font-semibold leading-[1.1] tracking-[-0.035em] text-white sm:text-4xl"
            >
              Welcome to NapVille!
            </h1>

            <p class="mt-5 max-w-md text-sm leading-6 text-neutral-400 sm:text-[15px]">
              Select the avatar that will appear in your battles,
              rankings and player profile.
            </p>
          </div>

          <div class="relative z-10 mt-10 lg:mt-12">
            <p class="text-sm font-medium text-white">
              Your performance still comes from your sleep.
            </p>

            <p class="mt-2 max-w-md text-xs leading-5 text-neutral-500">
              The avatar represents you visually, while your sleep data determines how strongly
              you perform in each battle.
            </p>
          </div>
        </section>

        <!-- Avatar selection -->
        <section
          class="relative min-w-0 px-5 py-7 before:absolute before:left-5 before:right-5 before:top-0 before:h-px before:bg-white/[0.06] sm:px-7 sm:py-8 lg:px-8 lg:py-10 lg:before:bottom-8 lg:before:left-0 lg:before:right-auto lg:before:top-8 lg:before:h-auto lg:before:w-px"
        >
          <div class="flex h-full min-w-0 flex-col">
            <!-- Avatar carousel -->
            <div class="mt-8 min-w-0">
              <div class="relative flex min-w-0 items-center justify-center gap-2 sm:gap-4">

                <!-- Previous button -->
                <button
                  type="button"
                  aria-label="Previous avatar"
                  class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-white/[0.05] text-lg text-neutral-300 transition hover:bg-white/[0.09] hover:text-white"
                  @click="prev()"
                >
                  ‹
                </button>

                <!-- Active avatar -->
                <div class="min-w-0 flex-1">
                  <div
                    class="relative mx-auto aspect-[4/5] w-full max-w-[280px] overflow-hidden rounded-2xl bg-(--kots-background-color)"
                  >
                    <Transition name="avatar" mode="out-in">
                      <img
                        :key="selectedAvatar.id"
                        :src="selectedAvatar.image"
                        :alt="`${selectedAvatar.name} avatar`"
                        class="h-full w-full object-cover"
                      />
                    </Transition>

                    <div
                      class="pointer-events-none absolute inset-x-0 bottom-0 h-2/5  from-black/80 to-transparent"
                    ></div>

                    <div class="absolute inset-x-0 bottom-0 p-5 text-center">
                      <p class="text-lg font-semibold text-white">
                        {{ selectedAvatar.name }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Next button -->
                <button
                  type="button"
                  aria-label="Next avatar"
                  class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-white/[0.05] text-lg text-neutral-300 transition hover:bg-white/[0.09] hover:text-white"
                  @click="next()"
                >
                  ›
                </button>

              </div>

              <!-- Pagination -->
              <div class="mt-5 flex flex-wrap items-center justify-center gap-2">
                <button
                  v-for="(avatar, index) in avatars"
                  :key="avatar.id"
                  type="button"
                  :aria-label="`Select ${avatar.name}`"
                  :aria-pressed="selectedAvatarIndex === index"
                  class="h-1.5 rounded-full transition-all"
                  :class="
                    selectedAvatarIndex === index
                      ? 'w-6 bg-cyan-100'
                      : 'w-1.5 bg-white/20 hover:bg-white/40'
                  "
                  @click="selectAvatar(index)"
                ></button>
              </div>

            </div>

            <div class="mt-auto pt-8">
              <button
                type="button"
                class="w-full rounded-lg bg-cyan-100 px-5 py-3 text-sm font-semibold text-[#171715] transition hover:bg-cyan-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-100 focus-visible:ring-offset-2 focus-visible:ring-offset-[#171715]"
                @click="onContinue"
              >
                Select
              </button>
            </div>
          </div>
        </section>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";

.overflow-y-auto {
  overscroll-behavior: contain;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.08);
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.14);
}

.avatar-enter-active,
.avatar-leave-active {
  transition:
    opacity 160ms ease,
    transform 160ms ease;
}

.avatar-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.avatar-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>