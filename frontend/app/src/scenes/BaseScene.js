import Phaser from 'phaser'
export let lastScene = null

export default class BaseScene extends Phaser.Scene {
  switchScene(key, data = {}) {
    lastScene = this.scene.key
    this.scene.start(key, data)
  }
}
