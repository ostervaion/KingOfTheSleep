<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'
import * as Phaser from 'phaser'

import LobbyScene from '@/scenes/LobbyScene'
import GameScene from '@/scenes/BattleScene'

const gameContainer = ref(null)

let game = null


const { isConnected, sendPayload } = useWebSocket()


/* ws.onmessage = ({ data: raw }) => {
	let data try { data = JSON.parse(raw) }
	catch { return } if (!scene) return switch (data.type) {




		case 'authenticated': scene.myUsername = data.username scene.ws = ws
		
		ws.send(JSON.stringify({ type: 'lobby_move', user: scene.myUsername, x: 2000, y: 2000 })) ws.send(JSON.stringify({ type: 'get_lobby_players' })) console.log(data.lobby_players) break case 'lobby_list': console.log(data.lobby_players) console.log('in lobby list') scene.spawnPlayers(data.lobby_players) break
	}
} */

watch(
	isConnected,
	(connected) => {
		if (!connected) return

		sendPayload('lobby_move', {
			x: 2000,
			y: 2000,
		})
	},
	{ immediate: true }
)

onMounted(() => {
	const el = gameContainer.value
	if (!el) return


	game = new Phaser.Game({
		type: Phaser.AUTO,
		parent: gameContainer.value,
		width: el.clientWidth,
		height: el.clientHeight,
		pixelArt: true,
		backgroundColor: '#81C784',
		physics: {
			default: 'arcade',
			arcade: {
				debug: false,
			},
		},
		scene: [LobbyScene, GameScene],
	})
})

onUnmounted(() => {
	game?.destroy(true)
	game = null
	scene = null
})
</script>

<template>
	<div
		class="font-inter text-sm text-heading flex-6 min-h-0 bg-(--kots-blocks-color) p-6 rounded-xl overflow-auto border-b border-[color:var(--border)]">
		<div ref="gameContainer" class="h-full"></div>
	</div>
</template>
