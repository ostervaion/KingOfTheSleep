<script setup>
defineProps({
  protocolImpacts: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div
    class="font-inter flex flex-2 min-h-0 min-w-0 w-full flex-col overflow-hidden rounded-xl bg-(--kots-blocks-color) border-b border-[color:var(--border)] shadow-md shadow-black/20"
  >
    <div class="px-6 pb-4 pt-5.5">
      <div class="flex items-center justify-between">
        <div class="border border-cyan-200 rounded-md px-1.5 py-0.5 text-gray-800 leading-none">
          <h2 class="text-cyan-200 text-xs font-medium text-heading">Protocol Impact</h2>
        </div>
        <div class="flex rounded-full px-1.25 text-right">
          <div class="flex rounded-full px-1.25 py-0.75 bg-(--kots-background-color)">
            <button
              @click=""
              class="p5 px-2 py-1 leading-none text-xs font-medium text-white text-heading"
            >
              filter
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      class="grid min-w-0 grid-cols-[minmax(0,1fr)_minmax(0,1.35fr)_52px] items-center gap-2 px-6 pb-2 text-xs text-body sm:grid-cols-[120px_minmax(0,1fr)_100px] sm:gap-4 text-zinc-400"
    >
      <div class="min-w-0 truncate">protocol name</div>
      <div class="min-w-0 text-center">impact</div>
      <div class="text-right">days used</div>
    </div>

    <div class="flex-1 min-h-0 min-w-0 overflow-x-hidden overflow-y-auto bg-white/[0.015] pt-2">
      <div
        v-for="item in protocolImpacts"
        :key="item.id"
        class="grid min-w-0 grid-cols-[minmax(0,1fr)_minmax(0,1.35fr)_52px] items-center gap-2 px-6 py-1.5 text-xs sm:grid-cols-[120px_minmax(0,1fr)_100px] sm:gap-4"
      >
        <div class="min-w-0 truncate pr-1 font-medium text-heading sm:pr-2">
          {{ item.name }}
        </div>

        <div
          class="grid min-w-0 grid-cols-[34px_minmax(0,1fr)_34px] items-center gap-1.5 sm:grid-cols-[48px_minmax(0,1fr)_48px] sm:gap-3"
        >
          <span
            :class="[
              'min-w-0 overflow-hidden whitespace-nowrap text-right text-xs',
              item.percentage < 0 ? 'font-medium text-red-400' : 'text-body/30',
            ]"
          >
            {{ item.percentage < 0 ? item.percentage + '%' : '' }}
          </span>

          <div class="relative h-2 min-w-0 overflow-hidden rounded-full bg-white/10 sm:h-2.5">
            <div
              class="absolute left-1/2 top-[-1px] z-10 h-[calc(100%+2px)] w-[2px] -translate-x-1/2 rounded-full bg-[#171715]"
            ></div>

            <div
              v-if="item.percentage < 0"
              class="absolute right-1/2 top-0 h-full rounded-l-full bg-red-400 transition-all duration-300"
              :style="{ width: Math.min(Math.abs(item.percentage) / 2, 50) + '%' }"
            ></div>

            <div
              v-if="item.percentage > 0"
              class="absolute left-1/2 top-0 h-full rounded-r-full bg-green-400 transition-all duration-300"
              :style="{ width: Math.min(item.percentage / 2, 50) + '%' }"
            ></div>
          </div>

          <span
            :class="[
              'min-w-0 overflow-hidden whitespace-nowrap text-left text-xs',
              item.percentage >= 0 ? 'font-medium text-green-400' : 'text-body/30',
            ]"
          >
            {{ item.percentage >= 0 ? '+' + item.percentage + '%' : '' }}
          </span>
        </div>

        <div class="min-w-0 truncate text-right text-xs text-body">
          {{ item.daysUsed }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@reference "@/assets/main.css";

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
