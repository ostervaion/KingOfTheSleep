import Phaser from 'phaser'

export default class BaseScene extends Phaser.Scene {
  switchScene(key) {
    this.scene.start(key)
  }
}
