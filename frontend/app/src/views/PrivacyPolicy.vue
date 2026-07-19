<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { RouterLink } from 'vue-router'

const previousTitle = document.title

onMounted(() => {
  document.title = 'Privacy Policy | KingOfTheSleep'

  let description = document.querySelector('meta[name="description"]')

  if (!description) {
    description = document.createElement('meta')
    description.setAttribute('name', 'description')
    document.head.appendChild(description)
  }

  description.setAttribute(
    'content',
    'Privacy Policy for the KingOfTheSleep educational web application.',
  )
})

onBeforeUnmount(() => {
  document.title = previousTitle
})
</script>

<template>
  <div class="legal-page">
    <a class="skip-link" href="#main-content"> Skip to main content </a>

    <header class="legal-header">
      <div class="header-inner">
        <RouterLink class="brand" to="/"> KingOfTheSleep </RouterLink>

        <nav aria-label="Legal pages">
          <RouterLink to="/privacy" aria-current="page"> Privacy Policy </RouterLink>

          <RouterLink to="/terms"> Terms of Service </RouterLink>
        </nav>
      </div>
    </header>

    <main id="main-content">
      <article>
        <h1>Privacy Policy</h1>

        <p class="meta">
          <strong>Effective date:</strong>
          19 July 2026
        </p>

        <div class="summary">
          <strong>Summary:</strong>
          KingOfTheSleep is an educational project. Personal data is used only to operate and
          evaluate this project. All project data will be permanently deleted after the project
          evaluation has been completed.
        </div>

        <h2>1. Who is responsible for the project?</h2>

        <p>
          KingOfTheSleep is a student project developed for educational and evaluation purposes.
          Questions about privacy or data deletion can be sent to
          <a href="mailto:eloymart@student.42urduliz.com"> eloymart@student.42urduliz.com </a>.
        </p>

        <h2>2. Data we collect</h2>

        <p>The application may process the following data:</p>

        <ul>
          <li>Email address.</li>
          <li>Username and authentication credentials.</li>
          <li>Profile information and avatar.</li>
          <li>Sleep-related values voluntarily entered by the user.</li>
          <li>Game parameters, scores, rankings, match results and activity data.</li>
          <li>Technical information strictly necessary to operate and secure the service.</li>
        </ul>
        <h2>3. Public and private information</h2>
        <p>
          A user's email address is private and is not shown to other users. Authentication
          credentials are also private.
        </p>
        <p>
          Other profile and game-related information may be public inside the application, including
          the username, avatar, sleep-game parameters, scores, rankings, match information and other
          data used to calculate or display game features.
        </p>

        <h2>4. How the data is used</h2>
        <p>Data is used exclusively to:</p>
        <ul>
          <li>Create, authenticate and manage user accounts.</li>
          <li>Display profiles, rankings and game activity.</li>
          <li>Calculate parameters and mechanics used by the game.</li>
          <li>Operate, test, secure and evaluate the KingOfTheSleep project.</li>
        </ul>
        <p>
          Data will not be sold, used for advertising, or used for purposes unrelated to this
          educational project.
        </p>

        <h2>5. Chat messages</h2>
        <p>
          Chat messages are not stored in the server database and no server-side chat history is
          created. The chat operates in a pseudo peer-to-peer manner: the server only relays
          messages between connected users and does not keep a persistent record of their content.
        </p>
        <p>
          Messages may exist temporarily in memory for the time strictly necessary to transmit them
          to the intended recipient.
        </p>

        <h2>6. Account deletion</h2>
        <p>
          Users can request account deletion from <strong>User Settings</strong>. After the request
          is submitted, the account and its associated stored data are scheduled for automatic
          permanent deletion at <strong>00:00 server local time on the same calendar day</strong>.
        </p>
        <p>
          Once deletion has been completed, the account and associated data cannot be recovered.
        </p>

        <h2>7. End-of-project deletion</h2>
        <p>
          Regardless of individual deletion requests, all personal data and project databases will
          be permanently deleted after the official project evaluation is completed, except where a
          limited technical backup must be retained temporarily to complete the deletion process.
        </p>

        <h2>8. Data retention</h2>
        <p>
          Data is retained only for as long as necessary to operate and evaluate the project, or
          until the user requests account deletion. Chat content is not retained as a server-side
          history.
        </p>

        <h2>9. Data sharing</h2>
        <p>
          Data is not shared with advertisers or sold to third parties. Public profile and game
          information is visible to other users of KingOfTheSleep as described in this policy. Data
          may also be viewed by project evaluators when necessary to assess the application's
          functionality.
        </p>

        <h2>10. Security</h2>
        <p>
          Reasonable technical measures are used to protect account information, including access
          controls, input validation, HTTPS for browser-to-server communication and secure password
          hashing. No online service can guarantee absolute security.
        </p>

        <h2>11. User rights and contact</h2>
        <p>
          Users may review or update their profile through User Settings and may request account
          deletion through the same section. Privacy-related questions can be sent to
          <a href="mailto:eloymart@student.42urduliz.com">eloymart@student.42urduliz.com</a>.
        </p>

        <h2>12. Changes to this policy</h2>

        <p>
          This policy may be updated when the project's functionality changes. The latest version
          will always be available from the application's legal links.
        </p>
      </article>
    </main>

    <footer class="legal-footer">
      <p>
        <RouterLink to="/privacy"> Privacy Policy </RouterLink>

        <span aria-hidden="true"> · </span>

        <RouterLink to="/terms"> Terms of Service </RouterLink>
      </p>

      <p>&copy; 2026 KingOfTheSleep — Educational project.</p>
    </footer>
  </div>
