<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { marked } from 'marked'
import CodeEditor from '../components/CodeEditor.vue'
import { getChallengeProgress, setChallengeProgress, setLastViewedChallengeId } from '../stores/challengeProgress.js'

const API_BASE = '/api'
const route = useRoute()
const router = useRouter()

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
    errorMessage.value = `Failed to load challenge: ${error.message}`
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

// Refetch when switching to a different challenge
watch(() => route.params.id, () => {
  if (route.params.id) {
    fetchChallenge()
  }
})

// Submit solution for testing (server spawns GHCi, runs tests, then closes process)
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
    errorMessage.value = `Submission failed: ${error.message}`
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

onMounted(() => {
  fetchChallenge()
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  saveProgress()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="challenge-view">
    <main class="main">
      <!-- Left Panel: Challenge Description -->
      <div class="panel description-panel">
        <div class="panel-header panel-header-with-action">
          <span>Challenge</span>
          <button
            type="button"
            class="btn btn-secondary btn-sm"
            @click="router.push('/challenge')"
          >
            Pick other challenge
          </button>
        </div>
        <div class="description-content">
          <div v-if="errorMessage && !challenge" class="error-message">
            {{ errorMessage }}
          </div>
          <div v-else-if="challenge" class="markdown-body" v-html="renderedDescription"></div>
          <div v-else class="loading">Loading challenge...</div>
        </div>
      </div>

      <!-- Right Panel: Code Editor & Results -->
      <div class="panel editor-results-panel">
        <div class="editor-section">
          <div class="panel-header">Solution</div>
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
            <span class="results-header-title">Test Results</span>
            <span v-if="results.length > 0" :class="['results-summary', allPassed ? 'all-passed' : 'some-failed']">
              {{ passedCount }}/{{ totalCount }} passed
            </span>
          </button>

          <div v-show="resultsExpanded" class="results-content">
            <div v-if="errorMessage" class="error-message">
              <pre>{{ errorMessage }}</pre>
            </div>

            <div v-else-if="results.length === 0" class="no-results">
              Submit your solution to see test results
            </div>

            <table v-else class="results-table">
              <thead>
                <tr>
                  <th class="status-col">Status</th>
                  <th class="test-col">Test</th>
                  <th class="expected-col">Expected</th>
                  <th class="actual-col">Result</th>
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
        {{ isSubmitting ? 'Running Tests...' : 'Submit (⌘+Enter)' }}
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
  flex: 0 0 40%;
  border-right: 1px solid #313244;
}

.editor-results-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
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
  border-top: 1px solid #313244;
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
  background: #181825;
  border: none;
  border-bottom: 1px solid #313244;
  color: #a6adc8;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: background 0.2s;
  text-align: left;
}

.results-header:hover {
  background: #1e1e2e;
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
  background: #181825;
  color: #a6adc8;
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
  background: #1e1e2e;
}

.results-content {
  flex: 1;
  overflow-y: auto;
  background: #1e1e2e;
}

.markdown-body {
  color: #cdd6f4;
  line-height: 1.6;
}

.markdown-body :deep(h2) {
  color: #89b4fa;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #313244;
}

.markdown-body :deep(h3) {
  color: #cba6f7;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.markdown-body :deep(code) {
  background: #313244;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.9em;
}

.markdown-body :deep(pre) {
  background: #181825;
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
  color: #f38ba8;
  padding: 1rem;
}

.error-message pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.9em;
}

.loading, .no-results {
  color: #6c7086;
  padding: 1rem;
  font-style: italic;
}

.results-summary {
  font-size: 0.75rem;
  text-transform: none;
  font-weight: 500;
}

.results-summary.all-passed {
  color: #a6e3a1;
}

.results-summary.some-failed {
  color: #f38ba8;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.results-table th {
  text-align: left;
  padding: 0.75rem 1rem;
  background: #181825;
  color: #a6adc8;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  border-bottom: 1px solid #313244;
}

.results-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #313244;
  color: #cdd6f4;
}

.results-table tr.passed td {
  background: rgba(166, 227, 161, 0.05);
}

.results-table tr.failed td {
  background: rgba(243, 139, 168, 0.05);
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
  color: #a6e3a1;
}

.status-icon.fail {
  color: #f38ba8;
}

.toolbar {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #181825;
  border-top: 1px solid #313244;
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
</style>
