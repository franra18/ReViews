import api from './api';

export const reviewService = {
  async getAll() {
    const response = await api.get('/reviews');
    return response.data;
  },

  async getById(id) {
    const response = await api.get(`/reviews/${id}`);
    return response.data;
  },

  async create(reviewData) {
    const response = await api.post('/reviews', reviewData);
    return response.data;
  }
};
