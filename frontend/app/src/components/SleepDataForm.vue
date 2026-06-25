<script setup>
import { ref } from 'vue'
import api from '@/api/api'

const loading = ref(false)
const mensaje = ref('')
const showMessage = ref(false)

const formData = ref({
  timeInBed: 8,
  awakeTime: 1,
  lightSleep: 2,
  slowWave: 3,
  rem: 2,
  disturbance: 0,
  baseline: 8,
  debt: 0,
  strain: 1,
  nap: 0,
  respiratoryRate: 16,
  performance: 80,
  consistency: 85,
  efficiency: 90,
})

async function submitForm() {
  if (loading.value) return

  loading.value = true
  mensaje.value = ''
  showMessage.value = false

  try {
    const response = await api.post('/sleep-data', {
      time_in_bed: formData.value.timeInBed,
      awake_time: formData.value.awakeTime,
      light_sleep: formData.value.lightSleep,
      slow_wave: formData.value.slowWave,
      rem: formData.value.rem,
      disturbance: formData.value.disturbance,
      baseline: formData.value.baseline,
      debt: formData.value.debt,
      strain: formData.value.strain,
      nap: formData.value.nap,
      respiratory_rate: formData.value.respiratoryRate,
      performance: formData.value.performance,
      consistency: formData.value.consistency,
      efficiency: formData.value.efficiency,
    })

    mensaje.value = '// data saved ✓'
    showMessage.value = true
    setTimeout(() => {
      showMessage.value = false
    }, 3000)
  } catch (error) {
    mensaje.value = '// error saving data'
    showMessage.value = true
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.value = {
    timeInBed: 8,
    awakeTime: 1,
    lightSleep: 2,
    slowWave: 3,
    rem: 2,
    disturbance: 0,
    baseline: 8,
    debt: 0,
    strain: 1,
    nap: 0,
    respiratoryRate: 16,
    performance: 80,
    consistency: 85,
    efficiency: 90,
  }
}
</script>

<template>
  <div
    class="w-full max-w-2xl mx-auto rounded-xl border border-(--border) bg-(--surface-soft) p-6 space-y-6"
  >
    <div>
      <span class="block text-[10px] tracking-[4px] uppercase text-(--accent) mb-4"
        >Sleep Data</span
      >
      <p class="text-xs text-(--muted) tracking-[1px]">Log your sleep information</p>
    </div>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Sleep Duration Section -->
      <div class="space-y-4">
        <h3 class="text-xs tracking-[2px] uppercase text-(--text) font-semibold">Sleep Duration</h3>

        <div class="space-y-3">
          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Time in Bed</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.timeInBed }}h</span>
            </div>
            <input
              v-model.number="formData.timeInBed"
              type="range"
              min="0"
              max="12"
              step="0.5"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Awake Time</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.awakeTime }}h</span>
            </div>
            <input
              v-model.number="formData.awakeTime"
              type="range"
              min="0"
              max="5"
              step="0.5"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Light Sleep</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.lightSleep }}h</span>
            </div>
            <input
              v-model.number="formData.lightSleep"
              type="range"
              min="0"
              max="8"
              step="0.5"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Slow Wave Sleep</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.slowWave }}h</span>
            </div>
            <input
              v-model.number="formData.slowWave"
              type="range"
              min="0"
              max="6"
              step="0.5"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">REM Sleep</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.rem }}h</span>
            </div>
            <input
              v-model.number="formData.rem"
              type="range"
              min="0"
              max="5"
              step="0.5"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>
        </div>
      </div>

      <!-- Sleep Quality Section -->
      <div class="space-y-4">
        <h3 class="text-xs tracking-[2px] uppercase text-(--text) font-semibold">Sleep Quality</h3>

        <div class="space-y-3">
          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Disturbance</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.disturbance }}</span>
            </div>
            <input
              v-model.number="formData.disturbance"
              type="range"
              min="0"
              max="20"
              step="1"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Baseline</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.baseline }}h</span>
            </div>
            <input
              v-model.number="formData.baseline"
              type="range"
              min="0"
              max="12"
              step="0.5"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Debt</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.debt }}h</span>
            </div>
            <input
              v-model.number="formData.debt"
              type="range"
              min="-5"
              max="5"
              step="0.5"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Strain</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.strain }}</span>
            </div>
            <input
              v-model.number="formData.strain"
              type="range"
              min="0"
              max="10"
              step="1"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Nap</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.nap }}h</span>
            </div>
            <input
              v-model.number="formData.nap"
              type="range"
              min="0"
              max="4"
              step="0.5"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>
        </div>
      </div>

      <!-- Performance Section -->
      <div class="space-y-4">
        <h3 class="text-xs tracking-[2px] uppercase text-(--text) font-semibold">Performance</h3>

        <div class="space-y-3">
          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Respiratory Rate</span>
              <span class="text-sm font-semibold text-(--accent)">{{
                formData.respiratoryRate
              }}</span>
            </div>
            <input
              v-model.number="formData.respiratoryRate"
              type="range"
              min="10"
              max="25"
              step="1"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Performance</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.performance }}%</span>
            </div>
            <input
              v-model.number="formData.performance"
              type="range"
              min="0"
              max="100"
              step="1"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Consistency</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.consistency }}%</span>
            </div>
            <input
              v-model.number="formData.consistency"
              type="range"
              min="0"
              max="100"
              step="1"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-2">
              <span class="text-xs tracking-[1px] text-(--muted) uppercase">Efficiency</span>
              <span class="text-sm font-semibold text-(--accent)">{{ formData.efficiency }}%</span>
            </div>
            <input
              v-model.number="formData.efficiency"
              type="range"
              min="0"
              max="100"
              step="1"
              class="w-full h-2 bg-(--surface) rounded-lg appearance-none cursor-pointer accent-(--accent)"
            />
          </label>
        </div>
      </div>

      <!-- Message -->
      <transition>
        <p v-if="showMessage" class="text-sm tracking-[1px] text-(--muted) text-center">
          {{ mensaje }}
        </p>
      </transition>

      <!-- Buttons -->
      <div class="flex gap-3 pt-4">
        <button
          type="submit"
          :disabled="loading"
          class="flex-1 rounded-2xl border border-(--accent) bg-(--surface-soft) px-4 py-3 text-sm font-semibold uppercase tracking-[2px] text-(--accent) hover:bg-(--surface) transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? '// sending...' : '▶ Save' }}
        </button>
        <button
          type="button"
          @click="resetForm"
          class="flex-1 rounded-2xl border border-(--muted) bg-(--surface-soft) px-4 py-3 text-sm font-semibold uppercase tracking-[2px] text-(--muted) hover:bg-(--surface) transition-colors duration-150"
        >
          ↻ Reset
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* Custom range input styling */
input[type='range'] {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 4px;
  outline: none;
}

input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent, #00d9ff);
  cursor: pointer;
  transition: all 150ms ease;
  box-shadow: 0 2px 4px rgba(0, 217, 255, 0.3);
}

input[type='range']::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 12px rgba(0, 217, 255, 0.6);
}

input[type='range']::-webkit-slider-thumb:active {
  transform: scale(1.1);
}

input[type='range']::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent, #00d9ff);
  cursor: pointer;
  border: none;
  transition: all 150ms ease;
  box-shadow: 0 2px 4px rgba(0, 217, 255, 0.3);
}

input[type='range']::-moz-range-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 12px rgba(0, 217, 255, 0.6);
}

input[type='range']::-moz-range-thumb:active {
  transform: scale(1.1);
}

input[type='range']::-moz-range-track {
  background: transparent;
  border: none;
}

input[type='range']::-webkit-slider-runnable-track {
  background: transparent;
  border: none;
}
</style>
