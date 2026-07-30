import { computed, ref } from 'vue'

const ws = ref(null)
const isConnected = ref(false)
const isAuthenticated = ref(false)
const onlineUsers = ref(new Set())
const updateDashboard = ref(false)
const lobbyPlayers = ref({})
const gameError = ref(false)
const gameEnemy = ref('')
const gameAccepted = ref(false)
const battlePaused = ref(false)

const chatMessages = ref([])
const globalMessages = ref([])
const myUsername = ref('')
const battleResume = ref(null)

// null, 'global' o el username del chat abierto.
const activeChatTarget = ref(null)

// Contadores de mensajes no leídos.
const unreadPrivate = ref({})
const unreadGlobal = ref(0)

const totalUnread = computed(() => {
  const privateTotal = Object.values(unreadPrivate.value).reduce(
    (total, count) => total + count,
    0,
  )

  return privateTotal + unreadGlobal.value
})

// Conversaciones privadas ordenadas por el último mensaje.
const conversations = computed(() => {
  const map = new Map()

  for (const message of chatMessages.value) {
    const otherUsername =
      message.from === myUsername.value
        ? message.to
        : message.from

    if (
      !otherUsername ||
      otherUsername === myUsername.value
    ) {
      continue
    }

    map.set(otherUsername, message)
  }

  return Array.from(map.entries()).map(
    ([username, lastMessage]) => ({
      username,
      lastMessage,
      unread: unreadPrivate.value[username] || 0,
    }),
  )
})

