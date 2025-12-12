<template>
  <div class="page">
    <header class="header">
      <h1>Reseñas</h1>
      <button @click="goToCreate" class="btn-primary">
        + Nueva Reseña
      </button>
    </header>

    <main class="content">
      <div v-if="reviews.length > 0" class="reviews-list">
        <div 
          v-for="review in reviews" 
          :key="review.id"
          class="review-card"
          @click="goToDetail(review.id)"
        >
          <h2>{{ review.nombre_establecimiento }}</h2>
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
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { reviewService } from '../services/review';

const router = useRouter();
const reviews = ref([]);

onMounted(async () => {
  try {
    reviews.value = await reviewService.getAll();
  } catch (error) {
    alert('No se pudieron cargar las reseñas');
  }
});

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

.header {
  background: white;
  padding: 20px 32px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #111827;
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

.content {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
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

.review-card p {
  margin: 8px 0;
  color: #6b7280;
  font-size: 14px;
}

.address {
  color: #374151;
}

.coordinates, .rating {
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
