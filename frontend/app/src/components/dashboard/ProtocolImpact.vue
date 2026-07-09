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
    class="font-inter text-sm text-heading flex-2 min-h-0 bg-(--kots-blocks-color) rounded-xl p-6 overflow-auto"
  >
    <h2 class="text-base font-semibold mb-4 text-main">Protocol Impact</h2>

    <div
      class="grid grid-cols-[120px_1fr_100px] px-2 pb-2 text-xs text-muted border-b border-border/50 font-medium"
    >
      <div>Protocol name</div>
      <div class="text-center">Impact</div>
      <div class="text-right">Days used</div>
    </div>
    <div class="divide-y divide-border/30">
      <div
        v-for="item in protocolImpacts"
        :key="item.id"
        class="grid grid-cols-[120px_1fr_100px] items-center px-2 py-3 text-xs"
      >
        <div class="font-medium text-main truncate pr-2">{{ item.name }}</div>

        <div class="flex items-center gap-3 px-4">
          <span
            :class="[
              'w-12 text-right font-mono',
              item.percentage < 0 ? 'text-red-500 font-semibold' : 'text-muted/30',
            ]"
          >
            {{ item.percentage < 0 ? item.percentage + '%' : '' }}
          </span>

          <div class="relative flex-1 h-3 bg-background rounded-full">
            <div class="absolute left-1/2 top-0 bottom-0 w-[2px] bg-neutral-500/50 z-10"></div>

            <div
              v-if="item.percentage < 0"
              class="absolute top-0 bottom-0 right-1/2 bg-red-500 rounded-l-full transition-all duration-300"
              :style="{ width: Math.min(Math.abs(item.percentage) / 2, 50) + '%' }"
            ></div>

            <div
              v-if="item.percentage > 0"
              class="absolute top-0 bottom-0 left-1/2 bg-emerald-500 rounded-r-full transition-all duration-300"
              :style="{ width: Math.min(item.percentage / 2, 50) + '%' }"
            ></div>
          </div>

          <span
            :class="[
              'w-12 text-left font-mono',
              item.percentage >= 0 ? 'text-emerald-500 font-semibold' : 'text-muted/30',
            ]"
          >
            {{ item.percentage >= 0 ? '+' + item.percentage + '%' : '' }}
          </span>
        </div>

        <div class="text-right text-body font-mono">{{ item.daysUsed }}</div>
      </div>
    </div>
  </div>
</template>
