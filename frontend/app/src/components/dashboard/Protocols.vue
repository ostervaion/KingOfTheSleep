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
    class="font-inter text-sm text-heading flex-1 min-h-0 bg-(--kots-blocks-color) p-6 rounded-xl overflow-auto"
  >
    Protocols
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
