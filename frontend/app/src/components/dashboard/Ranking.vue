<script setup>
import { computed, nextTick, ref } from 'vue'
import OtherProfiles from '@/components/dashboard/otherProfiles.vue'
import TriangleUp from '@/assets/triangle-up.svg'
import TriangleDown from '@/assets/triangle-down.svg'
import example from '@/assets/example.jpg'

const props = defineProps({
  rankingData: {
    type: Array,
    default: () => [],
  },
})

const selectedRanking = ref('today')
const selectedUser = ref(null)
const profileDialog = ref(null)

const usersRanking = computed(() => {
  return Array.isArray(props.rankingData) ? props.rankingData : []
})

function updateButtonColor(ranking) {
  selectedRanking.value = ranking
}

function buttonClass(ranking) {
  return {
    clickedButton: selectedRanking.value === ranking,
    unclickedButton: selectedRanking.value !== ranking,
  }
}

function getUsername(user) {
  return user?.username || user?.name || 'Unknown player'
}

function getRank(user) {
  return user?.ranking ?? user?.rank ?? '-'
}

function getPoints(user) {
  return user?.points ?? 0
}

function getExperience(user) {
  return user?.experience ?? 0
}

function getPositionChange(user) {
  const value = Number(user?.posChange)

  if (!Number.isFinite(value)) {
    return user?.posChange ?? '-'
  }

  return Math.abs(value)
}

function resolveAvatarPath(path) {
  if (!path || path === 'None' || path === 'null') {
    return example
  }

  if (
    path.startsWith('http://') ||
    path.startsWith('https://') ||
    path.startsWith('data:') ||
    path.startsWith('blob:')
  ) {
    return path
  }

  if (path.startsWith('/api/')) {
    return path
  }

  if (path.startsWith('/')) {
    return `/api${path}`
  }

  return `/api/${path}`
}

function getAvatar(user) {
  return resolveAvatarPath(user?.avatar_path || user?.profilePicture || '')
}

function getTrend(user) {
  if (user?.trend === 'up' || user?.trend === 'down') {
    return user.trend
  }

  const change = Number(user?.posChange)

  if (!Number.isFinite(change) || change === 0) {
    return 'same'
  }

  return change > 0 ? 'up' : 'down'
}

function profileFromRankingUser(user) {
  return {
    username: getUsername(user),
    profilePicture: getAvatar(user),
    rank: getRank(user),
    points: getPoints(user),
    experience: getExperience(user),
  }
}

async function openProfile(user) {
  selectedUser.value = profileFromRankingUser(user)

  await nextTick()

  if (profileDialog.value && !profileDialog.value.open) {
    profileDialog.value.showModal()
  }
}

function closeProfile() {
  if (profileDialog.value?.open) {
    profileDialog.value.close()
  }

  selectedUser.value = null
}

function handleDialogClose() {
  selectedUser.value = null
}
</script>

<template>
  <div
    class="font-inter flex min-h-0 flex-1 flex-col overflow-hidden rounded-xl border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20"
  >
    <div class="px-6 pb-4 pt-4">
      <div class="flex items-center justify-between py-0.75">
        <div
          class="rounded-md border border-cyan-200 px-1.5 py-0.5 leading-none text-gray-800"
        >
          <h2 class="text-heading text-xs font-medium text-cyan-200">Rankings</h2>
        </div>

        <div class="hidden rounded-full bg-(--kots-background-color) px-1.25 py-0.75">
          <button
            type="button"
            :class="buttonClass('today')"
            @click="updateButtonColor('today')"
          >
            today
          </button>

          <button
            type="button"
            :class="buttonClass('week')"
            @click="updateButtonColor('week')"
          >
            week
          </button>

          <button
            type="button"
            :class="buttonClass('global')"
            @click="updateButtonColor('global')"
          >
            global
          </button>
        </div>
      </div>
    </div>

    <div
      class="grid grid-cols-[40px_minmax(0,1fr)_100px_100px] px-6 pb-2 text-xs text-zinc-400"
    >
      <div>#</div>
      <div>player</div>
      <div class="text-right">points</div>
      <div class="text-right">change</div>
    </div>

    <div class="min-h-0 flex-1 overflow-y-auto">
      <ul v-if="usersRanking.length > 0">
        <li
          v-for="user in usersRanking"
          :key="user.id ?? getUsername(user)"
          class="border-t border-white/5"
        >
          <button
            type="button"
            class="grid w-full grid-cols-[40px_minmax(0,1fr)_100px_100px] items-center px-6 py-3 text-left transition hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-cyan-200"
            @click="openProfile(user)"
          >
            <span class="text-sm text-zinc-400">
              {{ getRank(user) }}
            </span>

            <span class="flex min-w-0 items-center gap-3">
              <img
                :src="getAvatar(user)"
                :alt="`${getUsername(user)} profile picture`"
                class="h-8 w-8 shrink-0 rounded-full object-cover"
              />

              <span class="truncate text-sm font-medium text-white">
                {{ getUsername(user) }}
              </span>
            </span>

            <span class="text-right text-sm text-white">
              {{ getPoints(user) }}
            </span>

            <span
              class="flex items-center justify-end gap-1 text-sm"
              :class="{
                'text-emerald-300': getTrend(user) === 'up',
                'text-red-300': getTrend(user) === 'down',
                'text-zinc-400': getTrend(user) === 'same',
              }"
            >
              <span
                v-if="getTrend(user) === 'up'"
                aria-hidden="true"
                class="ranking-arrow"
                :style="{
                  maskImage: `url(${TriangleUp})`,
                  WebkitMaskImage: `url(${TriangleUp})`,
                }"
              />

              <span
                v-else-if="getTrend(user) === 'down'"
                aria-hidden="true"
                class="ranking-arrow"
                :style="{
                  maskImage: `url(${TriangleDown})`,
                  WebkitMaskImage: `url(${TriangleDown})`,
                }"
              />

              <span v-else>—</span>

              <span v-if="getTrend(user) !== 'same'">
                {{ getPositionChange(user) }}
              </span>
            </span>
          </button>
        </li>
      </ul>

      <div
        v-else
        class="flex h-full items-center justify-center text-xs text-zinc-400"
      >
        No data yet
      </div>
    </div>
  </div>

  <!--
    Solo existe un OtherProfiles para todo el ranking.
    Además, se monta únicamente cuando el usuario abre un perfil.
  -->
  <dialog
    ref="profileDialog"
    class="m-auto w-[min(92vw,560px)] max-w-none overflow-visible bg-transparent p-0 backdrop:bg-black/70"
    @close="handleDialogClose"
    @cancel.prevent="closeProfile"
    @click.self="closeProfile"
  >
    <OtherProfiles
      v-if="selectedUser"
      :user="selectedUser"
      @close="closeProfile"
    />
  </dialog>
</template>

<style scoped>
@reference "@/assets/main.css";

.clickedButton {
  @apply rounded-full px-3 py-1.5 text-xs font-medium text-white transition;
  background-color: var(--kots-blocks-color);
}

.unclickedButton {
  @apply rounded-full px-3 py-1.5 text-xs font-medium text-white transition;
  background-color: var(--kots-background-color);
}

.ranking-arrow {
  display: inline-block;
  width: 0.8rem;
  height: 0.8rem;
  flex-shrink: 0;
  background-color: currentColor;
  mask-position: center;
  mask-repeat: no-repeat;
  mask-size: contain;
  -webkit-mask-position: center;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-size: contain;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.3);
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #333;
}
</style>