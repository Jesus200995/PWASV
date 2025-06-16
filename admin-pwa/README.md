# Panel Administrativo - Sembrando Vida

Panel de administración moderno construido con Vue.js 3 y Vite para gestionar los registros de la aplicación PWA Sembrando Vida.

## 🚀 Características

- **Vue.js 3** con Composition API
- **Vue Router** para navegación SPA
- **Axios** para comunicación con la API
- **Diseño responsivo** que funciona en desktop y móvil
- **Autenticación** con tokens JWT
- **Dashboard** con estadísticas en tiempo real
- **Gestión de registros** con visualización en tabla
- **Modal** para detalles y fotos
- **Estado de conexión** en tiempo real

## 📋 Requisitos

- Node.js 16+ 
- npm o yarn

## 🛠️ Instalación

1. **Instalar dependencias:**
   ```bash
   npm install
   ```

2. **Configurar la API:**
   - El proyecto está configurado para usar: `https://apipwa.sembrandodatos.com`
   - Si necesitas cambiar la URL, edita la constante `API_URL` en los archivos de Vue

## 🔧 Comandos Disponibles

### Desarrollo
```bash
npm run dev
```
Inicia el servidor de desarrollo en `http://localhost:3001`

### Compilar para Producción
```bash
npm run build
```
Genera los archivos optimizados en la carpeta `dist/`

### Vista previa de Producción
```bash
npm run preview
```
Sirve los archivos de la carpeta `dist/` para probar la versión de producción

## 📁 Estructura del Proyecto

```
src/
├── components/          # Componentes reutilizables
│   └── Sidebar.vue     # Barra lateral de navegación
├── views/              # Vistas principales
│   ├── LoginView.vue   # Página de inicio de sesión
│   └── DashboardView.vue # Panel principal
├── router/             # Configuración de rutas
│   └── index.js        # Rutas y guards de navegación
├── App.vue             # Componente raíz
├── main.js             # Punto de entrada
└── style.css           # Estilos globales
```

## 🔐 Autenticación

El sistema utiliza JWT tokens para la autenticación:

1. **Login:** Envía credenciales a `/admin/login`
2. **Token:** Se guarda en `localStorage`
3. **Guards:** Protegen rutas que requieren autenticación
4. **Auto-logout:** Si el token expira, redirige automáticamente al login

## 🌐 Despliegue

1. **Compilar el proyecto:**
   ```bash
   npm run build
   ```

2. **Subir la carpeta `dist/`** a tu servidor web

3. **Configurar el servidor** para servir el archivo `index.html` para todas las rutas (SPA routing)

### Ejemplo de configuración para Apache (.htaccess):
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]
```

### Ejemplo de configuración para Nginx:
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

## 🔧 Configuración Avanzada

### Cambiar Puerto de Desarrollo
Edita `vite.config.js`:
```javascript
server: {
  port: 3001, // Cambia aquí
  host: true
}
```

### Variables de Entorno
Puedes crear un archivo `.env` para configuraciones:
```
VITE_API_URL=https://apipwa.sembrandodatos.com
```

Y usarlo en el código:
```javascript
const API_URL = import.meta.env.VITE_API_URL
```

## 🐛 Troubleshooting

### Error de CORS
Si encuentras errores de CORS durante el desarrollo, asegúrate de que tu backend esté configurado correctamente para permitir el origen de desarrollo.

### Token Expirado
Si el token expira, el usuario será redirigido automáticamente al login.

### Problemas de Conectividad
El dashboard muestra el estado de conexión en tiempo real y maneja errores de red gracefully.

## 📞 Soporte

Para reportar bugs o solicitar características, contacta al equipo de desarrollo.
