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
  },
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

/// Temporal, aqui falta guardar el valor
function onContinue(){
  emit('close') 
}
</script>

<template>
  <div
    class="font-inter py-5 px-8 mx-auto flex max-h-[90dvh] w-full max-w-[420px] min-w-0 flex-col overflow-x-hidden overflow-y-auto rounded-lg bg-[#171715]  text-white shadow-[0_12px_30px_rgb(0_0_0_/_40%)]"
  >
    <!-- Welcome section -->
    <section class="min-w-0">
      <h1 class="pr-7 text-lg font-semibold text-white">
        Choose your avatar
      </h1>

      <p class="mt-2 text-xs leading-4 tracking-wide text-white">
        You now know how the arena works. Choose the avatar that will represent
        you in battles, rankings and your player profile.
      </p>
    </section>

    <!-- Avatar carousel -->
    <section class="mt-5 min-w-0">
      <div class="relative flex min-w-0 items-center justify-center gap-3">
        <!-- Previous button -->
        <button
          type="button"
          aria-label="Previous avatar"
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border-none bg-[#2a2a27] text-2xl text-white transition hover:bg-[#353531]"
          @click="prev()"
        >
          ‹
        </button>

        <!-- Active avatar -->
        <div class="min-w-0 flex-1">
          <div
            class="relative mx-auto aspect-[4/5] w-full max-w-[180px] overflow-hidden rounded-lg bg-(--kots-background-color)"
          >
            <Transition
              name="avatar"
              mode="out-in"
            >
              <img
                :key="selectedAvatar.id"
                :src="selectedAvatar.image"
                :alt="`${selectedAvatar.name} avatar`"
                class="h-full w-full object-cover"
              />
            </Transition>

            <div
              class="absolute inset-x-0 bottom-0 bg-black/40 px-3 py-2 text-center"
            >
              <p class="text-sm font-semibold text-white">
                {{ selectedAvatar.name }}
              </p>
            </div>
          </div>
        </div>

        <!-- Next button -->
        <button
          type="button"
          aria-label="Next avatar"
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border-none bg-[#2a2a27] text-2xl text-white transition hover:bg-[#353531]"
          @click="next()"
        >
          ›
        </button>
      </div>

      <!-- Pagination -->
      <div class="mt-4 flex flex-wrap items-center justify-center gap-2">
        <button
          v-for="(avatar, index) in avatars"
          :key="avatar.id"
          type="button"
          :aria-label="`Select ${avatar.name}`"
          :aria-pressed="selectedAvatarIndex === index"
          class="h-1.5 rounded-full transition-all"
          :class="
            selectedAvatarIndex === index
              ? 'w-6 bg-cyan-200'
              : 'w-1.5 bg-[#a2a1a6] hover:bg-white'
          "
          @click="selectAvatar(index)"
        ></button>
      </div>
    </section>

    <p class="mt-5 text-xs leading-4 tracking-wide text-[#a2a1a6]">
      Every avatar competes under the same conditions. Your real sleep data
      determines your performance in each automatic battle.
    </p>

    <div class="mt-5 px-5">
      <button
        type="button"
        class="rounded-lg w-full border-none bg-cyan-200 px-[14px] py-2 text-xs text-[#171715] transition hover:bg-cyan-100 "
        @click="onContinue"
      >
        Enter the arena
      </button>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";

.overflow-y-auto {
  overscroll-behavior: contain;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #2a2a27;
  border-radius: 8px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #3a3a36;
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