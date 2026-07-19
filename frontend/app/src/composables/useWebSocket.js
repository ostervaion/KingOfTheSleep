import { ref, computed } from 'vue'

const ws = ref(null)
const isConnected = ref(false)
const isAuthenticated = ref(false)
const onlineUsers = ref(new Set())
const updateDashboard = ref(false)

const chatMessages = ref([])
const globalMessages = ref([])
const myUsername = ref('')

// Chat actualmente abierto por el usuario: null (cerrado), 'global', o un username.
// Se usa para no marcar como "no leído" lo que ya se está viendo.
const activeChatTarget = ref(null)

// Contadores de mensajes no leídos
const unreadPrivate = ref({}) // { username: count }
const unreadGlobal = ref(0)

const totalUnread = computed(() => {
  const privateTotal = Object.values(unreadPrivate.value).reduce((a, b) => a + b, 0)
  return privateTotal + unreadGlobal.value
})

// Lista de personas con las que hay conversación (te han escrito o les has escrito),
// ordenadas por el mensaje más reciente primero.
const conversations = computed(() => {
  const map = new Map()
  for (const msg of chatMessages.value) {
    const other = msg.from === myUsername.value ? msg.to : msg.from
    if (!other || other === myUsername.value) continue
    map.set(other, msg) // se queda con el último mensaje de esa persona
  }
  return Array.from(map.entries()).map(([username, lastMessage]) => ({
    username,
    lastMessage,
    unread: unreadPrivate.value[username] || 0,
  }))
})

export function useWebSocket() {
  const API_WS_URL = 'api/ws'

  function connect() {
    if (ws.value && ws.value.readyState === WebSocket.OPEN) return

    ws.value = new WebSocket(API_WS_URL)

    ws.value.onopen = () => {
      isConnected.value = true

      const token = localStorage.getItem('token')
      if (token) {
        ws.value.send(
          JSON.stringify({
            type: 'auth',
            token: token,
          }),
        )
      } else {
        console.error('No se encontró un token en el localStorage para autenticar')
      }
    }

    ws.value.onmessage = (event) => {
      try {
        const response = JSON.parse(event.data)
        const msgType = response.type
        const payload = response.payload

        // Procesar según el tipo de mensaje recibido
        switch (msgType) {
          case 'auth:success':
            isAuthenticated.value = true
            myUsername.value = payload.username
            console.log('Autenticación exitosa como:', payload.username)
            break

          case 'auth:fail':
            isAuthenticated.value = false
            console.error('Fallo en la autenticación:', payload)
            disconnect()
            break

          case 'chat:message':
            // Guardamos el mensaje en nuestra lista global de chats
            chatMessages.value.push(payload)

            if (payload.from !== myUsername.value && activeChatTarget.value !== payload.from) {
              unreadPrivate.value = {
                ...unreadPrivate.value,
                [payload.from]: (unreadPrivate.value[payload.from] || 0) + 1,
              }
            }
            break

          case 'chat:global':
            globalMessages.value.push(payload)

            if (payload.from !== myUsername.value && activeChatTarget.value !== 'global') {
              unreadGlobal.value += 1
            }
            break

          case 'error':
            console.warn('Error recibido del servidor:', payload)
            break

          case 'presence:list':
            onlineUsers.value = new Set(payload.online)
            break
          case 'fetch':
            updateDashboard.value = true
            console.log('FETCH')
            break

          case 'presence:update':
            if (payload.online) {
              onlineUsers.value.add(payload.username)
            } else {
              onlineUsers.value.delete(payload.username)
            }
            onlineUsers.value = new Set(onlineUsers.value)
            break
          default:
            console.log('Mensaje no controlado:', response)
        }
      } catch (err) {
        // Por si el backend manda texto plano en lugar de JSON
        console.log('Mensaje de sistema:', event.data)
      }
    }

    ws.value.onerror = (error) => {
      console.error('Error en el WebSocket:', error)
    }

    ws.value.onclose = () => {
      isConnected.value = false
      isAuthenticated.value = false
      ws.value = null
      console.log('Conexión cerrada')
    }
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close(1000, 'Cierre controlado por el usuario')
    }
  }

  // Marca qué chat está viendo el usuario ahora mismo y limpia sus no leídos.
  // target: null (nada abierto), 'global', o un username.
  function setActiveChat(target) {
    activeChatTarget.value = target

    if (target === 'global') {
      unreadGlobal.value = 0
    } else if (target) {
      if (unreadPrivate.value[target]) {
        const next = { ...unreadPrivate.value }
        delete next[target]
        unreadPrivate.value = next
      }
    }
  }

  function sendPayload(type, data) {
    if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
      console.warn('No se puede enviar el mensaje, el socket está cerrado.')
      return
    }

    ws.value.send(
      JSON.stringify({
        type: type,
        ...data,
      }),
    )
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
  }
}
