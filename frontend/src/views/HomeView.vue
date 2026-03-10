<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'
import CodeEditor from '../components/CodeEditor.vue'
import Interpreter from '../components/Interpreter.vue'
import { encodeSharedCode, decodeSharedCode } from '../utils/shareCodec.js'

const { t } = useI18n()

const API_V1 = '/api/playground'
const API_V2 = '/api/v2/playground'
const DEFAULT_CODE = `-- Welcome to Haskellito!
-- Write your Haskell code here

-- Example: Simple function
double x = x * 2

-- Try evaluating: double 21
`

const apiMode = ref('shared')
const apiBase = computed(() => apiMode.value === 'dedicated' ? API_V1 : API_V2)

const code = ref(DEFAULT_CODE)

const output = ref([])
const sessionId = ref(null)
const isConnected = ref(false)
const isLoading = ref(false)
const serverHistory = ref([])
const fileInputRef = ref(null)
let lastLoadedShareFragment = null

async function startSession() {
  try {
    const response = await axios.post(`${apiBase.value}/sessions/`)
    sessionId.value = response.data.session_id
    isConnected.value = true
    serverHistory.value = []
    output.value.push({ type: 'system', text: t('playground.sessionStarted') })
  } catch (error) {
    output.value.push({ type: 'error', text: t('errors.error', { msg: error.message }) })
  }
}

async function evaluate() {
  if (!sessionId.value) {
    output.value.push({ type: 'error', text: t('playground.noSession') })
    return
  }

  isLoading.value = true
  const codeToEval = code.value
  output.value.push({ type: 'system', text: t('playground.loadingFromEditor') })

  const isShared = apiMode.value === 'shared'
  if (isShared) {
    serverHistory.value = []
  }

  const payload = isShared
    ? { history: [], code: codeToEval }
    : { code: codeToEval }

  try {
    const response = await axios.post(
      `${apiBase.value}/sessions/${sessionId.value}/eval`,
      payload
    )

    if (response.data.error) {
      output.value.push({ type: 'error', text: response.data.error })
    } else if (response.data.output) {
      output.value.push({ type: 'output', text: response.data.output })
      if (isShared) serverHistory.value.push(codeToEval)
    } else {
      output.value.push({ type: 'system', text: t('playground.loaded') })
      if (isShared) serverHistory.value.push(codeToEval)
    }
  } catch (error) {
    output.value.push({ type: 'error', text: t('errors.evalFailed', { msg: error.message }) })
  } finally {
    isLoading.value = false
  }
}

async function evaluateCommand(command) {
  if (!sessionId.value) {
    output.value.push({ type: 'error', text: t('playground.noSessionShort') })
    return
  }

  isLoading.value = true
  output.value.push({ type: 'input', text: command })

  const isShared = apiMode.value === 'shared'
  const payload = isShared
    ? { history: [...serverHistory.value], code: command }
    : { code: command }

  try {
    const response = await axios.post(
      `${apiBase.value}/sessions/${sessionId.value}/eval`,
      payload
    )

    if (response.data.history_failed) {
      serverHistory.value = []
      output.value.push({ type: 'error', text: response.data.error })
      output.value.push({ type: 'system', text: t('playground.historyCleared') })
    } else if (response.data.error) {
      output.value.push({ type: 'error', text: response.data.error })
    } else {
      if (response.data.output) {
        output.value.push({ type: 'output', text: response.data.output })
      }
      if (isShared) serverHistory.value.push(command)
    }
  } catch (error) {
    output.value.push({ type: 'error', text: t('errors.error', { msg: error.message }) })
  } finally {
    isLoading.value = false
  }
}

async function closeSession() {
  if (!sessionId.value) return

  try {
    await axios.post(`${apiBase.value}/sessions/${sessionId.value}/close`)
    output.value.push({ type: 'system', text: t('playground.sessionClosed') })
  } catch (error) {
    // Ignore errors on close
  } finally {
    sessionId.value = null
    isConnected.value = false
    serverHistory.value = []
  }
}

// Clear output
function clearOutput() {
  output.value = []
}

function applySharedCodeFromHash(rawHash = window.location.hash) {
  const hash = typeof rawHash === 'string' ? rawHash : window.location.hash

  if (!hash || hash === '#') {
    lastLoadedShareFragment = null
    return
  }

  const fragment = hash.startsWith('#') ? hash.slice(1) : hash

  if (!fragment) {
    lastLoadedShareFragment = null
    return
  }

  if (fragment === lastLoadedShareFragment) {
    return
  }

  try {
    code.value = decodeSharedCode(fragment)
    lastLoadedShareFragment = fragment
    output.value.push({ type: 'system', text: t('playground.sharedCodeLoaded') })
  } catch (error) {
    output.value.push({
      type: 'error',
      text: t('playground.shareDecodeFailed', { msg: error.message })
    })
  }
}

