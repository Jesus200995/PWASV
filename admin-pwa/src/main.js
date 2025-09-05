import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import Sidebar_NEW from './components/Sidebar_NEW.vue'

const app = createApp(App)

// Registrar Sidebar_NEW globalmente con el nombre Sidebar_NEW
app.component('Sidebar_NEW', Sidebar_NEW)

app.use(router)
app.mount('#app')
