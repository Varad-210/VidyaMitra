import api from './api';

export const authService = {
  // Login user
  async loginUser(credentials) {
    try {
      // Convert to URL-encoded form data for OAuth2PasswordRequestForm
      const params = new URLSearchParams();
      params.append('username', credentials.email); // Use email as username
      params.append('password', credentials.password);
      
      const response = await api.post('/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        }
      });
      
      const { access_token } = response.data;
      
      // Store token in localStorage
      localStorage.setItem('token', access_token);
      
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Login failed' };
    }
  },

  // Register user
  async registerUser(userData) {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Registration failed' };
    }
  },

  // Get current user
  async getCurrentUser() {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get user data' };
    }
  },

  // Logout user
  logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
  },

  // Check if user is authenticated
  isAuthenticated() {
    return !!localStorage.getItem('token');
  },

  // Get stored token
  getToken() {
    return localStorage.getItem('token');
  }
};

export default authService;
