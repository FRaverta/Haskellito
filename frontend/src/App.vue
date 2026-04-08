<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { lastViewedChallengeId } from './stores/challengeProgress.js'
import { theme, setTheme } from './stores/theme.js'
import { setLocale, getLocale } from './i18n.js'
import haskellitoLogo from './assets/haskellito.svg'

const route = useRoute()
const { t } = useI18n()
const currentLocale = computed(() => getLocale())
const currentTheme = computed(() => theme.value)

// Go to last challenge when clicking Challenges, otherwise to the list
const challengesLink = computed(() =>
  lastViewedChallengeId.value
    ? `/challenge/${lastViewedChallengeId.value}`
    : '/challenge'
)

function switchLocale(locale) {
  setLocale(locale)
}

function switchTheme(nextTheme) {
  setTheme(nextTheme)
}
</script>

<template>
  <div class="app">
    <header class="header">
      <router-link to="/" class="logo">
        <img :src="haskellitoLogo" alt="Haskellito" class="logo-icon" />
        <h1>Haskellito</h1>
      </router-link>
      <nav class="nav">
        <div class="nav-links">
          <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">
            {{ t('nav.playground') }}
          </router-link>
          <router-link :to="challengesLink" class="nav-link" :class="{ active: route.path.startsWith('/challenge') }">
            {{ t('nav.challenges') }}
          </router-link>
        </div>
        <div class="nav-controls">
          <span class="theme-switcher" role="group" :aria-label="t('theme.label')">
            <button
              type="button"
              class="theme-btn"
              :class="{ active: currentTheme === 'light' }"
              @click="switchTheme('light')"
            >
              {{ t('theme.light') }}
            </button>
            <button
              type="button"
              class="theme-btn"
              :class="{ active: currentTheme === 'dark' }"
              @click="switchTheme('dark')"
            >
              {{ t('theme.dark') }}
            </button>
          </span>
          <span class="locale-switcher" role="group" aria-label="Language">
            <button
              type="button"
              class="locale-btn"
              :class="{ active: currentLocale === 'en' }"
              @click="switchLocale('en')"
            >
              EN
            </button>
            <button
              type="button"
              class="locale-btn"
              :class="{ active: currentLocale === 'es' }"
              @click="switchLocale('es')"
            >
              ES
            </button>
          </span>
        </div>
      </nav>
    </header>

    <div class="app-content">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh; /* use dynamic viewport so layout fits visible area on mobile */
  max-height: 100svh; /* cap at small viewport so toolbar stays visible on phones (incl. desktop mode) */
  width: 100vw;
  overflow: hidden;
}

.app-content {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
}

.logo {
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 0;
}

.logo-icon {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--color-text);
  font-weight: 600;
}

.logo:hover h1 {
  color: var(--color-accent);
}

.nav {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.nav-links,
.nav-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.theme-switcher,
.locale-switcher {
  display: flex;
  gap: 0.25rem;
}

.theme-btn,
.locale-btn {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.theme-btn:hover,
.locale-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.theme-btn.active,
.locale-btn.active {
  background: var(--color-accent);
  color: var(--color-accent-contrast);
  border-color: var(--color-accent);
}

.nav-link {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: all 0.2s;
}

.nav-link:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.nav-link.active {
  background: var(--color-accent);
  color: var(--color-accent-contrast);
}

@media (max-width: 720px) {
  .header {
    padding: 0.75rem 1rem;
  }

  .nav {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .nav-links,
  .nav-controls {
    justify-content: space-between;
  }

  .logo h1 {
    font-size: 1.25rem;
  }
}
</style>
