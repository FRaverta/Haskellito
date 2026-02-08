<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'

const props = defineProps({
  output: {
    type: Array,
    default: () => []
  },
  isConnected: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit'])

const outputContainer = ref(null)
const inputField = ref(null)
const currentInput = ref('')
const commandHistory = ref([])
const historyIndex = ref(-1)

// Auto-scroll to bottom when new output is added
watch(() => props.output.length, async () => {
  await nextTick()
  scrollToBottom()
})

function scrollToBottom() {
  if (outputContainer.value) {
    outputContainer.value.scrollTop = outputContainer.value.scrollHeight
  }
}

function handleSubmit() {
  const command = currentInput.value.trim()
  if (!command || !props.isConnected || props.isLoading) return
  
  // Add to history
  if (command && (commandHistory.value.length === 0 || commandHistory.value[commandHistory.value.length - 1] !== command)) {
    commandHistory.value.push(command)
  }
  historyIndex.value = -1
  
  emit('submit', command)
  currentInput.value = ''
}

function handleKeydown(event) {
  if (event.key === 'ArrowUp') {
    event.preventDefault()
    if (commandHistory.value.length > 0) {
      if (historyIndex.value === -1) {
        historyIndex.value = commandHistory.value.length - 1
      } else if (historyIndex.value > 0) {
        historyIndex.value--
      }
      currentInput.value = commandHistory.value[historyIndex.value]
    }
  } else if (event.key === 'ArrowDown') {
    event.preventDefault()
    if (historyIndex.value !== -1) {
      if (historyIndex.value < commandHistory.value.length - 1) {
        historyIndex.value++
        currentInput.value = commandHistory.value[historyIndex.value]
      } else {
        historyIndex.value = -1
        currentInput.value = ''
      }
    }
  }
}

function focusInput() {
  if (inputField.value) {
    inputField.value.focus()
  }
}

onMounted(() => {
  focusInput()
})

// Expose focus method to parent
defineExpose({ focusInput })
</script>

<template>
  <div class="console-wrapper" @click="focusInput">
    <div ref="outputContainer" class="console-output">
      <div v-if="output.length === 0 && !isConnected" class="welcome-message">
        <pre class="ghci-banner">GHCi, version 9.x.x: https://www.haskell.org/ghc/  :? for help</pre>
        <div class="hint">Connect to GHCi to start...</div>
      </div>
      <div v-for="(item, index) in output" :key="index" :class="['output-line', item.type]">
        <pre>{{ item.text }}</pre>
      </div>
    </div>
    <div class="input-line">
      <span class="prompt" :class="{ disabled: !isConnected }">ghci&gt;</span>
      <input
        ref="inputField"
        v-model="currentInput"
        type="text"
        class="command-input"
        :placeholder="!isConnected ? 'Connect first...' : isLoading ? 'Running...' : 'Enter Haskell expression...'"
        :disabled="!isConnected || isLoading"
        @keydown.enter="handleSubmit"
        @keydown="handleKeydown"
        spellcheck="false"
        autocomplete="off"
      />
    </div>
  </div>
</template>

<style scoped>
.console-wrapper {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  background: #1e1e2e;
  font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
  font-size: 13px;
  cursor: text;
}

.console-output {
  flex: 1 1 0;
  min-height: 0;
  overflow-y: scroll;
  overflow-x: auto;
  padding: 1rem;
  padding-bottom: 0.5rem;
  -webkit-overflow-scrolling: touch;
}

.welcome-message {
  color: #6c7086;
}

.ghci-banner {
  color: #89b4fa;
  margin: 0 0 0.5rem 0;
}

.hint {
  color: #6c7086;
  font-style: italic;
}

.output-line {
  margin-bottom: 0.25rem;
}

.output-line pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.output-line.system {
  color: #89b4fa;
}

.output-line.input {
  color: #cdd6f4;
}

.output-line.input pre::before {
  content: 'ghci> ';
  color: #a6adc8;
}

.output-line.output {
  color: #a6e3a1;
}

.output-line.error {
  color: #f38ba8;
}

.input-line {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem 1rem 1rem;
  background: #1e1e2e;
  border-top: 1px solid #313244;
}

.prompt {
  color: #a6adc8;
  margin-right: 0.5rem;
  flex-shrink: 0;
}

.prompt.disabled {
  color: #45475a;
}

.command-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #cdd6f4;
  font-family: inherit;
  font-size: inherit;
  outline: none;
  padding: 0;
}

.command-input::placeholder {
  color: #45475a;
  font-style: italic;
}

.command-input:disabled {
  color: #6c7086;
}
</style>