</template>

<style scoped>
.legal-page {
  color-scheme: light dark;

  --legal-bg: #f6f7fb;
  --legal-surface: #ffffff;
  --legal-text: #1f2937;
  --legal-muted: #5f6b7a;
  --legal-border: #dce1e8;
  --legal-accent: #4f46e5;
  --legal-accent-soft: #eef2ff;
  --legal-max-width: 880px;

  min-height: 100vh;
  background: var(--legal-bg);
  color: var(--legal-text);
  font-family:
    Inter,
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;
  line-height: 1.65;
}

.legal-page,
.legal-page * {
  box-sizing: border-box;
}

.legal-page a {
  color: var(--legal-accent);
}

.legal-page a:hover,
.legal-page a:focus-visible {
  text-decoration-thickness: 2px;
}

.skip-link {
  position: fixed;
  top: 1rem;
  left: -9999px;
  z-index: 1000;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background: var(--legal-surface);
  color: var(--legal-text);
}

.skip-link:focus {
  left: 1rem;
}

.legal-header {
  border-bottom: 1px solid var(--legal-border);
  background: var(--legal-surface);
}

.header-inner,
.legal-page main,
.legal-footer {
  width: min(calc(100% - 2rem), var(--legal-max-width));
  margin-inline: auto;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 72px;
  gap: 1rem;
}

.brand {
  color: var(--legal-text) !important;
  font-weight: 800;
  letter-spacing: -0.02em;
  text-decoration: none;
}

nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
}

nav a {
  font-weight: 600;
  text-decoration: none;
}

nav a.router-link-active {
  text-decoration: underline;
  text-underline-offset: 0.3rem;
}

.legal-page main {
  padding-block: 3rem;
}

article {
  padding: clamp(1.25rem, 3vw, 2.5rem);
  border: 1px solid var(--legal-border);
  border-radius: 18px;
  background: var(--legal-surface);
  box-shadow: 0 18px 50px rgb(17 24 39 / 6%);
}

h1,
h2 {
  line-height: 1.2;
  letter-spacing: -0.025em;
}

h1 {
  margin-top: 0;
  font-size: clamp(2rem, 6vw, 3.3rem);
}

h2 {
  margin-top: 2.2rem;
  font-size: 1.35rem;
}

p,
li {
  max-width: 75ch;
}

.meta {
  margin-top: -0.75rem;
  margin-bottom: 2rem;
  color: var(--legal-muted);
}

.summary {
  padding: 1rem 1.1rem;
  border: 1px solid #c7d2fe;
  border-radius: 12px;
  background: var(--legal-accent-soft);
}

ul {
  padding-left: 1.3rem;
}

.legal-footer {
  padding-block: 0 2.5rem;
  color: var(--legal-muted);
  text-align: center;
}

.legal-footer a {
  margin-inline: 0.35rem;
}

@media (prefers-color-scheme: dark) {
  .legal-page {
    --legal-bg: #0f172a;
    --legal-surface: #111827;
    --legal-text: #f3f4f6;
    --legal-muted: #b8c0cc;
    --legal-border: #2f3a4a;
    --legal-accent: #a5b4fc;
    --legal-accent-soft: #1e1b4b;
  }

  article {
    box-shadow: none;
  }
}

@media (max-width: 620px) {
  .header-inner {
    align-items: flex-start;
    flex-direction: column;
    padding-block: 1rem;
  }

  .legal-page main {
    padding-block: 1.5rem;
  }
}
</style>
