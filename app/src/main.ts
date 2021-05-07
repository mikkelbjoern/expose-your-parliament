import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'

import registerDirectives from '@/directives'

const app = createApp(App)
app.use(router)
registerDirectives(app)
app.mount('#app')