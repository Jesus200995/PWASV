<template>
  <div class="permisos-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Permisos Administrativos</h1>
              <p class="header-subtitle">Gestiona los usuarios y permisos del panel de administración</p>
            </div>
          </div>
          <div class="header-actions">
            <button class="btn-primary" @click="mostrarModalCrear = true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14"/>
                <path d="M5 12h14"/>
              </svg>
              Nuevo Usuario Admin
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Mensaje de carga -->
        <div v-if="cargando" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Cargando usuarios administrativos...</p>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error && !cargando" class="error-state">
          <div class="error-icon">⚠️</div>
          <h3>Error al cargar usuarios administrativos</h3>
          <p>{{ error }}</p>
          <button class="btn-secondary" @click="cargarUsuariosAdmin">Reintentar</button>
        </div>

        <!-- Lista de usuarios administrativos -->
        <div v-if="!cargando && !error" class="usuarios-list">
          <div class="list-header">
            <h2>Usuarios Administrativos ({{ usuariosAdmin.length }})</h2>
            <div class="header-filters">
              <select v-model="filtroRol" class="filter-select" @change="aplicarFiltros">
                <option value="">Todos los roles</option>
                <option value="admin">Admin</option>
                <option value="user">Usuario</option>
              </select>
              <button class="btn-refresh" @click="cargarUsuariosAdmin" :disabled="cargando">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M23 4v6h-6"/>
                  <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                </svg>
                Actualizar
              </button>
            </div>
          </div>

          <!-- Tabla de usuarios administrativos -->
          <div class="usuarios-table-container">
            <table class="usuarios-table">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Información Personal</th>
                  <th>Rol</th>
                  <th>Territorio</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="usuario in usuariosFiltrados" :key="usuario.id" class="usuario-row">
                  <td class="name-cell">
                    <div class="user-info">
                      <div class="user-avatar">
                        {{ usuario.username.charAt(0).toUpperCase() }}
                      </div>
                      <div class="user-details">
                        <div class="user-name">{{ usuario.username }}</div>
                        <div class="user-supervisor">ID: {{ usuario.id }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="info-personal-cell">
                    <div class="info-personal">
                      <div class="info-item nombre-completo" v-if="usuario.nombre_completo">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                          <circle cx="12" cy="7" r="4"/>
                        </svg>
                        <span>{{ usuario.nombre_completo }}</span>
                      </div>
                      <div class="info-item curp" v-if="usuario.curp">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <rect x="3" y="4" width="18" height="16" rx="2"/>
                          <line x1="7" y1="8" x2="17" y2="8"/>
                          <line x1="7" y1="12" x2="13" y2="12"/>
                        </svg>
                        <span class="curp-text">{{ usuario.curp }}</span>
                      </div>
                      <div class="info-item cargo" v-if="usuario.cargo">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20 7H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/>
                          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                        </svg>
                        <span>{{ usuario.cargo }}</span>
                      </div>
                      <div class="info-empty" v-if="!usuario.nombre_completo && !usuario.curp && !usuario.cargo">
                        <span class="text-muted">Sin información</span>
                      </div>
                    </div>
                  </td>
                  <td class="rol-cell">
                    <span class="rol-badge" :class="usuario.rol">
                      <svg v-if="usuario.rol === 'admin'" class="rol-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2z"/>
                      </svg>
                      <svg v-else class="rol-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                        <circle cx="12" cy="7" r="4"/>
                      </svg>
                      <span class="rol-text">{{ usuario.rol === 'admin' ? 'Administrador' : 'Usuario' }}</span>
                    </span>
                  </td>
                  <td class="territorio-cell">
                    <span v-if="usuario.es_territorial" class="territorio-badge territorial">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                        <circle cx="12" cy="10" r="3"/>
                      </svg>
                      {{ usuario.territorio || 'Sin asignar' }}
                    </span>
                    <span v-else class="territorio-badge general">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M2 12h20"/>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                      </svg>
                      General
                    </span>
                  </td>
                  <td class="status-cell">
                    <span class="status-badge" :class="usuario.activo !== false ? 'status-active' : 'status-inactive'">
                      <svg v-if="usuario.activo !== false" class="status-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                      <svg v-else class="status-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                      </svg>
                      {{ usuario.activo !== false ? 'Activo' : 'Inactivo' }}
                    </span>
                  </td>
                  <td class="actions-cell">
                    <div class="action-buttons">
                      <button 
                        class="btn-action btn-edit" 
                        @click="editarUsuario(usuario)"
                        title="Editar usuario"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                          <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                      </button>
                      <button 
                        v-if="usuario.username !== 'admin'"
                        class="btn-action btn-delete" 
                        @click="confirmarEliminar(usuario)"
                        title="Eliminar usuario"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M3 6h18"/>
                          <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                          <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Estado vacío -->
            <div v-if="usuariosFiltrados.length === 0" class="empty-state">
              <div class="empty-icon">👥</div>
              <h3>No hay usuarios administrativos</h3>
              <p>Crea el primer usuario administrativo para gestionar el sistema.</p>
              <button class="btn-primary" @click="mostrarModalCrear = true">
                Crear Primer Usuario Admin
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Crear/Editar Usuario -->
    <div v-if="mostrarModalCrear || mostrarModalEditar" class="modal-overlay">
      <div class="modal-content modal-usuario" @click.stop>
        <div class="modal-header">
          <div class="modal-header-icon">
            <svg v-if="!modoEdicion" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="8.5" cy="7" r="4"/>
              <line x1="20" y1="8" x2="20" y2="14"/>
              <line x1="23" y1="11" x2="17" y2="11"/>
            </svg>
            <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </div>
          <h3>{{ modoEdicion ? 'Editar Usuario' : 'Nuevo Usuario Admin' }}</h3>
          <button class="btn-close" @click="cerrarModales" aria-label="Cerrar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="guardarUsuario">
            <!-- Sección de Información básica -->
            <div class="form-section">
              <div class="section-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                <h4>Información Básica</h4>
              </div>
              
              <!-- Nombre Completo -->
              <div class="form-group">
                <label for="nombre_completo">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  Nombre Completo
                </label>
                <input
                  id="nombre_completo"
                  v-model="formularioUsuario.nombre_completo"
                  type="text"
                  class="form-input uppercase-input"
                  placeholder="Ingrese el nombre completo"
                  @input="convertirMayusculas('nombre_completo')"
                />
                <small class="form-help">Se convertirá automáticamente a mayúsculas</small>
              </div>

              <!-- CURP -->
              <div class="form-group">
                <label for="curp">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="16" rx="2"/>
                    <line x1="7" y1="8" x2="17" y2="8"/>
                    <line x1="7" y1="12" x2="13" y2="12"/>
                  </svg>
                  CURP
                </label>
                <input
                  id="curp"
                  v-model="formularioUsuario.curp"
                  type="text"
                  class="form-input uppercase-input"
                  placeholder="Ingrese el CURP"
                  maxlength="18"
                  @input="convertirMayusculas('curp')"
                />
                <small class="form-help">18 caracteres - Se convertirá automáticamente a mayúsculas</small>
              </div>

              <!-- Cargo -->
              <div class="form-group">
                <label for="cargo">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 7H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/>
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                  </svg>
                  Cargo
                </label>
                <input
                  id="cargo"
                  v-model="formularioUsuario.cargo"
                  type="text"
                  class="form-input uppercase-input"
                  placeholder="Ingrese el cargo"
                  @input="convertirMayusculas('cargo')"
                />
                <small class="form-help">Se convertirá automáticamente a mayúsculas</small>
              </div>

              <!-- Username -->
              <div class="form-group">
                <label for="username">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  Nombre de Usuario
                  <span class="required">*</span>
                </label>
                <input
                  id="username"
                  v-model="formularioUsuario.username"
                  type="text"
                  class="form-input"
                  placeholder="Ingrese el nombre de usuario"
                  :disabled="modoEdicion && formularioUsuario.username === 'admin'"
                  required
                />
                <small class="form-help">Debe ser único y no puede contener espacios</small>
              </div>

              <!-- Password -->
              <div class="form-group">
                <label for="password">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  {{ modoEdicion ? 'Nueva Contraseña (opcional)' : 'Contraseña' }}
                  <span v-if="!modoEdicion" class="required">*</span>
                </label>
                <div class="input-password-wrapper">
                  <input
                    id="password"
                    v-model="formularioUsuario.password"
                    :type="mostrarPassword ? 'text' : 'password'"
                    class="form-input form-input-password"
                    placeholder="Ingrese la contraseña"
                    :required="!modoEdicion"
                  />
                  <button 
                    type="button" 
                    class="btn-toggle-password" 
                    @click="mostrarPassword = !mostrarPassword"
                    :title="mostrarPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                  >
                    <!-- Ojo abierto (visible) -->
                    <svg v-if="mostrarPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <!-- Ojo cerrado (oculto) -->
                    <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                  </button>
                </div>
                <small class="form-help">
                  {{ modoEdicion ? 'Deje vacío para mantener la contraseña actual' : 'Mínimo 6 caracteres' }}
                </small>
              </div>

              <!-- Confirmar Password (solo en modo creación) -->
              <div v-if="!modoEdicion" class="form-group">
                <label for="confirmPassword">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <polyline points="9 12 12 15 15 9"/>
                  </svg>
                  Confirmar Contraseña
                  <span class="required">*</span>
                </label>
                <div class="input-password-wrapper">
                  <input
                    id="confirmPassword"
                    v-model="formularioUsuario.confirmPassword"
                    :type="mostrarConfirmPassword ? 'text' : 'password'"
                    class="form-input form-input-password"
                    :class="{ 'input-error': formularioUsuario.confirmPassword && formularioUsuario.password !== formularioUsuario.confirmPassword, 'input-success': formularioUsuario.confirmPassword && formularioUsuario.password === formularioUsuario.confirmPassword }"
                    placeholder="Confirme la contraseña"
                    required
                  />
                  <button 
                    type="button" 
                    class="btn-toggle-password" 
                    @click="mostrarConfirmPassword = !mostrarConfirmPassword"
                    :title="mostrarConfirmPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                  >
                    <!-- Ojo abierto (visible) -->
                    <svg v-if="mostrarConfirmPassword" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    <!-- Ojo cerrado (oculto) -->
                    <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                  </button>
                </div>
                <small class="form-help" :class="{ 'help-error': formularioUsuario.confirmPassword && formularioUsuario.password !== formularioUsuario.confirmPassword, 'help-success': formularioUsuario.confirmPassword && formularioUsuario.password === formularioUsuario.confirmPassword }">
                  <template v-if="formularioUsuario.confirmPassword && formularioUsuario.password !== formularioUsuario.confirmPassword">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="15" y1="9" x2="9" y2="15"/>
                      <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                    Las contraseñas no coinciden
                  </template>
                  <template v-else-if="formularioUsuario.confirmPassword && formularioUsuario.password === formularioUsuario.confirmPassword">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    Las contraseñas coinciden
                  </template>
                  <template v-else>
                    Vuelva a escribir la contraseña para confirmar
                  </template>
                </small>
              </div>
            </div>

            <!-- Sección de Estado del Usuario (solo en modo edición) - MOVIDO ARRIBA -->
            <div v-if="modoEdicion" class="form-section estado-section">
              <div class="section-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
                <h4>Estado de la Cuenta</h4>
              </div>
              
              <div class="estado-toggle-container">
                <div class="estado-info">
                  <div class="estado-icon" :class="formularioUsuario.activo ? 'activo' : 'inactivo'">
                    <!-- Icono de check para activo -->
                    <svg v-if="formularioUsuario.activo" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                      <polyline points="22 4 12 14.01 9 11.01"/>
                    </svg>
                    <!-- Icono de X para inactivo -->
                    <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="15" y1="9" x2="9" y2="15"/>
                      <line x1="9" y1="9" x2="15" y2="15"/>
                    </svg>
                  </div>
                  <div class="estado-text">
                    <span class="estado-label">{{ formularioUsuario.activo ? 'Cuenta Activa' : 'Cuenta Inactiva' }}</span>
                    <span class="estado-desc">{{ formularioUsuario.activo ? 'El usuario puede acceder al sistema' : 'El usuario NO puede acceder al sistema' }}</span>
                  </div>
                </div>
                
                <label class="estado-switch" :class="{ 'disabled': formularioUsuario.username === 'admin' }">
                  <input 
                    type="checkbox" 
                    v-model="formularioUsuario.activo"
                    :disabled="formularioUsuario.username === 'admin'"
                  />
                  <span class="slider"></span>
                </label>
              </div>
              
              <div v-if="!formularioUsuario.activo" class="estado-warning">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
                <span>Al desactivar esta cuenta, el usuario será expulsado inmediatamente si está conectado.</span>
              </div>
              
              <div v-if="formularioUsuario.username === 'admin'" class="admin-protection-notice">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                <span>La cuenta de administrador principal no puede ser desactivada.</span>
              </div>
            </div>

            <!-- Sección de Restricción Territorial -->
            <div class="form-section territorial-section-modern">
              <div class="section-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                <h4>Restricción Territorial</h4>
              </div>
              <p class="section-description">Define si este usuario tendrá acceso restringido a un territorio específico</p>
              
              <!-- Toggle de Tipo de Acceso -->
              <div class="territorial-access-toggle">
                <div 
                  class="access-option" 
                  :class="{ 'selected': !formularioUsuario.es_territorial }"
                  @click="formularioUsuario.es_territorial = false; formularioUsuario.territorio = ''"
                >
                  <div class="access-option-icon global-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M2 12h20"/>
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                    </svg>
                  </div>
                  <div class="access-option-content">
                    <span class="access-option-title">Acceso Global</span>
                    <span class="access-option-desc">Ve información de todos los territorios</span>
                  </div>
                  <div class="access-checkmark">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                  </div>
                </div>
                
                <div 
                  class="access-option" 
                  :class="{ 'selected': formularioUsuario.es_territorial }"
                  @click="formularioUsuario.es_territorial = true"
                >
                  <div class="access-option-icon territorial-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                      <circle cx="12" cy="10" r="3"/>
                    </svg>
                  </div>
                  <div class="access-option-content">
                    <span class="access-option-title">Acceso Territorial</span>
                    <span class="access-option-desc">Solo ve información de un territorio</span>
                  </div>
                  <div class="access-checkmark">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                  </div>
                </div>
              </div>
              
              <!-- Selector de territorio (solo visible cuando es territorial) -->
              <transition name="slide-fade">
                <div v-if="formularioUsuario.es_territorial" class="territorio-selector-wrapper">
                  <div class="territorio-selector-header">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                      <circle cx="12" cy="10" r="3"/>
                    </svg>
                    <span>Selecciona el territorio asignado</span>
                  </div>
                  <select 
                    id="territorio-admin" 
                    v-model="formularioUsuario.territorio" 
                    class="form-select territorio-select-modern"
                    required
                  >
                    <option value="">-- Seleccione un territorio --</option>
                    <option 
                      v-for="terr in territoriosConEstado" 
                      :key="terr.nombre" 
                      :value="terr.nombre"
                      :disabled="terr.ocupado"
                      :class="{ 'territorio-ocupado': terr.ocupado }"
                    >
                      {{ terr.ocupado ? '🔒 ' + terr.nombre + ' (Asignado a: ' + terr.usuarioAsignado + ')' : terr.nombre }}
                    </option>
                  </select>
                  <div class="territorio-info-box">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="16" x2="12" y2="12"/>
                      <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                    <span>Este usuario solo podrá ver usuarios, registros y asistencias del territorio seleccionado</span>
                  </div>
                </div>
              </transition>
            </div>

            <!-- Sección de Rol -->
            <div class="form-section">
              <div class="section-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                <h4>Rol del Usuario</h4>
              </div>
              
              <div class="radio-group-modern">
                <div 
                  class="radio-card" 
                  :class="{ 'selected': formularioUsuario.rol === 'admin' }"
                  @click="formularioUsuario.rol = 'admin'"
                >
                  <input
                    v-model="formularioUsuario.rol"
                    type="radio"
                    value="admin"
                    :disabled="modoEdicion && formularioUsuario.username === 'admin'"
                  />
                  <div class="radio-card-icon admin-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 2L15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2z"/>
                    </svg>
                  </div>
                  <div class="radio-card-content">
                    <span class="radio-card-title">Administrador</span>
                    <span class="radio-card-desc">Acceso completo a todos los módulos</span>
                  </div>
                  <div class="radio-checkmark">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                  </div>
                </div>
                
                <div 
                  class="radio-card"
                  :class="{ 'selected': formularioUsuario.rol === 'user' }"
                  @click="formularioUsuario.rol = 'user'"
                >
                  <input
                    v-model="formularioUsuario.rol"
                    type="radio"
                    value="user"
                    :disabled="modoEdicion && formularioUsuario.username === 'admin'"
                  />
                  <div class="radio-card-icon user-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <div class="radio-card-content">
                    <span class="radio-card-title">Usuario</span>
                    <span class="radio-card-desc">Acceso limitado según permisos</span>
                  </div>
                  <div class="radio-checkmark">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Permisos de acceso (solo visible cuando el rol es 'user') -->
            <div v-if="formularioUsuario.rol === 'user'" class="form-section permisos-section-modern">
              <div class="section-header">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 12l2 2 4-4"/>
                  <circle cx="12" cy="12" r="10"/>
                </svg>
                <h4>Permisos de Acceso</h4>
              </div>
              <p class="section-description">Seleccione los módulos a los que el usuario tendrá acceso</p>
              
              <div class="permisos-grid-modern">
                <!-- Visor de Seguimiento (con sub-permiso de filtrador por territorio) -->
                <div class="permiso-card-wrapper" :class="{ 'expanded': formularioUsuario.permisos.visor }">
                  <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.visor }">
                    <input type="checkbox" v-model="formularioUsuario.permisos.visor" @change="onVisorChange" />
                    <div class="permiso-card-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M2 12h20"/>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                      </svg>
                    </div>
                    <span class="permiso-card-name">Visor de Seguimiento</span>
                    <div class="permiso-toggle">
                      <div class="toggle-track">
                        <div class="toggle-thumb"></div>
                      </div>
                    </div>
                  </label>
                  
                  <!-- Sub-permiso: Filtrador por Territorio -->
                  <div v-if="formularioUsuario.permisos.visor" class="sub-permiso-container">
                    <label class="sub-permiso-item" :class="{ 'active': formularioUsuario.permisos.visor_filtrador_territorio }">
                      <input type="checkbox" v-model="formularioUsuario.permisos.visor_filtrador_territorio" />
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                        <circle cx="12" cy="10" r="3"/>
                      </svg>
                      <span class="sub-permiso-text">Filtrador por territorio</span>
                      <div class="sub-toggle">
                        <div class="sub-toggle-track">
                          <div class="sub-toggle-thumb"></div>
                        </div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Asistencia -->
                <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.asistencia }">
                  <input type="checkbox" v-model="formularioUsuario.permisos.asistencia" />
                  <div class="permiso-card-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                      <polyline points="22 4 12 14.01 9 11.01"/>
                    </svg>
                  </div>
                  <span class="permiso-card-name">Asistencia</span>
                  <div class="permiso-toggle">
                    <div class="toggle-track">
                      <div class="toggle-thumb"></div>
                    </div>
                  </div>
                </label>

                <!-- Registros (con sub-permiso integrado) -->
                <div class="permiso-card-wrapper" :class="{ 'expanded': formularioUsuario.permisos.registros }">
                  <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.registros }">
                    <input type="checkbox" v-model="formularioUsuario.permisos.registros" @change="onRegistrosChange" />
                    <div class="permiso-card-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <line x1="16" y1="13" x2="8" y2="13"/>
                        <line x1="16" y1="17" x2="8" y2="17"/>
                      </svg>
                    </div>
                    <span class="permiso-card-name">Registros</span>
                    <div class="permiso-toggle">
                      <div class="toggle-track">
                        <div class="toggle-thumb"></div>
                      </div>
                    </div>
                  </label>
                  
                  <!-- Sub-permiso: Acciones de Registros (dentro del mismo recuadro) -->
                  <div v-if="formularioUsuario.permisos.registros" class="sub-permiso-container">
                    <label class="sub-permiso-item" :class="{ 'active': formularioUsuario.permisos.registros_acciones }">
                      <input type="checkbox" v-model="formularioUsuario.permisos.registros_acciones" />
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        <line x1="10" y1="11" x2="10" y2="17"/>
                        <line x1="14" y1="11" x2="14" y2="17"/>
                      </svg>
                      <span class="sub-permiso-text">Permitir eliminar</span>
                      <div class="sub-toggle">
                        <div class="sub-toggle-track">
                          <div class="sub-toggle-thumb"></div>
                        </div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Usuarios (con sub-permiso integrado) -->
                <div class="permiso-card-wrapper" :class="{ 'expanded': formularioUsuario.permisos.usuarios }">
                  <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.usuarios }">
                    <input type="checkbox" v-model="formularioUsuario.permisos.usuarios" @change="onUsuariosChange" />
                    <div class="permiso-card-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                      </svg>
                    </div>
                    <span class="permiso-card-name">Usuarios</span>
                    <div class="permiso-toggle">
                      <div class="toggle-track">
                        <div class="toggle-thumb"></div>
                      </div>
                    </div>
                  </label>
                  
                  <!-- Sub-permiso: Acciones de Usuarios (dentro del mismo recuadro) -->
                  <div v-if="formularioUsuario.permisos.usuarios" class="sub-permiso-container">
                    <label class="sub-permiso-item" :class="{ 'active': formularioUsuario.permisos.usuarios_acciones }">
                      <input type="checkbox" v-model="formularioUsuario.permisos.usuarios_acciones" />
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                      </svg>
                      <span class="sub-permiso-text">Permitir editar/eliminar</span>
                      <div class="sub-toggle">
                        <div class="sub-toggle-track">
                          <div class="sub-toggle-thumb"></div>
                        </div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Historiales -->
                <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.historiales }">
                  <input type="checkbox" v-model="formularioUsuario.permisos.historiales" />
                  <div class="permiso-card-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <polyline points="12 6 12 12 16 14"/>
                    </svg>
                  </div>
                  <span class="permiso-card-name">Historiales</span>
                  <div class="permiso-toggle">
                    <div class="toggle-track">
                      <div class="toggle-thumb"></div>
                    </div>
                  </div>
                </label>

                <!-- Notificaciones (con sub-permiso integrado) -->
                <div class="permiso-card-wrapper" :class="{ 'expanded': formularioUsuario.permisos.notificaciones }">
                  <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.notificaciones }">
                    <input type="checkbox" v-model="formularioUsuario.permisos.notificaciones" @change="onNotificacionesChange" />
                    <div class="permiso-card-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                      </svg>
                    </div>
                    <span class="permiso-card-name">Notificaciones</span>
                    <div class="permiso-toggle">
                      <div class="toggle-track">
                        <div class="toggle-thumb"></div>
                      </div>
                    </div>
                  </label>
                  
                  <!-- Sub-permiso: Acciones de Notificaciones (dentro del mismo recuadro) -->
                  <div v-if="formularioUsuario.permisos.notificaciones" class="sub-permiso-container">
                    <label class="sub-permiso-item" :class="{ 'active': formularioUsuario.permisos.notificaciones_acciones }">
                      <input type="checkbox" v-model="formularioUsuario.permisos.notificaciones_acciones" />
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                      </svg>
                      <span class="sub-permiso-text">Permitir editar/eliminar</span>
                      <div class="sub-toggle">
                        <div class="sub-toggle-track">
                          <div class="sub-toggle-thumb"></div>
                        </div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Permisos -->
                <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.permisos }">
                  <input type="checkbox" v-model="formularioUsuario.permisos.permisos" />
                  <div class="permiso-card-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                  </div>
                  <span class="permiso-card-name">Permisos</span>
                  <div class="permiso-toggle">
                    <div class="toggle-track">
                      <div class="toggle-thumb"></div>
                    </div>
                  </div>
                </label>

                <!-- Configuración -->
                <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.configuracion }">
                  <input type="checkbox" v-model="formularioUsuario.permisos.configuracion" />
                  <div class="permiso-card-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="3"/>
                      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                    </svg>
                  </div>
                  <span class="permiso-card-name">Configuración</span>
                  <div class="permiso-toggle">
                    <div class="toggle-track">
                      <div class="toggle-thumb"></div>
                    </div>
                  </div>
                </label>

                <!-- Reportes -->
                <label class="permiso-card" :class="{ 'active': formularioUsuario.permisos.reportes }">
                  <input type="checkbox" v-model="formularioUsuario.permisos.reportes" />
                  <div class="permiso-card-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="16" y1="13" x2="8" y2="13"/>
                      <line x1="16" y1="17" x2="8" y2="17"/>
                      <polyline points="10 9 9 9 8 9"/>
                    </svg>
                  </div>
                  <span class="permiso-card-name">Reportes</span>
                  <div class="permiso-toggle">
                    <div class="toggle-track">
                      <div class="toggle-thumb"></div>
                    </div>
                  </div>
                </label>
              </div>

              <!-- Botones rápidos de selección -->
              <div class="permisos-quick-actions">
                <button type="button" class="btn-quick-action btn-select-all" @click="seleccionarTodos">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="9 11 12 14 22 4"/>
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                  </svg>
                  Seleccionar todos
                </button>
                <button type="button" class="btn-quick-action btn-deselect-all" @click="deseleccionarTodos">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  </svg>
                  Deseleccionar todos
                </button>
              </div>
            </div>

            <!-- Info para admin (todos los permisos) -->
            <div v-if="formularioUsuario.rol === 'admin'" class="admin-info-banner">
              <div class="admin-banner-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
              </div>
              <div class="admin-banner-content">
                <strong>Acceso Completo</strong>
                <p>Los administradores tienen acceso a todos los módulos del sistema automáticamente.</p>
              </div>
            </div>

            <!-- Botones del formulario -->
            <div class="modal-footer">
              <button type="button" class="btn-modal btn-cancel" @click="cerrarModales">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                Cancelar
              </button>
              <button type="submit" class="btn-modal btn-submit" :disabled="guardando">
                <span v-if="guardando" class="btn-spinner"></span>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                {{ guardando ? 'Guardando...' : (modoEdicion ? 'Actualizar' : 'Crear Usuario') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal Confirmar Eliminación -->
    <div v-if="mostrarModalEliminar" class="modal-overlay">
      <div class="modal-content modal-confirm" @click.stop>
        <div class="modal-header modal-header-danger">
          <div class="modal-header-icon danger-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18"/>
              <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
              <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
              <line x1="10" y1="11" x2="10" y2="17"/>
              <line x1="14" y1="11" x2="14" y2="17"/>
            </svg>
          </div>
          <h3>Confirmar Eliminación</h3>
          <button class="btn-close" @click="cancelarEliminar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="confirm-content">
            <div class="confirm-icon">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
            </div>
            <h4>¿Estás seguro de que deseas eliminar este usuario?</h4>
            <p><strong>Usuario:</strong> {{ usuarioAEliminar?.username }}</p>
            <p><strong>Rol:</strong> {{ usuarioAEliminar?.rol === 'admin' ? 'Administrador' : 'Usuario' }}</p>
            
            <div class="warning-text">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
              Esta acción no se puede deshacer. El usuario perderá acceso inmediatamente.
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-modal btn-cancel" @click="cancelarEliminar">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
              Cancelar
            </button>
            <button class="btn-modal btn-delete" @click="eliminarUsuario" :disabled="eliminando">
              <span v-if="eliminando" class="btn-spinner"></span>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18"/>
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
              </svg>
              {{ eliminando ? 'Eliminando...' : 'Eliminar Usuario' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast de notificaciones -->
    <div v-if="toast.show" class="toast" :class="toast.type">
      <div class="toast-content">
        <div class="toast-icon">
          <svg v-if="toast.type === 'success'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
        </div>
        <div class="toast-message">{{ toast.message }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'
import permisosService from '../services/permisosService.js'
import authService from '../services/authService.js'

export default {
  name: 'PermisosView',
  components: {
    Sidebar
  },
  data() {
    return {
      isOnline: navigator.onLine,
      cargando: false,
      error: null,
      
      // Lista de usuarios admin
      usuariosAdmin: [],
      filtroRol: '',
      
      // Modal crear/editar usuario
      mostrarModalCrear: false,
      mostrarModalEditar: false,
      modoEdicion: false,
      usuarioEditando: null,
      guardando: false,
      mostrarPassword: false,
      mostrarConfirmPassword: false,
      formularioUsuario: {
        username: '',
        password: '',
        confirmPassword: '',
        rol: 'user',
        activo: true,
        es_territorial: false,
        territorio: '',
        permisos: {
          visor: false,
          visor_filtrador_territorio: false,
          asistencia: false,
          registros: false,
          registros_acciones: false,
          usuarios: false,
          usuarios_acciones: false,
          historiales: false,
          notificaciones: false,
          notificaciones_acciones: false,
          permisos: false,
          configuracion: false,
          reportes: false
        }
      },
      
      // Lista de territorios de Sembrando Vida
      territoriosSembrandoVida: [
        "Acapulco - Centro - Norte - Tierra Caliente",
        "Acayucan",
        "Balancán",
        "Chihuahua / Sonora",
        "Colima",
        "Comalcalco",
        "Córdoba",
        "Costa Chica - Montaña",
        "Costa Grande - Sierra",
        "Durango / Zacatecas",
        "Hidalgo",
        "Istmo",
        "Michoacán",
        "Mixteca",
        "Morelos",
        "Nayarit / Jalisco",
        "Ocosingo",
        "Palenque",
        "Papantla",
        "Pichucalco",
        "Puebla",
        "San Luis Potosí",
        "Sinaloa",
        "Tamaulipas",
        "Tantoyuca",
        "Tapachula",
        "Teapa",
        "Tlaxcala / Estado de México",
        "Tzucacab / Opb",
        "Xpujil",
        "Oficinas Centrales"
      ],
      
      // Permisos por defecto para nuevos usuarios (todos en false)
      permisosDefault: {
        visor: false,
        visor_filtrador_territorio: false,
        asistencia: false,
        registros: false,
        registros_acciones: false,
        usuarios: false,
        usuarios_acciones: false,
        historiales: false,
        notificaciones: false,
        notificaciones_acciones: false,
        permisos: false,
        configuracion: false,
        reportes: false
      },
      
      // Modal eliminar
      mostrarModalEliminar: false,
      usuarioAEliminar: null,
      eliminando: false,
      
      // Toast
      toast: {
        show: false,
        type: 'success',
        message: ''
      }
    }
  },
  
  computed: {
    usuariosFiltrados() {
      if (!this.filtroRol) return this.usuariosAdmin
      return this.usuariosAdmin.filter(usuario => usuario.rol === this.filtroRol)
    },
    
    // Territorios que ya están asignados a usuarios territoriales
    territoriosOcupados() {
      const ocupados = new Set()
      this.usuariosAdmin.forEach(usuario => {
        // Solo contar como ocupado si es territorial y tiene territorio asignado
        // Y no es el usuario que estamos editando actualmente
        if (usuario.es_territorial && usuario.territorio) {
          // Si estamos editando, no bloquear el territorio del usuario que editamos
          if (this.modoEdicion && this.usuarioEditando && usuario.id === this.usuarioEditando.id) {
            return
          }
          ocupados.add(usuario.territorio)
        }
      })
      return ocupados
    },
    
    // Lista de territorios con info de disponibilidad
    territoriosConEstado() {
      return this.territoriosSembrandoVida.map(territorio => {
        const ocupado = this.territoriosOcupados.has(territorio)
        const usuarioAsignado = ocupado ? this.usuariosAdmin.find(u => u.es_territorial && u.territorio === territorio) : null
        return {
          nombre: territorio,
          ocupado,
          usuarioAsignado: usuarioAsignado ? usuarioAsignado.username : null
        }
      })
    }
  },
  
  mounted() {
    this.configurarEventosConexion()
    this.cargarUsuariosAdmin()
  },
  
  methods: {
    configurarEventosConexion() {
      window.addEventListener('online', () => {
        this.isOnline = true
      })
      
      window.addEventListener('offline', () => {
        this.isOnline = false
      })
    },

    // Handler cuando se cambia el permiso de usuarios
    onUsuariosChange() {
      // Si se desactiva usuarios, también desactivar usuarios_acciones
      if (!this.formularioUsuario.permisos.usuarios) {
        this.formularioUsuario.permisos.usuarios_acciones = false
      }
    },

    // Handler cuando se cambia el permiso de registros
    onRegistrosChange() {
      // Si se desactiva registros, también desactivar registros_acciones
      if (!this.formularioUsuario.permisos.registros) {
        this.formularioUsuario.permisos.registros_acciones = false
      }
    },

    // Handler cuando se cambia el permiso de notificaciones
    onNotificacionesChange() {
      // Si se desactiva notificaciones, también desactivar notificaciones_acciones
      if (!this.formularioUsuario.permisos.notificaciones) {
        this.formularioUsuario.permisos.notificaciones_acciones = false
      }
    },

    // Handler cuando se cambia el permiso de visor
    onVisorChange() {
      // Si se desactiva visor, también desactivar visor_filtrador_territorio
      if (!this.formularioUsuario.permisos.visor) {
        this.formularioUsuario.permisos.visor_filtrador_territorio = false
      }
    },

    // Handler cuando se cambia el checkbox de territorial
    onTerritorialChange() {
      // Si se desactiva territorial, limpiar el territorio seleccionado
      if (!this.formularioUsuario.es_territorial) {
        this.formularioUsuario.territorio = ''
      }
    },

    // ==================== GESTIÓN DE USUARIOS ADMIN ====================
    
    async cargarUsuariosAdmin() {
      this.cargando = true
      this.error = null
      
      try {
        console.log('🔄 Cargando usuarios con servicio original...')
        const respuesta = await permisosService.listarUsuarios()
        this.usuariosAdmin = respuesta.usuarios || []
        console.log('✅ Usuarios admin cargados:', this.usuariosAdmin.length)
      } catch (error) {
        console.error('❌ Error cargando usuarios admin:', error)
        this.error = error.message
      } finally {
        this.cargando = false
      }
    },

    aplicarFiltros() {
      // Los filtros se aplican automáticamente a través del computed usuariosFiltrados
      console.log('🔍 Filtro aplicado:', this.filtroRol)
    },

    // ==================== CREAR/EDITAR USUARIO ADMIN ====================
    
    editarUsuario(usuario) {
      this.modoEdicion = true
      this.usuarioEditando = usuario
      
      // Cargar permisos del usuario o usar defaults
      const permisosUsuario = usuario.permisos ? { ...usuario.permisos } : { ...this.permisosDefault }
      
      // MIGRACIÓN: Si el usuario ya tiene visor activo pero no tiene el nuevo sub-permiso definido,
      // activarlo automáticamente (para usuarios que ya tenían visor antes de esta actualización)
      if (permisosUsuario.visor === true && permisosUsuario.visor_filtrador_territorio === undefined) {
        permisosUsuario.visor_filtrador_territorio = true
        console.log('🔄 Migración automática: Activando visor_filtrador_territorio para usuario con visor existente')
      }
      
      // Asegurar que el nuevo permiso existe en el objeto
      if (permisosUsuario.visor_filtrador_territorio === undefined) {
        permisosUsuario.visor_filtrador_territorio = false
      }
      
      this.formularioUsuario = {
        username: usuario.username,
        password: '', // No mostramos la contraseña actual
        confirmPassword: '',
        rol: usuario.rol,
        activo: usuario.activo !== false, // Por defecto true si no existe
        es_territorial: usuario.es_territorial || false,
        territorio: usuario.territorio || '',
        nombre_completo: usuario.nombre_completo || '',
        curp: usuario.curp || '',
        cargo: usuario.cargo || '',
        permisos: permisosUsuario
      }
      // Resetear visibilidad de contraseñas
      this.mostrarPassword = false
      this.mostrarConfirmPassword = false
      this.mostrarModalEditar = true
    },

    async guardarUsuario() {
      // Validaciones básicas
      if (!this.formularioUsuario.username.trim()) {
        this.mostrarToast('El nombre de usuario es obligatorio', 'error')
        return
      }
      
      // Validar que no tenga espacios
      if (this.formularioUsuario.username.includes(' ')) {
        this.mostrarToast('El nombre de usuario no puede contener espacios', 'error')
        return
      }
      
      if (!this.modoEdicion && !this.formularioUsuario.password.trim()) {
        this.mostrarToast('La contraseña es obligatoria para nuevos usuarios', 'error')
        return
      }

      if (this.formularioUsuario.password && this.formularioUsuario.password.length < 6) {
        this.mostrarToast('La contraseña debe tener al menos 6 caracteres', 'error')
        return
      }

      // Validar que las contraseñas coincidan (solo en modo creación)
      if (!this.modoEdicion && this.formularioUsuario.password !== this.formularioUsuario.confirmPassword) {
        this.mostrarToast('Las contraseñas no coinciden', 'error')
        return
      }

      // Validar territorio si es usuario territorial
      if (this.formularioUsuario.es_territorial && !this.formularioUsuario.territorio) {
        this.mostrarToast('Debe seleccionar un territorio para usuarios territoriales', 'error')
        return
      }
      
      this.guardando = true
      
      try {
        if (this.modoEdicion) {
          // Actualizar usuario existente
          const datosActualizacion = {
            username: this.formularioUsuario.username,
            rol: this.formularioUsuario.rol,
            permisos: this.formularioUsuario.rol === 'user' ? this.formularioUsuario.permisos : null,
            activo: this.formularioUsuario.activo,
            es_territorial: this.formularioUsuario.es_territorial,
            territorio: this.formularioUsuario.es_territorial ? this.formularioUsuario.territorio : null,
            nombre_completo: this.formularioUsuario.nombre_completo,
            curp: this.formularioUsuario.curp,
            cargo: this.formularioUsuario.cargo
          }
          
          // Solo incluir password si se proporcionó
          if (this.formularioUsuario.password.trim()) {
            datosActualizacion.password = this.formularioUsuario.password
          }
          
          await permisosService.actualizarUsuario(this.usuarioEditando.id, datosActualizacion)
          
          // Actualizar inmediatamente en el array local para respuesta instantánea
          const indexUsuario = this.usuariosAdmin.findIndex(u => u.id === this.usuarioEditando.id)
          if (indexUsuario !== -1) {
            this.usuariosAdmin[indexUsuario] = {
              ...this.usuariosAdmin[indexUsuario],
              username: datosActualizacion.username,
              rol: datosActualizacion.rol,
              permisos: datosActualizacion.permisos,
              activo: datosActualizacion.activo,
              es_territorial: datosActualizacion.es_territorial,
              territorio: datosActualizacion.territorio,
              nombre_completo: datosActualizacion.nombre_completo,
              curp: datosActualizacion.curp,
              cargo: datosActualizacion.cargo
            }
            // Forzar reactividad en Vue
            this.usuariosAdmin = [...this.usuariosAdmin]
            console.log('✅ Lista actualizada instantáneamente')
          }
          
          this.mostrarToast('Usuario administrativo actualizado exitosamente', 'success')
          
          // Si se editó el usuario actual, actualizar permisos inmediatamente
          const currentUser = authService.getCurrentUser()
          if (currentUser && currentUser.username === this.formularioUsuario.username) {
            const newUserData = {
              ...currentUser,
              rol: datosActualizacion.rol,
              permisos: datosActualizacion.permisos || currentUser.permisos,
              es_territorial: datosActualizacion.es_territorial,
              territorio: datosActualizacion.territorio
            }
            // Actualizar localStorage
            localStorage.setItem('admin_user_data', JSON.stringify(newUserData))
            // Disparar evento para actualizar todas las vistas
            window.dispatchEvent(new CustomEvent('user-session-updated', { 
              detail: newUserData 
            }))
            console.log('🔄 Permisos del usuario actual actualizados inmediatamente')
          }
        } else {
          // Crear nuevo usuario (siempre activo)
          const datosCreacion = {
            ...this.formularioUsuario,
            permisos: this.formularioUsuario.rol === 'user' ? this.formularioUsuario.permisos : null,
            es_territorial: this.formularioUsuario.es_territorial,
            territorio: this.formularioUsuario.es_territorial ? this.formularioUsuario.territorio : null
          }
          const respuesta = await permisosService.crearUsuario(datosCreacion)
          
          // Agregar inmediatamente al array local para respuesta instantánea
          const nuevoUsuario = {
            id: respuesta.id || Date.now(), // Usar ID devuelto o temporal
            username: datosCreacion.username,
            rol: datosCreacion.rol,
            permisos: datosCreacion.permisos,
            activo: true,
            es_territorial: datosCreacion.es_territorial,
            territorio: datosCreacion.territorio,
            nombre_completo: datosCreacion.nombre_completo,
            curp: datosCreacion.curp,
            cargo: datosCreacion.cargo
          }
          this.usuariosAdmin = [nuevoUsuario, ...this.usuariosAdmin]
          console.log('✅ Nuevo usuario agregado instantáneamente a la lista')
          
          this.mostrarToast('Usuario administrativo creado exitosamente', 'success')
        }
        
        // Recargar lista desde servidor para sincronizar (en background)
        this.cargarUsuariosAdmin()
        this.cerrarModales()
        
      } catch (error) {
        console.error('❌ Error guardando usuario admin:', error)
        this.mostrarToast(error.message, 'error')
      } finally {
        this.guardando = false
      }
    },

    cerrarModales() {
      this.mostrarModalCrear = false
      this.mostrarModalEditar = false
      this.modoEdicion = false
      this.usuarioEditando = null
      this.limpiarFormulario()
    },

    limpiarFormulario() {
      this.formularioUsuario = {
        username: '',
        password: '',
        confirmPassword: '',
        rol: 'user',
        activo: true,
        es_territorial: false,
        territorio: '',
        nombre_completo: '',
        curp: '',
        cargo: '',
        permisos: { ...this.permisosDefault }
      }
      // Resetear visibilidad de contraseñas
      this.mostrarPassword = false
      this.mostrarConfirmPassword = false
    },

    // Métodos para seleccionar/deseleccionar permisos
    seleccionarTodos() {
      Object.keys(this.formularioUsuario.permisos).forEach(key => {
        this.formularioUsuario.permisos[key] = true
      })
    },

    deseleccionarTodos() {
      Object.keys(this.formularioUsuario.permisos).forEach(key => {
        this.formularioUsuario.permisos[key] = false
      })
    },

    // Método para convertir campos a mayúsculas automáticamente
    convertirMayusculas(campo) {
      if (this.formularioUsuario[campo]) {
        this.formularioUsuario[campo] = this.formularioUsuario[campo].toUpperCase()
      }
    },

    // ==================== ELIMINAR USUARIO ADMIN ====================
    
    confirmarEliminar(usuario) {
      this.usuarioAEliminar = usuario
      this.mostrarModalEliminar = true
    },

    cancelarEliminar() {
      this.mostrarModalEliminar = false
      this.usuarioAEliminar = null
    },

    async eliminarUsuario() {
      if (!this.usuarioAEliminar) return
      
      this.eliminando = true
      
      try {
        await permisosService.eliminarUsuario(this.usuarioAEliminar.id)
        
        this.mostrarToast('Usuario administrativo eliminado exitosamente', 'success')
        this.cargarUsuariosAdmin()
        this.cancelarEliminar()
        
      } catch (error) {
        console.error('❌ Error eliminando usuario admin:', error)
        this.mostrarToast(error.message, 'error')
      } finally {
        this.eliminando = false
      }
    },

    // ==================== UTILIDADES ====================
    
    mostrarToast(message, type = 'success') {
      this.toast = {
        show: true,
        type,
        message
      }

      setTimeout(() => {
        this.toast.show = false
      }, 4000)
    },
    
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.permisos-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
  overflow-x: hidden;
}

/* === HEADER STYLES === */
.page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  padding: clamp(0.3rem, 0.8vw, 0.5rem);
  box-shadow: 
    0 4px 16px rgba(76, 175, 80, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
  margin: 0;
  gap: clamp(0.25rem, 0.8vw, 0.5rem);
  flex-wrap: wrap;
  width: 100%;
  position: relative;
  z-index: 2;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.2vw, 0.8rem);
  flex: 1;
  min-width: 140px;
  margin-left: clamp(0.3rem, 1vw, 0.6rem);
}

.header-icon {
  width: clamp(28px, 3vw, 32px);
  height: clamp(28px, 3vw, 32px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.header-icon svg {
  width: clamp(14px, 2.5vw, 16px);
  height: clamp(14px, 2.5vw, 16px);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: clamp(14px, 2.5vw, 16px);
  font-weight: 700;
  margin: 0 0 clamp(1px, 0.3vw, 2px) 0;
  background: linear-gradient(135deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.2;
}

.header-subtitle {
  font-size: clamp(9px, 1.8vw, 11px);
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.3;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.2vw, 0.75rem);
  flex-shrink: 0;
}

.btn-primary {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: clamp(6px, 1vw, 8px) clamp(12px, 2vw, 14px);
  border-radius: clamp(12px, 2vw, 14px);
  font-weight: 600;
  font-size: clamp(10px, 1.8vw, 11px);
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8vw, 6px);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: inherit;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.btn-primary:hover::before {
  opacity: 1;
}

.btn-primary svg {
  width: clamp(12px, 2vw, 14px);
  height: clamp(12px, 2vw, 14px);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
}

.btn-primary:hover svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  transform: scale(1.05);
}

/* === CONTENT STYLES === */
.page-content {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* === LOADING & ERROR STATES === */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e8f5e8;
  border-top: 3px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.btn-secondary {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  color: #333;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.btn-secondary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* === USUARIOS LIST === */
.usuarios-list {
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  border-radius: 16px;
  padding: 0;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 4px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(76, 175, 80, 0.1);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
}

.list-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.header-filters {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  font-size: 14px;
  background: white;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.filter-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.btn-refresh {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.btn-refresh:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* === USUARIOS TABLE === */
.usuarios-table-container {
  overflow-x: auto;
}

.usuarios-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Inter', sans-serif;
}

.usuarios-table th {
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  color: #2E7D32;
  font-weight: 600;
  font-size: 13px;
  padding: 14px 16px;
  text-align: center;
  border-bottom: 2px solid rgba(76, 175, 80, 0.2);
  white-space: nowrap;
}

.usuarios-table td {
  padding: 16px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  vertical-align: middle;
  text-align: center;
}

.usuario-row:hover {
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff4 100%);
}

.name-cell {
  min-width: 200px;
  text-align: left !important;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: flex-start;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: transparent;
  border: 1.5px solid #4CAF50;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4CAF50;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: left;
}

.user-name {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.user-supervisor {
  font-size: 12px;
  color: #666;
}

.rol-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
  width: 110px;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.rol-icon {
  flex-shrink: 0;
  width: 12px;
  height: 12px;
}

.rol-text {
  line-height: 1;
}

.rol-badge.admin {
  background: rgba(255, 152, 0, 0.1);
  color: #f57c00;
  border: 1.5px solid #ff9800;
}

.rol-badge.admin .rol-icon {
  color: #f57c00;
}

.rol-badge.admin:hover {
  background: rgba(255, 152, 0, 0.15);
}

.rol-badge.user {
  background: rgba(142, 36, 170, 0.1);
  color: #8e24aa;
  border: 1.5px solid #9c27b0;
}

.rol-badge.user .rol-icon {
  color: #8e24aa;
}

.rol-badge.user:hover {
  background: rgba(142, 36, 170, 0.15);
}

.rol-cell {
  text-align: center;
}

.status-cell {
  text-align: center;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  min-width: 80px;
}

.status-badge .status-icon {
  flex-shrink: 0;
}

.status-active {
  background: rgba(76, 175, 80, 0.1);
  color: #2e7d32;
  border: 1.5px solid #4CAF50;
}

.status-inactive {
  background: rgba(244, 67, 54, 0.1);
  color: #c62828;
  border: 1.5px solid #f44336;
}

/* Estilos para columna de Información Personal */
.info-personal-cell {
  vertical-align: middle;
  min-width: 200px;
  max-width: 280px;
}

.info-personal {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #333;
}

.info-item svg {
  flex-shrink: 0;
  color: #666;
}

.info-item.nombre-completo {
  font-weight: 600;
  color: #1a237e;
  font-size: 12px;
}

.info-item.curp .curp-text {
  font-family: 'Courier New', monospace;
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10px;
  letter-spacing: 0.5px;
}

.info-item.cargo {
  color: #00695c;
  font-style: italic;
}

.info-empty {
  text-align: center;
}

.info-empty .text-muted {
  color: #999;
  font-size: 11px;
  font-style: italic;
}

/* Estilos para badges territoriales en tabla */
.territorio-cell {
  text-align: center;
  vertical-align: middle;
}

.territorio-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 5px 10px;
  border-radius: 16px;
  font-size: 10px;
  font-weight: 600;
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.territorio-badge svg {
  flex-shrink: 0;
}

.territorio-badge.territorial {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.15) 0%, rgba(13, 148, 136, 0.2) 100%);
  color: #0f766e;
  border: 1.5px solid #14b8a6;
  box-shadow: 0 1px 3px rgba(20, 184, 166, 0.15);
}

.territorio-badge.territorial:hover {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.25) 0%, rgba(13, 148, 136, 0.3) 100%);
  box-shadow: 0 2px 6px rgba(20, 184, 166, 0.25);
}

.territorio-badge.general {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.12) 0%, rgba(2, 132, 199, 0.18) 100%);
  color: #0369a1;
  border: 1.5px solid #0ea5e9;
  box-shadow: 0 1px 3px rgba(14, 165, 233, 0.12);
}

.territorio-badge.general:hover {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(2, 132, 199, 0.28) 100%);
  box-shadow: 0 2px 6px rgba(14, 165, 233, 0.2);
}

.actions-cell {
  text-align: center;
}

.action-buttons {
  display: inline-flex;
  gap: 8px;
  justify-content: center;
}

.btn-action {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn-edit {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1976d2;
}

.btn-edit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
}

.btn-delete {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  color: #d32f2f;
}

.btn-delete:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.3);
}

