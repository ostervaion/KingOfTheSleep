<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const protocolImpacts = ref([
  { id: 1, name: 'Temperature Cycling', percentage: 145, daysUsed: 120 }, // Over 100% test
  { id: 2, name: 'Light Management', percentage: -25, daysUsed: 85 },
  { id: 3, name: 'Stimulant Control', percentage: 75, daysUsed: 210 },
  { id: 4, name: 'Magnesium Intake', percentage: -180, daysUsed: 45 }, // Under -100% test
  { id: 5, name: 'Melatonin Intake', percentage: 12, daysUsed: 300 },
  { id: 6, name: 'Sex Intake', percentage: -1250, daysUsed: 2 },
  { id: 7, name: 'Sunlight maxing', percentage: 20, daysUsed: 120 },
  { id: 8, name: 'Caffeine minimum', percentage: -10, daysUsed: 340 },
  { id: 9, name: 'Caffeine minimum', percentage: -10, daysUsed: 340 },
  { id: 10, name: 'Caffeine minimum', percentage: -10, daysUsed: 340 },
  { id: 11, name: 'Caffeine minimum', percentage: -10, daysUsed: 340 }
])
</script>

<template>
  <div class="font-inter text-sm text-heading flex-2 min-h-0 bg-(--kots-blocks-color) rounded-xl p-6 overflow-auto">
    <h2 class="text-base font-semibold mb-4 text-main">Protocol Impact</h2>
    
    <div class="grid grid-cols-[120px_1fr_100px] px-2 pb-2 text-xs text-muted border-b border-border/50 font-medium">
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
          <span :class="['w-12 text-right font-mono', item.percentage < 0 ? 'text-red-500 font-semibold' : 'text-muted/30']">
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

          <span :class="['w-12 text-left font-mono', item.percentage >= 0 ? 'text-emerald-500 font-semibold' : 'text-muted/30']">
            {{ item.percentage >= 0 ? '+' + item.percentage + '%' : '' }}
          </span>
        </div>

        <div class="text-right text-body font-mono">{{ item.daysUsed }}</div>
      </div>
    </div>
  </div>
</template>