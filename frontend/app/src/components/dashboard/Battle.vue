<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as Phaser from 'phaser'

import LobbyScene from '@/scenes/LobbyScene'
import GameScene from '@/scenes/BattleScene'

const gameContainer = ref(null)

let game = null

onMounted(() => {
  const el = gameContainer.value
  if (!el) return

  game = new Phaser.Game({
    type: Phaser.AUTO,
    parent: gameContainer.value,
    width: el.clientWidth,
    height: el.clientHeight,
    pixelArt: true,
    backgroundColor: '#81C784',
    physics: {
      default: 'arcade',
      arcade: {
        debug: false,
      },
    },
    scene: [LobbyScene, GameScene],
  })
})

onUnmounted(() => {
  game?.destroy(true)
  game = null
})
</script>

<template>
  <div
    class="font-inter text-sm text-heading flex-6 min-h-0 bg-(--kots-blocks-color) p-6 rounded-xl overflow-auto border-b border-[color:var(--border)]"
  >
    <div ref="gameContainer" class="h-full"></div>
  </div>
</template>
