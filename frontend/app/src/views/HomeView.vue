<script setup>
import { ref } from 'vue'
import LoginPanel from '@/components/LoginPanel.vue'
import RegisterPanel from '@/components/RegisterPanel.vue'
import SleepDataForm from '@/components/SleepDataForm.vue'

const mode = ref('default')
const homeEmail = ref('')
</script>

<template>
  <SleepDataForm />
  <div class="min-h-screen text-(--text) px-4 py-8 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto grid gap-6 lg:grid-cols-[1.2fr_0.9fr] items-start">
      <!-- Left content -->
      <section class="space-y-6">
        <div class="bg-(--surface) border border-(--border) p-8 rounded-xl">
          <h1
            class="text-3xl sm:text-4xl font-semibold leading-tight tracking-[-0.03em] text-(--text)"
          >
            Hero message...
          </h1>
          <p class="mt-4 max-w-xl text-sm text-(--muted) leading-7">
            Hero descripciónaaaaaaaaaaaaaaaaaaa... aquí puedes colocar un texto corto, potente y
            llamativo para tu producto.
          </p>
        </div>

        <div class="gap-4">
          <div class="bg-(--surface) border border-(--border) rounded-xl p-6">
            <p class="text-sm text-(--text) leading-6">Beneficio1 - característica 1</p>
            <p class="text-sm text-(--text) leading-6">Beneficio2 - característica 2</p>
            <p class="text-sm text-(--text) leading-6">beneficio 3 - característica 3</p>
          </div>
        </div>
      </section>

      <!-- Right content -->
      <aside class="space-y-6">
        <div class="bg-(--surface) border border-(--border) rounded-xl overflow-hidden">
          <div
            v-if="mode === 'default'"
            class="relative overflow-hidden pt-[56.25%] bg-(--surface-soft)"
          >
            <iframe
              class="absolute inset-0 h-full w-full"
              src="https://www.youtube.com/embed/dQw4w9WgXcQ"
              title="YouTube video player"
              frameborder="0"
              allow="
                accelerometer;
                autoplay;
                clipboard-write;
                encrypted-media;
                gyroscope;
                picture-in-picture;
              "
              allowfullscreen
            ></iframe>
          </div>
          <div class="p-6">
            <template v-if="mode === 'default'">
              <div class="space-y-4">
                <label class="block text-[10px] tracking-[4px] uppercase text-(--accent) mb-2"
                  >Email</label
                >
                <input
                  v-model="homeEmail"
                  type="email"
                  placeholder="Type your email here..."
                  class="w-full rounded-2xl border border-(--border) bg-(--surface-soft) px-4 py-3 text-sm text-(--text) placeholder:text-(--muted) focus:border-(--accent) focus:outline-none"
                />
                <button
                  type="button"
                  @click="mode = 'register'"
                  class="w-full rounded-2xl bg-(--button) px-4 py-3 text-sm font-semibold uppercase tracking-[2px] text-white hover:bg-(--button-hover) transition-colors"
                >
                  Join →
                </button>
                <p class="text-sm text-(--muted) leading-6">
                  Have an account?
                  <button
                    type="button"
                    @click="mode = 'login'"
                    class="text-(--accent) hover:text-(--button-hover) underline"
                  >
                    Login
                  </button>
                </p>
              </div>
            </template>

            <template v-else-if="mode === 'login'">
              <LoginPanel />
            </template>

            <template v-else>
              <RegisterPanel :email="homeEmail" @back="mode = 'default'" />
            </template>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>
