<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import CodeEditor from '../components/CodeEditor.vue'
import Interpreter from '../components/Interpreter.vue'

// In development, vite proxies /api to localhost:8000
// In production, nginx proxies /api to the backend
const API_BASE = '/api'

const code = ref(`-- Welcome to Haskellito!
-- Write your Haskell code here

-- Example: Simple function
double x = x * 2

-- Try evaluating: double 21
`)

const output = ref([])
const sessionId = ref(null)
const isConnected = ref(false)
const isLoading = ref(false)

// Start a new GHCi session
async function startSession() {
  try {
    const response = await axios.post(`${API_BASE}/sessions/`)
    sessionId.value = response.data.session_id
    isConnected.value = true
    output.value.push({ type: 'system', text: 'GHCi session started.' })
  } catch (error) {
    output.value.push({ type: 'error', text: `Failed to start session: ${error.message}` })
  }
}

// Evaluate code in GHCi (from editor - multiple lines)
async function evaluate() {
  if (!sessionId.value) {
    output.value.push({ type: 'error', text: 'No active session. Click "Connect" first.' })
    return
  }

  isLoading.value = true
  const codeToEval = code.value

  // Show what we're loading from editor
  output.value.push({ type: 'system', text: '-- Loading from editor...' })

  try {
    const response = await axios.post(`${API_BASE}/sessions/${sessionId.value}/eval`, {
      code: codeToEval
    })

    if (response.data.error) {
      output.value.push({ type: 'error', text: response.data.error })
    } else if (response.data.output) {
      output.value.push({ type: 'output', text: response.data.output })
    } else {
      output.value.push({ type: 'system', text: 'Loaded.' })
    }
  } catch (error) {
    output.value.push({ type: 'error', text: `Evaluation failed: ${error.message}` })
  } finally {
    isLoading.value = false
  }
}

// Evaluate a single command from the REPL input
async function evaluateCommand(command) {
  if (!sessionId.value) {
    output.value.push({ type: 'error', text: 'No active session.' })
    return
  }

  isLoading.value = true
  
  // Show the input command
  output.value.push({ type: 'input', text: command })

  try {
    const response = await axios.post(`${API_BASE}/sessions/${sessionId.value}/eval`, {
      code: command
    })

    if (response.data.error) {
      output.value.push({ type: 'error', text: response.data.error })
    } else if (response.data.output) {
      output.value.push({ type: 'output', text: response.data.output })
    }
  } catch (error) {
    output.value.push({ type: 'error', text: `Error: ${error.message}` })
  } finally {
    isLoading.value = false
  }
}

// Close the session
async function closeSession() {
  if (!sessionId.value) return

  try {
    await axios.post(`${API_BASE}/sessions/${sessionId.value}/close`)
    output.value.push({ type: 'system', text: 'Session closed.' })
  } catch (error) {
    // Ignore errors on close
  } finally {
    sessionId.value = null
    isConnected.value = false
  }
}

// Clear output
function clearOutput() {
  output.value = []
}

// Keyboard shortcut for evaluation
function handleKeydown(event) {
  if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
    event.preventDefault()
    evaluate()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  closeSession()
})
</script>

<template>
  <div class="home-view">
    <main class="main">
      <div class="panel editor-panel">
        <div class="panel-header">Editor</div>
        <CodeEditor v-model="code" />
      </div>

      <div class="panel interpreter-panel">
        <div class="panel-header">
          GHCi Console
          <span v-if="isConnected" class="status connected">● Connected</span>
          <span v-else class="status disconnected">○ Disconnected</span>
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
      <button 
        v-if="!isConnected" 
        @click="startSession" 
        class="btn btn-primary"
      >
        Connect to GHCi
      </button>
      <button 
        v-else 
        @click="closeSession" 
        class="btn btn-secondary"
      >
        Disconnect
      </button>
      <button 
        @click="evaluate" 
        :disabled="!isConnected || isLoading"
        class="btn btn-success"
      >
        {{ isLoading ? 'Loading...' : 'Load (⌘+Enter)' }}
      </button>
      <button @click="clearOutput" class="btn btn-secondary">
        Clear Output
      </button>
    </div>
  </div>
</template>

<style scoped>
.home-view {
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
  flex: 1;
  overflow: hidden;
}

.editor-panel {
  border-right: 1px solid #313244;
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
  display: flex;
  gap: 0.5rem;
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
