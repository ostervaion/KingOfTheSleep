import Phaser from 'phaser'

export default class BaseScene extends Phaser.Scene {
  switchScene(key, data = {}) {
    this.scene.start(key, data)
  }
}
