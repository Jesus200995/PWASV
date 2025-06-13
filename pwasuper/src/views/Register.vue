<template>
  <div class="container">
    <h2>Crear cuenta</h2>
    <form @submit.prevent="register">
      <input v-model="email" type="email" placeholder="Correo electrónico" required />
      <input v-model="password" type="password" placeholder="Contraseña" required />
      <button type="submit">Registrarme</button>
    </form>
    <p>
      ¿Ya tienes cuenta?
      <router-link to="/login">Iniciar sesión</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const router = useRouter()

function register() {
  // Aquí después conectarás con el backend
  alert('Usuario registrado: ' + email.value)
  router.push('/login')
}
</script>

<style scoped>
.container {
  max-width: 320px;
  margin: 40px auto;
  padding: 2em;
  border-radius: 12px;
  background: #f8f8f8;
  box-shadow: 0 2px 8px #0002;
}
input {
  display: block;
  width: 100%;
  margin-bottom: 1em;
  padding: .8em;
  border-radius: 8px;
  border: 1px solid #ccc;
}
button {
  width: 100%;
  background: #4caf50;
  color: white;
  border: none;
  padding: .9em;
  border-radius: 8px;
  font-weight: bold;
}
</style>
