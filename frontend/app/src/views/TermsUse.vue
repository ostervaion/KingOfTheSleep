<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { RouterLink } from 'vue-router'

let previousTitle = ''
let descriptionMeta = null
let previousDescription = ''

onMounted(() => {
  previousTitle = document.title
  document.title = 'Terms of Service | KingOfTheSleep'

  descriptionMeta = document.querySelector('meta[name="description"]')

  if (!descriptionMeta) {
    descriptionMeta = document.createElement('meta')
    descriptionMeta.setAttribute('name', 'description')
    document.head.appendChild(descriptionMeta)
  } else {
    previousDescription = descriptionMeta.getAttribute('content') ?? ''
  }

  descriptionMeta.setAttribute(
    'content',
    'Terms of Service for the KingOfTheSleep educational web application.',
  )
})

onBeforeUnmount(() => {
  document.title = previousTitle

  if (descriptionMeta) {
    descriptionMeta.setAttribute('content', previousDescription)
  }
})
</script>

<template>
  <div class="legal-page">
    <a class="skip-link" href="#main-content"> Skip to main content </a>

    <header class="legal-header">
      <div class="header-inner">
        <RouterLink class="brand" to="/"> KingOfTheSleep </RouterLink>

        <nav aria-label="Legal pages">
          <RouterLink to="/privacy"> Privacy Policy </RouterLink>

          <RouterLink to="/terms" aria-current="page"> Terms of Service </RouterLink>
        </nav>
      </div>
    </header>

    <main id="main-content">
      <article>
        <h1>Terms of Service</h1>

        <p class="meta">
          <strong>Effective date:</strong>
          19 July 2026
        </p>

        <div class="summary">
          <strong>Summary:</strong>
          KingOfTheSleep is a temporary educational project. By using it, you agree to use it
          lawfully and respectfully. All project data will be permanently deleted after the project
          evaluation.
        </div>

        <h2>1. About KingOfTheSleep</h2>

        <p>
          KingOfTheSleep is a student-built web application created exclusively for educational,
          demonstration and evaluation purposes.
        </p>

        <p>
          It is not a commercial service and may be modified, interrupted or discontinued at any
          time.
        </p>

        <h2>2. Acceptance of these terms</h2>

        <p>
          By creating an account or using the application, you agree to these Terms of Service and
          to the
          <RouterLink to="/privacy"> Privacy Policy </RouterLink>.
        </p>

        <p>You should not use the application if you do not agree with these terms.</p>

        <h2>3. Account registration</h2>

        <p>
          Users must provide accurate information and are responsible for keeping their login
          credentials confidential.
        </p>

        <p>
          Users must not access another person's account without permission or attempt to bypass
          authentication or authorization controls.
        </p>

        <h2>4. Public and private information</h2>

        <p>
          The user's email address and authentication credentials are private and are not displayed
          to other users.
        </p>

        <p>
          Other profile and game-related information may be publicly visible inside the application.
          This may include:
        </p>

        <ul>
          <li>Username.</li>
          <li>Avatar.</li>
          <li>Sleep-related game parameters.</li>
          <li>Scores and rankings.</li>
          <li>Match information and results.</li>
          <li>Game activity required for the application's features.</li>
        </ul>

        <p>
          This information is used exclusively to calculate, operate and display game-related
          features.
        </p>

        <h2>5. Permitted use</h2>

        <p>
          Users may use KingOfTheSleep only for its intended educational and game-related purposes.
        </p>

        <p>Users must not:</p>

        <ul>
          <li>Harass, threaten, impersonate or abuse other users.</li>

          <li>Upload unlawful, offensive, malicious or rights-infringing content.</li>

          <li>Cheat, manipulate rankings or interfere with game results.</li>

          <li>Attempt to exploit, attack, overload or disrupt the application.</li>

          <li>Attempt to access accounts, information or systems without authorization.</li>

          <li>Use automated tools to scrape, spam or interfere with the service.</li>

          <li>Introduce malware, malicious scripts or harmful files.</li>
        </ul>

        <h2>6. User-provided content</h2>

        <p>
          Users remain responsible for profile information, avatars and any other content they
          submit to the application.
        </p>

        <p>
          By uploading content, the user confirms that they have the right to use it and grants the
          project the limited permission necessary to store, process and display it within
          KingOfTheSleep.
        </p>

        <h2>7. Chat system</h2>

        <p>Chat messages are transmitted through the server using a pseudo peer-to-peer model.</p>

        <p>
          The server only relays messages between connected users. It does not create or retain a
          persistent server-side chat history.
        </p>

        <p>
          Messages may remain temporarily in server memory only for the time necessary to transmit
          them to the intended recipient.
        </p>

        <p>Users remain fully responsible for the messages they send.</p>

        <h2>8. Sleep-related information</h2>

        <div class="notice">
          <strong>Important:</strong>
          KingOfTheSleep is a game and an educational project. Sleep scores, parameters,
          recommendations, calculations and visualisations are not medical advice, a medical
          diagnosis or a substitute for assistance from a qualified healthcare professional.
        </div>

        <h2>9. Account suspension or removal</h2>

        <p>Access may be restricted, suspended or permanently removed when a user:</p>

        <ul>
          <li>Violates these Terms of Service.</li>
          <li>Threatens the security of the project.</li>
          <li>Disrupts the experience of other users.</li>
          <li>Misuses the application or its functionality.</li>
          <li>Attempts to manipulate game information or rankings.</li>
        </ul>

        <h2>10. Account deletion</h2>

        <p>
          Users can request account deletion from
          <strong>User Settings</strong>.
        </p>

        <p>
          After the deletion request has been submitted, the account and all associated stored data
          will be scheduled for automatic and permanent deletion at
          <strong> 00:00 server local time on the same calendar day </strong>.
        </p>

        <p>The deleted information may include:</p>

        <ul>
          <li>Account information.</li>
          <li>Profile information.</li>
          <li>Uploaded avatar.</li>
          <li>Sleep-related values.</li>
          <li>Scores and rankings.</li>
          <li>Match results and game activity.</li>
        </ul>

        <p>
          Once deletion has been completed, the account and associated data cannot be recovered.
        </p>

        <h2>11. End of the project</h2>

        <p>
          All personal data, account information and project databases will be permanently deleted
          after the official project evaluation has been completed.
        </p>

        <p>The service may then be taken offline without further notice.</p>

        <h2>12. Availability and changes</h2>

        <p>
          Because KingOfTheSleep is an educational project, uninterrupted availability is not
          guaranteed.
        </p>

        <p>
          Features, accounts, rankings or game information may be modified, reset or removed during
          development, testing or evaluation.
        </p>

        <p>
          These Terms of Service may also be updated when the application's functionality changes.
        </p>

        <h2>13. Disclaimer and limitation of responsibility</h2>

        <p>
          The application is provided on an “as is” and “as available” basis exclusively for
          educational purposes.
        </p>

        <p>
          To the extent permitted by applicable law, the project team is not responsible for losses
          resulting from:
        </p>

        <ul>
          <li>Temporary service interruptions.</li>
          <li>User misuse of the application.</li>
          <li>Loss of game progress or ranking information.</li>
          <li>Inaccurate game calculations.</li>
          <li>Reliance on sleep-related information as medical guidance.</li>
        </ul>

        <h2>14. Privacy</h2>

        <p>
          Information about data collection, visibility, use, retention and deletion is available in
          the
          <RouterLink to="/privacy"> Privacy Policy </RouterLink>.
        </p>

        <h2>15. Contact</h2>

        <p>
          Questions about these terms can be sent to
          <a href="mailto:eloymart@student.42urduliz.com"> eloymart@student.42urduliz.com </a>.
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
  --legal-warning-bg: #fff7ed;
  --legal-warning-border: #fdba74;
  --legal-warning-text: #9a3412;
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

.summary,
.notice {
  padding: 1rem 1.1rem;
  border-radius: 12px;
}

.summary {
  border: 1px solid #c7d2fe;
  background: var(--legal-accent-soft);
}

.notice {
  border: 1px solid var(--legal-warning-border);
  background: var(--legal-warning-bg);
  color: var(--legal-warning-text);
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
    --legal-warning-bg: #431407;
    --legal-warning-border: #9a3412;
    --legal-warning-text: #fed7aa;
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
