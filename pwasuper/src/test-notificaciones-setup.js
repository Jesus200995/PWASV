// Script para probar el sistema de notificaciones con datos de usuario simulados

console.log('🧪 Configurando datos de prueba para notificaciones...')

// Limpiar localStorage anterior
localStorage.clear()

// Crear datos de usuario de prueba
const usuarioPrueba = {
  id: 1,
  nombre_completo: 'Usuario de Prueba',
  correo: 'test@ejemplo.com',
  cargo: 'Desarrollador',
  supervisor: 'Administrador'
}

// Guardar en localStorage con el formato correcto
localStorage.setItem('user', JSON.stringify(usuarioPrueba))

console.log('✅ Datos de usuario guardados:', usuarioPrueba)
console.log('📱 Ahora puedes ir a la sección de Notificaciones')

// Mostrar contenido actual del localStorage
console.log('🔍 Contenido actual de localStorage:')
for (let i = 0; i < localStorage.length; i++) {
  const key = localStorage.key(i)
  const value = localStorage.getItem(key)
  console.log(`  ${key}: ${value}`)
}
