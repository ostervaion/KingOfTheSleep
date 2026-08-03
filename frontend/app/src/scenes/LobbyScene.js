import * as Phaser from 'phaser'
import BaseScene from './BaseScene'
import { watch } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'

const {
  myUsername,
  lobbyPlayers,
  gameError,
  gameEnemy,
  gameAccepted,
  sendPayload,
  battleResume,
  battleInitData,
} = useWebSocket()

const WORLD_WIDTH = 4000
const WORLD_HEIGHT = 4000
let scene = null
let waitingResponse = false

watch(
  lobbyPlayers,
  (players) => {
    if (!scene) return
    for (const username of Object.keys(scene.players)) {
      if (!(username in players)) {
        scene.players[username].sprite.destroy()
        scene.players[username].label.destroy()
        delete scene.players[username]
      }
    }
  },
  { deep: true },
)

watch(gameError, (stat) => {
  if (scene.popup) scene.closePopup()
  const width = 160
  const height = 70

  const bg = scene.add.rectangle(0, 0, width, height, 0xffffff, 0.95).setStrokeStyle(2, 0x000000)
  const prompt = scene.add
    .text(0, -18, `${scene.attackTarget} not online or declined`, {
      fontSize: '14px',
      fontFamily: 'monospace',
      color: '#000000',
      align: 'center',
    })
    .setOrigin(0.5)
  const prompt2 = scene.add
    .text(0, -5, `right click to go back to lobby`, {
      fontSize: '14px',
      fontFamily: 'monospace',
      color: '#000000',
      align: 'center',
    })
    .setOrigin(0.5)

  const cx = scene.cameras.main.width / 2
  const cy = scene.cameras.main.height / 2

  scene.popup = scene.add.container(cx, cy, [bg, prompt, prompt2])
  scene.popup.setDepth(1000)
  scene.popup.setScrollFactor(0)

  scene.input.once('pointerdown', () => scene.closePopup())
  waitingResponse = false
  gameError.value = false
})

watch(gameEnemy, (enemy) => {
  if (waitingResponse || enemy == '') {
    sendPayload('game:response', { accepted: false, target: enemy })
    return
  }

  if (scene.popup) scene.closePopup()
  const width = 160
  const height = 70

  const bg = scene.add.rectangle(0, 0, width, height, 0xffffff, 0.95).setStrokeStyle(2, 0x000000)

  const prompt = scene.add
    .text(0, -18, `${enemy} is challenging you`, {
      fontSize: '14px',
      fontFamily: 'monospace',
      color: '#000000',
      align: 'center',
    })
    .setOrigin(0.5)

  const acceptBtn = scene.add
    .text(-35, 12, 'Accept', {
      fontSize: '13px',
      fontFamily: 'monospace',
      color: '#ffffff',
      backgroundColor: '#aa2222',
      padding: { x: 6, y: 3 },
    })
    .setOrigin(0.5)
    .setInteractive()

  const declineBtn = scene.add
    .text(35, 12, 'Decline', {
      fontSize: '13px',
      fontFamily: 'monospace',
      color: '#ffffff',
      backgroundColor: '#555555',
      padding: { x: 6, y: 3 },
    })
    .setOrigin(0.5)
    .setInteractive()

  acceptBtn.on('pointerdown', (pointer, localX, localY, event) => {
    if (event) event.stopPropagation()
    gameEnemy.value = ''
    sendPayload('game:response', { accepted: true, target: enemy })
    waitingResponse = false
    scene.closePopup()
    sendPayload('game:disconnect')
    scene.pendingOpponent = enemy
  })

  declineBtn.on('pointerdown', (pointer, localX, localY, event) => {
    if (event) event.stopPropagation()
    gameEnemy.value = ''
    sendPayload('game:response', { accepted: false, target: enemy })
    waitingResponse = false
    scene.closePopup()
  })

  const cx = scene.cameras.main.worldView.x + scene.cameras.main.worldView.width / 2
  const cy = scene.cameras.main.worldView.y + scene.cameras.main.worldView.height / 2

  scene.popup = scene.add.container(cx, cy, [bg, prompt, acceptBtn, declineBtn])
  scene.popup.setDepth(1000)
})

watch(
  battleInitData,
  (battle) => {
    if (!battle || !scene) return

    let enemy

    if (scene.pendingOpponent) {
      enemy = scene.pendingOpponent
    } else {
      enemy = Object.keys(battle).find((username) => username !== myUsername.value)
    }

    scene.pendingOpponent = null

    scene.switchScene('GameScene', {
      player: battle[myUsername.value],
      opponent: battle[enemy],
    })
  },
  { deep: true },
)

watch(gameAccepted, (answer) => {
  if (answer) {
    gameAccepted.value = false
    waitingResponse = false
    scene.closePopup()
    sendPayload('game:disconnect')

    const battle = battleInitData.value
    if (!battle) {
      console.warn('gameAccepted fired but battleInitData is still null')
      return
    }

    scene.switchScene('GameScene', {
      player: battle[myUsername.value],
      opponent: battle[scene.attackTarget],
    })
  }
})

export default class LobbyScene extends BaseScene {
  constructor() {
    super({ key: 'LobbyScene' })
  }

  preload() {
    this.load.image('sheep', 'sheep.webp')
    this.load.image('lobbyBG', 'gameAssets/lobbyBG.png')
  }

