<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import authService from './services/authService.js'

// Iniciar verificación de sesión en tiempo real si el usuario ya está logueado
onMounted(() => {
  if (authService.isAuthenticated()) {
    console.log('🔄 Usuario ya logueado, iniciando verificación de sesión en tiempo real')
    authService.startSessionCheck()
  }
})

// Detener verificación al desmontar
onUnmounted(() => {
  authService.stopSessionCheck()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
}
</style>
