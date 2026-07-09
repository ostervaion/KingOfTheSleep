import Phaser, { LEFT } from 'phaser'
import Character from '../Character.js'

export default class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene')
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
  }
  create() {
    this.attackSfx = this.sound.add('attackSfx')
    this.lastHitSfx = this.sound.add('lastHitSfx')
    this.moveSfx = this.sound.add('moveSfx', {
      loop: true,
    })
    this.anims.create({
      key: 'idle',
      frames: this.anims.generateFrameNumbers('playerIdle', {
        start: 0,
        end: 9,
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

    //this.player1 = new Character("Perro0000", 12, 15, 0.1, 4, this, 125, 300);
    //this.player2 = new Character("Sanshe0000", 150, 12, 1, 6, this, 235, 300);

    this.player1 = new Character('Perro', 10, 15, 0.1, 4, this, -80, 300)
    this.player2 = new Character('Sanshe', 150, 12, 1, 6, this, 440, 300)
    this.player2.sprite.setFlipX(true)

    this.player1Icon = this.add.image(40, 40, 'icon1')
    this.player1Icon.setDisplaySize(48, 48)

    this.player2Icon = this.add.image(320, 40, 'icon2')
    this.player2Icon.setDisplaySize(48, 48)

    this.player1Bar = this.add.graphics()
    this.player2Bar = this.add.graphics()

    this.player1MaxHp = this.player1.hp
    this.player2MaxHp = this.player2.hp

    this.player1HpBar = this.add.graphics()
    this.player2HpBar = this.add.graphics()

    this.player1NameText = this.add
      .text(0, 0, this.player1.name, {
        fontSize: '16px',
        color: '#ffffff',
        align: 'left',
      })
      .setOrigin(0, 0.5)

    this.player2NameText = this.add
      .text(0, 0, this.player2.name, {
        fontSize: '16px',
        color: '#ffffff',
        align: 'right',
      })
      .setOrigin(1, 0.5)

    this.hitParticles = this.add.particles(0, 0, 'feather', {
      speed: { min: -180, max: 180 },
      angle: { min: 0, max: 180 },
      rotate: { min: 0, max: 180 },
      scale: { start: 0.05, end: 0 },
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
    // move to center positions
    this.tweens.add({
      targets: this.player1.sprite,
      x: 125,
      duration: 800,
      ease: 'Power2',
    })

    this.tweens.add({
      targets: this.player2.sprite,
      x: 235,
      duration: 800,
      ease: 'Power2',
      onComplete: () => {
        // switch to idle after entering
        this.player1.sprite.play('idle')
        this.player2.sprite.play('idle')

        // NOW start fighting
        this.player1.setTarget(this.player2)
        this.player2.setTarget(this.player1)
        this.moveSfx.stop()
      },
    })
  }

  spawnHitParticles(x, y) {
    const range = 20 // increase this for wider spread

    this.hitParticles.emitParticleAt(x, y + Phaser.Math.Between(-range, range))
  }

  spawnJewelRain() {
    return this.add.particles(0, 0, 'jewel', {
      tint: () => Phaser.Display.Color.RandomRGB().color,
      x: { min: 0, max: 360 },
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

    // background
    graphics.fillStyle(0xffffff)
    graphics.fillRect(x, y, width, height)

    graphics.fillStyle(0x00d9ff)

    const fillWidth = width * progress

    if (!flip) {
      // LEFT → RIGHT (Player 1)
      graphics.fillRect(x, y, fillWidth, height)
    } else {
      // RIGHT → LEFT (Player 2)
      graphics.fillRect(x + (width - fillWidth), y, fillWidth, height)
    }
  }
  drawHpBar(graphics, x, y, hp, maxHp) {
    const width = 140
    const height = 18
    const radius = 9

    const hpPercent = Phaser.Math.Clamp(hp / maxHp, 0, 1)

    graphics.clear()

    // White outer background
    graphics.fillStyle(0xffffff)
    graphics.fillRoundedRect(x, y, width, height, radius)

    // Dark inner background
    graphics.fillStyle(0xff1900)
    graphics.fillRoundedRect(x + 2, y + 2, width - 4, height - 4, radius)

    // Green HP fill
    graphics.fillStyle(0x08ff29)
    graphics.fillRoundedRect(x + 2, y + 2, (width - 4) * hpPercent, height - 4, radius)
  }

  gameOver(winner) {
    this.isGameOver = true

    // dark overlay
    const overlay = this.add.rectangle(180, 320, 360, 640, 0x000000, 0.5)

    overlay.setDepth(1)

    // winner name (comes from left)
    const topText = this.add.text(-200, 280, winner.name, {
      fontSize: '36px',
      color: '#ffffff',
      fontStyle: 'bold',
      stroke: '#000000',
      strokeThickness: 6,
    })

    topText.setOrigin(0.5)
    topText.setDepth(2)

    // wins text (comes from right)
    const bottomText = this.add.text(560, 340, 'WINS!', {
      fontSize: '42px',
      color: '#ffff00',
      fontStyle: 'bold',
      stroke: '#000000',
      strokeThickness: 6,
    })

    bottomText.setOrigin(0.5)
    bottomText.setDepth(2)

    // white flash
    const flash = this.add.rectangle(180, 320, 360, 640, 0xffffff, 1)

    flash.setAlpha(0)
    flash.setDepth(10)

    // top text animation
    this.tweens.add({
      targets: topText,
      x: 180,
      duration: 500,
      ease: 'Back.Out',
    })

    // bottom text animation
    this.tweens.add({
      targets: bottomText,
      x: 180,
      duration: 500,
      ease: 'Back.Out',

      onComplete: () => {
        // flash effect
        flash.setAlpha(1)

        this.tweens.add({
          targets: flash,
          alpha: 0,
          duration: 800,
          ease: 'Quad.Out',
        })

        // pulse animation
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
    // restore timescale
    this.time.delayedCall(1500, () => {
      this.time.timeScale = 1
      this.tweens.timeScale = 1
    })
  }

  update(time, delta) {
    if (this.isGameOver || this.player1.hp <= 0) return

    this.player1.update(delta)
    this.player2.update(delta)

    const atkY = 105

    // Player 1 attack bar (left)
    this.drawAttackBar(this.player1Bar, 20, atkY, this.player1.attackProgress)

    this.drawAttackBar(this.player2Bar, 242, atkY, this.player2.attackProgress, true)

    // HP bars
    this.player1HpBar.clear()
    this.player2HpBar.clear()

    // Player 1 HP (top left)
    this.drawHpBar(this.player1HpBar, 20, 85, this.player1.hp, this.player1MaxHp)

    // Player 2 HP (top right)
    this.drawHpBar(this.player2HpBar, 200, 85, this.player2.hp, this.player2MaxHp)

    const screenW = 360
    const hpW = 140
    const margin = 20

    // Player 1 name (left)
    this.player1NameText.setPosition(margin, 75)

    // Player 2 name (right aligned under bars)
    this.player2NameText.setPosition(screenW - margin, 75)
  }
}