/* === EMPTY STATE === */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  color: #2E7D32;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
  font-family: 'Inter', sans-serif;
}

.empty-state p {
  color: #666;
  margin: 0 0 24px 0;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

/* === MODALS === */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(6px);
  padding: 16px;
  box-sizing: border-box;
}

.modal-content {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 580px;
  max-height: calc(100vh - 32px);
  overflow: hidden;
  box-shadow: 
    0 24px 48px rgba(0, 0, 0, 0.25),
    0 12px 24px rgba(0, 0, 0, 0.15);
  animation: modalSlideIn 0.3s ease-out;
  display: flex;
  flex-direction: column;
}

.modal-usuario {
  max-width: 640px;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-confirm {
  max-width: 480px;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 24px;
  border-bottom: 1px solid #e8f5e9;
  background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%);
  flex-shrink: 0;
}

.modal-header-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.modal-header-icon svg {
  color: white;
}

.modal-header h3 {
  flex: 1;
  font-size: 18px;
  font-weight: 600;
  color: #1b5e20;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.btn-close {
  background: transparent;
  border: none;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  cursor: pointer;
  color: #666;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-close:hover {
  background: rgba(211, 47, 47, 0.1);
  color: #d32f2f;
}

.modal-body {
  padding: 16px;
  overflow-y: auto;
  flex: 1;
  max-height: calc(100vh - 180px);
}

