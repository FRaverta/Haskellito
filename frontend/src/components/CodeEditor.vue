<script setup>
import { ref, watch, onMounted } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { EditorState } from '@codemirror/state'
import { oneDark } from '@codemirror/theme-one-dark'
import { StreamLanguage } from '@codemirror/language'
import { haskell } from '@codemirror/legacy-modes/mode/haskell'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const editorContainer = ref(null)
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
      oneDark,
      updateListener,
      EditorView.theme({
        '&': {
          height: '100%',
          fontSize: '14px'
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
</script>

<template>
  <div ref="editorContainer" class="editor-container"></div>
</template>

<style scoped>
.editor-container {
  flex: 1;
  overflow: hidden;
  background: #1e1e2e;
}

.editor-container :deep(.cm-editor) {
  height: 100%;
}

.editor-container :deep(.cm-gutters) {
  background: #181825;
  border-right: 1px solid #313244;
}
</style>
