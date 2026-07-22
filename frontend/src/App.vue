<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { lastViewedChallengeId } from './stores/challengeProgress.js'
import { theme, setTheme } from './stores/theme.js'
import { setLocale, getLocale } from './i18n.js'
import {
  AUTH_LOGIN_REQUIRED_EVENT,
  authEnabled,
  isAuthenticated,
  signInWithPopup,
  signOut,
  userDisplayName,
} from './auth/cognito.js'
import haskellitoLogo from './assets/haskellito.svg'

const AUTH_NOTICE_KEY = 'haskellito:authNotice'

const route = useRoute()
const { t } = useI18n()
const currentLocale = computed(() => getLocale())
const currentTheme = computed(() => theme.value)
const accountMenuOpen = ref(false)
const loginInProgress = ref(false)
const authError = ref('')
const accountMenuRef = ref(null)
const loginRequiredOpen = ref(false)
const loginRequiredReturnTo = ref(window.location.href)
const notification = ref(null)
let notificationTimeout = null

// Go to last challenge when clicking Challenges, otherwise to the list
const challengesLink = computed(() =>
  lastViewedChallengeId.value
    ? `/challenge/${lastViewedChallengeId.value}`
    : '/challenge'
)
const accountButtonLabel = computed(() => {
  if (isAuthenticated.value) {
    return userDisplayName.value || t('auth.signedIn')
  }
  return t('auth.account')
})
const accountInitial = computed(() => accountButtonLabel.value.trim().charAt(0).toUpperCase() || 'A')

function switchLocale(locale) {
  setLocale(locale)
}

function switchTheme(nextTheme) {
  setTheme(nextTheme)
}

function toggleAccountMenu() {
  authError.value = ''
  accountMenuOpen.value = !accountMenuOpen.value
}

async function performSignIn(returnTo = window.location.href) {
  authError.value = ''
  loginInProgress.value = true
  try {
    await signInWithPopup(returnTo)
    showNotification(t('auth.loggedInAs', {
      name: userDisplayName.value || t('auth.signedIn'),
    }))
    accountMenuOpen.value = false
    loginRequiredOpen.value = false
  } catch (error) {
    console.error(error)
    authError.value = error.message || t('auth.signInFailed')
  } finally {
    loginInProgress.value = false
  }
}

function handleSignIn() {
  performSignIn(window.location.href)
}

function handleLoginRequiredSignIn() {
  performSignIn(loginRequiredReturnTo.value)
}

function handleSignOut() {
  const name = userDisplayName.value || t('auth.signedIn')
  persistNotification('auth.loggedOutUser', { name })
  authError.value = ''
  accountMenuOpen.value = false
  signOut()
}

function handleLoginRequired(event) {
  if (!authEnabled.value || isAuthenticated.value) return
  authError.value = ''
  accountMenuOpen.value = false
  loginRequiredReturnTo.value = event.detail?.returnTo || window.location.href
  loginRequiredOpen.value = true
}

function closeLoginRequired() {
  if (loginInProgress.value) return
  loginRequiredOpen.value = false
  authError.value = ''
}

function showNotification(message, variant = 'success') {
  if (notificationTimeout) {
    window.clearTimeout(notificationTimeout)
  }
  notification.value = {
    message,
    variant,
  }
  notificationTimeout = window.setTimeout(() => {
    notification.value = null
    notificationTimeout = null
  }, 5000)
}

function persistNotification(key, values = {}, variant = 'success') {
  try {
    sessionStorage.setItem(AUTH_NOTICE_KEY, JSON.stringify({
      key,
      values,
      variant,
    }))
  } catch (error) {
    // Ignore storage failures; the redirect can continue without the notice.
  }
}

function showPersistedNotification() {
  try {
    const raw = sessionStorage.getItem(AUTH_NOTICE_KEY)
    sessionStorage.removeItem(AUTH_NOTICE_KEY)
    if (!raw) return
    const notice = JSON.parse(raw)
    showNotification(t(notice.key, notice.values || {}), notice.variant || 'success')
  } catch (error) {
    sessionStorage.removeItem(AUTH_NOTICE_KEY)
  }
}

function handleDocumentPointerDown(event) {
  if (!accountMenuOpen.value) return
  if (accountMenuRef.value?.contains(event.target)) return
  accountMenuOpen.value = false
}

