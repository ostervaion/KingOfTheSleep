<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Phaser from 'phaser'
import GameScene from '../../scenes/BattleScene.js'

const gameContainer = ref(null)
let game = null

onMounted(() => {
  const el = gameContainer.value
  if (!el) return

  game = new Phaser.Game({
    type: Phaser.AUTO,
    parent: gameContainer.value,

    width: 360,
    height: 640,

    backgroundColor: '#aaaaaa',

    scale: {
      mode: Phaser.Scale.FIT,
      autoCenter: Phaser.Scale.CENTER_BOTH,
    },

    scene: [GameScene],
  })
})

onUnmounted(() => {
  game?.destroy(true)
  game = null
})
</script>

<template>
  <div class="h-full w-full">
    <div ref="gameContainer" class="h-full w-full"></div>
  </div>
</template>
