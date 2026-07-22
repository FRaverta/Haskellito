import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n.js'
import axios from 'axios'
import { applyTheme, theme } from './stores/theme.js'
import { clearAuthSession, getAccessToken, requestLogin } from './auth/cognito.js'

// Send current locale for challenge API requests so backend returns localized content
axios.interceptors.request.use(async (config) => {
  if (config.url && config.url.includes('challenges')) {
    config.params = { ...config.params, lang: i18n.global.locale.value }
  }

  const token = await getAccessToken()
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearAuthSession()
      requestLogin(window.location.href)
    }
    return Promise.reject(error)
  }
)

applyTheme(theme.value)

createApp(App).use(router).use(i18n).mount('#app')
