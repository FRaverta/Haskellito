<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { EditorState, Compartment } from '@codemirror/state'
import { oneDark } from '@codemirror/theme-one-dark'
import { StreamLanguage } from '@codemirror/language'
import { haskell } from '@codemirror/legacy-modes/mode/haskell'
import { theme } from '../stores/theme.js'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const editorContainer = ref(null)
const editorTheme = new Compartment()
let editorView = null

onMounted(() => {
  const updateListener = EditorView.updateListener.of((update) => {
    if (update.docChanged) {
      emit('update:modelValue', update.state.doc.toString())
    }
  })

  const state = EditorState.create({
    doc: props.modelValue,
    extensions: [
      basicSetup,
      StreamLanguage.define(haskell),
      editorTheme.of(theme.value === 'dark' ? oneDark : []),
      updateListener,
      EditorView.theme({
        '&': {
          height: '100%',
          fontSize: '14px',
          backgroundColor: 'var(--color-bg)',
          color: 'var(--color-text)'
        },
        '.cm-scroller': {
          overflow: 'auto',
          fontFamily: "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace"
        },
        '.cm-content': {
          padding: '1rem 0'
        },
        '.cm-line': {
          padding: '0 1rem'
        },
        '.cm-gutters': {
          backgroundColor: 'var(--color-surface)',
          color: 'var(--color-text-subtle)',
          borderRight: '1px solid var(--color-border)'
        }
      })
    ]
  })

  editorView = new EditorView({
    state,
    parent: editorContainer.value
  })
})

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  if (editorView && newValue !== editorView.state.doc.toString()) {
    editorView.dispatch({
      changes: {
        from: 0,
        to: editorView.state.doc.length,
        insert: newValue
      }
    })
  }
})

watch(theme, (nextTheme) => {
  if (!editorView) return

  editorView.dispatch({
    effects: editorTheme.reconfigure(nextTheme === 'dark' ? oneDark : [])
  })
})

onUnmounted(() => {
  editorView?.destroy()
  editorView = null
})
</script>

<template>
  <div ref="editorContainer" class="editor-container"></div>
</template>

<style scoped>
.editor-container {
  flex: 1;
  overflow: hidden;
  background: var(--color-bg);
}

.editor-container :deep(.cm-editor) {
  height: 100%;
}

.editor-container :deep(.cm-gutters) {
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
}
</style>
