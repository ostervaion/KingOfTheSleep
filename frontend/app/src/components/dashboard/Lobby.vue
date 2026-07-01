<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as Phaser from 'phaser'

const gameContainer = ref(null)

let game = null
let keyA = null
let keyS = null
let keyD = null
let keyW = null

onMounted(() => {
  game = new Phaser.Game({
    type: Phaser.AUTO,
    parent: gameContainer.value,
    width: 400,
    height: 300,
    backgroundColor: '#222',
    scene: {
      create: create,
      update: update,
    },
  })
})

// preload: preload

function create() {
  this.add.text(50, 50, 'Helo Phaser!', {
    fontSize: '32px',
    color: '#fff',
  })
  keyW = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W)
  keyA = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A)
  keyS = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S)
  keyD = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D)
}

function update() {
  if (keyA.isDown) {
    console.log('A key pressed')
  } else if (keyS.isDown) {
    console.log('S key pressed')
  } else if (keyD.isDown) {
    console.log('D key pressed')
  } else if (keyW.isDown) {
    console.log('W key pressed')
  }
}

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
