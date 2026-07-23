<script setup>
import { computed, ref } from 'vue'
import api from '@/api/api'

import PerformanceIcon from '@/assets/performance.svg'
import ConsistencyIcon from '@/assets/consistency.svg'
import EfficiencyIcon from '@/assets/efficiency.svg'
import DisturbanceIcon from '@/assets/disturbance.svg'
import TimeInBedIcon from '@/assets/timeInBed.svg'
import AwakeTimeIcon from '@/assets/awakeTime.svg'
import LightSleepIcon from '@/assets/lightSleep.svg'
import SlowWaveIcon from '@/assets/slowWave.svg'
import RemIcon from '@/assets/rem.svg'
import BaselineIcon from '@/assets/baseline.svg'
import DebtIcon from '@/assets/debt.svg'
import StrainIcon from '@/assets/strain.svg'
import NapIcon from '@/assets/lamb_battle.svg'
import RespiratoryRateIcon from '@/assets/lamb_battle.svg'

// step: 1 = sleep data, 2 = protocol selection
const step = ref(1)
const currentSection = ref(0)

const loading = ref(false)
const mensaje = ref('')
const showMessage = ref(false)

const formData = ref({
  timeInBed: 8,
  awakeTime: 1,
  lightSleep: 2,
  slowWave: 3,
  rem: 2,
  disturbance: 15,
  baseline: 8,
  debt: 0,
  strain: 1,
  nap: 0,
  respiratoryRate: 16,
  performance: 80,
  consistency: 85,
  efficiency: 90,
})

const sections = [
  {
    title: 'Sleep Quality',
    fields: ['performance', 'consistency', 'efficiency', 'disturbance'],
  },
  {
    title: 'Sleep Duration',
    fields: ['timeInBed', 'awakeTime', 'lightSleep', 'slowWave', 'rem'],
  },
  {
    title: 'Recovery',
    fields: ['baseline', 'debt', 'strain'],
  },
]

const fieldConfig = [
  { key: 'timeInBed', label: 'Time in Bed', min: 0, max: 12, step: 0.5, unit: 'h' },
  { key: 'awakeTime', label: 'Awake', min: 0, max: 5, step: 0.5, unit: 'h' },
  { key: 'lightSleep', label: 'Light', min: 0, max: 8, step: 0.5, unit: 'h' },
  { key: 'slowWave', label: 'Deep', min: 0, max: 6, step: 0.5, unit: 'h' },
  { key: 'rem', label: 'REM', min: 0, max: 5, step: 0.5, unit: 'h' },
  { key: 'disturbance', label: 'Disturbance', min: 0, max: 20, step: 1, unit: '' },
  { key: 'baseline', label: 'Baseline', min: 0, max: 12, step: 0.5, unit: 'h' },
  { key: 'debt', label: 'Debt', min: -5, max: 5, step: 0.5, unit: 'h' },
  { key: 'strain', label: 'Strain', min: 0, max: 10, step: 1, unit: '' },
  { key: 'nap', label: 'Nap', min: 0, max: 4, step: 0.5, unit: 'h' },
  {
    key: 'respiratoryRate',
    label: 'Respiratory Rate',
    min: 10,
    max: 25,
    step: 1,
    unit: '',
  },
  { key: 'performance', label: 'Performance', min: 0, max: 100, step: 1, unit: '%' },
  { key: 'consistency', label: 'Consistency', min: 0, max: 100, step: 1, unit: '%' },
  { key: 'efficiency', label: 'Efficiency', min: 0, max: 100, step: 1, unit: '%' },
]

const fieldIcons = {
  timeInBed: TimeInBedIcon,
  awakeTime: AwakeTimeIcon,
  lightSleep: LightSleepIcon,
  slowWave: SlowWaveIcon,
  rem: RemIcon,
  disturbance: DisturbanceIcon,
  baseline: BaselineIcon,
  debt: DebtIcon,
  strain: StrainIcon,
  nap: NapIcon,
  respiratoryRate: RespiratoryRateIcon,
  performance: PerformanceIcon,
  consistency: ConsistencyIcon,
  efficiency: EfficiencyIcon,
}

const visibleFields = computed(() =>
  fieldConfig.filter((field) => sections[currentSection.value].fields.includes(field.key)),
)

