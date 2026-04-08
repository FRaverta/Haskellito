import { ref } from 'vue'

export const THEME_KEY = 'haskellito-theme'
export const supportedThemes = ['dark', 'light']

function getSystemTheme() {
  if (
    typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-color-scheme: light)').matches
  ) {
    return 'light'
  }
  return 'dark'
}

function loadSavedTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY)
    if (saved && supportedThemes.includes(saved)) return saved
  } catch (_) {}

  return getSystemTheme()
}

export const theme = ref(loadSavedTheme())

export function applyTheme(nextTheme = theme.value) {
  if (typeof document === 'undefined') return

  document.documentElement.dataset.theme = nextTheme
  document.documentElement.style.colorScheme = nextTheme
}

export function setTheme(nextTheme) {
  if (!supportedThemes.includes(nextTheme)) return

  theme.value = nextTheme
  applyTheme(nextTheme)

  try {
    localStorage.setItem(THEME_KEY, nextTheme)
  } catch (_) {}
}

applyTheme(theme.value)
