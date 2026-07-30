import Phaser, { LEFT } from 'phaser'
import Character from '../Character.js'
import BaseScene from './BaseScene.js'
import { watch } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
const { battlePaused, sendPayload, battleHit, battleOpponentReconnected } = useWebSocket()
let scene = null
let isGamePaused = false

export default class GameScene extends BaseScene {
  constructor() {
    super({ key: 'GameScene' })
  }
  init(data) {
    this.playerData = data.player
    this.opponentData = data.opponent
    this.isReconnect = !!data.reconnect
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
    this.load.image('background', 'gameAssets/back.png')
    this.load.image('clouds', 'gameAssets/clouds.png')
  }
  resumeBattle(data) {
    this.isGamePaused = false

    this.physics.resume()
    this.anims.resumeAll()
    this.tweens.resumeAll()

    if (this.pauseText) {
      this.pauseText.destroy()
      this.pauseText = null
    }
  }
  pauseBattle() {
    console.log('pauseText exists?', !!this.pauseText)
    if (this.isGameOver || this.isGamePaused) {
      return
    }

    if (!this.scene.isActive('GameScene')) {
      return
    }
    this.isGamePaused = true
    this.physics.pause()
    this.anims.pauseAll()
    this.tweens.pauseAll()

    this.pauseText = this.add
      .text(this.scale.width / 2, this.scale.height / 2, 'Waiting for opponent to reconnect...', {
        fontSize: '28px',
        color: '#ffffff',
        backgroundColor: '#000000',
        padding: { x: 16, y: 8 },
      })
      .setOrigin(0.5)
      .setDepth(1000)
  }
  showBackgroundAt(focusX, focusY, scale = 1.5) {
    const bg = this.add.image(0, 0, 'background').setOrigin(0, 0).setScale(scale)

    bg.x = this.scale.width / 2 - focusX * scale
    bg.y = this.scale.height / 2 - focusY * scale

    return bg
  }
  createPlayers(scorePlayer1, scorePlayer2, usernamePlayer1, usernamePlayer2) {
    const centerX = this.cameras.main.midPoint.x

    const createStats = (score) => ({
      hp: 5000 + score * 4,
      attack: 70 + score * 0.15,
      attackSpeed: 1 + score * 0.01,
      defense: 5 + score * 0.05,
    })

    const s1 = createStats(scorePlayer1)
    const s2 = createStats(scorePlayer2)

    this.player1 = new Character(
      usernamePlayer1,
      this.playerData.hp ?? Math.round(s1.hp),
      Math.round(s1.attack),
      s1.attackSpeed,
      Math.round(s1.defense),
      scorePlayer1,
      this,
      -centerX * 2,
      300,
      true,
    )

    this.player2 = new Character(
      usernamePlayer2,
      this.opponentData.hp ?? Math.round(s2.hp),
      Math.round(s2.attack),
      s2.attackSpeed,
      Math.round(s2.defense),
      scorePlayer2,
      this,
      centerX * 2,
      300,
      false,
    )
    this.player1MaxHp = Math.round(s1.hp)
    this.player2MaxHp = Math.round(s2.hp)
    this.player2.sprite.setFlipX(true)
  }
  create() {
    this.isGameOver = false
    scene = this
    this.isGamePaused = this.isReconnect
    this.stopWatch = watch(battlePaused, (paused) => {
      console.log('[DEBUG] watcher disparado, paused =', paused)
      if (paused) {
        this.pauseBattle()
      } else {
        this.resumeBattle()
      }
    }) 
    this.stopHitWatch = watch(battleHit, (payload) => {
      console.log('HIT WATCH', this.scene.isActive())
      if (!payload) return
      const attackerChar = this.player1.name === payload.attacker ? this.player1 : this.player2
      attackerChar.receiveAttack(payload.damage, payload.targetHp)
      battleHit.value = null
    })
    this.stopReconnectWatch = watch(battleOpponentReconnected, () => {
      this.resumeBattle()
    })
    this.events.once(Phaser.Scenes.Events.DESTROY, () => {
      this.stopWatch?.()
      this.stopHitWatch?.()
      this.stopReconnectWatch?.()
    })
    this.input.mouse.disableContextMenu()
    this.attackSfx = this.sound.add('attackSfx')
    this.lastHitSfx = this.sound.add('lastHitSfx')
    this.moveSfx = this.sound.add('moveSfx', {
      loop: true,
    })
    if (!this.anims.exists('idle')) {
      this.anims.create({
        key: 'idle',
        frames: this.anims.generateFrameNumbers('playerIdle', {
          start: 0,
          end: 0,
        }),
        frameRate: 8,
        repeat: -1,
      })
    }
    if (!this.anims.exists('attack')) {
      this.anims.create({
        key: 'attack',
        frames: this.anims.generateFrameNumbers('playerAttack', {
          start: 0,
          end: 2,
        }),
        frameRate: 12,
        repeat: 0,
      })
    }
    if (!this.anims.exists('run')) {
      this.anims.create({
        key: 'run',
        frames: this.anims.generateFrameNumbers('playerRun', {
          start: 0,
          end: 7,
        }),
        frameRate: 12,
        repeat: -1,
      })
    }
    if (!this.anims.exists('hit')) {
      this.anims.create({
        key: 'hit',
        frames: this.anims.generateFrameNumbers('playerHit', {
          start: 0,
          end: 1,
        }),
        frameRate: 12,
        repeat: 0,
      })
    }
    if (!this.anims.exists('dead')) {
      this.anims.create({
        key: 'dead',
        frames: this.anims.generateFrameNumbers('playerDead', {
          start: 0,
          end: 3,
        }),
        frameRate: 12,
        repeat: 0,
      })
    }
    /////////////cloud logic///////////////////////////
    const screenW = this.scale.width
    const screenH = this.scale.height
    const overlap = 100

    // Left cloud
    const leftCloud = this.add
      .image(screenW / 4 + overlap / 2, screenH / 2, 'clouds')
      .setDisplaySize(screenW / 2 + overlap, screenH)
      .setFlipX(true)
      .setDepth(100)

    // Right cloud
    const rightCloud = this.add
      .image((screenW * 3) / 4 - overlap / 2, screenH / 2, 'clouds')
      .setDisplaySize(screenW / 2 + overlap, screenH)
      .setFlipY(true) // or setFlipX(true).setFlipY(true) depending on the artwork
      .setDepth(100)
    this.tweens.add({
      targets: leftCloud,
      x: -screenW / 2,
      duration: 1000,
      ease: 'Cubic.easeInOut',
    })

    this.tweens.add({
      targets: rightCloud,
      x: screenW + screenW / 2,
      duration: 1000,
      ease: 'Cubic.easeInOut',
      onComplete: () => {
        leftCloud.destroy()
        rightCloud.destroy()
      },
    })
    //////////cloud logic ends//////////////////////////////
    const centerX = this.cameras.main.midPoint.x
    const gap = 100
    const margin = 20
    this.showBackgroundAt(600, 500, 1.5)
    this.createPlayers(
      this.playerData.score,
      this.opponentData.score,
      this.playerData.username,
      this.opponentData.username,
    )
    this.player2.sprite.setFlipX(true)

    this.player1Icon = this.add.image(margin + 24, 40, 'icon1')
    this.player1Icon.setDisplaySize(48, 48)

    this.player2Icon = this.add.image(screenW - margin - 24, 40, 'icon2')
    this.player2Icon.setDisplaySize(48, 48)

    this.player1Bar = this.add.graphics()
    this.player2Bar = this.add.graphics()

    this.player1HpBar = this.add.graphics()
    this.player2HpBar = this.add.graphics()
    this.drawBars()
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
      x: centerX - gap / 2,
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
      x: centerX + gap / 2,
      duration: 800,
      ease: 'Power2',
      onComplete: () => {
        this.player1.sprite.play('idle')
        this.player2.sprite.play('idle')
        this.player1.setTarget(this.player2)
        this.player2.setTarget(this.player1)
        this.moveSfx.stop()
        if (this.isReconnect) {
          sendPayload('game:ready')
          // stay paused until server confirms via battle:opponent_reconnected
        } else {
          this.isGamePaused = false
        }
      },
    })
    this.input.on('pointerdown', (pointer) => {
      if (pointer.rightButtonDown() && this.isGameOver) {
        this.switchScene('LobbyScene')
      }
    })
  }

  spawnHitParticles(x, y) {
    const range = 20
    this.hitParticles.emitParticleAt(x, y + Phaser.Math.Between(-range, range))
  }
  reportAttack(targetName) {
    console.log('SENDING ATTACK', targetName)
    sendPayload('game:attack_action', { target: targetName })
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

  drawHpBar(graphics, x, y, hp, maxHp, flip = false) {
    const width = 140
    const height = 18
    const radius = 9
    const hpPercent = Phaser.Math.Clamp(hp / maxHp, 0, 1)

    graphics.clear()

    // Border
    graphics.fillStyle(0xffffff)
    graphics.fillRoundedRect(x, y, width, height, radius)

    // Background
    graphics.fillStyle(0xff1900)
    graphics.fillRoundedRect(x + 2, y + 2, width - 4, height - 4, radius)

    // Health
    graphics.fillStyle(0x08ff29)

    const hpWidth = (width - 4) * hpPercent

    if (flip) {
      graphics.fillRoundedRect(x + width - 2 - hpWidth, y + 2, hpWidth, height - 4, radius)
    } else {
      graphics.fillRoundedRect(x + 2, y + 2, hpWidth, height - 4, radius)
    }
  }

  gameOver(winner) {
    this.isGameOver = true
    sendPayload('battle:end', {})
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
    if (this.isGameOver) return

    // Always keep the UI in sync, even while paused/reconnecting
    this.drawBars()

    if (this.isGamePaused || this.player1.hp <= 0) return

    this.player1.update(delta)
    this.player2.update(delta)

    this.player1NameText.setPosition(20, 75)
    this.player2NameText.setPosition(this.scale.width - 20, 75)
  }

  drawBars() {
    const screenW = this.scale.width
    const margin = 20
    const hpBarWidth = 140
    const atkBarWidth = 96
    const hpY = 86
    const atkY = 110

    this.drawHpBar(this.player1HpBar, margin + 12, hpY, this.player1.hp, this.player1MaxHp)
    this.drawAttackBar(this.player1Bar, margin + 12, atkY, this.player1.attackProgress)

    const player2HpX = screenW - margin - hpBarWidth - 12
    this.drawHpBar(this.player2HpBar, player2HpX, hpY, this.player2.hp, this.player2MaxHp, true)

    const player2AtkX = screenW - margin - atkBarWidth - 12
    this.drawAttackBar(this.player2Bar, player2AtkX, atkY, this.player2.attackProgress, true)
  }
}