function getRangeProgress(field) {
  const value = Number(formData.value[field.key])
  const progress = ((value - field.min) / (field.max - field.min)) * 100

  return Math.min(100, Math.max(0, progress))
}

function nextSection() {
  if (currentSection.value < sections.length - 1) {
    currentSection.value += 1
    return
  }

  goToProtocolStep()
}

function previousSection() {
  if (currentSection.value > 0) {
    currentSection.value -= 1
  }
}

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
  currentSection.value = 0
}
</script>

<template>
  <div
    class="font-inter flex h-full min-h-0 w-full min-w-0 flex-6 flex-col overflow-auto rounded-xl border-b border-(--border) shadow-md shadow-black/20 bg-(--kots-blocks-color) p-4 text-sm text-(--text) sm:p-6"
  >
    <form
      v-if="step === 1"
      @submit.prevent="nextSection"
      class="flex min-h-0 w-full min-w-0 flex-1 flex-col"
    >
      <!-- Progress -->
      <div class="shrink-0 space-y-3">
        <div class="flex items-center justify-between gap-3">
          <div>
            <p class="text-[10px] font-medium uppercase tracking-[0.16em] text-yellow-400">
              Step {{ currentSection + 1 }} of {{ sections.length }}
            </p>

            <h3 class="mt-1 text-xl font-semibold">
              {{ sections[currentSection].title }}
            </h3>
          </div>

          <div class="flex items-center justify-center gap-1.5" aria-hidden="true">
            <span
              v-for="(_, index) in sections"
              :key="index"
              class="h-1.5 w-5 rounded-full transition-colors duration-150"
              :class="index <= currentSection ? 'bg-yellow-400' : 'bg-(--border)'"
            ></span>
          </div>
        </div>
      </div>

      <!-- Sleep Duration Section -->
      <!-- Sleep Quality Section -->
      <!-- Performance Section -->
      <div class="flex min-h-0 flex-1 py-4">
        <div class="grid h-full w-full grid-cols-3 items-stretch gap-3 sm:grid-cols-5">
          <label
            v-for="field in visibleFields"
            :key="field.key"
            class="flex min-h-0 min-w-0 flex-col p-3"
          >
            <!-- Label at the top -->
            <span class="min-h-8 shrink-0 text-center text-xs font-medium leading-4 text-zinc-400">
              {{ field.label }}
            </span>

            <div class="mt-2 shrink-0 text-center">
              <span class="text-base font-semibold text-yellow-400">
                {{ formData[field.key] }}{{ field.unit }}
              </span>
            </div>

            <!-- Slider fills the available vertical space -->
            <div class="mt-3 grid min-h-40 flex-1 grid-cols-[1fr_auto_1fr] items-stretch">
              <div
                class="flex h-full flex-col justify-between justify-self-end pr-2 text-[10px] text-(--muted)"
              >
                <span>{{ field.max }}{{ field.unit }}</span>
                <span>{{ field.min }}{{ field.unit }}</span>
              </div>

              <input
                v-model.number="formData[field.key]"
                type="range"
                :min="field.min"
                :max="field.max"
                :step="field.step"
                :aria-label="field.label"
                class="kots-range h-full justify-self-center"
                :style="{
                  '--range-progress': `${getRangeProgress(field)}%`,
                }"
              />

              <div aria-hidden="true"></div>
            </div>

            <!-- Icon at the bottom -->
            <div class="mt-3 flex shrink-0 justify-center">
              <component
                :is="fieldIcons[field.key]"
                class="h-6 w-6 shrink-0 opacity-80"
                aria-hidden="true"
              />
            </div>
          </label>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex shrink-0 flex-wrap gap-3 pt-4">
        <button
          v-if="currentSection > 0"
          type="button"
          @click="previousSection"
          class="min-w-24 flex-1 rounded-lg border border-[color:var(--border)] bg-(--kots-blocks-color) px-4 py-2.5 text-xs font-medium text-(--muted) transition-colors duration-150 hover:bg-(--surface-strong)"
        >
          Back
        </button>

        <button
          type="submit"
          class="min-w-24 flex-1 rounded-lg border border-yellow-400 bg-yellow-400 px-4 py-2.5 text-xs font-semibold text-neutral-950 transition-colors duration-150 hover:bg-yellow-300"
        >
          Next
        </button>
      </div>
    </form>

    <!-- Step 2: Protocol selection -->
    <form
      v-if="step === 2"
      @submit.prevent="submitAll"
      class="flex min-h-0 w-full min-w-0 flex-1 flex-col"
    >
      <div class="shrink-0 space-y-3">
        <h3 class="text-xs font-medium uppercase tracking-wide text-(--muted)">Protocols</h3>

        <p class="text-xs text-(--muted)">Select the protocols you followed today</p>
      </div>

      <div class="flex min-h-0 flex-1 items-center py-6">
        <div class="grid w-full grid-cols-2 gap-2">
          <button
            v-for="protocol in protocolOptions"
            :key="protocol.id"
            type="button"
            @click="toggleProtocol(protocol.id)"
            class="rounded-lg border px-3 py-2.5 text-left text-xs font-medium transition-colors duration-150"
            :class="
              selectedProtocols.includes(protocol.id)
                ? 'border-yellow-400 bg-(--surface-strong) text-(--text)'
                : 'border-[color:var(--border)] bg-(--kots-blocks-color) text-(--muted) hover:bg-(--surface-strong)'
            "
          >
            {{ protocol.label }}
          </button>
        </div>
      </div>

      <transition>
        <p v-if="showMessage" class="shrink-0 pb-3 text-center text-xs text-(--muted)">
          {{ mensaje }}
        </p>
      </transition>

      <div class="flex shrink-0 gap-3 pt-4">
        <button
          type="button"
          @click="backToSleepStep"
          class="flex-1 rounded-lg border border-[color:var(--border)] bg-(--kots-blocks-color) px-4 py-2.5 text-xs font-medium text-(--muted) transition-colors duration-150 hover:bg-(--surface-strong)"
        >
          Back
        </button>

        <button
          type="submit"
          :disabled="loading"
          @click="$emit('saved')"
          class="flex-1 rounded-lg border border-yellow-400 bg-yellow-400 px-4 py-2.5 text-xs font-semibold text-neutral-950 transition-colors duration-150 hover:bg-yellow-300 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ loading ? 'Sending...' : 'Save' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.kots-range {
  --range-progress: 0%;

  -webkit-appearance: none;
  appearance: none;
  writing-mode: vertical-lr;
  direction: rtl;
  width: 5px;
  height: 100%;
  min-height: 160px;
  padding: 0;
  border-radius: 999px;
  outline: none;
  background: linear-gradient(
      to top,
      #facc15 0%,
      #facc15 var(--range-progress),
      var(--border) var(--range-progress),
      var(--border) 100%
    )
    center / 5px 100% no-repeat;
  cursor: pointer;
  touch-action: none;
}

