import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import es from './locales/es.json'

const LOCALE_KEY = 'haskellito-locale'
const supportedLocales = ['en', 'es']

function loadSavedLocale() {
  try {
    const saved = localStorage.getItem(LOCALE_KEY)
    if (saved && supportedLocales.includes(saved)) return saved
  } catch (_) {}
  return 'en'
}

const i18n = createI18n({
  legacy: false,
  locale: loadSavedLocale(),
  fallbackLocale: 'en',
  messages: { en, es },
})

export function setLocale(locale) {
  if (!supportedLocales.includes(locale)) return
  i18n.global.locale.value = locale
  try {
    localStorage.setItem(LOCALE_KEY, locale)
  } catch (_) {}
}

export function getLocale() {
  return i18n.global.locale.value
}

export { supportedLocales, LOCALE_KEY }
export default i18n