/* === FORM SECTIONS === */
.form-section {
  margin-bottom: 12px;
  padding: 12px 14px;
  background: #fafffe;
  border-radius: 10px;
  border: 1px solid #e8f5e9;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e8f5e9;
}

.section-header svg {
  width: 16px;
  height: 16px;
  color: #4CAF50;
  flex-shrink: 0;
}

.section-header h4 {
  font-size: 13px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.section-description {
  color: #666;
  font-size: 11px;
  margin: 0 0 10px 0;
}

/* === FORM INPUTS === */
.form-group {
  margin-bottom: 10px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
  font-size: 11px;
  font-family: 'Inter', sans-serif;
}

.form-group label svg {
  width: 12px;
  height: 12px;
  color: #4CAF50;
  flex-shrink: 0;
}

.required {
  color: #d32f2f;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 8px 10px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 12px;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s ease;
  box-sizing: border-box;
  background: #fff;
}

.form-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.form-input:disabled {
  background: #f5f5f5;
  color: #999;
}

/* Input para mayúsculas automáticas */
.form-input.uppercase-input {
  text-transform: uppercase;
}

.form-input.uppercase-input::placeholder {
  text-transform: none;
}

.form-help {
  font-size: 10px;
  color: #888;
  margin-top: 4px;
  display: block;
}

/* === PASSWORD INPUT WITH TOGGLE === */
.input-password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input-password {
  padding-right: 36px !important;
}

.btn-toggle-password {
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
  color: #666;
}

.btn-toggle-password:hover {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.btn-toggle-password:active {
  transform: translateY(-50%) scale(0.95);
}

.btn-toggle-password svg {
  width: 16px;
  height: 16px;
}

/* Estados de validación para contraseñas */
.form-input.input-error {
  border-color: #d32f2f;
  background: #fff5f5;
}

.form-input.input-error:focus {
  border-color: #d32f2f;
  box-shadow: 0 0 0 4px rgba(211, 47, 47, 0.1);
}

.form-input.input-success {
  border-color: #4CAF50;
  background: #f5fff5;
}

.form-input.input-success:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 4px rgba(76, 175, 80, 0.15);
}

/* Mensajes de ayuda con estado */
.form-help.help-error {
  color: #d32f2f;
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-help.help-error svg {
  color: #d32f2f;
}

.form-help.help-success {
  color: #4CAF50;
  display: flex;
  align-items: center;
  gap: 4px;
}

.form-help.help-success svg {
  color: #4CAF50;
}

/* === RADIO CARDS (ROL) === */
.radio-group-modern {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.radio-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 12px 10px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s ease;
  background: #fff;
}

.radio-card:hover {
  border-color: #bdbdbd;
  background: #fafafa;
}

.radio-card.selected {
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
}

/* Admin seleccionado - Naranja */
.radio-card.selected:has(.admin-icon),
.radio-card.selected .admin-icon ~ * {
  border-color: transparent;
}

.radio-card input[type="radio"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio-card-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 6px;
  transition: all 0.25s ease;
}

.radio-card-icon svg {
  width: 18px;
  height: 18px;
}

/* Admin - Naranja */
.admin-icon {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  color: #f57c00;
}

.radio-card.selected .admin-icon {
  background: linear-gradient(135deg, #f57c00 0%, #e65100 100%);
  color: white;
}

.radio-card:has(.admin-icon).selected {
  border-color: #f57c00;
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
}

/* Usuario - Púrpura/Violeta */
.user-icon {
  background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
  color: #8e24aa;
}

.radio-card.selected .user-icon {
  background: linear-gradient(135deg, #8e24aa 0%, #6a1b9a 100%);
  color: white;
}

.radio-card:has(.user-icon).selected {
  border-color: #8e24aa;
  background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
}

.radio-card-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.radio-card-title {
  font-weight: 600;
  color: #333;
  font-size: 11px;
}

.radio-card-desc {
  font-size: 9px;
  color: #666;
  line-height: 1.25;
}

.radio-checkmark {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.25s ease;
}

.radio-checkmark svg {
  width: 10px;
  height: 10px;
}

.radio-card:has(.admin-icon).selected .radio-checkmark {
  opacity: 1;
  transform: scale(1);
  background: #f57c00;
  color: white;
}

.radio-card:has(.user-icon).selected .radio-checkmark {
  opacity: 1;
  transform: scale(1);
  background: #8e24aa;
  color: white;
}

/* === PERMISOS GRID MODERN === */
.permisos-section-modern {
  background: linear-gradient(135deg, #faf5fc 0%, #f3e5f5 100%);
  border-color: #e1bee7;
}

.permisos-section-modern .section-header svg {
  color: #8e24aa;
}

.permisos-section-modern .section-header h4 {
  color: #6a1b9a;
}

.permisos-section-modern .section-description {
  color: #7b1fa2;
}

.permisos-grid-modern {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.permiso-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border: 1.5px solid #e8e8e8;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #fff;
}

.permiso-card:hover {
  border-color: #ce93d8;
  background: #faf5fc;
}

.permiso-card.active {
  border-color: #8e24aa;
  background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
}

.permiso-card input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.permiso-card-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
  color: #666;
}

.permiso-card-icon svg {
  width: 14px;
  height: 14px;
}

.permiso-card.active .permiso-card-icon {
  background: linear-gradient(135deg, #8e24aa 0%, #6a1b9a 100%);
  color: white;
}

.permiso-card-name {
  flex: 1;
  font-size: 11px;
  font-weight: 500;
  color: #333;
}

.permiso-toggle {
  flex-shrink: 0;
}

.toggle-track {
  width: 32px;
  height: 16px;
  background: #e0e0e0;
  border-radius: 8px;
  position: relative;
  transition: all 0.2s ease;
}

.permiso-card.active .toggle-track {
  background: #8e24aa;
}

.toggle-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.permiso-card.active .toggle-thumb {
  left: 18px;
}

/* === WRAPPER PARA PERMISOS CON SUB-PERMISOS === */
.permiso-card-wrapper {
  display: flex;
  flex-direction: column;
}

.permiso-card-wrapper .permiso-card {
  flex: none;
}

.permiso-card-wrapper.expanded .permiso-card {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom-color: transparent;
}

/* === SUB-PERMISOS INTEGRADOS === */
.sub-permiso-container {
  background: linear-gradient(135deg, #faf5fc 0%, #f3e5f5 100%);
  border: 1.5px solid #8e24aa;
  border-top: 1px dashed #ce93d8;
  border-radius: 0 0 8px 8px;
  padding: 6px 10px;
  margin-top: -1.5px;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.sub-permiso-item {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 5px 8px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.6);
  transition: all 0.2s ease;
}

.sub-permiso-item:hover {
  background: rgba(255, 255, 255, 0.9);
}

.sub-permiso-item input[type="checkbox"] {
  display: none;
}

.sub-permiso-item svg {
  width: 12px;
  height: 12px;
  color: #9ca3af;
  transition: color 0.2s ease;
}

.sub-permiso-item.active svg {
  color: #8e24aa;
}

.sub-permiso-text {
  flex: 1;
  font-size: 10px;
  color: #4b5563;
  font-weight: 500;
}

.sub-permiso-item.active .sub-permiso-text {
  color: #6a1b9a;
}

/* Mini toggle para sub-permisos */
.sub-toggle {
  margin-left: auto;
}

.sub-toggle-track {
  width: 26px;
  height: 14px;
  background: #d1d5db;
  border-radius: 7px;
  position: relative;
  transition: background 0.2s ease;
}

.sub-permiso-item.active .sub-toggle-track {
  background: #8e24aa;
}

.sub-toggle-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 10px;
  height: 10px;
  background: white;
  border-radius: 50%;
  transition: left 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.sub-permiso-item.active .sub-toggle-thumb {
  left: 18px;
}

/* === QUICK ACTIONS === */
.permisos-quick-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #e0e0e0;
}

.btn-quick-action {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  border: 1px solid #e0e0e0;
  background: #fff;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
}

.btn-quick-action svg {
  width: 12px;
  height: 12px;
}

.btn-select-all {
  color: #8e24aa;
  border-color: #ce93d8;
}

.btn-select-all:hover {
  background: #f3e5f5;
  border-color: #8e24aa;
}

.btn-deselect-all {
  color: #757575;
}

.btn-deselect-all:hover {
  background: #f5f5f5;
  border-color: #bdbdbd;
}

/* === ADMIN INFO BANNER === */
.admin-info-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
  border: 1px solid #ffe082;
  border-radius: 10px;
  padding: 10px 12px;
  margin-top: 4px;
}

.admin-banner-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #ffa726 0%, #f57c00 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
}

.admin-banner-icon svg {
  width: 16px;
  height: 16px;
}

.admin-banner-content {
  flex: 1;
}

.admin-banner-content strong {
  display: block;
  color: #e65100;
  font-size: 12px;
  margin-bottom: 2px;
}

.admin-banner-content p {
  margin: 0;
  color: #666;
  font-size: 11px;
  line-height: 1.3;
}

/* === ESTADO DEL USUARIO TOGGLE === */
.estado-section {
  margin-top: 8px;
}

.estado-toggle-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 10px;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
}

.estado-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.estado-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.estado-icon svg {
  width: 16px;
  height: 16px;
}

.estado-icon.activo {
  background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%);
  color: white;
  box-shadow: 0 3px 8px rgba(76, 175, 80, 0.3);
}

.estado-icon.inactivo {
  background: linear-gradient(135deg, #f44336 0%, #c62828 100%);
  color: white;
  box-shadow: 0 3px 8px rgba(244, 67, 54, 0.3);
}

.estado-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.estado-label {
  font-size: 12px;
  font-weight: 600;
  color: #333;
}

.estado-desc {
  font-size: 10px;
  color: #666;
}

/* Switch Toggle */
.estado-switch {
  position: relative;
  width: 56px;
  height: 30px;
  flex-shrink: 0;
  cursor: pointer;
}

.estado-switch.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.estado-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.estado-switch .slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #f44336 0%, #c62828 100%);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 30px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.estado-switch .slider:before {
  position: absolute;
  content: "";
  height: 24px;
  width: 24px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.estado-switch input:checked + .slider {
  background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%);
}

.estado-switch input:checked + .slider:before {
  transform: translateX(26px);
}

.estado-switch.disabled .slider {
  background: #bdbdbd;
}

/* Warning de usuario inactivo */
.estado-warning {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border: 1px solid #ffb74d;
  border-radius: 10px;
  padding: 12px 14px;
  margin-top: 12px;
  font-size: 12px;
  color: #e65100;
  line-height: 1.5;
}

.estado-warning svg {
  flex-shrink: 0;
  margin-top: 1px;
  color: #f57c00;
}

/* Notice de protección para admin */
.admin-protection-notice {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border: 1px solid #64b5f6;
  border-radius: 10px;
  padding: 12px 14px;
  margin-top: 12px;
  font-size: 12px;
  color: #1565c0;
  line-height: 1.5;
}

.admin-protection-notice svg {
  flex-shrink: 0;
  margin-top: 1px;
  color: #1976d2;
}

/* Estado activo container */
.estado-toggle-container:has(.estado-icon.activo) {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  border-color: #81c784;
}

/* Estado inactivo container */
.estado-toggle-container:has(.estado-icon.inactivo) {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  border-color: #e57373;
}

/* === SECCIÓN RESTRICCIÓN TERRITORIAL MODERNA === */
.territorial-section-modern {
  margin-top: 8px;
}

.territorial-section-modern .section-description {
  font-size: 11px;
  color: #666;
  margin: -8px 0 10px 0;
  padding-left: 2px;
}

/* Toggle de acceso territorial - estilo tarjetas */
.territorial-access-toggle {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.access-option {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 10px;
  background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid #dee2e6;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.access-option:hover {
  border-color: #adb5bd;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.access-option.selected {
  border-width: 2px;
}

/* Opción Global seleccionada - AZUL */
.access-option.selected:has(.global-icon) {
  background: linear-gradient(145deg, #e0f2fe 0%, #bae6fd 100%);
  border-color: #0ea5e9;
  box-shadow: 0 3px 10px rgba(14, 165, 233, 0.2);
}

.access-option.selected:has(.global-icon) .global-icon {
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  color: white;
  box-shadow: 0 3px 8px rgba(14, 165, 233, 0.35);
}

/* Opción Territorial seleccionada - CYAN/TEAL */
.access-option.selected:has(.territorial-icon) {
  background: linear-gradient(145deg, #ccfbf1 0%, #99f6e4 100%);
  border-color: #14b8a6;
  box-shadow: 0 3px 10px rgba(20, 184, 166, 0.2);
}

.access-option.selected:has(.territorial-icon) .territorial-icon {
  background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
  color: white;
  box-shadow: 0 3px 8px rgba(20, 184, 166, 0.35);
}

.access-option-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.access-option-icon svg {
  width: 18px;
  height: 18px;
}

.access-option-icon.global-icon {
  background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
  color: white;
}

.access-option-icon.territorial-icon {
  background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
  color: white;
}

.access-option-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.access-option-title {
  font-size: 11px;
  font-weight: 600;
  color: #333;
}

.access-option-desc {
  font-size: 9px;
  color: #666;
  line-height: 1.25;
}

/* Checkmark de selección */
.access-checkmark {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.access-checkmark svg {
  width: 10px;
  height: 10px;
  color: #999;
}

.access-option.selected .access-checkmark {
  opacity: 1;
}

.access-option.selected:has(.global-icon) .access-checkmark {
  background: #0ea5e9;
}

.access-option.selected:has(.global-icon) .access-checkmark svg {
  color: white;
}

.access-option.selected:has(.territorial-icon) .access-checkmark {
  background: #14b8a6;
}

.access-option.selected:has(.territorial-icon) .access-checkmark svg {
  color: white;
}

/* Selector de territorio animado */
.territorio-selector-wrapper {
  margin-top: 10px;
  padding: 12px;
  background: linear-gradient(145deg, #f0fdfa 0%, #ccfbf1 100%);
  border-radius: 8px;
  border: 1.5px solid #5eead4;
}

.territorio-selector-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #0f766e;
  margin-bottom: 8px;
}

.territorio-selector-header svg {
  width: 13px;
  height: 13px;
  color: #14b8a6;
}

.territorio-select-modern {
  width: 100%;
  padding: 9px 12px;
  font-size: 12px;
  border: 1.5px solid #5eead4;
  border-radius: 8px;
  background-color: white;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2314b8a6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 14px;
  font-weight: 500;
}

.territorio-select-modern:focus {
  outline: none;
  border-color: #14b8a6;
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.12);
}

/* Estilos para opciones de territorio ocupado/bloqueado */
.territorio-select-modern option.territorio-ocupado,
.territorio-select-modern option:disabled {
  color: #9ca3af;
  font-style: italic;
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.territorio-info-box {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-top: 8px;
  padding: 7px 9px;
  background: rgba(20, 184, 166, 0.1);
  border-radius: 6px;
  font-size: 10px;
  color: #0f766e;
  line-height: 1.3;
}

.territorio-info-box svg {
  flex-shrink: 0;
  width: 11px;
  height: 11px;
  margin-top: 1px;
  color: #14b8a6;
}

/* Animación slide-fade */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* Responsive para móviles */
@media (max-width: 480px) {
  .territorial-access-toggle {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .access-option {
    flex-direction: row;
    padding: 12px;
    gap: 12px;
  }
  
  .access-option-icon {
    width: 36px;
    height: 36px;
  }
  
  .access-option-icon svg {
    width: 18px;
    height: 18px;
  }
  
  .access-option-content {
    text-align: left;
    flex: 1;
  }
}

/* === MODAL FOOTER === */
.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e8f5e9;
}

.btn-modal {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
  min-width: 120px;
}

.btn-cancel {
  background: #fff;
  border: 2px solid #e0e0e0;
  color: #666;
}

.btn-cancel:hover {
  background: #f5f5f5;
  border-color: #bdbdbd;
}

.btn-submit {
  /* Forzar verde suave incluso en modo oscuro */
  background: #4CAF50 !important;
  border: none;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn-submit:hover:not(:disabled) {
  background: #43A047 !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* === CONFIRM MODAL === */
.confirm-content {
  text-align: center;
}

.confirm-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #d32f2f;
}

.confirm-content h4 {
  color: #333;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  font-family: 'Inter', sans-serif;
}

.confirm-content p {
  color: #666;
  font-size: 14px;
  margin: 4px 0;
}

.warning-text {
  color: #d32f2f;
  font-weight: 500;
  margin: 16px 0 0 0;
  font-size: 13px;
  padding: 12px;
  background: #ffebee;
  border-radius: 8px;
}

.btn-danger {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%) !important;
  color: white !important;
  border: none;
  padding: 12px 20px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-danger:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Modal Delete Header */
.modal-header-danger {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  border-bottom-color: #ffcdd2;
}

.modal-header-danger h3 {
  color: #c62828;
}

.danger-icon {
  background: linear-gradient(135deg, #f44336 0%, #c62828 100%) !important;
}

/* Delete button */
.btn-delete {
  background: #f44336 !important;
  border: none;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.btn-delete:hover:not(:disabled) {
  background: #d32f2f !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(244, 67, 54, 0.4);
}

.btn-delete:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* Confirm icon style update */
.warning-text {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #c62828;
  font-weight: 500;
  margin: 16px 0 0 0;
  font-size: 13px;
  padding: 12px;
  background: #ffebee;
  border-radius: 8px;
  border: 1px solid #ffcdd2;
}

.warning-text svg {
  flex-shrink: 0;
  color: #d32f2f;
}

/* === TOAST === */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  animation: toastSlideIn 0.3s ease-out;
  min-width: 300px;
  max-width: 500px;
}

.toast.success {
  border-left: 4px solid #4CAF50;
}

.toast.success .toast-icon {
  color: #4CAF50;
}

.toast.error {
  border-left: 4px solid #f44336;
}

.toast.error .toast-icon {
  color: #f44336;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toast-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-message {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

@keyframes toastSlideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* === RESPONSIVE DESIGN === */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

/* Tablet portrait - 481px a 768px */
@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 250px;
    width: calc(100vw - 250px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
    max-width: calc(100vw - 240px);
  }
  
  .page-content {
    padding: 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: space-between;
  }
  
  .usuarios-table-container {
    overflow-x: scroll;
  }
  
  /* Modal responsive */
  .modal-content {
    max-width: none;
    margin: 0;
    border-radius: 12px;
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .form-section {
    padding: 14px;
  }
  
  .radio-group-modern {
    grid-template-columns: 1fr;
  }
  
  .permisos-grid-modern {
    grid-template-columns: 1fr;
  }
  
  .permisos-quick-actions {
    flex-direction: column;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
  }
  
  .btn-modal {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: 12px;
  }
  
  .modal-overlay {
    padding: 8px;
  }
  
  .modal-header {
    padding: 14px 16px;
  }
  
  .modal-header h3 {
    font-size: 16px;
  }
  
  .modal-header-icon {
    width: 36px;
    height: 36px;
  }
  
  .modal-header-icon svg {
    width: 18px;
    height: 18px;
  }
  
  .form-section {
    padding: 12px;
  }
  
  .section-header h4 {
    font-size: 14px;
  }
  
  .radio-card {
    padding: 14px 10px;
  }
  
  .radio-card-icon {
    width: 40px;
    height: 40px;
  }
  
  .permiso-card {
    padding: 10px 12px;
  }
  
  .permiso-card-icon {
    width: 32px;
    height: 32px;
  }
  
  .permiso-card-name {
    font-size: 12px;
  }
  
  .toggle-track {
    width: 36px;
    height: 20px;
  }
  
  .toggle-thumb {
    width: 16px;
    height: 16px;
  }
  
  .permiso-card.active .toggle-thumb {
    left: 18px;
  }
  
  /* Sub-permiso responsive */
  .sub-permiso-container {
    padding: 8px 10px;
  }
  
  .sub-permiso-item {
    padding: 6px 8px;
    gap: 8px;
  }
  
  .sub-permiso-text {
    font-size: 11px;
  }
  
  .sub-toggle-track {
    width: 28px;
    height: 14px;
  }
  
  .sub-toggle-thumb {
    width: 10px;
    height: 10px;
  }
  
  .sub-permiso-item.active .sub-toggle-thumb {
    left: 16px;
  }
}

/* Tablet landscape */
@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
  }
  
  .modal-content {
    max-height: 90vh;
  }
  
  .modal-body {
    max-height: calc(90vh - 140px);
    overflow-y: auto;
  }
  
  .permisos-grid-modern {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile landscape */
@media (max-height: 500px) and (orientation: landscape) {
  .modal-overlay {
    padding: 4px;
    align-items: flex-start;
  }
  
  .modal-content {
    max-height: 98vh;
    border-radius: 8px;
  }
  
  .modal-header {
    padding: 10px 14px;
  }
  
  .modal-header-icon {
    width: 32px;
    height: 32px;
  }
  
  .modal-body {
    max-height: calc(98vh - 120px);
    overflow-y: auto;
    padding: 10px;
  }
  
  .form-section {
    padding: 10px;
    margin-bottom: 10px;
  }
  
  .section-header {
    margin-bottom: 8px;
  }
  
  .radio-group-modern {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  
  .permisos-grid-modern {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
  
  .permiso-card {
    padding: 8px 10px;
    gap: 8px;
  }
  
  .permiso-card-icon {
    width: 28px;
    height: 28px;
  }
  
  .permiso-card-name {
    font-size: 11px;
  }
  
  .modal-footer {
    padding: 10px 14px;
    flex-direction: row;
  }
  
  .btn-modal {
    padding: 8px 16px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
  }
}

/* Force light theme colors for submit button */
@media (prefers-color-scheme: dark) {
  .btn-submit {
    background: #4CAF50 !important;
    color: #ffffff !important;
  }
  
  .btn-submit:hover:not(:disabled) {
    background: #43A047 !important;
  }
  
  .modal-content {
    background: #ffffff;
  }
  
  .form-input {
    background: #ffffff;
    color: #333;
  }
}
</style>