.kots-range:focus-visible {
  outline: 2px solid rgb(250 204 21 / 55%);
  outline-offset: 3px;
}

.kots-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  margin-left: -3%;
  width: 24px;
  height: 12px;
  border: 2px solid var(--kots-blocks-color);
  border-radius: 4px;
  background: #facc15;
  cursor: grab;
  transition:
    transform 150ms ease,
    background-color 150ms ease;
}

.kots-range::-webkit-slider-thumb:hover {
  transform: scale(1.05);
  background: #fde047;
}

.kots-range::-webkit-slider-thumb:active {
  cursor: grabbing;
}

.kots-range::-moz-range-thumb {
  width: 24px;
  height: 14px;
  border: 2px solid var(--kots-blocks-color);
  border-radius: 4px;
  background: #facc15;
  cursor: grab;
  transition:
    transform 150ms ease,
    background-color 150ms ease;
}

.kots-range::-moz-range-thumb:hover {
  transform: scale(1.05);
  background: #fde047;
}

.kots-range::-moz-range-thumb:active {
  cursor: grabbing;
}

.kots-range::-moz-range-track {
  width: 5px;
  height: 100%;
  border: none;
  border-radius: 999px;
  background: transparent;
}

.kots-range::-moz-range-progress {
  background: transparent;
}

.kots-range::-webkit-slider-runnable-track {
  width: 5px;
  height: 100%;
  border: none;
  border-radius: 999px;
  background: transparent;
}

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