  create() {
    scene = this
    this.players = {}
    this.pendingOpponent = null
    this.bg = this.add.tileSprite(0, 0, WORLD_WIDTH, WORLD_HEIGHT, 'lobbyBG')
    this.bg.setOrigin(0, 0)
    this.bg.setDepth(-1)
    this.stopResumeWatcher = watch(
      battleResume,
      (data) => {
        if (!data) return
        this.switchScene('GameScene', {
          reconnect: true,
          player: data.player,
          opponent: data.opponent,
        })

        battleResume.value = null
      },
      { immediate: true },
    )

    this.events.once('shutdown', () => {
      this.stopResumeWatcher()
    })
    const stopWatchers = [
      watch(
        lobbyPlayers,
        (players) => {
          if (scene === this) this.spawnPlayers(players)
        },
        { deep: true },
      ),
      watch(
        lobbyPlayers,
        (players) => {
          if (scene !== this) return
          for (const username of Object.keys(this.players)) {
            if (!(username in players)) {
              this.players[username].sprite.destroy()
              this.players[username].label.destroy()
              delete this.players[username]
            }
          }
        },
        { deep: true },
      ),
    ]
    this.events.once('shutdown', () => stopWatchers.forEach((stop) => stop()))

    sendPayload('get_lobby_players')
    this.input.mouse.disableContextMenu()
    this.physics.world.setBounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
    this.cameras.main.setBounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
    this.player = this.physics.add
      .sprite(2000, 2000, 'sheep')
      .setScale(0.05)
      .setCollideWorldBounds(true)
    this.cameras.main.startFollow(this.player)

    sendPayload('lobby:move', {
      x: Math.round(this.player.x),
      y: Math.round(this.player.y),
    })

    this.target = new Phaser.Math.Vector2(this.player.x, this.player.y)

    this.input.on('pointerdown', (pointer, currentlyOver) => {
      if (this.popup) return
      if (currentlyOver.length > 0) return
      if (pointer.rightButtonDown()) {
      } else {
        this.target.set(pointer.worldX, pointer.worldY)
        sendPayload('lobby:move', {
          x: Math.round(this.target.x),
          y: Math.round(this.target.y),
        })
      }
    })
    this.popup = null
  }

  update() {
    this.moveAndWiggle(this.player, this.target)

    for (const remote of Object.values(this.players)) {
      this.moveAndWiggle(remote.sprite, remote.target)
      remote.label.setPosition(
        remote.sprite.x,
        remote.sprite.y - remote.sprite.displayHeight / 2 - 6,
      )
    }
  }

  spawnPlayers(players) {
    if (!this.sys.isActive()) return
    if (!this.physics?.add) return
    for (const [username, [x, y]] of Object.entries(players)) {
      if (username == myUsername.value) continue

      const existing = this.players[username]
      if (!existing || !existing.sprite || !existing.sprite.active) {
        this.players[username] = {
          sprite: this.physics.add.sprite(x, y, 'sheep').setScale(0.05).setInteractive(),
          label: this.add
            .text(x, y, username, {
              fontSize: '16px',
              fontFamily: 'monospace',
              color: '#000000',
            })
            .setOrigin(0.5, 1),
          target: new Phaser.Math.Vector2(x, y),
        }
        this.players[username].sprite.on('pointerdown', (pointer, localX, localY, event) => {
          if (this.popup) return
          event.stopPropagation()
          this.showConfirmPopup(username)
        })
      } else {
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

  showConfirmPopup(username) {
    if (this.popup) this.closePopup()

    const width = 160
    const height = 70

    const bg = this.add.rectangle(0, 0, width, height, 0xffffff, 0.95).setStrokeStyle(2, 0x000000)

    const prompt = this.add
      .text(0, -18, `Attack ${username}?`, {
        fontSize: '14px',
        fontFamily: 'monospace',
        color: '#000000',
        align: 'center',
      })
      .setOrigin(0.5)

    const confirmBtn = this.add
      .text(-35, 12, 'Attack', {
        fontSize: '13px',
        fontFamily: 'monospace',
        color: '#ffffff',
        backgroundColor: '#aa2222',
        padding: { x: 6, y: 3 },
      })
      .setOrigin(0.5)
      .setInteractive()

    const cancelBtn = this.add
      .text(35, 12, 'Cancel', {
        fontSize: '13px',
        fontFamily: 'monospace',
        color: '#ffffff',
        backgroundColor: '#555555',
        padding: { x: 6, y: 3 },
      })
      .setOrigin(0.5)
      .setInteractive()

    confirmBtn.on('pointerdown', (pointer, localX, localY, event) => {
      if (event) event.stopPropagation()
      waitingResponse = true
      this.attackTarget = username
      sendPayload('game:attack', { user: username })

      this.showWaitingPopup(`Waiting for ${username} to respond...`)
    })

    cancelBtn.on('pointerdown', (pointer, localX, localY, event) => {
      if (event) event.stopPropagation()
      this.closePopup()
    })

    const cx = this.cameras.main.worldView.x + this.cameras.main.worldView.width / 2
    const cy = this.cameras.main.worldView.y + this.cameras.main.worldView.height / 2

    this.popup = this.add.container(cx, cy, [bg, prompt, confirmBtn, cancelBtn])
    this.popup.setDepth(1000)
  }

  closePopup() {
    if (this.popup) {
      this.popup.destroy()
      this.popup = null
      this.popupTarget = null
    }
  }

  showWaitingPopup(message) {
    this.closePopup()

    const width = 160
    const height = 70

    const bg = this.add.rectangle(0, 0, width, height, 0xffffff, 0.95).setStrokeStyle(2, 0x000000)
    const prompt = this.add
      .text(0, 0, message, {
        fontSize: '14px',
        fontFamily: 'monospace',
        color: '#000000',
        align: 'center',
        wordWrap: { width: width - 20 },
      })
      .setOrigin(0.5)

    const cx = this.cameras.main.worldView.x + this.cameras.main.worldView.width / 2
    const cy = this.cameras.main.worldView.y + this.cameras.main.worldView.height / 2

    this.popup = this.add.container(cx, cy, [bg, prompt])
    this.popup.setDepth(1000)
  }
}
