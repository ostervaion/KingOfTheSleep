import Phaser, { LEFT } from 'phaser'
import Character from '../Character.js'
import BaseScene from './BaseScene.js'

export default class GameScene extends BaseScene {
  constructor() {
    super({ key: 'GameScene' })
  }
  preload() {
    this.load.audio('moveSfx', 'gameAssets/move.ogg')
    this.load.audio('attackSfx', 'gameAssets/regular_attack.ogg')
    this.load.audio('lastHitSfx', 'gameAssets/last_hit.ogg')
    this.load.spritesheet('playerIdle', 'gameAssets/Idle.png', {
      frameWidth: 78,
      frameHeight: 58,
    })

    this.load.spritesheet('playerAttack', 'gameAssets/Attack.png', {
      frameWidth: 78,
      frameHeight: 58,
    })

    this.load.spritesheet('playerRun', 'gameAssets/Run.png', {
      frameWidth: 78,
      frameHeight: 58,
    })

    this.load.spritesheet('playerHit', 'gameAssets/Hit.png', {
      frameWidth: 78,
      frameHeight: 58,
    })

    this.load.spritesheet('playerDead', 'gameAssets/Dead.png', {
      frameWidth: 78,
      frameHeight: 58,
    })
    this.load.image('feather', 'gameAssets/feather.png')
    this.load.image('icon1', 'gameAssets/lamb-icon-1.jpg')
    this.load.image('icon2', 'gameAssets/lamb-icon-1.jpg')
    this.load.image('steam', 'gameAssets/steam.png')
    this.load.image('jewel', 'gameAssets/jewel.png')
    this.load.image('LifeBar', 'gameAssets/LifeBar.png')
  }
  create() {
    this.input.mouse.disableContextMenu()
    this.attackSfx = this.sound.add('attackSfx')
    this.lastHitSfx = this.sound.add('lastHitSfx')
    this.moveSfx = this.sound.add('moveSfx', {
      loop: true,
    })
    this.anims.create({
      key: 'idle',
      frames: this.anims.generateFrameNumbers('playerIdle', {
        start: 0,
        end: 0,
      }),
      frameRate: 8,
      repeat: -1,
    })

    this.anims.create({
      key: 'attack',
      frames: this.anims.generateFrameNumbers('playerAttack', {
        start: 0,
        end: 2,
      }),
      frameRate: 12,
      repeat: 0,
    })
    this.anims.create({
      key: 'run',
      frames: this.anims.generateFrameNumbers('playerRun', {
        start: 0,
        end: 8,
      }),
      frameRate: 12,
      repeat: -1,
    })

    this.anims.create({
      key: 'hit',
      frames: this.anims.generateFrameNumbers('playerHit', {
        start: 0,
        end: 2,
      }),
      frameRate: 12,
      repeat: 0,
    })

    this.anims.create({
      key: 'dead',
      frames: this.anims.generateFrameNumbers('playerDead', {
        start: 0,
        end: 4,
      }),
      frameRate: 12,
      repeat: 0,
    })

    this.player1 = new Character('Perro', 10, 15, 0.1, 4, this, -80, 300)
    this.player2 = new Character('Sanshe', 150, 12, 1, 6, this, 440, 300)
    this.player2.sprite.setFlipX(true)

    const screenW = this.scale.width
    const margin = 20

    this.player1Icon = this.add.image(margin + 24, 40, 'icon1')
    this.player1Icon.setDisplaySize(48, 48)

    this.player2Icon = this.add.image(screenW - margin - 24, 40, 'icon2')
    this.player2Icon.setDisplaySize(48, 48)

    this.player1Bar = this.add.graphics()
    this.player2Bar = this.add.graphics()

    this.player1MaxHp = this.player1.hp
    this.player2MaxHp = this.player2.hp

    this.player1HpBar = this.add.graphics()
    this.player2HpBar = this.add.graphics()

    this.player1NameText = this.add
      .text(margin, 75, this.player1.name, {
        fontSize: '16px',
        color: '#ffffff',
        align: 'left',
      })
      .setOrigin(0, 0.5)

    this.player2NameText = this.add
      .text(screenW - margin, 75, this.player2.name, {
        fontSize: '16px',
        color: '#ffffff',
        align: 'right',
      })
      .setOrigin(1, 0.5)

    this.hitParticles = this.add.particles(0, 0, 'feather', {
      speed: { min: -180, max: 280 },
      angle: { min: 0, max: 180 },
      rotate: { min: 0, max: 180 },
      scale: { start: 0.4, end: 0 },
      lifespan: 700,
      quantity: 7,
      gravityY: 50,
      emitting: false,
    })
    this.deathParticles = this.add.particles(0, 0, 'steam', {
      speed: { min: -50, max: 50 },
      scale: { start: 0.2, end: 0.4 },
      alpha: { start: 0.7, end: 0 },
      lifespan: 1200,
      quantity: 13,
      frequency: -1,
      rotate: {
        min: 0,
        max: 360,
      },
      angularVelocity: {
        min: -120,
        max: 120,
      },
    })

    this.player1.sprite.play('run')
    this.player2.sprite.play('run')
    this.moveSfx.play({
      loop: true,
      rate: 2,
    })

    this.tweens.add({
      targets: this.player1.sprite,
      x: 125,
      duration: 800,
      ease: 'Power2',
    })

    this.player1LifeBar = this.add.image(margin + 85, 95, 'LifeBar')
    this.player1LifeBar.setDisplaySize(160, 22)
    this.player1LifeBar.setDepth(1)

    this.player1AtkBar = this.add.image(margin + 56, 115, 'LifeBar')
    this.player1AtkBar.setDisplaySize(110, 22)
    this.player1AtkBar.setDepth(1)

    this.player2LifeBar = this.add.image(screenW - margin - 85, 95, 'LifeBar')
    this.player2LifeBar.setDisplaySize(160, 22)
    this.player2LifeBar.setFlipX(true)
    this.player2LifeBar.setDepth(1)

    this.player2AtkBar = this.add.image(screenW - margin - 56, 115, 'LifeBar')
    this.player2AtkBar.setDisplaySize(110, 22)
    this.player2AtkBar.setFlipX(true)
    this.player2AtkBar.setDepth(1)

    this.player1HpBar.setDepth(0)
    this.player1Bar.setDepth(0)
    this.player2HpBar.setDepth(0)
    this.player2Bar.setDepth(0)

    this.tweens.add({
      targets: this.player2.sprite,
      x: 235,
      duration: 800,
      ease: 'Power2',
      onComplete: () => {
        this.player1.sprite.play('idle')
        this.player2.sprite.play('idle')
        this.player1.setTarget(this.player2)
        this.player2.setTarget(this.player1)
        this.moveSfx.stop()
      },
    })
    this.input.on('pointerdown', (pointer) => {
      if (pointer.rightButtonDown()) {
        this.switchScene('LobbyScene')
      }
    })
  }