export function useWebSocket() {
  /**
   * En producción:
   * https://localhost       -> wss://localhost/api/ws
   *
   * En desarrollo HTTP:
   * http://localhost        -> ws://localhost/api/ws
   *
   * Caddy elimina /api y lo envía al backend como /ws.
   */
  const wsProtocol =
    window.location.protocol === 'https:'
      ? 'wss:'
      : 'ws:'

  const API_WS_URL =
    `${wsProtocol}//${window.location.host}/api/ws`

  function connect() {
    // Evita abrir conexiones duplicadas si ya está conectado
    // o todavía está intentando conectar.
    if (
      ws.value &&
      (
        ws.value.readyState === WebSocket.OPEN ||
        ws.value.readyState === WebSocket.CONNECTING
      )
    ) {
      return
    }

    console.log(
      'Conectando WebSocket a:',
      API_WS_URL,
    )

    const socket = new WebSocket(API_WS_URL)
    ws.value = socket

    socket.onopen = () => {
      // Evita modificar el estado con una conexión antigua.
      if (ws.value !== socket) return

      isConnected.value = true

      console.log(
        'WebSocket conectado:',
        API_WS_URL,
      )

      // Admite ambas claves por si el login usa una u otra.
      const token =
        localStorage.getItem('token') ||
        localStorage.getItem('access_token')

      if (!token) {
        console.error(
          'No se encontró ningún token para autenticar el WebSocket',
        )
        return
      }

      socket.send(
        JSON.stringify({
          type: 'auth',
          token,
        }),
      )
    }

    socket.onmessage = (event) => {
      try {
        const response = JSON.parse(event.data)
        const msgType = response.type
        const payload = response.payload

        switch (msgType) {
          case 'auth:success':
            isAuthenticated.value = true
            myUsername.value = payload.username

            console.log(
              'Autenticación exitosa como:',
              payload.username,
            )
            break

          case 'auth:fail':
            isAuthenticated.value = false

            console.error(
              'Fallo en la autenticación:',
              payload,
            )

            disconnect()
            break

          case 'chat:message':
            chatMessages.value.push(payload)

            if (
              payload.from !== myUsername.value &&
              activeChatTarget.value !== payload.from
            ) {
              unreadPrivate.value = {
                ...unreadPrivate.value,

                [payload.from]:
                  (
                    unreadPrivate.value[
                      payload.from
                    ] || 0
                  ) + 1,
              }
            }
            break

          case 'chat:global':
            globalMessages.value.push(payload)

            if (
              payload.from !== myUsername.value &&
              activeChatTarget.value !== 'global'
            ) {
              unreadGlobal.value += 1
            }
            break

          case 'error':
            console.warn(
              'Error recibido del servidor:',
              payload,
            )
            break

          case 'presence:list':
            onlineUsers.value = new Set(
              payload?.online || [],
            )
            break

          case 'presence:update':
            if (!payload?.username) break

            if (payload.online) {
              onlineUsers.value.add(
                payload.username,
              )
            } else {
              /*
               * Si el usuario que se desconecta era quien
               * había enviado el desafío, se rechaza.
               *
               * Antes se utilizaba `enemy`, que no existía.
               */
              if (
                gameEnemy.value === payload.username
              ) {
                sendPayload('game:response', {
                  accepted: false,
                  target: gameEnemy.value,
                })

                gameEnemy.value = ''
              }

              onlineUsers.value.delete(
                payload.username,
              )

              delete lobbyPlayers.value[
                payload.username
              ]
            }

            // Nueva referencia para que Vue detecte el cambio.
            onlineUsers.value = new Set(
              onlineUsers.value,
            )

            // Nueva referencia para actualizar el lobby.
            lobbyPlayers.value = {
              ...lobbyPlayers.value,
            }
            break

          case 'fetch':
            updateDashboard.value = true
            console.log('FETCH')
            break

          case 'sheep_move':
            if (!response.username) break

            lobbyPlayers.value = {
              ...lobbyPlayers.value,

              [response.username]: [
                response.x,
                response.y,
              ],
            }
            break

          case 'lobby_list':
            lobbyPlayers.value = {
              ...(payload?.lobby_players || {}),
            }
            break

          case 'game:error':
            gameError.value = true
            break

          case 'game:game_petition':
            gameError.value = false
            gameEnemy.value =
              payload?.enemy || ''
            break

          case 'game:answer':
            console.log(
              'game:answer',
              response,
            )

            if (response.response) {
              gameAccepted.value = true
              gameError.value = false
            } else {
              gameAccepted.value = false
              gameError.value = true
            }
            break

          case 'game:disconnect':
            if (!response.user) break

            delete lobbyPlayers.value[
              response.user
            ]

            lobbyPlayers.value = {
              ...lobbyPlayers.value,
            }
            break

          case 'battle:paused':
            battlePaused.value = true
            break

          case 'battle:resume':
            battlePaused.value = false
            battleResume.value = payload
            break

          case 'battle:destroyed':
            battlePaused.value = false
            battleResume.value = null
            break

          case 'battle:opponent_reconnected':
            console.log(
              '[DEBUG] opponent_reconnected',
            )

            battlePaused.value = false
            break

          default:
            console.log(
              'Mensaje WebSocket no controlado:',
              response,
            )
        }
      } catch (error) {
        console.error(
          'No se pudo procesar el mensaje WebSocket:',
          error,
          event.data,
        )
      }
    }

    socket.onerror = (error) => {
      console.error(
        'Error en el WebSocket:',
        error,
      )
    }

    socket.onclose = (event) => {
      /*
       * Si ya existe otro socket nuevo, no permitimos que
       * el cierre de una conexión antigua borre su estado.
       */
      if (ws.value !== socket) return

      isConnected.value = false
      isAuthenticated.value = false
      ws.value = null

      console.log(
        'Conexión WebSocket cerrada:',
        {
          code: event.code,
          reason: event.reason,
          clean: event.wasClean,
        },
      )
    }
  }

  function disconnect() {
    const socket = ws.value

    if (!socket) return

    /*
     * Solo se puede enviar close cuando está conectado
     * o intentando conectar.
     */
    if (
      socket.readyState === WebSocket.OPEN ||
      socket.readyState === WebSocket.CONNECTING
    ) {
      socket.close(
        1000,
        'Cierre controlado por el usuario',
      )
    }

    if (ws.value === socket) {
      ws.value = null
    }

    isConnected.value = false
    isAuthenticated.value = false
  }

  // target: null, 'global' o un username.
  function setActiveChat(target) {
    activeChatTarget.value = target

    if (target === 'global') {
      unreadGlobal.value = 0
      return
    }

    if (
      target &&
      unreadPrivate.value[target]
    ) {
      const nextUnread = {
        ...unreadPrivate.value,
      }

      delete nextUnread[target]
      unreadPrivate.value = nextUnread
    }
  }

  function sendPayload(type, data = {}) {
    if (
      !ws.value ||
      ws.value.readyState !== WebSocket.OPEN
    ) {
      console.warn(
        'No se puede enviar el mensaje: el WebSocket está cerrado',
      )

      return false
    }

    ws.value.send(
      JSON.stringify({
        type,
        ...data,
      }),
    )

    return true
  }

  return {
    connect,
    disconnect,
    sendPayload,

    isConnected,
    isAuthenticated,

    chatMessages,
    globalMessages,
    myUsername,
    onlineUsers,
    updateDashboard,

    conversations,
    unreadPrivate,
    unreadGlobal,
    totalUnread,
    setActiveChat,

    lobbyPlayers,
    gameError,
    gameEnemy,
    gameAccepted,

    battlePaused,
    battleResume,
  }
}