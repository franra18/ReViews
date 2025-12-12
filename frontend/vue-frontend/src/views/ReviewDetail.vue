<template>
  <div class="page">
    <nav class="navbar">
      <div class="nav-content">
        <div class="nav-left">
          <button @click="goBack" class="btn-back">← Volver</button>
          <h1 class="nav-title">Detalle de Reseña</h1>
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
      <div v-if="review" class="detail-card">
        <div class="card-header">
          <h2>{{ review.nombre_establecimiento }}</h2>
          <p class="subtitle">{{ review.direccion_postal }}</p>
        </div>

        <div class="detail-section">
          <h3>Coordenadas GPS</h3>
          <p>Longitud: {{ review.coordenadas.lon }}</p>
          <p>Latitud: {{ review.coordenadas.lat }}</p>
        </div>

        <div class="detail-section">
          <h3>Valoración</h3>
          <p>{{ review.valoracion }}/5 puntos</p>
        </div>

        <div class="detail-section">
          <h3>Autor</h3>
          <p>Nombre: {{ review.nombre_autor }}</p>
          <p>Email: {{ review.email_autor }}</p>
        </div>

        <div class="detail-section">
          <h3>Fecha de Emisión del Token</h3>
          <p>{{ formatDate(review.fecha_emision) }}</p>
        </div>

        <div class="detail-section">
          <h3>Fecha de Caducidad del Token</h3>
          <p>{{ formatDate(review.fecha_caducidad) }}</p>
        </div>

        <div class="detail-section">
          <h3>Token OAuth</h3>
          <p class="token-text">{{ review.token_oauth }}</p>
        </div>

        <div v-if="review.imagenes && review.imagenes.length > 0" class="detail-section">
          <h3>Imágenes</h3>
          <div class="images-grid">
            <img 
              v-for="(img, index) in review.imagenes" 
              :key="index" 
              :src="img" 
              :alt="`Imagen ${index + 1}`"
            />
          </div>
        </div>
      </div>

      <div v-else class="loading">
        <p>Cargando...</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { reviewService } from '../services/review';

const route = useRoute();
const router = useRouter();
const review = ref(null);

onMounted(async () => {
  try {
    const id = route.params.id;
    review.value = await reviewService.getById(id);
  } catch (error) {
    alert('No se pudo cargar el detalle de la reseña');
  }
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
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
  max-width: 800px;
  margin: 0 auto;
}

.detail-card {
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.card-header {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.card-header h2 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #111827;
}

.subtitle {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

.detail-section {
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.detail-section:last-child {
  border-bottom: none;
}

.detail-section h3 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #2563eb;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-section p {
  margin: 4px 0;
  color: #374151;
  font-size: 15px;
}

.token-text {
  word-break: break-all;
  font-family: monospace;
  font-size: 13px;
  max-height: 100px;
  overflow-y: auto;
  background: #f9fafb;
  padding: 12px;
  border-radius: 4px;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.images-grid img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.loading {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
}
</style>
