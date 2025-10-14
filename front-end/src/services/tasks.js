import api from './api';

export const taskService = {
  async getAllTasks() {
    try {
      const response = await api.get('/tasks/');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  async createTask(taskData) {
    try {
      const response = await api.post('/tasks/', taskData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  async updateTask(taskId, taskData) {
    try {
      const response = await api.put(`/tasks/${taskId}`, taskData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  async deleteTask(taskId) {
    try {
      await api.delete(`/tasks/${taskId}`);
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  async toggleTaskComplete(taskId) {
    try {
      const response = await api.patch(`/tasks/${taskId}/toggle`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }
};
