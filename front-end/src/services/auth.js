import api from './api';

export const authService = {
  async login(email, password) {
    try {
      // Create FormData object as the backend expects form data
      const formData = new URLSearchParams();
      formData.append('username', email); // Backend expects 'username' field
      formData.append('password', password);

      const response = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      console.log('Login response:', response.data);
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        return response.data;
      } else {
        throw new Error('No access token received');
      }
    } catch (error) {
      console.error('Login error:', error.response || error);
      if (error.response?.data) {
        throw error.response.data;
      } else if (error.response) {
        throw { message: `Server error: ${error.response.status}` };
      } else {
        throw { message: error.message || 'Failed to login' };
      }
    }
  },

  async register(userData) {
    try {
      console.log('Sending registration request:', userData);
      const response = await api.post('/auth/register', userData);
      console.log('Registration response:', response.data);
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        return response.data;
      } else {
        throw new Error('No access token received in response');
      }
    } catch (error) {
      console.error('Registration error:', error.response || error);
      if (error.response?.data) {
        throw error.response.data;
      } else if (error.response) {
        throw { message: `Server error: ${error.response.status}` };
      } else {
        throw { message: error.message || 'Failed to register' };
      }
    }
  },

  async logout() {
    localStorage.removeItem('token');
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  },

  getToken() {
    return localStorage.getItem('token');
  }
};
