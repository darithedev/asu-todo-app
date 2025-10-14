import api from './api';

const handleError = (error) => {
  if (error.response?.status === 403) {
    throw new Error('You do not have permission to perform this action');
  }
  if (error.response?.data?.detail) {
    throw new Error(error.response.data.detail);
  }
  throw error.response?.data || error.message;
};

export const labelService = {
  async getAllLabels() {
    try {
      const response = await api.get('/labels/');
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },

  async createLabel(labelData) {
    try {
      const response = await api.post('/labels/', labelData);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },

  async updateLabel(labelId, labelData) {
    try {
      const response = await api.patch(`/labels/${labelId}`, labelData);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },

  async deleteLabel(labelId) {
    try {
      await api.delete(`/labels/${labelId}`);
    } catch (error) {
      throw handleError(error);
    }
  },

  async getUserLabels(userId) {
    try {
      const response = await api.get(`/labels/user/${userId}`);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  }
};
