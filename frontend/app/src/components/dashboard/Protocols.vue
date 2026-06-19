<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ThumbsUpIcon from '@/assets/thumbs-up-svgrepo-com.svg'
import ThumbsDownIcon from '@/assets/thumbs-down-svgrepo-com.svg'
</script>

<template>
  <div
    class="font-inter flex flex-col flex-1 min-h-0 overflow-hidden rounded-xl bg-(--kots-blocks-color) shadow-md shadow-black/20 border-b border-[color:var(--border)]"
  >
    <div class="px-6 pb-4 pt-4">
      <div class="flex items-center justify-between">
        <div class="border border-cyan-100 rounded-md px-2 py-0.5 text-gray-800 leading-none">
          <h2 class="text-cyan-100 text-sm font-medium text-heading">Protocols</h2>
        </div>
        <div class="flex rounded-full bg-(--kots-background-color) px-1.25 py-0.75">
          <button
            class="rounded-full bg-(--kots-blocks-color) px-3 py-1.5 text-xs font-medium text-white transition"
          >
            today
          </button>

          <button class="rounded-full px-3 py-1.5 text-xs text-body transition hover:text-heading">
            week
          </button>

          <button class="rounded-full px-3 py-1.5 text-xs text-body transition hover:text-heading">
            global
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-[40px_1fr_100px_100px] px-6 pb-2 text-xs text-body">
      <div>
        <ThumbsUpIcon class="-mt-0.5 w-5 h-5" />
      </div>
      <div>protocol</div>
      <div class="text-right">usage</div>
      <div class="text-right">win rate</div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#1</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">DreamWalker</span>
            </div>
            <div class="text-right text-sm text-heading">% 61</div>
            <div class="text-right text-sm font-medium text-green-400">% 85</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#2</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">% 61</div>

            <div class="text-right text-sm font-medium text-green-400">% 35</div>
          </div>
        </li>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#2</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">% 61</div>

            <div class="text-right text-sm font-medium text-green-400">% 35</div>
          </div>
        </li>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#2</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">% 61</div>

            <div class="text-right text-sm font-medium text-green-400">% 35</div>
          </div>
        </li>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#3</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">% 61</div>

            <div class="text-right text-sm font-medium text-green-400">% 35</div>
          </div>
        </li>
      </ul>
    </div>
    <div class="mt-4 grid grid-cols-[40px_1fr_100px_100px] px-6 pb-2 text-xs text-body">
      <div>
        <ThumbsDownIcon class="-mt-0.5 w-5 h-5" />
      </div>
      <div>protocol</div>
      <div class="text-right">usage</div>
      <div class="text-right">win rate</div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#1</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">DreamWalker</span>
            </div>

            <div class="text-right text-sm text-heading">% 24</div>

            <div class="text-right text-sm font-medium text-red-400">% 7</div>
          </div>
        </li>

        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#2</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">% 23</div>

            <div class="text-right text-sm font-medium text-red-400">% 5</div>
          </div>
        </li>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#3</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">% 20</div>

            <div class="text-right text-sm font-medium text-red-400">% 4</div>
          </div>
        </li>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#2</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">% 19</div>

            <div class="text-right text-sm font-medium text-red-400">% 3</div>
          </div>
        </li>
        <li class="odd:bg-white/[0.015] even:bg-transparent">
          <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
            <div class="text-base text-heading">#4</div>

            <div class="flex items-center gap-3">
              <span class="text-sm text-heading">SleepNinja</span>
            </div>

            <div class="text-right text-sm text-heading">% 28</div>

            <div class="text-right text-sm font-medium text-red-400">% 1</div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
<style scoped>
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #333;
}
</style>
