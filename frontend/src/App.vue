<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { lastViewedChallengeId } from './stores/challengeProgress.js'

const route = useRoute()

// Go to last challenge when clicking Challenges, otherwise to the list
const challengesLink = computed(() =>
  lastViewedChallengeId.value
    ? `/challenge/${lastViewedChallengeId.value}`
    : '/challenge'
)
</script>

<template>
  <div class="app">
    <header class="header">
      <router-link to="/" class="logo">
        <h1>Haskellito</h1>
      </router-link>
      <nav class="nav">
        <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">
          Playground
        </router-link>
        <router-link :to="challengesLink" class="nav-link" :class="{ active: route.path.startsWith('/challenge') }">
          Challenges
        </router-link>
      </nav>
    </header>

    <router-view />
  </div>
</template>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
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
