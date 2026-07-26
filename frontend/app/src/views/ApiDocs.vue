<script setup>
import { reactive } from "vue";

const fields = [
  { name: "time_in_bed", type: "number", desc: "Total time spent in bed." },
  { name: "awake_time", type: "number", desc: "Time spent awake during the recorded period." },
  { name: "light_sleep", type: "number", desc: "Duration of light sleep." },
  { name: "slow_wave", type: "number", desc: "Duration of deep or slow-wave sleep." },
  { name: "rem", type: "number", desc: "Duration of REM sleep." },
  { name: "disturbance", type: "number", desc: "Value associated with disturbances or interruptions." },
  { name: "baseline", type: "number", desc: "User's baseline reference value." },
  { name: "debt", type: "number", desc: "Estimated sleep debt." },
  { name: "strain", type: "number", desc: "Strain or load level." },
  { name: "nap", type: "number", desc: "Nap duration or value." },
  { name: "respiratory_rate", type: "number", desc: "Respiratory rate." },
  { name: "performance", type: "number", desc: "Performance score." },
  { name: "consistency", type: "number", desc: "Consistency score." },
  { name: "efficiency", type: "number", desc: "Sleep efficiency score." },
];

const sleepPayload = `{
  "time_in_bed": 480,
  "awake_time": 35,
  "light_sleep": 220,
  "slow_wave": 90,
  "rem": 135,
  "disturbance": 2,
  "baseline": 80,
  "debt": 15,
  "strain": 45,
  "nap": 0,
  "respiratory_rate": 14.2,
  "performance": 87,
  "consistency": 82,
  "efficiency": 91
}`;

const sleepPayloadUpdated = `{
  "time_in_bed": 500,
  "awake_time": 30,
  "light_sleep": 225,
  "slow_wave": 100,
  "rem": 145,
  "disturbance": 1,
  "baseline": 80,
  "debt": 10,
  "strain": 40,
  "nap": 0,
  "respiratory_rate": 14,
  "performance": 91,
  "consistency": 85,
  "efficiency": 94
}`;

