import { ref } from 'vue'

const ws = ref(null)
const isConnected = ref(false)
const isAuthenticated = ref(false)
const onlineUsers = ref(new Set())

// Estados para los distintos módulos de tu app
const chatMessages = ref([])
const myUsername = ref('')

export function useWebSocket() {
  const API_WS_URL = 'api/ws' // Cambia por tu URL de FastAPI

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
          })
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
            break

          case 'error':
            console.warn('Error recibido del servidor:', payload)
            break
          
          case 'presence:list':
            onlineUsers.value = new Set(payload.online)
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

  // Función genérica para enviar datos de forma segura
  function sendPayload(type, data) {
    if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
      console.warn('No se puede enviar el mensaje, el socket está cerrado.')
      return
    }
    
    ws.value.send(
      JSON.stringify({
        type: type,
        ...data,
      })
    )
  }

  return {
    connect,
    disconnect,
    sendPayload,
    isConnected,
    isAuthenticated,
    chatMessages,
    myUsername,
    onlineUsers,
  }
}