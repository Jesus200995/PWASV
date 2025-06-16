const API_URL = 'https://apipwa.sembrandodatos.com';

// Variables globales
let registrosData = [];
let adminToken = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si ya hay token guardado
    adminToken = sessionStorage.getItem('admin_token');
    if (adminToken) {
        mostrarPanelAdmin();
        cargarDatos();
    }
});

// Función de login
async function loginAdmin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const loginBtn = document.getElementById('login-btn');
    const btnText = loginBtn.querySelector('.btn-text');
    const spinner = loginBtn.querySelector('.spinner');
    const errorDiv = document.getElementById('login-error');
    
    if (!username || !password) {
        mostrarError('Por favor completa todos los campos');
        return;
    }
    
    // Mostrar estado de carga
    loginBtn.disabled = true;
    btnText.textContent = 'Iniciando sesión...';
    spinner.style.display = 'inline-block';
    errorDiv.classList.remove('show');
    
    try {
        const formData = new URLSearchParams();
        formData.append('grant_type', '');
        formData.append('username', username);
        formData.append('password', password);
        formData.append('scope', '');
        formData.append('client_id', '');
        formData.append('client_secret', '');
        
        const response = await fetch(`${API_URL}/admin/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString()
        });
        
        const data = await response.json();
        
        if (response.ok && data.access_token) {
            // Login exitoso
            adminToken = data.access_token;
            sessionStorage.setItem('admin_token', adminToken);
            sessionStorage.setItem('admin_user', username);
            
            mostrarPanelAdmin();
            cargarDatos();
        } else {
            // Error de login
            mostrarError(data.detail || 'Credenciales incorrectas');
        }
    } catch (error) {
        console.error('Error de login:', error);
        mostrarError('No se pudo conectar con el servidor. Verifica tu conexión a internet.');
    } finally {
        // Restaurar estado del botón
        loginBtn.disabled = false;
        btnText.textContent = 'Iniciar Sesión';
        spinner.style.display = 'none';
    }
}

// Mostrar error de login
function mostrarError(mensaje) {
    const errorDiv = document.getElementById('login-error');
    errorDiv.textContent = mensaje;
    errorDiv.classList.add('show');
}

// Mostrar panel de administración
function mostrarPanelAdmin() {
    document.getElementById('login-panel').style.display = 'none';
    document.getElementById('admin-panel').style.display = 'block';
    
    // Mostrar nombre de usuario
    const username = sessionStorage.getItem('admin_user');
    if (username) {
        document.getElementById('admin-user').textContent = `Hola, ${username}`;
    }
}

// Cargar todos los datos
async function cargarDatos() {
    await Promise.all([
        cargarRegistros(),
        cargarEstadisticas()
    ]);
}

// Cargar registros
async function cargarRegistros() {
    const loadingDiv = document.getElementById('loading');
    const registrosContainer = document.getElementById('registros-tabla');
    const errorDiv = document.getElementById('error-message');
    const refreshBtn = document.getElementById('refresh-btn');
    
    // Mostrar estado de carga
    loadingDiv.style.display = 'block';
    errorDiv.style.display = 'none';
    refreshBtn.classList.add('loading');
    
    try {
        const response = await fetch(`${API_URL}/registros`, {
            headers: {
                'Authorization': `Bearer ${adminToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        registrosData = data.registros || [];
        
        mostrarTablaRegistros(registrosData);
        
    } catch (error) {
        console.error('Error al cargar registros:', error);
        errorDiv.textContent = 'Error al cargar los registros: ' + error.message;
        errorDiv.style.display = 'block';
        registrosContainer.innerHTML = '';
    } finally {
        loadingDiv.style.display = 'none';
        refreshBtn.classList.remove('loading');
    }
}

// Mostrar tabla de registros
function mostrarTablaRegistros(registros) {
    const container = document.getElementById('registros-tabla');
    
    if (!registros || registros.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #718096;">
                <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
                <h3>No hay registros</h3>
                <p>Aún no se han creado registros en la aplicación.</p>
            </div>
        `;
        return;
    }
    
    let html = `
        <table class="registros-tabla">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Foto</th>
                    <th>Ubicación</th>
                    <th>Descripción</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    registros.forEach(registro => {
        const fecha = new Date(registro.fecha_hora).toLocaleString('es-ES');
        const lat = Number(registro.latitud).toFixed(6);
        const lng = Number(registro.longitud).toFixed(6);
        const descripcion = registro.descripcion || 'Sin descripción';
        const fotoUrl = registro.foto_url ? `${API_URL}/${registro.foto_url}` : null;
        
        html += `
            <tr>
                <td>#${registro.id}</td>
                <td>Usuario ${registro.usuario_id}</td>
                <td>
                    ${fotoUrl ? 
                        `<img src="${fotoUrl}" alt="Foto" class="foto-mini" onclick="verFoto('${fotoUrl}')">` : 
                        '<span style="color: #999;">Sin foto</span>'
                    }
                </td>
                <td>
                    <small>${lat}, ${lng}</small>
                </td>
                <td>
                    <div style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${descripcion}">
                        ${descripcion}
                    </div>
                </td>
                <td><small>${fecha}</small></td>
                <td>
                    <button class="btn-ver" onclick="verDetalles(${registro.id})">
                        Ver Detalles
                    </button>
                </td>
            </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
    `;
    
    container.innerHTML = html;
    container.classList.add('fade-in');
}

// Cargar estadísticas
async function cargarEstadisticas() {
    try {
        // Por ahora calculamos estadísticas desde los registros
        // En el futuro podrías crear endpoints específicos para estadísticas
        
        const totalRegistros = registrosData.length;
        const usuariosUnicos = [...new Set(registrosData.map(r => r.usuario_id))].length;
        
        // Registros de hoy
        const hoy = new Date().toDateString();
        const registrosHoy = registrosData.filter(r => {
            const fechaRegistro = new Date(r.fecha_hora).toDateString();
            return fechaRegistro === hoy;
        }).length;
        
        // Actualizar DOM
        document.getElementById('total-registros').textContent = totalRegistros;
        document.getElementById('total-usuarios').textContent = usuariosUnicos;
        document.getElementById('registros-hoy').textContent = registrosHoy;
        
    } catch (error) {
        console.error('Error al calcular estadísticas:', error);
        document.getElementById('total-registros').textContent = '?';
        document.getElementById('total-usuarios').textContent = '?';
        document.getElementById('registros-hoy').textContent = '?';
    }
}

// Ver detalles de un registro
function verDetalles(registroId) {
    const registro = registrosData.find(r => r.id === registroId);
    if (!registro) return;
    
    const fecha = new Date(registro.fecha_hora).toLocaleString('es-ES');
    const fotoUrl = registro.foto_url ? `${API_URL}/${registro.foto_url}` : null;
    
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <div style="display: grid; gap: 20px;">
            <div>
                <strong>ID del Registro:</strong> #${registro.id}
            </div>
            <div>
                <strong>Usuario:</strong> Usuario ${registro.usuario_id}
            </div>
            <div>
                <strong>Fecha y Hora:</strong> ${fecha}
            </div>
            <div>
                <strong>Ubicación:</strong><br>
                Latitud: ${Number(registro.latitud).toFixed(6)}<br>
                Longitud: ${Number(registro.longitud).toFixed(6)}
            </div>
            <div>
                <strong>Descripción:</strong><br>
                ${registro.descripcion || 'Sin descripción'}
            </div>
            ${fotoUrl ? `
                <div>
                    <strong>Fotografía:</strong><br>
                    <img src="${fotoUrl}" alt="Foto del registro" style="max-width: 100%; height: auto; border-radius: 8px; margin-top: 10px;">
                </div>
            ` : '<div><strong>Fotografía:</strong> No disponible</div>'}
            <div>
                <strong>Ver en Google Maps:</strong><br>
                <a href="https://www.google.com/maps?q=${registro.latitud},${registro.longitud}" target="_blank" style="color: #4CAF50; text-decoration: none;">
                    📍 Abrir ubicación en Google Maps
                </a>
            </div>
        </div>
    `;
    
    document.getElementById('modal-overlay').style.display = 'flex';
}

// Ver foto en modal
function verFoto(fotoUrl) {
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <div style="text-align: center;">
            <img src="${fotoUrl}" alt="Fotografía del registro" style="max-width: 100%; height: auto; border-radius: 8px;">
        </div>
    `;
    
    document.getElementById('modal-overlay').style.display = 'flex';
}

// Cerrar modal
function cerrarModal() {
    document.getElementById('modal-overlay').style.display = 'none';
}

// Cerrar sesión
function logout() {
    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
        // Limpiar datos de sesión
        sessionStorage.removeItem('admin_token');
        sessionStorage.removeItem('admin_user');
        adminToken = null;
        registrosData = [];
        
        // Mostrar panel de login
        document.getElementById('admin-panel').style.display = 'none';
        document.getElementById('login-panel').style.display = 'flex';
        
        // Limpiar formulario
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
        document.getElementById('login-error').classList.remove('show');
    }
}

// Manejar errores de autenticación
window.addEventListener('unhandledrejection', function(event) {
    if (event.reason && event.reason.message && event.reason.message.includes('401')) {
        alert('Tu sesión ha expirado. Por favor inicia sesión nuevamente.');
        logout();
    }
});

// Cerrar modal con tecla Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        cerrarModal();
    }
});