const sections = [
  {
    title: "API key management",
    intro:
      "These endpoints require a valid session and the Authorization: Bearer <JWT_TOKEN> header.",
    endpoints: [
      {
        id: "get-api-keys",
        method: "GET",
        path: "/admin/apikeys",
        description:
          "Returns the API keys associated with the authenticated user. The full key is not normally returned; only information such as name, prefix, status, and creation date is shown.",
        headers: [
          { name: "Authorization", value: "Bearer <JWT_TOKEN>", required: true },
        ],
        curl: `curl -X GET "http://localhost:8000/admin/apikeys" \\
  -H "Authorization: Bearer JWT_TOKEN"`,
        response: `[
  {
    "id": 12,
    "name": "telegram bot",
    "key_prefix": "kots_ab12",
    "active": true,
    "created_at": "2026-07-22T18:00:00"
  }
]`,
        statuses: [
          { code: "200 OK", type: "success" },
          { code: "401 Unauthorized", type: "error" },
        ],
      },
      {
        id: "post-api-key",
        method: "POST",
        path: "/admin/apikeys",
        description:
          "Creates a new API key. The response includes the full key so the user can save it.",
        body: [{ name: "name", type: "string", required: true }],
        curl: `curl -X POST "http://localhost:8000/admin/apikeys" \\
  -H "Authorization: Bearer JWT_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "telegram bot"
  }'`,
        response: `{
  "id": 12,
  "name": "telegram bot",
  "api_key": "kots_generated_full_key"
}`,
        statuses: [
          { code: "200 / 201", type: "success" },
          { code: "400 Bad Request", type: "error" },
          { code: "401 Unauthorized", type: "error" },
        ],
      },
      {
        id: "delete-api-key",
        method: "DELETE",
        path: "/admin/apikeys/{id}",
        description: "Revokes or deletes an API key by its identifier.",
        pathParams: [{ name: "id", type: "integer or string", required: true }],
        curl: `curl -X DELETE "http://localhost:8000/admin/apikeys/12" \\
  -H "Authorization: Bearer JWT_TOKEN"`,
        statuses: [
          { code: "200 / 204", type: "success" },
          { code: "401 Unauthorized", type: "error" },
          { code: "404 Not Found", type: "error" },
        ],
      },
    ],
  },
  {
    title: "Sleep-data endpoints",
    intro: "All of these endpoints require the X-API-Key header.",
    endpoints: [
      {
        id: "get-sleep-data",
        method: "GET",
        path: "/publicAPI/sleep-data",
        description: "Returns a list of sleep records.",
        query: [
          {
            name: "limit",
            type: "integer",
            desc: "Maximum number of records. The tester uses 20 by default.",
            optional: true,
          },
        ],
        curl: `curl -X GET "http://localhost:8000/publicAPI/sleep-data?limit=20" \\
  -H "X-API-Key: kots_your_api_key"`,
        response: `[
  {
    "id": 42,
${sleepPayload
  .split("\n")
  .slice(1, -1)
  .map((line) => "    " + line.trim())
  .join("\n")}
  }
]`,
        statuses: [
          { code: "200 OK", type: "success" },
          { code: "401 Unauthorized", type: "error" },
          { code: "429 Too Many Requests", type: "error" },
        ],
      },
      {
        id: "get-sleep-data-id",
        method: "GET",
        path: "/publicAPI/sleep-data/{id}",
        description: "Fetches a single sleep record by its ID.",
        pathParams: [{ name: "id", type: "integer or string", required: true }],
        curl: `curl -X GET "http://localhost:8000/publicAPI/sleep-data/42" \\
  -H "X-API-Key: kots_your_api_key"`,
        statuses: [
          { code: "200 OK", type: "success" },
          { code: "401 Unauthorized", type: "error" },
          { code: "404 Not Found", type: "error" },
          { code: "429 Too Many Requests", type: "error" },
        ],
      },
      {
        id: "post-sleep-data",
        method: "POST",
        path: "/publicAPI/sleep-data",
        description: "Creates a new sleep record.",
        curl: `curl -X POST "http://localhost:8000/publicAPI/sleep-data" \\
  -H "X-API-Key: kots_your_api_key" \\
  -H "Content-Type: application/json" \\
  -d '${sleepPayload}'`,
        statuses: [
          { code: "200 / 201", type: "success" },
          { code: "400 Bad Request", type: "error" },
          { code: "401 Unauthorized", type: "error" },
          { code: "422 Validation Error", type: "error" },
          { code: "429 Too Many Requests", type: "error" },
        ],
      },
      {
        id: "put-sleep-data",
        method: "PUT",
        path: "/publicAPI/sleep-data/{id}",
        description:
          "Replaces the content of an existing record. Since this is a PUT request, the client should send the full object.",
        curl: `curl -X PUT "http://localhost:8000/publicAPI/sleep-data/42" \\
  -H "X-API-Key: kots_your_api_key" \\
  -H "Content-Type: application/json" \\
  -d '${sleepPayloadUpdated}'`,
        statuses: [
          { code: "200 OK", type: "success" },
          { code: "400 Bad Request", type: "error" },
          { code: "401 Unauthorized", type: "error" },
          { code: "404 Not Found", type: "error" },
          { code: "422 Validation Error", type: "error" },
          { code: "429 Too Many Requests", type: "error" },
        ],
      },
      {
        id: "delete-sleep-data",
        method: "DELETE",
        path: "/publicAPI/sleep-data/{id}",
        description: "Deletes a sleep record by its ID.",
        curl: `curl -X DELETE "http://localhost:8000/publicAPI/sleep-data/42" \\
  -H "X-API-Key: kots_your_api_key"`,
        statuses: [
          { code: "200 / 204", type: "success" },
          { code: "401 Unauthorized", type: "error" },
          { code: "404 Not Found", type: "error" },
          { code: "429 Too Many Requests", type: "error" },
        ],
      },
    ],
  },
];

const errorFormat = `{
  "detail": "Descriptive error message"
}`;

const copiedState = reactive({});

async function copy(key, text) {
  try {
    await navigator.clipboard.writeText(text);
    copiedState[key] = true;
    setTimeout(() => {
      copiedState[key] = false;
    }, 1200);
  } catch {
    copiedState[key] = "error";
    setTimeout(() => {
      copiedState[key] = false;
    }, 1200);
  }
}

function copyLabel(key) {
  if (copiedState[key] === true) return "Copied";
  if (copiedState[key] === "error") return "Couldn't copy";
  return "Copy";
}

function methodClass(method) {
  return method.toLowerCase();
}
</script>

