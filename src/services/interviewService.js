import api from './api';

export const interviewService = {
  // Start interview
  async startInterview(interviewData) {
    try {
      const response = await api.post('/interview/start', interviewData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to start interview' };
    }
  },

  // Submit interview answer
  async submitAnswer(answerData) {
    try {
      const response = await api.post('/interview/answer', answerData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to submit answer' };
    }
  },

  // Get interview feedback
  async getInterviewFeedback(interviewId) {
    try {
      const response = await api.get(`/interview/${interviewId}/feedback`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get interview feedback' };
    }
  },

  // Get all interviews for current user
  async getUserInterviews() {
    try {
      const response = await api.get('/interview/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get interviews' };
    }
  },

  // Get interview by ID
  async getInterviewById(interviewId) {
    try {
      const response = await api.get(`/interview/${interviewId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get interview' };
    }
  }
};

export default interviewService;
