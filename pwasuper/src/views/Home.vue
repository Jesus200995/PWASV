<template>
  <div class="container">
    <h2>Registrar ubicación</h2>
    <form @submit.prevent="enviarRegistro">
      <button type="button" @click="getUbicacion">Obtener ubicación</button>
      <div v-if="latitud && longitud" class="coordenadas">
        Latitud: <b>{{ latitud }}</b><br />
        Longitud: <b>{{ longitud }}</b>
      </div>
      <input type="file" accept="image/*" @change="onFileChange" ref="fileInput" />
      <textarea
        v-model="descripcion"
        placeholder="Descripción (opcional)"
        rows="2"
      ></textarea>
      <button
        type="submit"
        :disabled="!latitud || !longitud || !foto"
        :class="{ 'loading': enviando }"
      >
        {{ enviando ? 'Enviando...' : 'Guardar registro' }}
      </button>
    </form>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <h3>Historial local</h3>
    <ul>
      <li v-for="(r, i) in historial" :key="i">
        <small>{{ r.fecha }}</small> -
        <span>Lat: {{ r.latitud }}, Lon: {{ r.longitud }}</span><br />
        <span>{{ r.descripcion }}</span><br />
        <img
          v-if="r.foto"
          :src="r.foto"
          width="90"
          style="margin-top:4px"
        />
        <div v-if="r.backend" class="backend-response">
          <small>Respuesta del servidor: {{ JSON.stringify(r.backend) }}</small>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const API_URL = "http://31.97.8.51:8000"; // Dirección del servidor backend

const latitud = ref(null);
const longitud = ref(null);
const foto = ref(null);
const archivoFoto = ref(null);
const fileInput = ref(null);
const descripcion = ref("");
const historial = ref([]);
const enviando = ref(false);
const error = ref(null);

function getUbicacion() {
  if (!navigator.geolocation) {
    error.value = "Tu navegador no soporta geolocalización";
    return;
  }
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      latitud.value = pos.coords.latitude;
      longitud.value = pos.coords.longitude;
      error.value = null;
    },
    (err) => {
      error.value = "Error obteniendo ubicación: " + err.message;
    }
  );
}

function onFileChange(e) {
  const file = e.target.files[0];
  archivoFoto.value = file;
  if (file) {
    const reader = new FileReader();
    reader.onload = (e2) => {
      foto.value = e2.target.result;
    };
    reader.readAsDataURL(file);
  }
}

async function enviarRegistro() {
  if (!latitud.value || !longitud.value || !archivoFoto.value) {
    error.value = "Falta información: necesitas ubicación y foto";
    return;
  }

  enviando.value = true;
  error.value = null;

  try {
    // Crear FormData para enviar al servidor
    const formData = new FormData();
    formData.append("usuario_id", "demo"); // Usa el ID real si tienes login
    formData.append("latitud", latitud.value);
    formData.append("longitud", longitud.value);
    formData.append("descripcion", descripcion.value);
    formData.append("foto", archivoFoto.value);

    // Enviar datos al backend
    const response = await axios.post(`${API_URL}/registro`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    // Guardar en historial local
    historial.value.unshift({
      fecha: new Date().toLocaleString(),
      latitud: latitud.value,
      longitud: longitud.value,
      descripcion: descripcion.value,
      foto: foto.value,
      backend: response.data,
    });

    // Limpiar campos
    descripcion.value = "";
    foto.value = null;
    archivoFoto.value = null;
    latitud.value = null;
    longitud.value = null;
    if (fileInput.value) {
      fileInput.value.value = ""; // Limpiar input file
    }

    alert("¡Registro enviado y guardado correctamente!");
  } catch (err) {
    console.error("Error al enviar datos:", err);
    error.value = `Error al enviar datos: ${err.message}`;

    if (err.response) {
      console.error("Respuesta del servidor:", err.response.data);
      error.value = "Error al enviar: " + (err?.response?.data?.detail || err.message);
    }
  } finally {
    enviando.value = false;
  }
}
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: 30px auto;
  background: #f8f8f8;
  padding: 2em;
  border-radius: 12px;
  box-shadow: 0 2px 10px #0001;
}
button {
  width: 100%;
  background: #4caf50;
  color: white;
  border: none;
  padding: 1em;
  margin-bottom: 1em;
  border-radius: 8px;
  font-weight: bold;
}
button.loading {
  background: #999;
  cursor: not-allowed;
}
button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
input[type="file"],
textarea {
  width: 100%;
  margin-bottom: 1em;
  padding: 0.8em;
  border-radius: 8px;
  border: 1px solid #ccc;
}
.coordenadas {
  font-size: 1.1em;
  margin: 0.6em 0;
  color: #444;
  background: #e8ffe8;
  border-radius: 7px;
  padding: 0.4em;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  background: #fff;
  margin-bottom: 1em;
  padding: 1em;
  border-radius: 8px;
  box-shadow: 0 1px 4px #0001;
}
img {
  border-radius: 8px;
  margin-top: 4px;
}
.error-message {
  background: #fff0f0;
  color: #d32f2f;
  padding: 1em;
  border-radius: 8px;
  margin: 1em 0;
  border-left: 4px solid #d32f2f;
}
.backend-response {
  margin-top: 8px;
  font-size: 0.8em;
  color: #666;
  background: #f5f5f5;
  padding: 0.5em;
  border-radius: 4px;
  word-break: break-all;
}
</style>
