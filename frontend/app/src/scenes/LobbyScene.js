import * as Phaser from 'phaser'
import BaseScene from './BaseScene'
import { watch } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
const { lobbyPlayers, sendPayload } = useWebSocket()

const WORLD_WIDTH = 4000
const WORLD_HEIGHT = 4000
let scene = null

watch(lobbyPlayers, (lobbytest) => {
  if (!lobbytest) return
  scene.spawnPlayers(lobbytest)
})

export default class LobbyScene extends BaseScene {
  constructor() {
    super({ key: 'LobbyScene' })
    this.players = {}
    this.lastUpdate = 0
  }

  preload() {
    this.load.image('sheep', 'sheep.webp')
  }

  create() {
    scene = this
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
      }
    })
  }

  update(time) {
    const speed = 150

    const distance = Phaser.Math.Distance.Between(
      this.player.x,
      this.player.y,
      this.target.x,
      this.target.y,
    )

    if (distance < 4) {
      this.player.setVelocity(0, 0)
      this.player.setPosition(this.target.x, this.target.y)
      this.player.setAngle(0)
      return
    }

    this.physics.moveTo(this.player, this.target.x, this.target.y, speed)

    this.player.setFlipX(this.target.x > this.player.x)

    const wiggle = Math.sin(this.time.now * 0.02) * 6
    const tilt = Phaser.Math.Clamp(this.player.body.velocity.y * 0.03, -10, 10)

    this.player.setAngle(tilt + wiggle)

    if (time - this.lastUpdate >= 50) {
      this.lastUpdate = time

      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(
          JSON.stringify({
            type: 'lobby_move',
            user: this.myUsername,
            x: Math.round(this.player.x),
            y: Math.round(this.player.y),
          }),
        )
      }
    }
  }

  spawnPlayers(players) {
    for (const [username, [x, y]] of Object.entries(players)) {
      this.players[username] = this.physics.add.sprite(x, y, 'sheep').setScale(0.05)
    }
  }
}
