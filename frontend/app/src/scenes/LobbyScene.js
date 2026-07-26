import * as Phaser from 'phaser'
import BaseScene from './BaseScene'

const WORLD_WIDTH = 4000
const WORLD_HEIGHT = 4000

export default class LobbyScene extends BaseScene {
  constructor() {
    super({ key: 'LobbyScene' })
  }

  preload() {
    this.load.image('sheep', 'sheep.webp')
  }

  create() {
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

  update() {
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
      return
    }

    this.physics.moveTo(this.player, this.target.x, this.target.y, speed)
  }
}
