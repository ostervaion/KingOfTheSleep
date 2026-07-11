<script setup>
import { ref } from 'vue'
import api from '@/api/api'

// step: 1 = sleep data, 2 = protocol selection
const step = ref(1)

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

// Lista fija de protocolos (genérica, ajustable después)
const protocolOptions = [
  { id: 'no_caffeine', label: 'No caffeine after 2pm' },
  { id: 'no_screens', label: 'No screens before bed' },
  { id: 'consistent_schedule', label: 'Consistent sleep schedule' },
  { id: 'meditation', label: 'Meditation' },
  { id: 'reading', label: 'Reading before bed' },
  { id: 'cold_room', label: 'Cold room temperature' },
  { id: 'exercise', label: 'Exercise during the day' },
  { id: 'blue_light', label: 'Blue light blocking glasses' },
]

const selectedProtocols = ref([])

function toggleProtocol(id) {
  const idx = selectedProtocols.value.indexOf(id)
  if (idx === -1) {
    selectedProtocols.value.push(id)
  } else {
    selectedProtocols.value.splice(idx, 1)
  }
}

function goToProtocolStep() {
  step.value = 2
}

function backToSleepStep() {
  step.value = 1
}

async function submitAll() {
  if (loading.value) return

  loading.value = true
  mensaje.value = ''
  showMessage.value = false

  try {
    await api.post('/sleep-data', {
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

    await api.post('/protocol', {
      protocols: selectedProtocols.value,
    })

    mensaje.value = 'Data saved'
    showMessage.value = true
    step.value = 1
    resetForm()
    selectedProtocols.value = []
    setTimeout(() => {
      showMessage.value = false
    }, 3000)
  } catch (error) {
    mensaje.value = 'Error saving data'
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
    class="font-inter text-sm text-(--text) flex-6 min-h-0 bg-(--kots-blocks-color) p-6 rounded-xl overflow-auto border-[color:var(--border)] border"
  >
    <div class="mb-4">
      <h2 class="text-sm font-semibold text-(--text)">Sleep Data</h2>
      <p class="text-xs text-(--muted)">Log your sleep information</p>
    </div>

    <form v-if="step === 1" @submit.prevent="goToProtocolStep" class="space-y-6">
      <!-- Sleep Duration Section -->
      <div class="space-y-3">
        <h3 class="text-xs font-medium text-(--muted) uppercase tracking-wide">Sleep Duration</h3>

        <div class="space-y-3">
          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Time in Bed</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.timeInBed }}h</span>
            </div>
            <input
              v-model.number="formData.timeInBed"
              type="range"
              min="0"
              max="12"
              step="0.5"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Awake Time</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.awakeTime }}h</span>
            </div>
            <input
              v-model.number="formData.awakeTime"
              type="range"
              min="0"
              max="5"
              step="0.5"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Light Sleep</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.lightSleep }}h</span>
            </div>
            <input
              v-model.number="formData.lightSleep"
              type="range"
              min="0"
              max="8"
              step="0.5"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Slow Wave Sleep</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.slowWave }}h</span>
            </div>
            <input
              v-model.number="formData.slowWave"
              type="range"
              min="0"
              max="6"
              step="0.5"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">REM Sleep</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.rem }}h</span>
            </div>
            <input
              v-model.number="formData.rem"
              type="range"
              min="0"
              max="5"
              step="0.5"
              class="kots-range"
            />
          </label>
        </div>
      </div>

      <!-- Sleep Quality Section -->
      <div class="space-y-3">
        <h3 class="text-xs font-medium text-(--muted) uppercase tracking-wide">Sleep Quality</h3>

        <div class="space-y-3">
          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Disturbance</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.disturbance }}</span>
            </div>
            <input
              v-model.number="formData.disturbance"
              type="range"
              min="0"
              max="20"
              step="1"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Baseline</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.baseline }}h</span>
            </div>
            <input
              v-model.number="formData.baseline"
              type="range"
              min="0"
              max="12"
              step="0.5"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Debt</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.debt }}h</span>
            </div>
            <input
              v-model.number="formData.debt"
              type="range"
              min="-5"
              max="5"
              step="0.5"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Strain</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.strain }}</span>
            </div>
            <input
              v-model.number="formData.strain"
              type="range"
              min="0"
              max="10"
              step="1"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Nap</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.nap }}h</span>
            </div>
            <input
              v-model.number="formData.nap"
              type="range"
              min="0"
              max="4"
              step="0.5"
              class="kots-range"
            />
          </label>
        </div>
      </div>

      <!-- Performance Section -->
      <div class="space-y-3">
        <h3 class="text-xs font-medium text-(--muted) uppercase tracking-wide">Performance</h3>

        <div class="space-y-3">
          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Respiratory Rate</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.respiratoryRate }}</span>
            </div>
            <input
              v-model.number="formData.respiratoryRate"
              type="range"
              min="10"
              max="25"
              step="1"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Performance</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.performance }}%</span>
            </div>
            <input
              v-model.number="formData.performance"
              type="range"
              min="0"
              max="100"
              step="1"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Consistency</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.consistency }}%</span>
            </div>
            <input
              v-model.number="formData.consistency"
              type="range"
              min="0"
              max="100"
              step="1"
              class="kots-range"
            />
          </label>

          <label class="block">
            <div class="flex justify-between mb-1.5">
              <span class="text-xs text-(--muted)">Efficiency</span>
              <span class="text-xs font-medium text-(--text)">{{ formData.efficiency }}%</span>
            </div>
            <input
              v-model.number="formData.efficiency"
              type="range"
              min="0"
              max="100"
              step="1"
              class="kots-range"
            />
          </label>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex gap-3 pt-2">
        <button
          type="submit"
          class="flex-1 rounded-lg border-[color:var(--border)] border bg-(--kots-blocks-color) px-4 py-2.5 text-xs font-medium text-(--text) hover:bg-(--surface-strong) transition-colors duration-150"
        >
          Next
        </button>
        <button
          type="button"
          @click="resetForm"
          class="flex-1 rounded-lg border-[color:var(--border)] border bg-(--kots-blocks-color) px-4 py-2.5 text-xs font-medium text-(--muted) hover:bg-(--surface-strong) transition-colors duration-150"
        >
          Reset
        </button>
      </div>
    </form>

    <!-- Step 2: Protocol selection -->
    <form v-if="step === 2" @submit.prevent="submitAll" class="space-y-6">
      <div class="space-y-3">
        <h3 class="text-xs font-medium text-(--muted) uppercase tracking-wide">Protocols</h3>
        <p class="text-xs text-(--muted)">Select the protocols you followed today</p>

        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="protocol in protocolOptions"
            :key="protocol.id"
            type="button"
            @click="toggleProtocol(protocol.id)"
            class="text-left rounded-lg border px-3 py-2.5 text-xs font-medium transition-colors duration-150"
            :class="
              selectedProtocols.includes(protocol.id)
                ? 'border-[color:var(--text)] bg-(--surface-strong) text-(--text)'
                : 'border-[color:var(--border)] bg-(--kots-blocks-color) text-(--muted) hover:bg-(--surface-strong)'
            "
          >
            {{ protocol.label }}
          </button>
        </div>
      </div>
      <transition>
        <p v-if="showMessage" class="text-xs text-(--muted) text-center">
          {{ mensaje }}
        </p>
      </transition>
      <div class="flex gap-3 pt-2">
        <button
          type="submit"
          :disabled="loading"
          @click="$emit('saved')"
          class="flex-1 rounded-lg border-[color:var(--border)] border bg-(--kots-blocks-color) px-4 py-2.5 text-xs font-medium text-(--text) hover:bg-(--surface-strong) transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Sending...' : 'Save' }}
        </button>
        <button
          type="button"
          @click="backToSleepStep"
          class="flex-1 rounded-lg border-[color:var(--border)] border bg-(--kots-blocks-color) px-4 py-2.5 text-xs font-medium text-(--muted) hover:bg-(--surface-strong) transition-colors duration-150"
        >
          Back
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.kots-range {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 4px;
  border-radius: 4px;
  outline: none;
  background: var(--border);
}

.kots-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--text);
  cursor: pointer;
  transition: transform 150ms ease;
}

.kots-range::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.kots-range::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--text);
  cursor: pointer;
  border: none;
  transition: transform 150ms ease;
}

.kots-range::-moz-range-thumb:hover {
  transform: scale(1.15);
}

.kots-range::-moz-range-track {
  background: transparent;
  border: none;
}

.kots-range::-webkit-slider-runnable-track {
  background: transparent;
  border: none;
}
</style>