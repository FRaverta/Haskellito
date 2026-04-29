<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import axios from 'axios'
import { marked } from 'marked'
import CodeEditor from '../components/CodeEditor.vue'
import { getChallengeProgress, setChallengeProgress, setLastViewedChallengeId } from '../stores/challengeProgress.js'

const API_BASE = '/api/v2/playground'
const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

const challenge = ref(null)
const code = ref('')
const isSubmitting = ref(false)
const results = ref([])
const errorMessage = ref('')
// Keep current challenge id so we can save progress on unmount (route may already have changed)
const currentChallengeId = ref(null)
// Collapsible test results panel (expanded by default)
const resultsExpanded = ref(true)

const renderedDescription = computed(() => {
  if (!challenge.value) return ''
  return marked(challenge.value.description)
})

const passedCount = computed(() => results.value.filter(r => r.passed).length)
const totalCount = computed(() => results.value.length)
const allPassed = computed(() => passedCount.value === totalCount.value && totalCount.value > 0)

// Fetch challenge details and restore progress if any
async function fetchChallenge() {
  const challengeId = route.params.id
  currentChallengeId.value = challengeId
  setLastViewedChallengeId(challengeId)
  try {
    const response = await axios.get(`${API_BASE}/challenges/${challengeId}`)
    if (response.data.error) {
      errorMessage.value = response.data.error
      return
    }
    challenge.value = response.data
    const saved = getChallengeProgress(challengeId)
    if (saved) {
      code.value = saved.code ?? ''
      results.value = Array.isArray(saved.results) ? [...saved.results] : []
    } else {
      code.value = response.data.starter_code || ''
      results.value = []
    }
  } catch (error) {
    errorMessage.value = t('errors.challengeLoad', { msg: error.message })
  }
}

function saveProgress() {
  const id = currentChallengeId.value
  if (id) {
    setChallengeProgress(id, {
      code: code.value,
      results: results.value
    })
  }
}

// Persist progress when code or results change
watch([code, results], saveProgress, { deep: true })

// Refetch when switching to a different challenge or locale
watch(() => route.params.id, () => {
  if (route.params.id) {
    fetchChallenge()
  }
})
watch(locale, () => {
  if (route.params.id) fetchChallenge()
})

// Submit solution for testing. The v2 API resets a shared worker per request.
async function submitSolution() {
  isSubmitting.value = true
  errorMessage.value = ''
  results.value = []

  try {
    const response = await axios.post(`${API_BASE}/challenges/${route.params.id}/submit`, {
      code: code.value
    })

    if (response.data.error) {
      errorMessage.value = response.data.error
    } else {
      results.value = response.data.results
    }
  } catch (error) {
    errorMessage.value = t('errors.submitFailed', { msg: error.message })
  } finally {
    isSubmitting.value = false
  }
}

// Keyboard shortcut for submission
function handleKeydown(event) {
  if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
    event.preventDefault()
    submitSolution()
  }
}

// --- Resizable splitter logic ---
const splitPercent = ref(40) // description panel width as a percentage
const isDragging = ref(false)
const mainRef = ref(null)

