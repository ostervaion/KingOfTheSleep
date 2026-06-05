<template>
  <div id="app">
    <h1>Hello from Vue + FastAPI + Caddy</h1>
    <ul>
      <li v-for="item in items" :key="item.id">{{ item.name }}</li>
    </ul>
    <input v-model="newName" placeholder="New item name" />
    <button @click="addItem">Add</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API = import.meta.env.VITE_API_BASE_URL || '/api'

const items = ref([])
const newName = ref('')

async function fetchItems() {
  const res = await fetch(`${API}/items/`)
  items.value = await res.json()
}

async function addItem() {
  if (!newName.value.trim()) return
  await fetch(`${API}/items/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: newName.value }),
  })
  newName.value = ''
  await fetchItems()
}

onMounted(fetchItems)
</script>
