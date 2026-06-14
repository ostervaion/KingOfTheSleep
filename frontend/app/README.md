# Configuración del frontend

## Tailwind CSS

Tailwind está instalado y disponible en todo el proyecto.

La configuración se aplica mediante el archivo `main.css`, ubicado dentro de la carpeta `src/assets/`. Este archivo se importa de forma global, por lo que las clases de Tailwind pueden utilizarse directamente en cualquier componente de Vue.

Ejemplo:

```vue
<template>
  <button class="bg-blue-500 text-white px-4 py-2 rounded">
    Iniciar sesión
  </button>
</template>
```

---

## Pinia

Pinia se utiliza como **store global del frontend**, es decir, como un gestor de estado centralizado para la aplicación.

Actualmente, en la store de autenticación se guardan los siguientes datos:

* `token`
* `username`
* `isAuthenticated`

Estos valores permiten mantener información importante del usuario en el frontend, como saber si está autenticado o conservar su sesión sin tener que hacer peticiones constantes al servidor.

Además, gracias a Pinia podemos gestionar mejor el flujo de la aplicación, especialmente en tareas como el login, el logout y el control de rutas protegidas.

Actualmente, la store tiene dos funciones principales:

* `login()`: inicia sesión, guarda el token y almacena los datos necesarios.
* `logout()`: cierra sesión y elimina los datos guardados.

En el futuro puede ser interesante añadir más información a esta store, como datos del perfil del usuario, roles, permisos o preferencias de la aplicación.

### Ejemplo de uso

Para utilizar la store en un componente:

```js
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

auth.login(user.value, password.value)
```

También se puede consultar si el usuario está autenticado:

```js
if (auth.isAuthenticated) {
  console.log('Usuario autenticado')
}
```

---

## Axios

Axios se utiliza como gestor de peticiones HTTP.

Nos permite evitar tener que construir manualmente todas las URLs, gestionar configuraciones repetidas o escribir siempre la misma lógica para comunicarnos con el backend.

La configuración principal de Axios se encuentra en:

```txt
src/api/api.js
```

En este archivo se define una instancia de Axios con una URL base. Gracias a eso, en lugar de escribir la URL completa en cada petición, podemos hacer llamadas más simples como:

```js
api.post('/login')
```

Esto hace que el código sea más limpio, reutilizable y fácil de mantener.

### Importación

Para usar Axios en cualquier componente o store:

```js
import api from '@/api/api'
```

### Ejemplo de uso con GET

```js
import api from '@/api/api'

async function getUserData() {
  try {
    const response = await api.get('/user')

    console.log(response.data)
  } catch (error) {
    console.error('Error al obtener los datos del usuario:', error)
  }
}
```

### Ejemplo de uso con POST

```js
import api from '@/api/api'

async function sendData() {
  try {
    const response = await api.post('/example', {
      name: 'Usuario',
      email: 'usuario@example.com'
    })

    console.log(response.data)
  } catch (error) {
    console.error('Error al enviar los datos:', error)
  }
}
```

---

## Resumen

En este proyecto:

* **Tailwind** se encarga de los estilos.
* **Pinia** se encarga de guardar y gestionar el estado global del frontend.
* **Axios** se encarga de realizar las peticiones al backend.

Estas tres herramientas ayudan a tener un frontend más organizado, mantenible y fácil de escalar.
