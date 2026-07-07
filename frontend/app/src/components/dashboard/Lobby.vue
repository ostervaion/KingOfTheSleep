<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as Phaser from 'phaser'

const gameContainer = ref(null)

let game = null

class LobbyScene extends Phaser.Scene {
  constructor() {
    super('Lobby')
  }

  preload() {
    this.load.image('sheep', 'sheep.webp')
  }

  create() {
    const marker = this.add.image(-100, -100, 'sheep').setScale(0.05)

    this.input.on('pointerdown', (pointer) => {
      this.tweens.add({
        targets: marker,
        x: pointer.x,
        y: pointer.y,
        duration: 500,
        ease: 'Linear',
      })
    })
  }

  update() {}
}

class GameScene extends Phaser.Scene {
  constructor() {
    super('Game')
  }

  create() {
    this.add.text(100, 100, 'Match!')

    this.time.delayedCall(5000, () => {
      this.scene.start('Lobby')
    })
  }
}

onMounted(() => {
  const el = gameContainer.value
  if (!el) return

  game = new Phaser.Game({
    type: Phaser.AUTO,
    parent: gameContainer.value,
    width: el.clientWidth,
    height: el.clientHeight,
    backgroundColor: '#81C784',
    scene: [LobbyScene, GameScene],
  })
})

onUnmounted(() => {
  game?.destroy(true)
})
</script>

<template>
  <div
    class="font-inter text-sm text-heading flex-6 min-h-0 bg-(--kots-blocks-color) p-6 rounded-xl overflow-auto border-b border-[color:var(--border)]"
  >
    <div ref="gameContainer" class="h-full"></div>
  </div>
</template>
