// Archivo de configuración para registrar componentes globales en la aplicación
import { app } from '../main.js';
import Sidebar from '../components/Sidebar.vue';

// Registrar el componente Sidebar como un componente global
app.component('Sidebar', Sidebar);
