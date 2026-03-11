import api from './api';

export const progressService = {
  // Get user progress
  async getUserProgress(userId) {
    try {
      const response = await api.get(`/progress/${userId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get user progress' };
    }
  },

  // Track progress
  async trackProgress(progressData) {
    try {
      const response = await api.post('/progress/track', progressData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to track progress' };
    }
  },

  // Get progress summary
  async getProgressSummary(userId) {
    try {
      // The backend uses authenticated user, so no userId needed in URL
      const response = await api.get('/progress/summary');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get progress summary' };
    }
  },

  // Get progress timeline
  async getProgressTimeline(userId, metricType) {
    try {
      const response = await api.get(`/progress/${userId}/timeline`, {
        params: { metric_type: metricType }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get progress timeline' };
    }
  },

  // Get achievements
  async getAchievements(userId) {
    try {
      const response = await api.get(`/progress/${userId}/achievements`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get achievements' };
    }
  },

  // Get statistics
  async getStatistics(userId) {
    try {
      const response = await api.get(`/progress/${userId}/statistics`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get statistics' };
    }
  }
};

export default progressService;