async function shareCode() {
  const fragment = encodeSharedCode(code.value)
  const url = new URL(window.location.href)

  url.hash = fragment
  window.history.replaceState(null, '', url.toString())
  lastLoadedShareFragment = fragment

  try {
    await navigator.clipboard.writeText(url.toString())
    output.value.push({ type: 'system', text: t('playground.shareCopied') })
  } catch (error) {
    output.value.push({ type: 'system', text: t('playground.shareReady') })
    output.value.push({ type: 'output', text: url.toString() })
  }
}

function saveCodeToFile() {
  const blob = new Blob([code.value], { type: 'text/x-haskell;charset=utf-8' })
  const objectUrl = URL.createObjectURL(blob)
  const link = document.createElement('a')

  link.href = objectUrl
  link.download = 'playground.hs'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(objectUrl)

  output.value.push({ type: 'system', text: t('playground.fileSaved') })
}

function openLoadDialog() {
  fileInputRef.value?.click()
}

async function loadCodeFromFile(event) {
  const input = event.target
  const [file] = input.files ?? []

  if (!file) {
    return
  }

  try {
    code.value = await file.text()
    output.value.push({
      type: 'system',
      text: t('playground.fileLoaded', { name: file.name })
    })
  } catch (error) {
    output.value.push({
      type: 'error',
      text: t('playground.fileLoadFailed', { msg: error.message })
    })
  } finally {
    input.value = ''
  }
}

// --- Resizable splitter logic ---
const splitPercent = ref(50) // editor width as a percentage
const isDragging = ref(false)
const mainRef = ref(null)

const editorStyle = computed(() => ({
  flex: 'none',
  width: `${splitPercent.value}%`,
}))
const interpreterStyle = computed(() => ({
  flex: 'none',
  width: `${100 - splitPercent.value}%`,
}))

function onSplitterPointerDown(e) {
  e.preventDefault()
  isDragging.value = true
  document.addEventListener('pointermove', onPointerMove)
  document.addEventListener('pointerup', onPointerUp)
}

function onPointerMove(e) {
  if (!isDragging.value || !mainRef.value) return
  const rect = mainRef.value.getBoundingClientRect()
  let percent = ((e.clientX - rect.left) / rect.width) * 100
  // Clamp between 20% and 80%
  percent = Math.min(80, Math.max(20, percent))
  splitPercent.value = percent
}

function onPointerUp() {
  isDragging.value = false
  document.removeEventListener('pointermove', onPointerMove)
  document.removeEventListener('pointerup', onPointerUp)
}

// Keyboard shortcut for evaluation
function handleKeydown(event) {
  if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
    event.preventDefault()
    evaluate()
  }
}

onMounted(() => {
  applySharedCodeFromHash()
  window.addEventListener('keydown', handleKeydown)
  window.addEventListener('hashchange', applySharedCodeFromHash)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('hashchange', applySharedCodeFromHash)
  document.removeEventListener('pointermove', onPointerMove)
  document.removeEventListener('pointerup', onPointerUp)
  closeSession()
})
</script>

