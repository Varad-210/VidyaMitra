import api from './api';

export const recommendationService = {
  // Get skill recommendations (using market trends as fallback)
  async getSkillRecommendations(userId) {
    try {
      // Since there's no direct skills endpoint, use market trends
      const response = await api.get('/recommendations/market-trends');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get skill recommendations' };
    }
  },

  // Get career roadmap
  async getCareerRoadmap(userId) {
    try {
      // Use a default roadmap request since the endpoint requires POST
      const response = await api.post('/recommendations/roadmap', {
        user_skills: ['JavaScript', 'React', 'Node.js'], // Default skills
        target_role: 'Software Engineer',
        experience_level: 'beginner'
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get career roadmap' };
    }
  },

  // Get personalized recommendations
  async getPersonalizedRecommendations(userId, targetRole) {
    try {
      const response = await api.get(`/recommendations/personalized/${userId}`, {
        params: { target_role: targetRole }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get personalized recommendations' };
    }
  },

  // Get learning resources
  async getLearningResources(skillName) {
    try {
      const response = await api.get(`/recommendations/resources/${skillName}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get learning resources' };
    }
  },

  // Get market insights
  async getMarketInsights() {
    try {
      const response = await api.get('/recommendations/market-insights');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get market insights' };
    }
  }
};

export default recommendationService;
