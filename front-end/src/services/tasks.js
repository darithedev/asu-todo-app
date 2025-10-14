import api from './api';

const handleError = (error) => {
  if (error.response?.status === 403) {
    throw new Error('You do not have permission to perform this action');
  }
  throw error.response?.data || error.message;
};

export const taskService = {
  async getAllTasks(userId) {
    try {
      const response = await api.get(`/tasks/user/${userId}`);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },

  async createTask(taskData) {
    try {
      const response = await api.post('/tasks/', taskData);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },

  async updateTask(taskId, taskData) {
    try {
      // If only updating labels, use the labels endpoint
      if (Object.keys(taskData).length === 1 && taskData.label_ids) {
        const response = await api.put(`/tasks/${taskId}/labels`, { label_ids: taskData.label_ids });
        return response.data;
      }
      // Otherwise use the regular update endpoint
      const response = await api.patch(`/tasks/${taskId}`, taskData);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  },

  async deleteTask(taskId) {
    try {
      await api.delete(`/tasks/${taskId}`);
    } catch (error) {
      throw handleError(error);
    }
  },

  async toggleTaskComplete(taskId) {
    try {
      const response = await api.patch(`/tasks/${taskId}/toggle`);
      return response.data;
    } catch (error) {
      throw handleError(error);
    }
  }
};
