<template>
  <div class="page">
    <nav class="navbar">
      <div class="nav-content">
        <div class="nav-left">
          <button @click="goBack" class="btn-back">← Volver</button>
          <h1 class="nav-title">Crear Reseña</h1>
        </div>
        <button @click="logout" class="btn-logout">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          Cerrar Sesión
        </button>
      </div>
    </nav>

    <main class="content">
      <!-- Toast Notification -->
      <transition name="toast">
        <div v-if="toast.show" :class="['toast', `toast-${toast.type}`]">
          {{ toast.message }}
        </div>
      </transition>

      <form @submit.prevent="handleSubmit" class="form-card">
        <div class="form-group">
          <label>Nombre del Establecimiento *</label>
          <input
            v-model="formData.nombre_establecimiento"
            type="text"
            placeholder="Ej. Casa Lola"
            required
          />
        </div>

        <div class="form-group">
          <label>Dirección Postal *</label>
          <div class="address-input-group">
            <input
              v-model="formData.direccion_postal"
              type="text"
              placeholder="Ej. Calle Granada 46, Málaga"
              required
            />
            <button type="button" @click="geocodeAddress" class="btn-geocode" :disabled="geocoding">
              {{ geocoding ? 'Buscando...' : '🔍 Obtener coordenadas' }}
            </button>
          </div>
          <p v-if="geocodeError" class="error-msg">{{ geocodeError }}</p>
          <p v-if="geocodeSuccess" class="success-msg">✓ Coordenadas obtenidas correctamente</p>
        </div>

        <div class="coordinates-group">
          <div class="form-group">
            <label>Longitud (GPS) *</label>
            <input
              v-model.number="formData.coordenadas.lon"
              type="number"
              step="any"
              placeholder="Ej. -4.4189788"
              required
              readonly
            />
          </div>

          <div class="form-group">
            <label>Latitud (GPS) *</label>
            <input
              v-model.number="formData.coordenadas.lat"
              type="number"
              step="any"
              placeholder="Ej. 36.7220033"
              required
              readonly
            />
          </div>
        </div>

        <div class="form-group">
          <label>Valoración (0-5) *</label>
          <input
            v-model.number="formData.valoracion"
            type="number"
            min="0"
            max="5"
            placeholder="Ej. 4"
            required
          />
        </div>

        <div class="form-group">
          <label>Imágenes del Establecimiento</label>
          <ImageUpload v-model="images" />
        </div>

        <button type="submit" class="btn-submit">
          Crear Reseña
        </button>
      </form>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { reviewService } from '../services/review';
import ImageUpload from '../components/ImageUpload.vue';

const router = useRouter();

const formData = ref({
  nombre_establecimiento: '',
  direccion_postal: '',
  coordenadas: {
    lon: null,
    lat: null
  },
  valoracion: null
});

const images = ref([]);
const geocoding = ref(false);
const geocodeError = ref('');
const geocodeSuccess = ref(false);
const toast = ref({ show: false, message: '', type: 'success' });

const showToast = (message, type = 'success') => {
  toast.value = { show: true, message, type };
  setTimeout(() => {
    toast.value.show = false;
  }, 3000);
};

const geocodeAddress = async () => {
  if (!formData.value.direccion_postal.trim()) {
    geocodeError.value = 'Por favor ingresa una dirección postal';
    return;
  }

  geocoding.value = true;
  geocodeError.value = '';
  geocodeSuccess.value = false;

  try {
    const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&q=${encodeURIComponent(formData.value.direccion_postal)}`;
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'ReViews App (Educational Project)'
      }
    });

    const results = await response.json();

    if (results.length > 0) {
      formData.value.coordenadas.lat = parseFloat(results[0].lat);
      formData.value.coordenadas.lon = parseFloat(results[0].lon);
      geocodeSuccess.value = true;
      
      // Limpiar mensaje de éxito después de 3 segundos
      setTimeout(() => {
        geocodeSuccess.value = false;
      }, 3000);
    } else {
      geocodeError.value = 'No se encontraron coordenadas para esta dirección. Intenta con otra.';
    }
  } catch (error) {
    console.error('Error al obtener coordenadas:', error);
    geocodeError.value = 'Error al conectar con el servicio de geocodificación.';
  } finally {
    geocoding.value = false;
  }
};

const handleSubmit = async () => {
  if (!formData.value.nombre_establecimiento || !formData.value.direccion_postal) {
    showToast('Por favor completa todos los campos obligatorios', 'error');
    return;
  }

  if (formData.value.valoracion < 0 || formData.value.valoracion > 5) {
    showToast('La valoración debe estar entre 0 y 5', 'error');
    return;
  }

  if (!formData.value.coordenadas.lat || !formData.value.coordenadas.lon) {
    showToast('Por favor obtén las coordenadas GPS usando el botón "Obtener coordenadas"', 'error');
    return;
  }

  try {
    await reviewService.create({
      ...formData.value,
      imagenes: images.value
    });
    showToast('Reseña creada correctamente', 'success');
    setTimeout(() => {
      router.push('/dashboard');
    }, 1500);
  } catch (error) {
    showToast(error.response?.data?.detail || 'No se pudo crear la reseña', 'error');
  }
};

const goBack = () => {
  router.push('/dashboard');
};

const logout = () => {
  localStorage.removeItem('token');
  router.push('/');
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 10000;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.btn-back {
  padding: 8px 16px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-back:hover {
  background: #f9fafb;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-logout:hover {
  background: #f9fafb;
}

.content {
  padding: 32px;
  max-width: 600px;
  margin: 0 auto;
  position: relative;
}

.toast {
  position: fixed;
  top: 100px;
  right: 32px;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  font-size: 14px;
  font-weight: 500;
  z-index: 1000;
  max-width: 400px;
}

.toast-success {
  background: #10b981;
  color: white;
}

.toast-error {
  background: #ef4444;
  color: white;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.form-card {
  background: white;
  padding: 32px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 15px;
  color: #111827;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #2563eb;
}

.address-input-group {
  display: flex;
  gap: 8px;
}

.address-input-group input {
  flex: 1;
}

.btn-geocode {
  padding: 10px 16px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.btn-geocode:hover:not(:disabled) {
  background: #059669;
}

.btn-geocode:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.coordinates-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.coordinates-group .form-group {
  margin-bottom: 0;
}

.coordinates-group input {
  background: #f9fafb;
}

.error-msg {
  margin-top: 8px;
  font-size: 13px;
  color: #dc2626;
}

.success-msg {
  margin-top: 8px;
  font-size: 13px;
  color: #10b981;
  font-weight: 500;
}

.btn-submit {
  width: 100%;
  padding: 12px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-submit:hover {
  background: #1d4ed8;
}
</style>
