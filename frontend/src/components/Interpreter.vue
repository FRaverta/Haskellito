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
  background: var(--color-bg);
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
  color: var(--color-text-subtle);
}

.ghci-banner {
  color: var(--color-accent);
  margin: 0 0 0.5rem 0;
}

.hint {
  color: var(--color-text-subtle);
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
  color: var(--color-accent);
}

.output-line.input {
  color: var(--color-text);
}

.output-line.input pre::before {
  content: 'ghci> ';
  color: var(--color-text-muted);
}

.output-line.output {
  color: var(--color-success);
}

.output-line.error {
  color: var(--color-danger);
}

.input-line {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem 1rem 1rem;
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
}

.prompt {
  color: var(--color-text-muted);
  margin-right: 0.5rem;
  flex-shrink: 0;
}

.prompt.disabled {
  color: var(--color-text-disabled);
}

.command-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--color-text);
  font-family: inherit;
  font-size: inherit;
  outline: none;
  padding: 0;
}

.command-input::placeholder {
  color: var(--color-text-disabled);
  font-style: italic;
}

.command-input:disabled {
  color: var(--color-text-subtle);
}
</style>
