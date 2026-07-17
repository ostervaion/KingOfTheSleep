<script setup>
import { ref, computed } from 'vue'
import example from '@/assets/example.jpg'
import OtherProfiles from '@/components/dashboard/otherProfiles.vue'

const dialog = ref(null)

const props = defineProps({
  ranking: String,
  name: String,
  points: String,
  posChange: String,
  profilePicture: String,
  trend: {
    type: String,
    default: 'same',
  },
})

const trendClass = computed(() => {
  if (props.trend === 'up') return 'text-green-400'
  if (props.trend === 'down') return 'text-red-400'
  return 'text-gray-400'
})

function openDialog() {
  if (!dialog.value) return

  if (!dialog.value.open) {
    dialog.value.showModal()
  }
}

function closeDialog() {
  if (dialog.value?.open) {
    dialog.value.close()
  }
}
</script>

<template>
  <li
    @click="openDialog"
    class="cursor-pointer odd:bg-white/[0.015] even:bg-transparent transition hover:bg-white/[0.04]"
  >
    <div class="grid grid-cols-[40px_1fr_100px_100px] items-center px-6 py-1.5">
      <div class="text-sm text-heading">{{ props.ranking }}</div>
      <div class="flex items-center gap-3">
        <img class="h-8 w-8 rounded-full object-cover" :src="props.profilePicture || example" alt="" />
        <span class="text-sm text-heading">{{ props.name }}</span>
      </div>

      <div class="text-right text-sm text-heading">{{ props.points }}</div>

      <div class="text-right text-sm font-medium" :class="trendClass">
        <span v-if="props.trend === 'up'">↑</span>
        <span v-else-if="props.trend === 'down'">↓</span>
        <span v-else>→</span>
        {{ props.posChange }}
      </div>
    </div>
  </li>

  <Teleport to="body">
    <dialog
      ref="dialog"
      class="m-auto w-[420px] max-w-[94vw] rounded-xl border-none bg-transparent p-0"
    >
      <OtherProfiles
        :user="{
          username: props.name,
          profilePicture: props.profilePicture || example,
          rank: props.ranking,
          level: '42',
          points: props.points,
        }"
        @close="closeDialog"
      />
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
