<script setup>
import {
  Chart as ChartJS,
  Tooltip,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement, Tooltip)

const chartData = {
  labels: ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SUN'],
  datasets: [
    {
      data: [75, 80, 70, 90, 73, 80],
      borderColor: 'rgba(104, 166, 43, 1)',
      backgroundColor: 'rgba(104, 166, 43, 1)',
      pointStyle: 'circle',
      pointRadius: 8,
      pointHoverRadius: 15,
    },
  ],
}

const chartOptions = {
  responsive: true,
  scales: {
    x: {
      border: {
        color: '#ffffff',
        width: 1,
      },
      ticks: {
        color: '#ffffff',
        padding: 12,
        font: {
          size: 12,
          weight: '500',
        },
      },
    },
    y: {
      max: 100,
      min: 0,
      border: {
        color: '#ffffff',
        width: 1,
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.1)',
        drawBorder: true,
      },
      ticks: {
        stepSize: 25,
        color: '#ffffff',
        padding: 16,
        font: {
          size: 12,
          weight: '500',
        },
      },
    },
  },
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#ffffff',
      },
    },
  },
}
</script>

<template>
  <div class="flex-2 min-h-0 bg-(--surface) border border-(--border) rounded-xl p-6">
    <div class="flex h-full min-h-0 flex-col">
      <p class="mb-4 text-lg font-semibold">Sleep Score</p>
      <div class="flex-1 min-h-0">
        <Line class="h-full w-full" :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>
