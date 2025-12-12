<template>
  <div class="page">
    <nav class="navbar">
      <div class="nav-content">
        <h1 class="nav-title">Reseñas</h1>
        <div class="nav-actions">
          <span v-if="user" class="user-name">{{ user.username }}</span>
          <button @click="logout" class="btn-logout">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            Cerrar Sesión
          </button>
        </div>
      </div>
    </nav>

    <main class="content">
      <div class="content-header">
        <button @click="goToCreate" class="btn-primary">
          + Nueva Reseña
        </button>
      </div>

      <div class="main-grid">
        <div class="reviews-section">
          <h2 class="section-title">Listado de Reseñas</h2>
          <div v-if="reviews.length > 0" class="reviews-list">
            <div 
              v-for="review in reviews" 
              :key="review.id"
              class="review-card"
              @click="goToDetail(review.id)"
            >
              <h3>{{ review.nombre_establecimiento }}</h3>
              <p class="address">{{ review.direccion_postal }}</p>
              <p class="coordinates">
                📍 Coordenadas: {{ review.coordenadas.lon }}, {{ review.coordenadas.lat }}
              </p>
              <p class="rating">
                ⭐ Valoración: {{ review.valoracion }}/5
              </p>
            </div>
          </div>

          <div v-else class="empty-state">
            <p>No hay reseñas disponibles</p>
          </div>
        </div>

        <div class="map-section">
          <h2 class="section-title">Mapa de Establecimientos</h2>
          <MapView :reviews="reviews" />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import { reviewService } from '../services/review';
import MapView from '../components/MapView.vue';

const router = useRouter();
const user = ref(null);
const reviews = ref([]);

onMounted(async () => {
  try {
    const response = await api.get('/users/me');
    user.value = response.data;
    reviews.value = await reviewService.getAll();
  } catch (error) {
    console.error("Error al cargar datos", error);
    logout();
  }
});

const logout = () => {
  localStorage.removeItem('token');
  router.push('/');
};

const goToDetail = (id) => {
  router.push(`/reviews/${id}`);
};

const goToCreate = () => {
  router.push('/reviews/create');
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

.nav-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #111827;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
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
  max-width: 1200px;
  margin: 0 auto;
}

.content-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 24px;
}

.btn-primary {
  padding: 10px 20px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #1d4ed8;
}

.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.reviews-section,
.map-section {
  min-height: 400px;
}

.reviews-list {
  display: grid;
  gap: 16px;
}

.review-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s;
}

.review-card:hover {
  border-color: #2563eb;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.review-card h2 {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.review-card h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.review-card p {
  margin: 8px 0;
  color: #6b7280;
  font-size: 14px;
}

.address {
  color: #374151;
}

.coordinates,
.rating {
  display: flex;
  align-items: center;
  gap: 4px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6b7280;
}
</style>