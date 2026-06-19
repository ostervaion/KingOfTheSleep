<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Phaser from 'phaser'

const gameContainer = ref(null)

let game

onMounted(() => {
  game = new Phaser.Game({
    type: Phaser.AUTO,
    parent: gameContainer.value,
    width: 400,
    height: 300,
    backgroundColor: '#222',
    scene: {
      create() {
        this.add.text(50, 50, 'Hello Phaser!', {
          fontSize: '32px',
          color: '#fff'
        })
      }
    }
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
    <div ref="gameContainer"></div>
  </div>
</template>