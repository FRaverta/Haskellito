import { computed, reactive } from 'vue'

const TOKEN_STORAGE_KEY = 'haskellito:cognitoTokens'
const AUTH_REQUEST_KEY = 'haskellito:cognitoAuthRequest'
const AUTH_REQUEST_STORAGE_PREFIX = `${AUTH_REQUEST_KEY}:`
export const AUTH_POPUP_MESSAGE = 'haskellito:cognitoPopupComplete'
export const AUTH_LOGIN_REQUIRED_EVENT = 'haskellito:authLoginRequired'
export const AUTH_STATE_CHANGED_EVENT = 'haskellito:authStateChanged'
const EXPIRY_SKEW_MS = 60_000
const AUTH_REQUEST_TTL_MS = 10 * 60 * 1000
const AUTH_POPUP_TIMEOUT_MS = 5 * 60 * 1000

function envFlag(value, defaultValue = false) {
  if (value == null || value === '') return defaultValue
  return ['1', 'true', 'yes', 'on'].includes(String(value).toLowerCase())
}

function normalizeDomain(domain) {
  const trimmed = (domain || '').trim().replace(/\/+$/, '')
  if (!trimmed) return ''
  return /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`
}

const config = {
  cognitoDomain: normalizeDomain(import.meta.env.VITE_COGNITO_DOMAIN),
  clientId: import.meta.env.VITE_COGNITO_APP_CLIENT_ID || '',
  redirectUri: import.meta.env.VITE_COGNITO_REDIRECT_URI || `${window.location.origin}/auth/callback`,
  logoutUri: import.meta.env.VITE_COGNITO_LOGOUT_URI || `${window.location.origin}/`,
  identityProvider: import.meta.env.VITE_COGNITO_IDENTITY_PROVIDER ?? 'Google',
  scopes: import.meta.env.VITE_COGNITO_SCOPES || 'openid email profile',
}

const explicitAuthEnabled = import.meta.env.VITE_AUTH_ENABLED
let refreshPromise = null
const authState = reactive({
  tokens: loadStoredTokens(),
  user: null,
  isRefreshing: false,
})

authState.user = decodeUser(authState.tokens?.idToken)

window.addEventListener('storage', (event) => {
  if (event.key === TOKEN_STORAGE_KEY) {
    syncStoredAuthState()
  }
})

export const authEnabled = computed(() => {
  const hasCognitoConfig = Boolean(config.cognitoDomain && config.clientId)
  return envFlag(explicitAuthEnabled, hasCognitoConfig)
})

export const isAuthenticated = computed(() => hasValidAccessToken())
export const currentUser = computed(() => authState.user)
export const userDisplayName = computed(() => {
  const user = currentUser.value
  return user?.name || user?.email || ''
})

function loadStoredTokens() {
  try {
    const raw = localStorage.getItem(TOKEN_STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch (error) {
    localStorage.removeItem(TOKEN_STORAGE_KEY)
    return null
  }
}

function storeTokens(tokens, reason = null) {
  const wasAuthenticated = hasValidAccessToken()
  authState.tokens = tokens
  authState.user = decodeUser(tokens?.idToken)
  if (tokens) {
    localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify(tokens))
  } else {
    localStorage.removeItem(TOKEN_STORAGE_KEY)
  }
  if (reason) {
    emitAuthStateChanged(reason, wasAuthenticated)
  }
}

function saveTokenResponse(tokenResponse, reason = null) {
  const expiresInSeconds = Number(tokenResponse.expires_in || 3600)
  storeTokens({
    accessToken: tokenResponse.access_token,
    idToken: tokenResponse.id_token,
    refreshToken: tokenResponse.refresh_token || authState.tokens?.refreshToken || null,
    expiresAt: Date.now() + expiresInSeconds * 1000,
  }, reason)
}

function hasValidAccessToken() {
  return Boolean(
    authState.tokens?.accessToken
    && authState.tokens.expiresAt
    && authState.tokens.expiresAt - EXPIRY_SKEW_MS > Date.now()
  )
}

function assertConfigured() {
  if (!config.cognitoDomain || !config.clientId) {
    throw new Error(
      'Cognito auth is enabled but VITE_COGNITO_DOMAIN and '
      + 'VITE_COGNITO_APP_CLIENT_ID are not configured.'
    )
  }
}

export async function ensureAuthenticated(returnTo = window.location.href) {
  if (!authEnabled.value) return true

  const token = await getAccessToken()
  if (token) return true

  requestLogin(returnTo)
  return false
}

export async function getAccessToken() {
  if (!authEnabled.value) return null
  if (hasValidAccessToken()) return authState.tokens.accessToken
  if (authState.tokens?.refreshToken) {
    try {
      await refreshTokens()
      if (hasValidAccessToken()) return authState.tokens.accessToken
    } catch (error) {
      storeTokens(null)
    }
  }
  return null
}

export async function signIn(returnTo = window.location.href) {
  assertConfigured()

  const { authorizationUrl } = await createAuthorizationRequest(returnTo, 'redirect')
  window.location.assign(authorizationUrl)
}

export async function signInWithPopup(returnTo = window.location.href) {
  assertConfigured()

  const popup = openAuthPopup()
  if (!popup) {
    throw new Error('Login popup was blocked. Allow popups for Haskellito and try again.')
  }

  try {
    const { authorizationUrl, state } = await createAuthorizationRequest(returnTo, 'popup')
    popup.location.assign(authorizationUrl)
    return waitForPopupCompletion(popup, state)
  } catch (error) {
    popup.close()
    throw error
  }
}

async function createAuthorizationRequest(returnTo, mode) {
  const state = randomString()
  const nonce = randomString()
  const codeVerifier = randomString(64)
  const codeChallenge = await pkceChallenge(codeVerifier)
  const authRequest = {
    state,
    nonce,
    codeVerifier,
    returnTo,
    mode,
    createdAt: Date.now(),
  }

  saveAuthRequest(authRequest)

  const params = new URLSearchParams({
    client_id: config.clientId,
    response_type: 'code',
    scope: config.scopes,
    redirect_uri: config.redirectUri,
    state,
    nonce,
    code_challenge_method: 'S256',
    code_challenge: codeChallenge,
  })

  if (config.identityProvider) {
    params.set('identity_provider', config.identityProvider)
  }

  return {
    authorizationUrl: `${config.cognitoDomain}/oauth2/authorize?${params}`,
    state,
  }
}

export async function completeSignInFromRedirect() {
  assertConfigured()

  const params = new URLSearchParams(window.location.search)
  const error = params.get('error')
  if (error) {
    throw new Error(params.get('error_description') || error)
  }

  const code = params.get('code')
  const state = params.get('state')
  if (!code || !state) {
    throw new Error('Missing Cognito authorization response.')
  }

  const authRequest = readAuthRequest(state)
  if (authRequest.state !== state) {
    throw new Error('Invalid Cognito state parameter.')
  }
  if (authRequest.createdAt + AUTH_REQUEST_TTL_MS < Date.now()) {
    clearAuthRequest(state)
    throw new Error('Cognito login request expired.')
  }

  const tokenResponse = await tokenRequest({
    grant_type: 'authorization_code',
    client_id: config.clientId,
    code,
    redirect_uri: config.redirectUri,
    code_verifier: authRequest.codeVerifier,
  })

  saveTokenResponse(tokenResponse, 'login')
  clearAuthRequest(state)
  return {
    returnTo: localRoute(authRequest.returnTo),
    state,
    popup: authRequest.mode === 'popup',
  }
}

export function signOut() {
  storeTokens(null, 'logout')

  if (!authEnabled.value) return
  assertConfigured()

  const params = new URLSearchParams({
    client_id: config.clientId,
    logout_uri: config.logoutUri,
  })
  window.location.assign(`${config.cognitoDomain}/logout?${params}`)
}

export function clearAuthSession() {
  storeTokens(null)
}

export function requestLogin(returnTo = window.location.href) {
  window.dispatchEvent(new CustomEvent(AUTH_LOGIN_REQUIRED_EVENT, {
    detail: {
      returnTo,
    },
  }))
}

export function syncStoredAuthState(reason = null) {
  const wasAuthenticated = hasValidAccessToken()
  authState.tokens = loadStoredTokens()
  authState.user = decodeUser(authState.tokens?.idToken)
  if (reason) {
    emitAuthStateChanged(reason, wasAuthenticated)
  }
}

async function refreshTokens() {
  if (refreshPromise) return refreshPromise
  refreshPromise = doRefreshTokens().finally(() => {
    refreshPromise = null
  })
  return refreshPromise
}

async function doRefreshTokens() {
  assertConfigured()
  authState.isRefreshing = true
  try {
    const tokenResponse = await tokenRequest({
      grant_type: 'refresh_token',
      client_id: config.clientId,
      refresh_token: authState.tokens.refreshToken,
    })
    saveTokenResponse(tokenResponse, 'refresh')
  } finally {
    authState.isRefreshing = false
  }
}

async function tokenRequest(fields) {
  const response = await fetch(`${config.cognitoDomain}/oauth2/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams(fields),
  })

  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Token request failed with ${response.status}`)
  }

  return response.json()
}

function saveAuthRequest(authRequest) {
  cleanupExpiredAuthRequests()
  const serialized = JSON.stringify(authRequest)
  sessionStorage.setItem(AUTH_REQUEST_KEY, serialized)
  localStorage.setItem(`${AUTH_REQUEST_STORAGE_PREFIX}${authRequest.state}`, serialized)
}

function readAuthRequest(state) {
  const sessionRequest = parseAuthRequest(sessionStorage.getItem(AUTH_REQUEST_KEY))
  if (sessionRequest?.state === state) return sessionRequest

  const storedRequest = parseAuthRequest(localStorage.getItem(`${AUTH_REQUEST_STORAGE_PREFIX}${state}`))
  if (storedRequest?.state === state) return storedRequest

  throw new Error('Missing Cognito login request.')
}

function parseAuthRequest(raw) {
  if (!raw) return null

  try {
    return JSON.parse(raw)
  } catch (error) {
    return null
  }
}

function clearAuthRequest(state) {
  const sessionRequest = parseAuthRequest(sessionStorage.getItem(AUTH_REQUEST_KEY))
  if (!state || sessionRequest?.state === state) {
    sessionStorage.removeItem(AUTH_REQUEST_KEY)
  }
  if (state) {
    localStorage.removeItem(`${AUTH_REQUEST_STORAGE_PREFIX}${state}`)
  }
}

function cleanupExpiredAuthRequests() {
  const expiresBefore = Date.now() - AUTH_REQUEST_TTL_MS
  for (let index = 0; index < localStorage.length; index += 1) {
    const key = localStorage.key(index)
    if (!key?.startsWith(AUTH_REQUEST_STORAGE_PREFIX)) continue
    const request = parseAuthRequest(localStorage.getItem(key))
    if (!request || request.createdAt < expiresBefore) {
      localStorage.removeItem(key)
      index -= 1
    }
  }
}

function openAuthPopup() {
  const width = 520
  const height = 720
  const left = Math.max(0, window.screenX + (window.outerWidth - width) / 2)
  const top = Math.max(0, window.screenY + (window.outerHeight - height) / 2)
  return window.open(
    'about:blank',
    'haskellito-login',
    [
      `width=${width}`,
      `height=${height}`,
      `left=${Math.round(left)}`,
      `top=${Math.round(top)}`,
      'popup=yes',
      'resizable=yes',
      'scrollbars=yes',
    ].join(',')
  )
}

function waitForPopupCompletion(popup, state) {
  return new Promise((resolve, reject) => {
    const startedAt = Date.now()
    let settled = false

    function settle(callback, value) {
      if (settled) return
      settled = true
      window.removeEventListener('message', handleMessage)
      window.removeEventListener('storage', handleStorage)
      window.clearInterval(popupCheckInterval)
      callback(value)
    }

    function handleMessage(event) {
      if (event.origin !== window.location.origin) return
      if (event.data?.type !== AUTH_POPUP_MESSAGE || event.data.state !== state) return

      if (event.data.status === 'success') {
        syncStoredAuthState('login')
        settle(resolve, event.data)
        return
      }

      settle(reject, new Error(event.data.message || 'Sign-in failed.'))
    }

    function handleStorage(event) {
      if (event.key !== TOKEN_STORAGE_KEY) return
      syncStoredAuthState('login')
      if (hasValidAccessToken()) {
        settle(resolve, {
          status: 'success',
          state,
        })
      }
    }

    const popupCheckInterval = window.setInterval(() => {
      if (popup.closed) {
        const wasAuthenticated = hasValidAccessToken()
        syncStoredAuthState()
        if (hasValidAccessToken()) {
          emitAuthStateChanged('login', wasAuthenticated)
          settle(resolve, {
            status: 'success',
            state,
          })
        } else {
          settle(reject, new Error('Login window was closed before sign-in completed.'))
        }
      } else if (Date.now() - startedAt > AUTH_POPUP_TIMEOUT_MS) {
        popup.close()
        settle(reject, new Error('Login window timed out. Please try again.'))
      }
    }, 500)

    window.addEventListener('message', handleMessage)
    window.addEventListener('storage', handleStorage)
  })
}

function localRoute(returnTo) {
  try {
    const url = new URL(returnTo || '/', window.location.origin)
    if (url.origin !== window.location.origin) return '/'
    return `${url.pathname}${url.search}${url.hash}` || '/'
  } catch (error) {
    return '/'
  }
}

function emitAuthStateChanged(reason, wasAuthenticated) {
  window.dispatchEvent(new CustomEvent(AUTH_STATE_CHANGED_EVENT, {
    detail: {
      reason,
      wasAuthenticated,
      isAuthenticated: hasValidAccessToken(),
      user: authState.user,
    },
  }))
}

function decodeUser(idToken) {
  const payload = decodeJwtPayload(idToken)
  if (!payload) return null
  return {
    sub: payload.sub,
    email: payload.email,
    name: payload.name
      || [payload.given_name, payload.family_name].filter(Boolean).join(' ')
      || payload['cognito:username'],
  }
}

function decodeJwtPayload(token) {
  if (!token) return null
  const [, payload] = token.split('.')
  if (!payload) return null

  try {
    const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
    const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, '=')
    const bytes = Uint8Array.from(atob(padded), (char) => char.charCodeAt(0))
    return JSON.parse(new TextDecoder().decode(bytes))
  } catch (error) {
    return null
  }
}

function randomString(byteLength = 32) {
  const bytes = new Uint8Array(byteLength)
  crypto.getRandomValues(bytes)
  return base64Url(bytes)
}

async function pkceChallenge(codeVerifier) {
  const bytes = new TextEncoder().encode(codeVerifier)
  const digest = await crypto.subtle.digest('SHA-256', bytes)
  return base64Url(new Uint8Array(digest))
}

function base64Url(bytes) {
  const binary = String.fromCharCode(...bytes)
  return btoa(binary)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '')
}