const descriptionStyle = computed(() => ({
  flex: 'none',
  width: `${splitPercent.value}%`,
}))
const editorResultsStyle = computed(() => ({
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

onMounted(() => {
  fetchChallenge()
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  saveProgress()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('pointermove', onPointerMove)
  document.removeEventListener('pointerup', onPointerUp)
})
</script>

<template>
  <div class="challenge-view">
    <main ref="mainRef" class="main" :class="{ 'is-dragging': isDragging }">
      <!-- Left Panel: Challenge Description -->
      <div class="panel description-panel" :style="descriptionStyle">
        <div class="panel-header panel-header-with-action">
          <span>{{ t('challenge.title') }}</span>
          <button
            type="button"
            class="btn btn-secondary btn-sm"
            @click="router.push('/challenge')"
          >
            {{ t('challenge.pickOther') }}
          </button>
        </div>
        <div class="description-content">
          <div v-if="errorMessage && !challenge" class="error-message">
            {{ errorMessage }}
          </div>
          <div v-else-if="challenge" class="markdown-body" v-html="renderedDescription"></div>
          <div v-else class="loading">{{ t('challenge.loading') }}</div>
        </div>
      </div>

      <!-- Draggable Splitter -->
      <div
        class="splitter"
        @pointerdown="onSplitterPointerDown"
      >
        <div class="splitter-handle" />
      </div>

      <!-- Right Panel: Code Editor & Results -->
      <div class="panel editor-results-panel" :style="editorResultsStyle">
        <div class="editor-section">
          <div class="panel-header">{{ t('challenge.solution') }}</div>
          <CodeEditor v-model="code" />
        </div>

        <div class="results-section" :class="{ 'results-section--collapsed': !resultsExpanded }">
          <button
            type="button"
            class="results-header"
            @click="resultsExpanded = !resultsExpanded"
          >
            <span class="results-header-chevron" :class="{ 'results-header-chevron--collapsed': !resultsExpanded }">
              ▼
            </span>
            <span class="results-header-title">{{ t('challenge.testResults') }}</span>
            <span v-if="results.length > 0" :class="['results-summary', allPassed ? 'all-passed' : 'some-failed']">
              {{ passedCount }}/{{ totalCount }} {{ t('challenge.passed') }}
            </span>
          </button>

          <div v-show="resultsExpanded" class="results-content">
            <div v-if="errorMessage" class="error-message">
              <pre>{{ errorMessage }}</pre>
            </div>

            <div v-else-if="results.length === 0" class="no-results">
              {{ t('challenge.submitHint') }}
            </div>

            <table v-else class="results-table">
              <thead>
                <tr>
                  <th class="status-col">{{ t('challenge.status') }}</th>
                  <th class="test-col">{{ t('challenge.test') }}</th>
                  <th class="expected-col">{{ t('challenge.expected') }}</th>
                  <th class="actual-col">{{ t('challenge.result') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(result, index) in results" :key="index" :class="{ passed: result.passed, failed: !result.passed }">
                  <td class="status-col">
                    <span v-if="result.passed" class="status-icon pass">✓</span>
                    <span v-else class="status-icon fail">✗</span>
                  </td>
                  <td class="test-col"><code>{{ result.test_code }}</code></td>
                  <td class="expected-col"><code>{{ result.expected }}</code></td>
                  <td class="actual-col"><code>{{ result.actual }}</code></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

    <div class="toolbar">
      <button
        @click="submitSolution"
        :disabled="isSubmitting"
        class="btn btn-success"
      >
        {{ isSubmitting ? t('challenge.submitting') : t('challenge.submit') }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.challenge-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.description-panel {
  min-width: 0;
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
  background: var(--color-surface-hover);
  transition: background 0.15s;
  touch-action: none;
}

.splitter:hover,
.splitter:active {
  background: var(--color-accent);
}

.splitter-handle {
  width: 2px;
  height: 32px;
  border-radius: 1px;
  background: var(--color-surface-stronger);
  transition: background 0.15s;
}

.splitter:hover .splitter-handle,
.splitter:active .splitter-handle {
  background: var(--color-text);
}

.editor-results-panel {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.editor-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.results-section {
  flex: 0 0 250px;
  display: flex;
  flex-direction: column;
  border-top: 1px solid var(--color-border);
}

.results-section--collapsed {
  flex: 0 0 auto;
}

.results-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.5rem 1rem;
  background: var(--color-surface);
  border: none;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: background 0.2s;
  text-align: left;
}

.results-header:hover {
  background: var(--color-surface-raised);
}

.results-header-chevron {
  font-size: 0.6rem;
  transition: transform 0.2s;
  flex-shrink: 0;
}

.results-header-chevron--collapsed {
  transform: rotate(-90deg);
}

.results-header-title {
  flex: 0 0 auto;
}

.results-header .results-summary {
  margin-left: auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  flex-shrink: 0;
}

.description-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  background: var(--color-bg);
}

.results-content {
  flex: 1;
  overflow-y: auto;
  background: var(--color-bg);
}

.markdown-body {
  color: var(--color-text);
  line-height: 1.6;
}

.markdown-body :deep(h2) {
  color: var(--color-accent);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.markdown-body :deep(h3) {
  color: var(--color-secondary-accent);
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.markdown-body :deep(code) {
  background: var(--color-inline-code-bg);
  color: var(--color-inline-code-text);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.9em;
}

.markdown-body :deep(pre) {
  background: var(--color-surface);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1rem 0;
}

.markdown-body :deep(pre code) {
  background: transparent;
  padding: 0;
}

.error-message {
  color: var(--color-danger);
  padding: 1rem;
}

.error-message pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.9em;
}

.loading, .no-results {
  color: var(--color-text-subtle);
  padding: 1rem;
  font-style: italic;
}

.results-summary {
  font-size: 0.75rem;
  text-transform: none;
  font-weight: 500;
}

.results-summary.all-passed {
  color: var(--color-success);
}

.results-summary.some-failed {
  color: var(--color-danger);
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.results-table th {
  text-align: left;
  padding: 0.75rem 1rem;
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  border-bottom: 1px solid var(--color-border);
}

.results-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
}

.results-table tr.passed td {
  background: var(--result-pass-bg);
}

.results-table tr.failed td {
  background: var(--result-fail-bg);
}

.results-table code {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.85em;
}

.status-col {
  width: 60px;
  text-align: center;
}

.test-col {
  width: 35%;
}

.expected-col, .actual-col {
  width: 20%;
}

.status-icon {
  font-weight: bold;
  font-size: 1rem;
}

.status-icon.pass {
  color: var(--color-success);
}

.status-icon.fail {
  color: var(--color-danger);
}

.toolbar {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
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

.btn-sm {
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--color-accent);
  color: var(--color-accent-contrast);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-accent-hover);
}

.btn-secondary {
  background: var(--color-surface-strong);
  color: var(--color-text);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-surface-stronger);
}

.btn-success {
  background: var(--color-success);
  color: var(--color-success-contrast);
}

.btn-success:hover:not(:disabled) {
  background: var(--color-success-hover);
}
</style>