  spawnHitParticles(x, y) {
    const range = 20
    this.hitParticles.emitParticleAt(x, y + Phaser.Math.Between(-range, range))
  }

  spawnJewelRain() {
    const screenW = this.scale.width
    return this.add.particles(0, 0, 'jewel', {
      tint: () => Phaser.Display.Color.RandomRGB().color,
      x: { min: 0, max: screenW },
      y: -50,
      speedY: { min: 250, max: 600 },
      speedX: { min: -150, max: 150 },
      lifespan: 5000,
      quantity: 2,
      frequency: 30,
      scale: { start: 0.09, end: 0.3 },
      rotate: { min: 0, max: 360 },
    })
  }

  drawAttackBar(graphics, x, y, progress, flip = false) {
    graphics.clear()
    const width = 96
    const height = 10

    graphics.fillStyle(0xffffff)
    graphics.fillRect(x, y, width, height)

    graphics.fillStyle(0x00d9ff)
    const fillWidth = width * progress

    if (!flip) {
      graphics.fillRect(x, y, fillWidth, height)
    } else {
      graphics.fillRect(x + (width - fillWidth), y, fillWidth, height)
    }
  }

  drawHpBar(graphics, x, y, hp, maxHp) {
    const width = 140
    const height = 18
    const radius = 9
    const hpPercent = Phaser.Math.Clamp(hp / maxHp, 0, 1)

    graphics.clear()

    graphics.fillStyle(0xffffff)
    graphics.fillRoundedRect(x, y, width, height, radius)

    graphics.fillStyle(0xff1900)
    graphics.fillRoundedRect(x + 2, y + 2, width - 4, height - 4, radius)

    graphics.fillStyle(0x08ff29)
    graphics.fillRoundedRect(x + 2, y + 2, (width - 4) * hpPercent, height - 4, radius)
  }

