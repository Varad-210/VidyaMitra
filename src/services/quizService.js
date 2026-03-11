import api from './api';

export const quizService = {
  // Start quiz
  async startQuiz(quizData) {
    try {
      const response = await api.post('/quiz/start', quizData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to start quiz' };
    }
  },

  // Submit quiz answer
  async submitQuizAnswer(answerData) {
    try {
      const response = await api.post('/quiz/answer', answerData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to submit quiz answer' };
    }
  },

  // Get quiz results
  async getQuizResults(attemptId) {
    try {
      const response = await api.get(`/quiz/${attemptId}/results`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get quiz results' };
    }
  },

  // Get all quiz attempts for current user
  async getUserQuizAttempts() {
    try {
      const response = await api.get('/quiz/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get quiz attempts' };
    }
  },

  // Get available quiz categories
  async getQuizCategories() {
    try {
      const response = await api.get('/quiz/categories');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get quiz categories' };
    }
  },

  // Get quiz by ID
  async getQuizById(quizId) {
    try {
      const response = await api.get(`/quiz/${quizId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get quiz' };
    }
  }
};

export default quizService;
