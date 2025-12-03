import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import Sidebar from './components/Sidebar.vue'

const app = createApp(App)

// Registrar Sidebar globalmente
app.component('Sidebar', Sidebar)

app.use(router)
app.mount('#app')
