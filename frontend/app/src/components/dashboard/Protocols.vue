<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ThumbsUpIcon from '@/assets/thumbs-up-svgrepo-com.svg'
import ThumbsDownIcon from '@/assets/thumbs-down-svgrepo-com.svg'
import ProtocolCard from '@/components/dashboard/protocolCard.vue'

const selectedRanking = ref('today')
var protocolsUp = ref([])
var protocolsDown = ref([])

onMounted(() => {
  loadProtocols()
})

function loadProtocols() {
  protocolsUp.value = [
    { ranking: '1', protocol: 'Martin', usage: '%30', winrate: '%3' },
    { ranking: '2', protocol: 'Martin', usage: '%30', winrate: '%3' },
    { ranking: '3', protocol: 'Martin', usage: '%30', winrate: '%3' },
    { ranking: '4', protocol: 'Other', usage: '%20', winrate: '%5' },
    { ranking: '5', protocol: 'Another', usage: '%15', winrate: '%8' },
    { ranking: '6', protocol: 'Other', usage: '%20', winrate: '%5' },
    { ranking: '7', protocol: 'Another', usage: '%15', winrate: '%8' },
  ]
    ///llamar a funcion back para tener todos los protocolos y sus datos en descendiente por punto

  protocolsDown.value = [
    { ranking: '1', protocol: 'Other', usage: '%20', winrate: '%5' },
    { ranking: '2', protocol: 'Another', usage: '%15', winrate: '%8' },
    { ranking: '3', protocol: 'Other', usage: '%20', winrate: '%5' },
    { ranking: '4', protocol: 'Another', usage: '%15', winrate: '%8' },
    { ranking: '5', protocol: 'Other', usage: '%20', winrate: '%5' },
    { ranking: '6', protocol: 'Another', usage: '%15', winrate: '%8' },
  ]
    ///llamar a funcion back para tener todos los protocolos y sus datos en descendiente por punto

}

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
      <div class="flex items-center justify-between">
        <div class="border border-cyan-100 rounded-md px-2 py-0.5 text-gray-800 leading-none">
          <h2 class="text-cyan-100 text-sm font-medium text-heading">Protocols</h2>
        </div>
        <div class="flex rounded-full bg-(--kots-background-color) px-1.25 py-0.75">
          <button :class="buttonClass('today')" @click="updateButtonColor('today')">today</button>

          <button :class="buttonClass('week')" @click="updateButtonColor('week')">week</button>

          <button :class="buttonClass('global')" @click="updateButtonColor('global')">
            global
          </button>
        </div>
      </div>
    </div>

    <div class=" grid grid-cols-[40px_1fr_100px_100px] px-6 pb-2 text-xs text-body">
      <div>
        <ThumbsUpIcon class="-mt-0.5 w-5 h-5" />
      </div>
      <div>winning protocols</div>
      <div class="text-right">usage</div>
      <div class="text-right">win rate</div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul>
        <!--poner en la key la id del protocolo, no el nombre -->
        <ProtocolCard
          v-for="protocolup in protocolsUp"
          :key="protocolup.protocol"
          :ranking="protocolup.ranking"
          :name="protocolup.protocol"
          :usage="protocolup.usage"
          :winrate="protocolup.winrate"
        />
      </ul>
    </div>
    <div class="mt-4 grid grid-cols-[40px_1fr_100px_100px] px-6 pb-2 text-xs text-body">
      <div>
        <ThumbsDownIcon class="-mt-0.5 w-5 h-5" />
      </div>
      <div>losing protocols</div>
      <div class="text-right">usage</div>
      <div class="text-right">win rate</div>
    </div>

    <div class="flex-1 min-h-0 overflow-y-auto">
      <ul>
        <ProtocolCard
          v-for="protocoldown in protocolsDown"
          :key="protocoldown.protocol"
          :ranking="protocoldown.ranking"
          :name="protocoldown.protocol"
          :usage="protocoldown.usage"
          :winrate="protocoldown.winrate"
        />
      </ul>
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