<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <strong>&gt; KOTS API</strong>
        <span>Endpoint documentation</span>
      </div>

      <nav>
        <div class="nav-title">Introduction</div>
        <a href="#overview">Overview</a>
        <a href="#authentication">Authentication</a>
        <a href="#model">Sleep-data model</a>

        <template v-for="section in sections" :key="section.title">
          <div class="nav-title">{{ section.title }}</div>
          <a
            v-for="endpoint in section.endpoints"
            :key="endpoint.id"
            :href="`#${endpoint.id}`"
          >
            <span class="nav-method" :class="methodClass(endpoint.method)">
              {{ endpoint.method }}
            </span>
            {{ endpoint.description.split(".")[0] }}
          </a>
        </template>

        <div class="nav-title">Reference</div>
        <a href="#errors">Status codes & errors</a>
      </nav>
    </aside>

    <main class="main">
      <section id="overview" class="hero">
        <p class="eyebrow">KingOfTheSleep</p>
        <h1>Public API</h1>

        <p class="hero-description">
          Reference for managing API keys and reading, creating, updating, or
          deleting sleep records via HTTP requests.
        </p>

        <div class="base-url">
          <span>Base URL</span>
          <code>http://localhost:8000</code>
        </div>
      </section>

      <section id="authentication" class="section">
        <h2>Authentication</h2>

        <p class="section-intro">
          The API uses two separate authentication systems. Administrative
          endpoints use the user's session JWT, while the public sleep-data
          endpoints use an API key.
        </p>

        <div class="auth-grid">
          <article class="info-card">
            <h3>JWT for administration</h3>
            <p>Used on the <code>/admin/apikeys</code> endpoints.</p>
            <div class="code-box">
              <pre>Authorization: Bearer &lt;JWT_TOKEN&gt;</pre>
            </div>
          </article>

          <article class="info-card">
            <h3>API key for the Public API</h3>
            <p>
              Used on all <code>/publicAPI/sleep-data</code> endpoints.
            </p>
            <div class="code-box">
              <pre>X-API-Key: kots_your_api_key</pre>
            </div>
          </article>
        </div>

        <div class="notice">
          <strong>Important:</strong>
          the full API key should only be shown when it's created. Keep it
          somewhere safe and never publish it in the frontend, repositories,
          or screenshots.
        </div>
      </section>

      <section id="model" class="section">
        <h2>Sleep-data model</h2>

        <p class="section-intro">
          The POST and PUT endpoints receive a JSON object with the following
          numeric fields.
        </p>

        <table class="fields-table">
          <thead>
            <tr>
              <th>Field</th>
              <th>Type</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="field in fields" :key="field.name">
              <td><code>{{ field.name }}</code></td>
              <td>{{ field.type }}</td>
              <td>{{ field.desc }}</td>
            </tr>
          </tbody>
        </table>

        <div class="notice">
          Units, allowed ranges, and required fields should match the schemas
          defined in the backend. The descriptions above are indicative,
          based on the field names.
        </div>
      </section>

      <section v-for="section in sections" :key="section.title" class="section">
        <h2>{{ section.title }}</h2>
        <p class="section-intro">{{ section.intro }}</p>

        <article
          v-for="endpoint in section.endpoints"
          :id="endpoint.id"
          :key="endpoint.id"
          class="endpoint"
        >
          <div class="endpoint-header">
            <span class="method" :class="methodClass(endpoint.method)">
              {{ endpoint.method }}
            </span>
            <code class="endpoint-path">{{ endpoint.path }}</code>
          </div>

          <div class="endpoint-body">
            <p class="endpoint-description">{{ endpoint.description }}</p>

            <div v-if="endpoint.headers" class="block">
              <div class="block-title">Headers</div>
              <table>
                <thead>
                  <tr><th>Name</th><th>Value</th><th>Required</th></tr>
                </thead>
                <tbody>
                  <tr v-for="header in endpoint.headers" :key="header.name">
                    <td><code>{{ header.name }}</code></td>
                    <td><code>{{ header.value }}</code></td>
                    <td>
                      <span v-if="header.required" class="required">YES</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="endpoint.pathParams" class="block">
              <div class="block-title">Path parameters</div>
              <table>
                <thead>
                  <tr><th>Parameter</th><th>Type</th><th>Required</th></tr>
                </thead>
                <tbody>
                  <tr v-for="param in endpoint.pathParams" :key="param.name">
                    <td><code>{{ param.name }}</code></td>
                    <td>{{ param.type }}</td>
                    <td>
                      <span v-if="param.required" class="required">YES</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="endpoint.query" class="block">
              <div class="block-title">Query parameters</div>
              <table>
                <thead>
                  <tr><th>Parameter</th><th>Type</th><th>Description</th></tr>
                </thead>
                <tbody>
                  <tr v-for="param in endpoint.query" :key="param.name">
                    <td><code>{{ param.name }}</code></td>
                    <td>{{ param.type }}</td>
                    <td>
                      {{ param.desc }}
                      <span v-if="param.optional" class="optional">OPTIONAL</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="endpoint.body" class="block">
              <div class="block-title">JSON body</div>
              <table>
                <thead>
                  <tr><th>Field</th><th>Type</th><th>Required</th></tr>
                </thead>
                <tbody>
                  <tr v-for="field in endpoint.body" :key="field.name">
                    <td><code>{{ field.name }}</code></td>
                    <td>{{ field.type }}</td>
                    <td>
                      <span v-if="field.required" class="required">YES</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="endpoint.curl" class="block">
              <div class="block-title">cURL example</div>
              <div class="code-box">
                <button
                  class="copy-button"
                  @click="copy(`${endpoint.id}-curl`, endpoint.curl)"
                >
                  {{ copyLabel(`${endpoint.id}-curl`) }}
                </button>
                <pre>{{ endpoint.curl }}</pre>
              </div>
            </div>

            <div v-if="endpoint.response" class="block">
              <div class="block-title">Sample response</div>
              <div class="code-box">
                <button
                  class="copy-button"
                  @click="copy(`${endpoint.id}-response`, endpoint.response)"
                >
                  {{ copyLabel(`${endpoint.id}-response`) }}
                </button>
                <pre>{{ endpoint.response }}</pre>
              </div>
            </div>

            <div class="block">
              <span
                v-for="status in endpoint.statuses"
                :key="status.code"
                class="status"
                :class="status.type"
              >
                {{ status.code }}
              </span>
            </div>
          </div>
        </article>
      </section>

      <section id="errors" class="section">
        <h2>Status codes & errors</h2>

        <p class="section-intro">
          The exact codes depend on the backend implementation. These are the
          typical statuses an API like this returns.
        </p>

        <div class="status-grid">
          <article class="info-card">
            <h3>Success responses</h3>
            <p><span class="status success">200 OK</span> Request completed.</p>
            <p><span class="status success">201 Created</span> Resource created.</p>
            <p><span class="status success">204 No Content</span> Successful operation with no body.</p>
          </article>

          <article class="info-card">
            <h3>Error responses</h3>
            <p><span class="status error">400</span> Invalid data.</p>
            <p><span class="status error">401</span> Invalid JWT or API key.</p>
            <p><span class="status error">404</span> Resource not found.</p>
            <p><span class="status error">422</span> Validation error.</p>
            <p><span class="status error">429</span> Rate limit exceeded.</p>
          </article>
        </div>

        <div class="block">
          <div class="block-title">Sample error format</div>
          <div class="code-box">
            <button class="copy-button" @click="copy('error-format', errorFormat)">
              {{ copyLabel("error-format") }}
            </button>
            <pre>{{ errorFormat }}</pre>
          </div>
        </div>
      </section>

      <footer class="footer">
        Documentation generated from the endpoints used by the Public API
        Playground component. Check the backend schemas to fill in exact
        types, ranges, units, and responses.
      </footer>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 270px minmax(0, 1fr);
  min-height: 100vh;
  color: white;
  background: #0f0f0f;
  font-family: monospace;
}

