import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import i18n from './i18n.js'
import axios from 'axios'

// Send current locale for challenge API requests so backend returns localized content
axios.interceptors.request.use((config) => {
  if (config.url && config.url.includes('challenges')) {
    config.params = { ...config.params, lang: i18n.global.locale.value }
  }
  return config
})

createApp(App).use(router).use(i18n).mount('#app')
