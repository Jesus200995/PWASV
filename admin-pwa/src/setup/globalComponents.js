// Archivo de configuración para registrar componentes globales en la aplicación
import { app } from '../main.js';
import Sidebar_NEW from '../components/Sidebar_NEW.vue';

// Registrar el componente Sidebar_NEW como un componente global con el nombre Sidebar
app.component('Sidebar_NEW', Sidebar_NEW);