.layout *,
.layout *::before,
.layout *::after {
  box-sizing: border-box;
}

a {
  color: inherit;
  text-decoration: none;
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  padding: 28px 20px;
  overflow-y: auto;
  background: #171717;
  border-right: 1px solid #444;
}

.brand {
  margin-bottom: 28px;
}

.brand strong {
  display: block;
  color: #b78cff;
  font-size: 19px;
}

.brand span {
  color: #aaa;
  font-size: 13px;
}

.nav-title {
  margin: 22px 10px 8px;
  color: #aaa;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

nav a {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-bottom: 4px;
  padding: 9px 10px;
  color: white;
  border: 1px solid transparent;
}

nav a:hover {
  border-color: #b78cff;
}

.nav-method {
  min-width: 48px;
  font-size: 11px;
  font-weight: 800;
}

.main {
  width: min(100%, 1120px);
  padding: 48px 56px 80px;
}

.hero {
  padding-bottom: 38px;
  border-bottom: 1px solid #444;
}

.eyebrow {
  margin: 0 0 8px;
  color: #b78cff;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: clamp(32px, 5vw, 56px);
  line-height: 1.1;
}

.hero-description {
  max-width: 720px;
  margin: 18px 0 24px;
  color: #bbb;
  font-size: 17px;
}

.base-url {
  display: flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  max-width: 100%;
  padding: 10px 14px;
  background: #171717;
  border: 1px solid #444;
}

.base-url span {
  color: #aaa;
  font-size: 13px;
}

.base-url code {
  overflow-wrap: anywhere;
  color: white;
  font-size: 14px;
}

.section {
  padding-top: 48px;
}

h2 {
  margin: 0 0 14px;
  font-size: 29px;
}

h3 {
  margin: 0 0 10px;
  font-size: 18px;
}

p {
  margin-top: 0;
}

.section-intro {
  max-width: 760px;
  margin-bottom: 24px;
  color: #bbb;
}

.notice {
  margin: 22px 0;
  padding: 16px 18px;
  background: #211a29;
  border: 1px solid #b78cff;
  border-left: 4px solid #b78cff;
}

.notice strong {
  color: #b78cff;
}

.auth-grid,
.status-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.info-card {
  padding: 20px;
  background: #171717;
  border: 1px solid #444;
}

.info-card p:last-child {
  margin-bottom: 0;
}

.endpoint {
  margin-top: 28px;
  overflow: hidden;
  background: #171717;
  border: 1px solid #444;
}

.endpoint-header {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 17px 20px;
  background: #1c1c1c;
  border-bottom: 1px solid #444;
}

.method {
  min-width: 68px;
  padding: 5px 9px;
  text-align: center;
  border: 1px solid currentColor;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.04em;
}

.get {
  color: #70b7ff;
}

.post {
  color: #7cf0a6;
}

.put {
  color: #ffb86b;
}

.delete {
  color: #ff8c8c;
}

.endpoint-path {
  min-width: 0;
  overflow-wrap: anywhere;
  color: white;
  font-size: 15px;
  font-weight: 700;
}

.endpoint-body {
  padding: 22px;
}

.endpoint-description {
  color: #bbb;
}

.block {
  margin-top: 24px;
}

.block-title {
  margin-bottom: 9px;
  color: #e6e6ec;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.code-box {
  position: relative;
  overflow: hidden;
  background: #080808;
  border: 1px solid #444;
}

pre {
  margin: 0;
  padding: 18px;
  overflow-x: auto;
  color: white;
  font-size: 13px;
  line-height: 1.65;
  white-space: pre;
}

.copy-button {
  position: absolute;
  top: 9px;
  right: 9px;
  padding: 6px 10px;
  color: white;
  cursor: pointer;
  background: #222;
  border: 1px solid #555;
  font: inherit;
  font-size: 11px;
}

.copy-button:hover {
  border-color: #b78cff;
}

table {
  width: 100%;
  overflow: hidden;
  border-collapse: collapse;
  background: #171717;
  border: 1px solid #444;
  font-size: 14px;
}

th,
td {
  padding: 11px 13px;
  text-align: left;
  vertical-align: top;
  border-bottom: 1px solid #444;
  color: white;
}

th {
  color: #aaa;
  background: #1c1c1c;
  font-size: 12px;
  text-transform: uppercase;
}

tr:last-child td {
  border-bottom: 0;
}

td code {
  color: #d39bff;
  overflow-wrap: anywhere;
}

.required {
  color: #ff8c8c;
  font-size: 11px;
  font-weight: 800;
}

.optional {
  color: #aaa;
  font-size: 11px;
}

.status {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  margin: 3px 7px 3px 0;
  padding: 5px 9px;
  background: #080808;
  border: 1px solid #444;
  font-size: 12px;
}

.status.success {
  color: #7cf0a6;
}

.status.error {
  color: #ff8c8c;
}

.fields-table td:first-child {
  width: 27%;
}

.footer {
  margin-top: 60px;
  padding-top: 24px;
  color: #aaa;
  border-top: 1px solid #444;
  font-size: 13px;
}

@media (max-width: 900px) {
  .layout {
    display: block;
  }

  .sidebar {
    position: static;
    width: 100%;
    height: auto;
    border-right: 0;
    border-bottom: 1px solid #444;
  }

  nav {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .main {
    padding: 36px 24px 60px;
  }
}

@media (max-width: 620px) {
  nav,
  .auth-grid,
  .status-grid {
    grid-template-columns: 1fr;
  }

  .endpoint-header {
    align-items: flex-start;
    flex-direction: column;
  }

  th,
  td {
    padding: 9px;
    font-size: 12px;
  }

  .fields-table td:first-child {
    width: auto;
  }
}
</style>