function handleDocumentKeyDown(event) {
  if (event.key === 'Escape') {
    accountMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('pointerdown', handleDocumentPointerDown)
  document.addEventListener('keydown', handleDocumentKeyDown)
  window.addEventListener(AUTH_LOGIN_REQUIRED_EVENT, handleLoginRequired)
  showPersistedNotification()
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', handleDocumentPointerDown)
  document.removeEventListener('keydown', handleDocumentKeyDown)
  window.removeEventListener(AUTH_LOGIN_REQUIRED_EVENT, handleLoginRequired)
  if (notificationTimeout) {
    window.clearTimeout(notificationTimeout)
  }
})
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
          <div v-if="authEnabled" ref="accountMenuRef" class="account-menu">
            <button
              type="button"
              class="account-menu-button"
              :aria-expanded="accountMenuOpen"
              :aria-label="t('auth.accountMenu')"
              aria-haspopup="menu"
              @click.stop="toggleAccountMenu"
            >
              <span class="account-avatar" aria-hidden="true">{{ accountInitial }}</span>
              <span class="account-label">{{ accountButtonLabel }}</span>
              <span class="account-caret" aria-hidden="true"></span>
            </button>
            <div v-if="accountMenuOpen" class="account-popover" role="menu">
              <div v-if="isAuthenticated" class="account-user">
                {{ userDisplayName || t('auth.signedIn') }}
              </div>
              <button
                v-if="isAuthenticated"
                type="button"
                class="account-menu-item"
                role="menuitem"
                @click="handleSignOut"
              >
                {{ t('auth.logout') }}
              </button>
              <button
                v-else
                type="button"
                class="account-menu-item"
                role="menuitem"
                :disabled="loginInProgress"
                @click="handleSignIn"
              >
                {{ loginInProgress ? t('auth.loggingIn') : t('auth.login') }}
              </button>
              <p v-if="authError" class="account-error">
                {{ authError }}
              </p>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <div class="app-content">
      <router-view />
    </div>

    <div
      v-if="notification"
      class="app-notification"
      :class="`app-notification-${notification.variant}`"
      role="status"
      aria-live="polite"
    >
      {{ notification.message }}
    </div>

    <div
      v-if="loginRequiredOpen"
      class="modal-backdrop"
      @click.self="closeLoginRequired"
    >
      <section
        class="login-required-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="login-required-title"
      >
        <h2 id="login-required-title">{{ t('auth.loginRequiredTitle') }}</h2>
        <p>{{ t('auth.loginRequiredMessage') }}</p>
        <p v-if="authError" class="login-required-error">
          {{ authError }}
        </p>
        <div class="login-required-actions">
          <button
            type="button"
            class="modal-btn modal-btn-secondary"
            :disabled="loginInProgress"
            @click="closeLoginRequired"
          >
            {{ t('auth.cancel') }}
          </button>
          <button
            type="button"
            class="modal-btn modal-btn-primary"
            :disabled="loginInProgress"
            @click="handleLoginRequiredSignIn"
          >
            {{ loginInProgress ? t('auth.loggingIn') : t('auth.loginWithGoogle') }}
          </button>
        </div>
      </section>
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

.app-notification {
  position: fixed;
  top: 4.25rem;
  right: 1rem;
  z-index: 40;
  width: min(24rem, calc(100vw - 2rem));
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-success);
  border-radius: 8px;
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: var(--shadow-elevated);
  font-size: 0.875rem;
  line-height: 1.35;
}

.app-notification-success {
  border-color: var(--color-success);
  background: color-mix(in srgb, var(--color-success) 14%, var(--color-surface));
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: grid;
  place-items: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.55);
}

.login-required-modal {
  width: min(28rem, 100%);
  padding: 1.25rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: var(--shadow-elevated);
}

.login-required-modal h2 {
  margin: 0 0 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
}

.login-required-modal p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 0.875rem;
  line-height: 1.45;
}

.login-required-error {
  margin-top: 0.75rem !important;
  color: var(--color-danger) !important;
}

.login-required-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.modal-btn {
  min-height: 2.25rem;
  padding: 0.5rem 0.875rem;
  border: 0;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
}

.modal-btn:disabled {
  opacity: 0.65;
  cursor: wait;
}

.modal-btn-primary {
  background: var(--color-accent);
  color: var(--color-accent-contrast);
}

.modal-btn-secondary {
  background: var(--color-surface-strong);
  color: var(--color-text);
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
  align-items: center;
}

.account-menu {
  position: relative;
}

.account-menu-button {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  min-height: 2rem;
  max-width: 15rem;
  padding: 0.25rem 0.5rem 0.25rem 0.375rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-surface-raised);
  color: var(--color-text);
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.account-avatar {
  display: inline-grid;
  place-items: center;
  width: 1.375rem;
  height: 1.375rem;
  flex: 0 0 auto;
  border-radius: 50%;
  background: var(--color-accent);
  color: var(--color-accent-contrast);
  font-size: 0.6875rem;
  font-weight: 700;
}

.account-label {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-caret {
  width: 0;
  height: 0;
  flex: 0 0 auto;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 5px solid currentColor;
  opacity: 0.7;
}

.account-popover {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  z-index: 20;
  display: flex;
  width: min(17rem, calc(100vw - 2rem));
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.375rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-surface);
  box-shadow: var(--shadow-elevated);
}

.account-user {
  padding: 0.5rem 0.625rem;
  color: var(--color-text-muted);
  font-size: 0.75rem;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-menu-item {
  width: 100%;
  min-height: 2rem;
  padding: 0.375rem 0.625rem;
  border: 0;
  border-radius: 4px;
  background: transparent;
  color: var(--color-text);
  text-align: left;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
}

.account-error {
  margin: 0.25rem 0.25rem 0;
  color: var(--color-danger);
  font-size: 0.75rem;
  line-height: 1.35;
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

.account-menu-button:hover,
.account-menu-item:hover:not(:disabled) {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.account-menu-item:disabled {
  color: var(--color-text-disabled);
  cursor: wait;
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

  .account-menu {
    order: 3;
  }

  .account-menu-button {
    max-width: 11rem;
  }

  .logo h1 {
    font-size: 1.25rem;
  }
}
</style>
