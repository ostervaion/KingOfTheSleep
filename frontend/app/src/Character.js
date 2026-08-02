import Phaser from 'phaser'

export default class Character {
  constructor(name, hp, attack, attackSpeed, defense, score, scene, x, y, isLocal = false) {
    this.name = name
    this.hp = hp
    this.attack = attack
    this.attackSpeed = attackSpeed
    this.defense = defense
    this.score = score

    this.scene = scene
    this.isLocal = isLocal

    this.target = null
    this.lastAttackTime = 0
    this.attackProgress = 0
    this.isAttacking = false

    this.sprite = scene.add.sprite(x, y, 'playerIdle')
    this.sprite.setScale(3)
    this.sprite.play('idle')
  }

  setTarget(target) {
    this.target = target
  }

  update(delta) {
    if (!this.target || this.hp <= 0) return

    if (!this.isLocal) {
      this.attackProgress = Math.min(1, this.attackProgress + (delta / 1000) * this.attackSpeed)
      return
    }

    this.attackProgress += (delta / 1000) * this.attackSpeed

    if (this.attackProgress >= 1) {
      this.attackProgress = 0
      this.attackTarget()
    }
  }

  attackTarget() {
    if (!this.target || this.target.hp <= 0) return
    this.scene.reportAttack(this.target.name)
  }

  receiveAttack(damage, hp) {
    this.attackProgress = 0

    if (!this.target || this.target.hp <= 0) return

    this.isAttacking = true
    this.sprite.setTexture('playerAttack')
    this.sprite.play('attack')

    this.sprite.once('animationcomplete', () => {
      this.sprite.setTexture('playerIdle')
      this.sprite.play('idle')
      this.isAttacking = false
    })

    this.target.hp = hp !== undefined && hp !== null ? hp : Math.max(0, this.target.hp - damage)

    if (!this.target.isAttacking) {
      this.target.sprite.stop()
      this.target.sprite.play('hit')
    }
    this.target.sprite.once('animationcomplete', () => {
      if (this.target.hp > 0) {
        this.target.sprite.play('idle')
      } else {
        this.target.sprite.play('dead')
      }
    })

    // hit effect at target position
    this.scene.spawnHitParticles(this.target.sprite.x, this.target.sprite.y)
    this.scene.cameras.main.shake(100, 0.005)
    this.target.sprite.setTint(0xff0000)

    this.scene.time.delayedCall(100, () => {
      this.target.sprite.clearTint()
    })

    if (this.target.hp <= 0) {
      this.target.hp = 0
      this.scene.anims.globalTimeScale = 0.2
      this.scene.time.delayedCall(2100, () => {
        this.target.sprite.setVisible(false)
      })
      this.scene.time.delayedCall(1900, () => {
        this.scene.deathParticles.emitParticleAt(this.target.sprite.x, this.target.sprite.y)
        this.scene.anims.globalTimeScale = 1
        this.scene.gameOver(this)
      })
    }
  }
}
