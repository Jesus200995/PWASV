# Panel Administrativo - Sembrando Vida

Panel de administración desarrollado con Vue.js 3 + Vite para gestionar los registros de la aplicación PWA Sembrando Vida.

## 🚀 Características

- ✅ **SPA con Vue.js 3** (Composition API)
- ✅ **Navegación con Vue Router**
- ✅ **Autenticación JWT** conectada al backend FastAPI
- ✅ **Dashboard responsivo** con estadísticas en tiempo real
- ✅ **Gestión de registros** con visualización de fotos y ubicaciones
- ✅ **Sidebar colapsable** para móvil
- ✅ **Diseño moderno** con CSS custom

## 📋 Requisitos

- Node.js 16+ 
- npm o yarn
- Backend FastAPI corriendo en `https://apipwa.sembrandodatos.com`

## 🛠️ Instalación

1. **Instalar dependencias:**
```bash
npm install
```

2. **Desarrollo local:**
```bash
npm run dev
```
El servidor de desarrollo se ejecutará en `http://localhost:3000`

3. **Compilar para producción:**
```bash
npm run build
```
Los archivos compilados estarán en la carpeta `dist/`

4. **Previsualizar build de producción:**
```bash
npm run preview
```

## 📁 Estructura del Proyecto

```
admin-pwa/
├── public/
│   └── index.html          # HTML base
├── src/
│   ├── components/
│   │   └── Sidebar.vue     # Componente de barra lateral
│   ├── views/
│   │   ├── LoginView.vue   # Vista de login
│   │   └── DashboardView.vue # Vista del dashboard
│   ├── main.js            # Punto de entrada
│   ├── App.vue            # Componente raíz
│   └── style.css          # Estilos globales
├── package.json           # Dependencias y scripts
├── vite.config.js         # Configuración de Vite
└── README.md             # Este archivo
```

## 🔐 Autenticación

El panel se conecta al endpoint `/admin/login` del backend FastAPI:
- **URL:** `https://apipwa.sembrandodatos.com/admin/login`
- **Método:** POST
- **Formato:** OAuth2PasswordRequestForm
- **Token:** JWT guardado en localStorage

### Flujo de autenticación:
1. Usuario ingresa credenciales en `/login`
2. Se envía request al backend con formato OAuth2
3. Si es exitoso, se guarda el token JWT
4. Redirección automática a `/dashboard`
5. Guard de navegación protege rutas privadas

## 📱 Funcionalidades

### Dashboard
- **Estadísticas en tiempo real:** Total de registros, usuarios activos, registros del día
- **Actividad reciente:** Lista de últimas acciones del sistema
- **Gráficas:** Placeholder para futuras visualizaciones

### Gestión de Registros
- **Tabla completa** con todos los registros
- **Visualización de fotos** en modal
- **Detalles completos** de cada registro
- **Integración con Google Maps** para ubicaciones
- **Búsqueda y filtros** (próximamente)

### Responsive Design
- **Sidebar colapsable** en dispositivos móviles
- **Adaptativo** para tablets y escritorio
- **Touch-friendly** para dispositivos táctiles

## 🎨 Personalización

### Colores principales:
- **Primario:** #4CAF50 (verde)
- **Secundario:** #f8fafc (gris claro)
- **Accent:** #667eea (azul degradado)

### Modificar estilos:
- Estilos globales: `src/style.css`
- Componentes: `<style scoped>` en cada `.vue`
- Variables CSS en `:root` para colores consistentes

## 🚀 Despliegue

### Build para producción:
```bash
npm run build
```

### Subir archivos:
1. Compilar el proyecto con `npm run build`
2. Subir contenido de la carpeta `dist/` al servidor web
3. Configurar servidor para servir `index.html` en todas las rutas (SPA)

### Configuración del servidor:
Para servidores Apache, agregar `.htaccess`:
```apache
RewriteEngine On
RewriteRule ^(?!.*\.).*$ /index.html [L]
```

Para servidores Nginx:
```nginx
try_files $uri $uri/ /index.html;
```

## 🔧 Scripts Disponibles

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Compilar para producción
- `npm run preview` - Previsualizar build de producción

## 🐛 Troubleshooting

### Problemas comunes:

1. **Error de CORS:**
   - Verificar que el backend permite requests desde el dominio del panel

2. **Token expirado:**
   - El sistema redirige automáticamente al login cuando el token expira

3. **Error 404 en producción:**
   - Configurar el servidor web para servir `index.html` en todas las rutas

4. **Estilos no cargan:**
   - Verificar que la ruta base esté correctamente configurada en `vite.config.js`

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contactar al equipo de desarrollo.

---
*Panel Administrativo v1.0 - Sembrando Vida 2025*
