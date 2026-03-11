import api from './api';

export const resumeService = {
  // Upload resume
  async uploadResume(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/resume/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Resume upload failed' };
    }
  },

  // Get resume analysis
  async getResumeAnalysis(resumeId) {
    try {
      const response = await api.get(`/resume/${resumeId}/analysis`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get resume analysis' };
    }
  },

  // Get all resumes for current user
  async getUserResumes() {
    try {
      const response = await api.get('/resume/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to get resumes' };
    }
  },

  // Delete resume
  async deleteResume(resumeId) {
    try {
      const response = await api.delete(`/resume/${resumeId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to delete resume' };
    }
  }
};

export default resumeService;
