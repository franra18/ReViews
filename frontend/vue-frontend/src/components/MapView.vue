<template>
  <div class="map-container">
    <div class="search-box">
      <input
        v-model="searchQuery"
        @keyup.enter="searchAddress"
        type="text"
        placeholder="Buscar dirección (ej. Calle Granada 46, Málaga)"
        class="search-input"
      />
      <button @click="searchAddress" class="btn-search">Buscar</button>
    </div>
    <div ref="mapContainer" class="map"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  reviews: {
    type: Array,
    default: () => []
  }
});

const router = useRouter();
const mapContainer = ref(null);
const searchQuery = ref('');
let map = null;
let markers = [];

// Fix para iconos de Leaflet en Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

onMounted(() => {
  // Inicializar mapa centrado en España
  map = L.map(mapContainer.value).setView([40.4168, -3.7038], 6);

  // Añadir capa de OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map);

  // Función global para navegar desde el popup
  window.navigateToReview = (reviewId) => {
    router.push(`/reviews/${reviewId}`);
  };

  // Añadir marcadores iniciales
  updateMarkers();
});

watch(() => props.reviews, () => {
  updateMarkers();
}, { deep: true });

const updateMarkers = () => {
  if (!map) return;

  // Limpiar marcadores existentes
  markers.forEach(marker => marker.remove());
  markers = [];

  // Añadir nuevos marcadores
  if (props.reviews.length > 0) {
    props.reviews.forEach(review => {
      const marker = L.marker([review.coordenadas.lat, review.coordenadas.lon])
        .addTo(map)
        .bindPopup(`
          <div style="text-align: center; cursor: pointer;" onclick="window.navigateToReview('${review.id}')">
            <strong>${review.nombre_establecimiento}</strong><br>
            ${review.direccion_postal}<br>
            ⭐ ${review.valoracion}/5<br>
            <span style="color: #2563eb; font-size: 12px; margin-top: 4px; display: inline-block;">
              Ver detalles 
            </span>
          </div>
        `);
      markers.push(marker);
    });

    // Ajustar zoom para mostrar todos los marcadores
    if (markers.length === 1) {
      map.setView([props.reviews[0].coordenadas.lat, props.reviews[0].coordenadas.lon], 13);
    } else if (markers.length > 1) {
      const bounds = L.latLngBounds(
        props.reviews.map(r => [r.coordenadas.lat, r.coordenadas.lon])
      );
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }
};

const searchAddress = async () => {
  if (!searchQuery.value.trim()) {
    alert('Por favor ingresa una dirección');
    return;
  }

  try {
    const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&q=${encodeURIComponent(searchQuery.value)}`;
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'ReViews App (Educational Project)'
      }
    });

    const results = await response.json();

    if (results.length > 0) {
      const { lat, lon } = results[0];
      map.setView([parseFloat(lat), parseFloat(lon)], 15);
      
      // Añadir marcador temporal
      const tempMarker = L.marker([parseFloat(lat), parseFloat(lon)])
        .addTo(map)
        .bindPopup(`<strong>${searchQuery.value}</strong>`)
        .openPopup();
      
      // Eliminar marcador temporal después de 3 segundos
      setTimeout(() => {
        tempMarker.remove();
      }, 3000);
    } else {
      alert('No se encontró la dirección. Intenta con otra búsqueda.');
    }
  } catch (error) {
    console.error('Error al buscar dirección:', error);
    alert('Error al buscar la dirección');
  }
};
</script>

<style scoped>
.map-container {
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.search-box {
  padding: 16px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  gap: 12px;
}

.search-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  color: #111827;
}

.search-input:focus {
  outline: none;
  border-color: #2563eb;
}

.btn-search {
  padding: 10px 20px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.btn-search:hover {
  background: #1d4ed8;
}

.map {
  height: 500px;
  width: 100%;
}
</style>
