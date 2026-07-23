<script setup>
import { computed, reactive, ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const apiBase = ref(import.meta.env.VITE_API_BASE || "");

const response = reactive({
  method: "",
  url: "",
  status: null,
  ok: false,
  body: null,
  loading: false,
});

async function request(method, path, body = null, headers = {}) {
  response.method = method;
  response.url = path;
  response.status = null;
  response.body = null;
  response.loading = true;

  try {
    const options = {
      method,
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
    };

    if (body !== null) {
      options.body = JSON.stringify(body);
    }

    const res = await fetch(`${apiBase.value}${path}`, options);
    const text = await res.text();

    response.status = res.status;
    response.ok = res.ok;

    try {
      response.body = text ? JSON.parse(text) : null;
    } catch {
      response.body = text;
    }

    return {
      ok: res.ok,
      body: response.body,
    };
  } catch (error) {
    response.ok = false;
    response.status = "error de red";
    response.body = String(error);

    return {
      ok: false,
      body: null,
    };
  } finally {
    response.loading = false;
  }
}

/* API KEYS */

const apiKeys = ref([]);
const newKeyName = ref("");
const createdKey = ref(null);
const testApiKey = ref("");

const authHeaders = computed(() => ({
  Authorization: `Bearer ${auth.token}`,
}));

async function loadApiKeys() {
  const result = await request(
    "GET",
    "/admin/apikeys",
    null,
    authHeaders.value
  );

  if (result.ok) {
    apiKeys.value = result.body;
  }
}

async function createApiKey() {
  const name = newKeyName.value.trim();
  if (!name) return;

  const result = await request(
    "POST",
    "/admin/apikeys",
    { name },
    authHeaders.value
  );

  if (!result.ok) return;

  createdKey.value = result.body;
  testApiKey.value = result.body.api_key;
  newKeyName.value = "";

  await loadApiKeys();
}

async function revokeApiKey(id) {
  const result = await request(
    "DELETE",
    `/admin/apikeys/${id}`,
    null,
    authHeaders.value
  );

  if (result.ok) {
    await loadApiKeys();
  }
}

function copyKey(key) {
  navigator.clipboard?.writeText(key);
}

/* SLEEP DATA */

const fields = [
  "time_in_bed",
  "awake_time",
  "light_sleep",
  "slow_wave",
  "rem",
  "disturbance",
  "baseline",
  "debt",
  "strain",
  "nap",
  "respiratory_rate",
  "performance",
  "consistency",
  "efficiency",
];

const sleepForm = reactive(
  Object.fromEntries(fields.map((field) => [field, 0]))
);

const targetId = ref("");
const listLimit = ref(20);

const apiKeyHeaders = computed(() => ({
  "X-API-Key": testApiKey.value.trim(),
}));

function hasApiKey() {
  return Boolean(testApiKey.value.trim());
}

function listSleepData() {
  if (!hasApiKey()) return;

  request(
    "GET",
    `/publicAPI/sleep-data?limit=${listLimit.value}`,
    null,
    apiKeyHeaders.value
  );
}

function getSleepData() {
  if (!hasApiKey() || !targetId.value) return;

  request(
    "GET",
    `/publicAPI/sleep-data/${targetId.value}`,
    null,
    apiKeyHeaders.value
  );
}

function createSleepData() {
  if (!hasApiKey()) return;

  request(
    "POST",
    "/publicAPI/sleep-data",
    { ...sleepForm },
    apiKeyHeaders.value
  );
}

function updateSleepData() {
  if (!hasApiKey() || !targetId.value) return;

  request(
    "PUT",
    `/publicAPI/sleep-data/${targetId.value}`,
    { ...sleepForm },
    apiKeyHeaders.value
  );
}

function deleteSleepData() {
  if (!hasApiKey() || !targetId.value) return;

  request(
    "DELETE",
    `/publicAPI/sleep-data/${targetId.value}`,
    null,
    apiKeyHeaders.value
  );
}
</script>

<template>
  <main class="api-playground">
    <header>
      <h1>Public API Playground</h1>

      <label>
        Base URL
        <input
          v-model="apiBase"
          placeholder="http://localhost:8000"
        />
      </label>
    </header>

    <section>
      <h2>API keys</h2>

      <div class="row">
        <input
          v-model="newKeyName"
          placeholder="Nombre de la API key"
          @keyup.enter="createApiKey"
        />

        <button class="accent" @click="createApiKey">
          Generar
        </button>

        <button @click="loadApiKeys">
          Refrescar
        </button>
      </div>

      <div v-if="createdKey" class="message">
        <p>Copia esta key ahora. No volverá a mostrarse.</p>

        <div class="row">
          <code>{{ createdKey.api_key }}</code>
          <button @click="copyKey(createdKey.api_key)">
            Copiar
          </button>
        </div>
      </div>

      <div v-if="apiKeys.length" class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Prefijo</th>
              <th>Activa</th>
              <th>Creada</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="key in apiKeys" :key="key.id">
              <td>{{ key.name }}</td>
              <td>{{ key.key_prefix }}…</td>
              <td>{{ key.active ? "Sí" : "No" }}</td>
              <td>{{ new Date(key.created_at).toLocaleString() }}</td>
              <td>
                <button class="danger" @click="revokeApiKey(key.id)">
                  Revocar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="muted">
        No hay API keys cargadas.
      </p>
    </section>

    <section>
      <h2>Probar sleep-data</h2>

      <input
        v-model="testApiKey"
        class="full-width"
        placeholder="X-API-Key"
      />

      <div class="two-columns">
        <article>
          <h3>Listar datos</h3>

          <input
            v-model.number="listLimit"
            type="number"
            min="1"
            placeholder="Límite"
          />

          <button @click="listSleepData">
            GET
          </button>
        </article>

        <article>
          <h3>Buscar o eliminar por ID</h3>

          <input
            v-model="targetId"
            placeholder="Sleep data ID"
          />

          <div class="row">
            <button @click="getSleepData">
              GET
            </button>

            <button class="danger" @click="deleteSleepData">
              DELETE
            </button>
          </div>
        </article>
      </div>

      <article>
        <h3>Crear o actualizar datos</h3>

        <div class="form-grid">
          <label v-for="field in fields" :key="field">
            {{ field }}

            <input
              v-model.number="sleepForm[field]"
              type="number"
              step="any"
            />
          </label>
        </div>

        <div class="row">
          <button class="accent" @click="createSleepData">
            POST
          </button>

          <button class="accent" @click="updateSleepData">
            PUT
          </button>
        </div>
      </article>
    </section>

    <section>
      <h2>Respuesta</h2>

      <div class="response-header">
        <strong>{{ response.method || "—" }}</strong>
        <span>{{ response.url || "Todavía no hay peticiones" }}</span>

        <span
          v-if="response.status !== null"
          :class="response.ok ? 'success' : 'error'"
        >
          {{ response.status }}
        </span>

        <span v-if="response.loading">
          Cargando...
        </span>
      </div>

      <pre>{{
        response.body !== null
          ? JSON.stringify(response.body, null, 2)
          : ""
      }}</pre>
    </section>
  </main>
</template>

<style scoped>
.api-playground {
  width: min(100%, 960px);
  margin: 0 auto;
  padding: 24px;
  color: white;
  background: #0f0f0f;
  font-family: monospace;
}

.api-playground *,
.api-playground *::before,
.api-playground *::after {
  box-sizing: border-box;
}

header,
section,
article {
  border: 1px solid #444;
  background: #171717;
}

header,
section {
  margin-bottom: 20px;
  padding: 20px;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

article {
  padding: 16px;
}

h1,
h2,
h3,
p,
label,
span,
strong,
code,
th,
td {
  color: white;
}

h1,
h2,
h3 {
  margin-top: 0;
}

h1 {
  margin-bottom: 0;
  font-size: 20px;
}

h2 {
  font-size: 17px;
}

h3 {
  font-size: 14px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

input,
button {
  min-height: 38px;
  padding: 8px 12px;
  color: white;
  background: #222;
  border: 1px solid #555;
  font: inherit;
}

input {
  width: 100%;
}

input::placeholder {
  color: #aaa;
}

input:focus,
button:hover {
  border-color: #b78cff;
  outline: none;
}

button {
  width: auto;
  cursor: pointer;
}

button.accent {
  border-color: #b78cff;
}

button.danger,
.error {
  color: #ff8c8c;
}

.success {
  color: #7cf0a6;
}

.row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 12px;
}

.row input {
  flex: 1;
  min-width: 220px;
}

.full-width {
  margin-bottom: 16px;
}

.two-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.message {
  margin: 16px 0;
  padding: 14px;
  border: 1px dashed #b78cff;
  background: #211a29;
}

.message code {
  overflow-wrap: anywhere;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #444;
}

.muted {
  color: #bbb;
}

.response-header {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}

pre {
  min-height: 100px;
  max-height: 420px;
  margin: 0;
  padding: 16px;
  overflow: auto;
  color: white;
  background: #080808;
  border: 1px solid #444;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

@media (max-width: 700px) {
  .api-playground {
    padding: 12px;
  }

  header {
    align-items: stretch;
    flex-direction: column;
  }

  .two-columns {
    grid-template-columns: 1fr;
  }
}
</style>