<template>
  <div class="home-view">
    <main ref="mainRef" class="main" :class="{ 'is-dragging': isDragging }">
      <div class="panel editor-panel" :style="editorStyle">
        <div class="panel-header">
          <span>{{ t('playground.editor') }}</span>
          <div class="panel-header-actions">
            <button
              type="button"
              class="icon-btn"
              :title="t('playground.loadTooltip')"
              :aria-label="t('playground.loadTooltip')"
              @click="openLoadDialog"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M12 16V5m0 0-4 4m4-4 4 4M5 19h14"
                  fill="none"
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.8"
                />
              </svg>
            </button>
            <button
              type="button"
              class="icon-btn"
              :title="t('playground.saveTooltip')"
              :aria-label="t('playground.saveTooltip')"
              @click="saveCodeToFile"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M5 20h14V8.5L15.5 5H5v15Zm3-10h8m-8 4h8"
                  fill="none"
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.8"
                />
                <path
                  d="M9 5v4h6"
                  fill="none"
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.8"
                />
              </svg>
            </button>
            <button
              type="button"
              class="icon-btn"
              :title="t('playground.shareTooltip')"
              :aria-label="t('playground.shareTooltip')"
              @click="shareCode"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M14 6 20 12 14 18M20 12H9"
                  fill="none"
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.8"
                />
                <path
                  d="M12 6H7a3 3 0 0 0-3 3v6a3 3 0 0 0 3 3h5"
                  fill="none"
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.8"
                />
              </svg>
            </button>
          </div>
        </div>
        <input
          ref="fileInputRef"
          type="file"
          accept=".hs,.lhs,text/x-haskell,text/plain"
          class="file-input"
          @change="loadCodeFromFile"
        />
        <CodeEditor v-model="code" />
      </div>

      <div
        class="splitter"
        @pointerdown="onSplitterPointerDown"
      >
        <div class="splitter-handle" />
      </div>

      <div class="panel interpreter-panel" :style="interpreterStyle">
        <div class="panel-header">
          {{ t('playground.ghciConsole') }}
          <span v-if="isConnected" class="status connected">{{ t('playground.connected') }}</span>
          <span v-else class="status disconnected">{{ t('playground.disconnected') }}</span>
        </div>
        <Interpreter 
          :output="output" 
          :is-connected="isConnected"
          :is-loading="isLoading"
          @submit="evaluateCommand"
        />
      </div>
    </main>

    <div class="toolbar">
      <div v-show="false" class="mode-toggle" :class="{ disabled: isConnected }">
        <button
          class="mode-btn"
          :class="{ active: apiMode === 'dedicated' }"
          :disabled="isConnected"
          @click="apiMode = 'dedicated'"
        >{{ t('playground.modeDedicated') }}</button>
        <button
          class="mode-btn"
          :class="{ active: apiMode === 'shared' }"
          :disabled="isConnected"
          @click="apiMode = 'shared'"
        >{{ t('playground.modeShared') }}</button>
      </div>
      <button 
        v-if="!isConnected" 
        @click="startSession" 
        class="btn btn-primary"
      >
        {{ t('playground.connect') }}
      </button>
      <button 
        v-else 
        @click="closeSession" 
        class="btn btn-secondary"
      >
        {{ t('playground.disconnect') }}
      </button>
      <button 
        @click="evaluate" 
        :disabled="!isConnected || isLoading"
        class="btn btn-success"
      >
        {{ isLoading ? t('playground.loading') : t('playground.load') }}
      </button>
      <button @click="clearOutput" class="btn btn-secondary">
        {{ t('playground.clearOutput') }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.main {
  display: flex;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.panel {
  display: flex;
  flex-direction: column;
  min-height: 0;
  min-width: 0;
  overflow: hidden;
}

/* Prevent text selection while dragging the splitter */
.main.is-dragging {
  user-select: none;
  cursor: col-resize;
}

/* --- Splitter --- */
.splitter {
  flex-shrink: 0;
  width: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: col-resize;
  background: #313244;
  transition: background 0.15s;
  touch-action: none;
}

.splitter:hover,
.splitter:active {
  background: #89b4fa;
}

.splitter-handle {
  width: 2px;
  height: 32px;
  border-radius: 1px;
  background: #585b70;
  transition: background 0.15s;
}

.splitter:hover .splitter-handle,
.splitter:active .splitter-handle {
  background: #cdd6f4;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #181825;
  color: #a6adc8;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.panel-header-actions {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  padding: 0;
  border: 1px solid #45475a;
  border-radius: 6px;
  background: #232336;
  color: #cdd6f4;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}

.icon-btn:hover {
  background: #313244;
  border-color: #585b70;
}

.icon-btn:focus-visible {
  outline: 2px solid #89b4fa;
  outline-offset: 2px;
}

.icon-btn svg {
  width: 1rem;
  height: 1rem;
}

.file-input {
  display: none;
}

.status {
  font-size: 0.7rem;
  text-transform: none;
}

.status.connected {
  color: #a6e3a1;
}

.status.disconnected {
  color: #f38ba8;
}

.toolbar {
  flex-shrink: 0;
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  padding-bottom: calc(0.75rem + env(safe-area-inset-bottom, 0px));
  background: #181825;
  border-top: 1px solid #313244;
}

/* Short viewport (phone, or desktop layout on phone): fix toolbar to bottom of screen so it's always visible */
@media (max-width: 768px), (max-height: 700px) {
  .home-view {
    padding-bottom: calc(58px + env(safe-area-inset-bottom, 0px));
  }

  .toolbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 10;
    box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.3);
  }
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #89b4fa;
  color: #1e1e2e;
}

.btn-primary:hover:not(:disabled) {
  background: #b4befe;
}

.btn-secondary {
  background: #45475a;
  color: #cdd6f4;
}

.btn-secondary:hover:not(:disabled) {
  background: #585b70;
}

.btn-success {
  background: #a6e3a1;
  color: #1e1e2e;
}

.btn-success:hover:not(:disabled) {
  background: #94e2d5;
}

.mode-toggle {
  display: flex;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #45475a;
  margin-right: 0.25rem;
}

.mode-toggle.disabled {
  opacity: 0.5;
}

.mode-btn {
  padding: 0.4rem 0.65rem;
  border: none;
  background: #313244;
  color: #a6adc8;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.mode-btn:disabled {
  cursor: not-allowed;
}

.mode-btn.active {
  background: #89b4fa;
  color: #1e1e2e;
}

.mode-btn:not(.active):not(:disabled):hover {
  background: #45475a;
}
</style>
