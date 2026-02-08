<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { lastViewedChallengeId } from './stores/challengeProgress.js'
import { setLocale, getLocale } from './i18n.js'

const route = useRoute()
const { t } = useI18n()

// Go to last challenge when clicking Challenges, otherwise to the list
const challengesLink = computed(() =>
  lastViewedChallengeId.value
    ? `/challenge/${lastViewedChallengeId.value}`
    : '/challenge'
)

function switchLocale(locale) {
  setLocale(locale)
}
</script>

<template>
  <div class="app">
    <header class="header">
      <router-link to="/" class="logo">
        <h1>Haskellito</h1>
      </router-link>
      <nav class="nav">
        <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">
          {{ t('nav.playground') }}
        </router-link>
        <router-link :to="challengesLink" class="nav-link" :class="{ active: route.path.startsWith('/challenge') }">
          {{ t('nav.challenges') }}
        </router-link>
        <span class="locale-switcher">
          <button
            type="button"
            class="locale-btn"
            :class="{ active: getLocale() === 'en' }"
            @click="switchLocale('en')"
          >
            EN
          </button>
          <button
            type="button"
            class="locale-btn"
            :class="{ active: getLocale() === 'es' }"
            @click="switchLocale('es')"
          >
            ES
          </button>
        </span>
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
  padding: 0.75rem 1.5rem;
  background: #1e1e2e;
  border-bottom: 1px solid #313244;
}

.logo {
  text-decoration: none;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #cdd6f4;
  font-weight: 600;
}

.logo:hover h1 {
  color: #89b4fa;
}

.nav {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.locale-switcher {
  display: flex;
  gap: 0.25rem;
  margin-left: 0.5rem;
}

.locale-btn {
  padding: 0.25rem 0.5rem;
  border: 1px solid #313244;
  border-radius: 4px;
  background: transparent;
  color: #a6adc8;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.locale-btn:hover {
  background: #313244;
  color: #cdd6f4;
}

.locale-btn.active {
  background: #89b4fa;
  color: #1e1e2e;
  border-color: #89b4fa;
}

.nav-link {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #a6adc8;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #313244;
  color: #cdd6f4;
}

.nav-link.active {
  background: #89b4fa;
  color: #1e1e2e;
}
</style>