  gameOver(winner) {
    this.isGameOver = true
    const midX = this.scale.width / 2
    const midY = this.scale.height / 2

    const overlay = this.add.rectangle(
      midX,
      midY,
      this.scale.width,
      this.scale.height,
      0x000000,
      0.5,
    )
    overlay.setDepth(2)

    const topText = this.add.text(-200, 280, winner.name, {
      fontSize: '36px',
      color: '#ffffff',
      fontStyle: 'bold',
      stroke: '#000000',
      strokeThickness: 6,
    })

    topText.setOrigin(0.5)
    topText.setDepth(3)

    const bottomText = this.add.text(this.scale.width + 200, 340, 'WINS!', {
      fontSize: '42px',
      color: '#ffff00',
      fontStyle: 'bold',
      stroke: '#000000',
      strokeThickness: 6,
    })

    bottomText.setOrigin(0.5)
    bottomText.setDepth(3)

    const flash = this.add.rectangle(midX, midY, this.scale.width, this.scale.height, 0xffffff, 1)
    flash.setAlpha(0)
    flash.setDepth(10)

    this.tweens.add({
      targets: topText,
      x: midX,
      duration: 500,
      ease: 'Back.Out',
    })

    this.tweens.add({
      targets: bottomText,
      x: midX,
      duration: 500,
      ease: 'Back.Out',
      onComplete: () => {
        flash.setAlpha(1)
        this.tweens.add({
          targets: flash,
          alpha: 0,
          duration: 800,
          ease: 'Quad.Out',
        })

        this.tweens.add({
          targets: [topText, bottomText],
          scale: 1.15,
          duration: 500,
          yoyo: true,
          repeat: -1,
          ease: 'Sine.easeInOut',
        })
      },
    })
    this.spawnJewelRain()
    this.time.delayedCall(1500, () => {
      this.time.timeScale = 1
      this.tweens.timeScale = 1
    })
  }

  update(time, delta) {
    if (this.isGameOver || this.player1.hp <= 0) return

    this.player1.update(delta)
    this.player2.update(delta)

    const screenW = this.scale.width
    const margin = 20
    const hpBarWidth = 140
    const atkBarWidth = 96

    const hpY = 86
    const atkY = 110

    this.drawHpBar(this.player1HpBar, margin + 12, hpY, this.player1.hp, this.player1MaxHp)
    this.drawAttackBar(this.player1Bar, margin + 12, atkY, this.player1.attackProgress)

    const player2HpX = screenW - margin - hpBarWidth - 12
    this.drawHpBar(this.player2HpBar, player2HpX, hpY, this.player2.hp, this.player2MaxHp)

    const player2AtkX = screenW - margin - atkBarWidth - 12
    this.drawAttackBar(this.player2Bar, player2AtkX, atkY, this.player2.attackProgress, true)

    this.player1NameText.setPosition(margin, 75)
    this.player2NameText.setPosition(screenW - margin, 75)
  }
}
