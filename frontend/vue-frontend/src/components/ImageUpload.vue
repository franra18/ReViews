<template>
  <div class="image-upload">
    <div class="upload-area">
      <input
        type="file"
        ref="fileInput"
        @change="handleFileSelect"
        accept="image/*"
        multiple
        class="file-input"
      />
      <button type="button" @click="triggerFileInput" class="btn-upload">
        Seleccionar Imágenes
      </button>
      <p class="help-text">Puedes seleccionar varias imágenes</p>
    </div>

    <div v-if="uploading" class="upload-status">
      <p>Subiendo imágenes... {{ uploadedCount }}/{{ totalFiles }}</p>
    </div>

    <div v-if="images.length > 0" class="images-preview">
      <div v-for="(image, index) in images" :key="index" class="image-item">
        <img :src="image" :alt="`Imagen ${index + 1}`" />
        <button type="button" @click="removeImage(index)" class="btn-remove">
          ✕
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue']);

const fileInput = ref(null);
const uploading = ref(false);
const uploadedCount = ref(0);
const totalFiles = ref(0);
const images = ref([...props.modelValue]);

const cloudinaryCloudName = import.meta.env.VITE_CLOUDINARY_CLOUD_NAME;
const cloudinaryUploadPreset = import.meta.env.VITE_CLOUDINARY_UPLOAD_PRESET;

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileSelect = async (event) => {
  const files = Array.from(event.target.files);
  if (files.length === 0) return;

  // Validar tamaño de archivos (máximo 5MB por imagen)
  const maxSize = 5 * 1024 * 1024; // 5MB
  const invalidFiles = files.filter(file => file.size > maxSize);
  
  if (invalidFiles.length > 0) {
    alert(`Algunas imágenes superan el tamaño máximo de 5MB`);
    return;
  }

  uploading.value = true;
  uploadedCount.value = 0;
  totalFiles.value = files.length;

  try {
    const uploadPromises = files.map(file => uploadToCloudinary(file));
    const urls = await Promise.all(uploadPromises);
    
    images.value = [...images.value, ...urls];
    emit('update:modelValue', images.value);
    
    // Limpiar input
    event.target.value = '';
  } catch (error) {
    console.error('Error al subir imágenes:', error);
    alert('Error al subir las imágenes. Por favor intenta de nuevo.');
  } finally {
    uploading.value = false;
    uploadedCount.value = 0;
    totalFiles.value = 0;
  }
};

const uploadToCloudinary = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('upload_preset', cloudinaryUploadPreset);

  const response = await fetch(
    `https://api.cloudinary.com/v1_1/${cloudinaryCloudName}/image/upload`,
    {
      method: 'POST',
      body: formData
    }
  );

  if (!response.ok) {
    throw new Error('Error al subir imagen a Cloudinary');
  }

  const data = await response.json();
  uploadedCount.value++;
  return data.secure_url;
};

const removeImage = (index) => {
  images.value.splice(index, 1);
  emit('update:modelValue', images.value);
};
</script>

<style scoped>
.image-upload {
  margin: 24px 0;
}

.upload-area {
  text-align: center;
  padding: 20px;
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  background: #f9fafb;
}

.file-input {
  display: none;
}

.btn-upload {
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

.btn-upload:hover {
  background: #1d4ed8;
}

.help-text {
  margin: 8px 0 0 0;
  font-size: 12px;
  color: #6b7280;
}

.upload-status {
  margin-top: 16px;
  text-align: center;
  color: #2563eb;
  font-weight: 500;
}

.images-preview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
  margin-top: 20px;
}

.image-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  line-height: 1;
  transition: background 0.2s;
}

.btn-remove:hover {
  background: rgba(220, 38, 38, 0.9);
}
</style>
