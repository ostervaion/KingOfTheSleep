<script setup>
import { computed, ref } from 'vue'
import ThumbsUpIcon from '@/assets/thumbs-up-svgrepo-com.svg'
import ThumbsDownIcon from '@/assets/thumbs-down-svgrepo-com.svg'
import ProtocolCard from '@/components/dashboard/protocolCard.vue'

const props = defineProps({
  protocolsData: {
    type: Object,
    default: () => ({
      winner_protocols: [],
      loser_protocols: [],
    }),
  },
})

const selectedRanking = ref('today')

function formatWinrate(value) {
  const number = Number(value)

  if (!Number.isFinite(number)) return '0%'

  return `${(number * 100).toFixed(1).replace('.0', '')}%`
}

function normalizeProtocols(protocols) {
  if (!Array.isArray(protocols)) return []

  return protocols.map((protocol, index) => ({
    ranking: protocol?.ranking ?? index + 1,
    protocol: protocol?.protocol ?? 'Unknown protocol',
    usage: protocol?.usage ?? 0,
    winrate: formatWinrate(protocol?.winrate),
  }))
}

const protocolsUp = computed(() => normalizeProtocols(props.protocolsData?.winner_protocols))

const protocolsDown = computed(() => normalizeProtocols(props.protocolsData?.loser_protocols))

function updateButtonColor(ranking) {
  selectedRanking.value = ranking
}

function buttonClass(ranking) {
  return {
    clickedButton: selectedRanking.value === ranking,
    unclickedButton: selectedRanking.value !== ranking,
  }
}
</script>

<template>
  <div
    class="font-inter flex flex-col flex-1 min-h-0 overflow-hidden rounded-xl bg-(--kots-blocks-color) shadow-md shadow-black/20 border-b border-[color:var(--border)]"
  >
    <div class="px-6 pb-4 pt-4">
      <div class="flex py-0.75 items-center justify-between">
        <div class="border border-cyan-200 rounded-md px-1.5 py-0.5 text-gray-800 leading-none">
          <h2 class="text-cyan-200 text-xs font-medium text-heading">Protocols</h2>
        </div>
        <div class="hidden flex rounded-full bg-(--kots-background-color) px-1.25 py-0.75">
          <button :class="buttonClass('today')" @click="updateButtonColor('today')">today</button>

          <button :class="buttonClass('week')" @click="updateButtonColor('week')">week</button>

          <button :class="buttonClass('global')" @click="updateButtonColor('global')">
            global
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-[40px_1fr_100px_100px] px-6 pb-2 text-xs text-body text-zinc-400">
      <div>
        <ThumbsUpIcon class="-mt-0.5 w-5 h-5" />
      </div>
      <div>winning protocols</div>
      <div class="text-right">usage</div>
      <div class="text-right">win rate</div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul v-if="protocolsUp.length > 0">
        <!--poner en la key la id del protocolo, no el nombre -->
        <ProtocolCard
          v-for="protocolup in protocolsUp"
          :key="`winner-${protocolup.ranking}-${protocolup.protocol}`"
          type="winner"
          :ranking="protocolup.ranking"
          :name="protocolup.protocol"
          :usage="protocolup.usage"
          :winrate="protocolup.winrate"
        />
      </ul>
        <div v-else class="flex h-full items-center justify-center text-xs text-zinc-400">
          No data yet
      </div>
    </div>
    <div
      class="mt-4 grid grid-cols-[40px_1fr_100px_100px] px-6 pb-2 text-xs text-body text-zinc-400"
    >
      <div>
        <ThumbsDownIcon class="-mt-0.5 w-5 h-5" />
      </div>
      <div>losing protocols</div>
      <div class="text-right">usage</div>
      <div class="text-right">win rate</div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul v-if="protocolsDown.length > 0">
        <ProtocolCard
          v-for="protocoldown in protocolsDown"
          :key="`loser-${protocoldown.ranking}-${protocoldown.protocol}`"
          type="loser"
          :ranking="protocoldown.ranking"
          :name="protocoldown.protocol"
          :usage="protocoldown.usage"
          :winrate="protocoldown.winrate"
        />
      </ul>
        <div v-else class="flex h-full items-center justify-center text-xs text-zinc-400">
          No data yet
      </div>
    </div>
  </div>
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
