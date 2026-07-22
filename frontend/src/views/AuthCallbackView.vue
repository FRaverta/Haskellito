<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { AUTH_POPUP_MESSAGE, completeSignInFromRedirect } from '../auth/cognito.js'

const router = useRouter()
const { t } = useI18n()
const errorMessage = ref('')
const closingPopup = ref(false)

onMounted(async () => {
  try {
    const result = await completeSignInFromRedirect()
    if (result.popup) {
      const notified = notifyOpener({
        status: 'success',
        state: result.state,
        returnTo: result.returnTo,
      })
      closingPopup.value = true
      window.setTimeout(() => {
        window.close()
      }, notified ? 100 : 500)
      if (!notified) {
        window.setTimeout(() => {
          router.replace(result.returnTo)
        }, 1000)
      }
      return
    }

    router.replace(result.returnTo)
  } catch (error) {
    const state = new URLSearchParams(window.location.search).get('state')
    notifyOpener({
      status: 'error',
      state,
      message: error.message,
    })
    errorMessage.value = error.message
  }
})

function notifyOpener(payload) {
  if (!window.opener || window.opener.closed) return false
  window.opener.postMessage(
    {
      type: AUTH_POPUP_MESSAGE,
      ...payload,
    },
    window.location.origin
  )
  return true
}
</script>

<template>
  <main class="auth-callback">
    <div v-if="errorMessage" class="auth-message auth-message-error">
      <h2>{{ t('auth.signInFailed') }}</h2>
      <p>{{ errorMessage }}</p>
      <router-link to="/" class="btn btn-primary">
        {{ t('auth.backToApp') }}
      </router-link>
    </div>
    <div v-else class="auth-message">
      <h2 v-if="closingPopup">{{ t('auth.closingPopup') }}</h2>
      <h2 v-else>{{ t('auth.signingIn') }}</h2>
    </div>
  </main>
</template>

<style scoped>
.auth-callback {
  display: grid;
  place-items: center;
  min-height: 100%;
  padding: 2rem;
  background: var(--color-bg);
  color: var(--color-text);
}

.auth-message {
  width: min(100%, 32rem);
  padding: 1.5rem;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.auth-message h2 {
  margin: 0 0 0.75rem;
  color: var(--color-text);
}

.auth-message p {
  margin: 0 0 1rem;
  color: var(--color-text-muted);
}

.auth-message-error h2 {
  color: var(--color-danger);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
}

.btn-primary {
  background: var(--color-accent);
  color: var(--color-accent-contrast);
}
</style>
