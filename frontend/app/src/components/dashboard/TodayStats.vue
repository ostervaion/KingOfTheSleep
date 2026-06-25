<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LambBattleIcon from '@/assets/lamb_battle.svg'
</script>

<template>
  <div
    class="font-inter flex flex-col flex-2 min-h-0 overflow-hidden rounded-xl bg-(--kots-blocks-color) shadow-md shadow-black/20 border-b border-[color:var(--border)]"
  >
  <div class="px-6 pb-4 pt-5">
    <div class="flex items-center justify-between">
          <div class="border border-cyan-100 rounded-md px-2 py-0.5 text-gray-800 leading-none">
            <h2 class="text-cyan-100 text-sm font-medium text-heading">Today's Stats</h2>
          </div>
          <div class="flex rounded-full px-1.25 text-right">
            <div class="flex rounded-full px-1.25 py-0.75 bg-(--kots-background-color) ">
              <button class="p5 px-2 py-1 leading-none text-xs font-medium text-white text-heading">
                see all
              </button>
            </div>

          </div>
        </div>
      <div class="pt-2 px-5 flex items-center justify-between">
        <div class="pt-3 items-center">
          <LambBattleIcon class="text-center -mt-0.5 w-10 h-10" />
          <p class="text-center text-xs font-medium  text-body">battles</p>
          <p class="text-center mb-2 text-xl font-light text-white">18</p>
        </div>
        <div class="pt-3 items-center">
          <LambBattleIcon class="text-center -mt-0.5 w-10 h-10" />
          <p class="text-center text-xs font-medium  text-body">wins</p>
          <p class="text-center mb-2 text-xl font-light text-white">14</p>
        </div>
        <div class="pt-3 items-center">
          <LambBattleIcon class="text-center -mt-0.5 w-10 h-10" />
          <p class="text-center text-xs font-medium  text-body">looses</p>
          <p class="text-center mb-2 text-xl font-light text-white">4</p>
        </div>
                <div class="pt-3 items-center">
          <LambBattleIcon class="text-center -mt-0.5 w-10 h-10" />
          <p class="text-center text-xs font-medium  text-body">win rate</p>
          <p class="text-center mb-2 text-xl font-light text-green-400">% 70</p>
        </div>
</div>
      </div>



  </div>
</template>

