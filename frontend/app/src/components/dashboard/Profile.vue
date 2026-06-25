<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LogOut from '@/components/dashboard/logOut.vue'

var usersData = ref({
  rank: '',
  level: '',
  xp: '',
  nextxp: '',
  todaysSleepScore: '',
})

const dialog = ref(null)

function openDialog() {
  dialog.value.showModal()
} 

function closeDialog() {
  dialog.value.close()
} 

onMounted(() => {
  loadUsersData()
})

function loadUsersData() {
  usersData.value = {
    rank: '4,432',
    level: '42',
    currentxp: '18,450',
    nextxp: '25,000',
    todaysSleepScore: '82',
  }
}
</script>
<template>
  <div
    class="font-inter text-sm text-heading flex-1 min-h-0 bg-(--kots-blocks-color) p-6 rounded-xl overflow-auto"
  >
    Player Profile
  </div>

<Teleport to="body">
  <dialog
    ref="dialog"
    class="m-auto w-[400px] max-w-[90vw] rounded-xl border-none p-0"
  >
    <LogOut @close="closeDialog" />
  </dialog>
</Teleport>
</template>

<style scoped>
dialog::backdrop {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(1px);
}
dialog {
  background: transparent;
  padding: 0;
  border: none;
}
</style>
