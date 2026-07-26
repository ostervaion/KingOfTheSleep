import * as Phaser from 'phaser'
import BaseScene from './BaseScene'
import { watch } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
const { myUsername, lobbyPlayers, onlineUsers, sendPayload } = useWebSocket()

const WORLD_WIDTH = 4000
const WORLD_HEIGHT = 4000
let scene = null

watch(
  lobbyPlayers,
  (players) => {
    scene.spawnPlayers(players)
  },
  { deep: true },
)

watch(
  onlineUsers,
  (online) => {
    if (!scene) return
    for (const username of Object.keys(scene.players)) {
      if (!online.has(username)) {
        console.log('sheep logged out', username)
        scene.players[username].sprite.destroy()
        delete scene.players[username]
      }
    }
  },
  { deep: true },
)

export default class LobbyScene extends BaseScene {
  constructor() {
    super({ key: 'LobbyScene' })
  }

  preload() {
    this.load.image('sheep', 'sheep.webp')
  }

  create() {
    scene = this
    this.players = {}
    sendPayload('get_lobby_players')
    this.input.mouse.disableContextMenu()
    this.physics.world.setBounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
    this.cameras.main.setBounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
    this.player = this.physics.add
      .sprite(2000, 2000, 'sheep')
      .setScale(0.05)
      .setCollideWorldBounds(true)
    this.cameras.main.startFollow(this.player)

    this.target = new Phaser.Math.Vector2(this.player.x, this.player.y)

    this.input.on('pointerdown', (pointer) => {
      if (pointer.rightButtonDown()) {
        this.switchScene('GameScene')
      } else {
        this.target.set(pointer.worldX, pointer.worldY)
        console.log('sending', this.target)
        sendPayload('lobby_move', {
          x: Math.round(this.target.x),
          y: Math.round(this.target.y),
        })
      }
    })
  }

  update() {
    this.moveAndWiggle(this.player, this.target)

    for (const remote of Object.values(this.players)) {
      this.moveAndWiggle(remote.sprite, remote.target)
    }
  }

  spawnPlayers(players) {
    for (const [username, [x, y]] of Object.entries(players)) {
      if (username == myUsername.value) continue

      const existing = this.players[username]
      if (!existing || !existing.sprite.active) {
        console.log('new sheep', username)
        this.players[username] = {
          sprite: this.physics.add.sprite(x, y, 'sheep').setScale(0.05),
          target: new Phaser.Math.Vector2(x, y),
        }
      } else {
        console.log('sheep move', username, existing.target)
        existing.target.set(x, y)
      }
    }
  }

  moveAndWiggle(sprite, target) {
    const speed = 150

    const distance = Phaser.Math.Distance.Between(sprite.x, sprite.y, target.x, target.y)

    if (distance < 4) {
      sprite.setVelocity(0, 0)
      sprite.setPosition(target.x, target.y)
      sprite.setAngle(0)
      return
    }

    this.physics.moveTo(sprite, target.x, target.y, speed)

    sprite.setFlipX(target.x > sprite.x)

    const wiggle = Math.sin(this.time.now * 0.02) * 6
    const tilt = Phaser.Math.Clamp(sprite.body.velocity.y * 0.03, -10, 10)

    sprite.setAngle(tilt + wiggle)
  }
}
