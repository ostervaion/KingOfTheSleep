<script setup>
import { computed } from 'vue'

import {
  Chart as ChartJS,
  Tooltip,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Filler,
} from 'chart.js'

import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement, Tooltip, Filler)

const props = defineProps({
  sleepScore: {
    type: Object,
    default: () => ({
      labels: [],
      scores: [],
    }),
  },
})

const scores = computed(() => props.sleepScore?.scores ?? [])

const latestScore = computed(() => {
  if (!scores.value.length) return 0
  return Math.round(scores.value.at(-1))
})

const scoreChange = computed(() => {
  if (scores.value.length < 2) return 0
  return Math.round(scores.value.at(-1) - scores.value.at(-2))
})

const averageScore = computed(() => {
  if (!scores.value.length) return 0

  const total = scores.value.reduce((sum, score) => sum + Number(score || 0), 0)
  return Math.round(total / scores.value.length)
})

const chartData = computed(() => ({
  labels: props.sleepScore?.labels ?? [],
  datasets: [
    {
      data: scores.value,
      borderColor: '#05df72',
      backgroundColor: (context) => {
        const { chart } = context
        const { ctx, chartArea } = chart

        if (!chartArea) return 'rgba(74, 222, 128, 0.18)'

        const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom)
        gradient.addColorStop(0, 'rgba(74, 222, 128, 0.36)')
        gradient.addColorStop(1, 'rgba(74, 222, 128, 0)')
        return gradient
      },
      fill: true,
      borderWidth: 3,
      tension: 0.38,
      pointRadius: 0,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: '#4ADE80',
      pointHoverBorderColor: '#171715',
      pointHoverBorderWidth: 2,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    intersect: false,
    mode: 'index',
  },
  layout: {
    padding: 0,
  },
  scales: {
    x: {
      display: false,
      border: {
        display: false,
      },
      grid: {
        display: false,
      },
      ticks: {
        display: false,
      },
    },
    y: {
      display: false,
      min: 50,
      max: 100,
      grid: {
        display: false,
      },
    },
  },
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      displayColors: false,
      backgroundColor: '#1B1B19',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
      titleColor: '#A2A1A6',
      bodyColor: '#FFFFFF',
      padding: 10,
      cornerRadius: 8,
      callbacks: {
        label: (context) => `Sleep score: ${context.parsed.y}`,
      },
    },
  },
}
</script>

<template>
  <div
    class="font-inter flex min-h-0 h-full flex-2 flex-col overflow-hidden rounded-xl border-b border-[color:var(--border)] bg-(--kots-blocks-color) shadow-md shadow-black/20"
  >
    <div class="flex items-start justify-between gap-4 px-5 pt-5 sm:px-6 sm:pt-6">
      <div>
        <div class="mb-3 inline-flex rounded-md border border-cyan-200 px-2 py-0.5 leading-none">
          <h2 class="text-heading text-sm font-medium text-cyan-200">Sleep score</h2>
        </div>
      </div>

      <div
        class="flex items-center gap-1 pt-1 text-3xl font-semibold"
        :class="scoreChange >= 0 ? 'text-green-500' : 'text-red-400'"
      >
        <p class="font-inter pb-1 text-xs font-medium text-white">since latest score</p>
        <svg
          class="h-4 w-4"
          :class="scoreChange < 0 ? 'rotate-180' : ''"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 19V6m0 0 4 4m-4-4-4 4"
          />
        </svg>
        {{ Math.abs(scoreChange) }}
      </div>
    </div>

    <div class="relative min-h-0 flex-1">
      <!-- Graph background -->
      <Line class="absolute inset-0 h-full w-full" :data="chartData" :options="chartOptions" />

      <!-- Average overlay -->
      <div
        class="pointer-events-none absolute bottom-5 right-5 z-10 text-right sm:bottom-6 sm:right-6"
      >
        <p class="text-xs font-medium text-[#A2A1A6]">Last 7 days</p>

        <p class="mt-0.5 text-sm font-medium text-white">{{ averageScore }} average</p>
      </div>
    </div>
  </div>
</template>
