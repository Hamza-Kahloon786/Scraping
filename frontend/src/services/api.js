/**
 * API service for communicating with the Flask backend
 */
import axios from 'axios';

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // Increased to 60 seconds for scraping
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.response?.data);
    
    // Handle specific error cases
    if (error.response?.status === 404) {
      console.error('Resource not found');
    } else if (error.response?.status >= 500) {
      console.error('Server error occurred');
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout');
    } else if (!error.response) {
      console.error('Network error - backend might not be running');
    }
    
    return Promise.reject(error);
  }
);

/**
 * Job API endpoints - Updated to match your Flask backend
 */
export const jobAPI = {
  /**
   * Get all jobs with optional filters
   * @param {Object} params - Query parameters
   * @returns {Promise<Array>} Array of jobs
   */
  async getAllJobs(params = {}) {
    try {
      const response = await api.get('/jobs', { params });
      // Handle Flask API response format with success/data structure
      if (response.data.success) {
        return response.data.data || [];
      } else {
        console.warn('API returned success: false', response.data);
        return [];
      }
    } catch (error) {
      console.error('Error fetching jobs:', error);
      // Return empty array on error to prevent app crashes
      return [];
    }
  },

  /**
   * Get a single job by ID
   * @param {number} jobId - Job ID
   * @returns {Promise<Object|null>} Job object or null
   */
  async getJobById(jobId) {
    try {
      const response = await api.get(`/jobs/${jobId}`);
      if (response.data.success) {
        return response.data.data;
      } else {
        console.warn(`Job ${jobId} not found or API error`, response.data);
        return null;
      }
    } catch (error) {
      console.error(`Error fetching job ${jobId}:`, error);
      return null;
    }
  },

  /**
   * Create a new job
   * @param {Object} jobData - Job data
   * @returns {Promise<Object>} Created job object
   */
  async addJob(jobData) {
    try {
      // Format the job data before sending
      const formattedData = apiUtils.formatJobForAPI(jobData);
      const response = await api.post('/jobs', formattedData);
      
      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Failed to create job');
      }
    } catch (error) {
      console.error('Error creating job:', error);
      throw new Error(
        error.response?.data?.error || 
        error.message || 
        'Failed to create job'
      );
    }
  },

  /**
   * Update an existing job
   * @param {number} jobId - Job ID
   * @param {Object} jobData - Updated job data
   * @returns {Promise<Object>} Updated job object
   */
  async updateJob(jobId, jobData) {
    try {
      const formattedData = apiUtils.formatJobForAPI(jobData);
      const response = await api.put(`/jobs/${jobId}`, formattedData);
      
      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Failed to update job');
      }
    } catch (error) {
      console.error(`Error updating job ${jobId}:`, error);
      throw new Error(
        error.response?.data?.error || 
        error.message || 
        'Failed to update job'
      );
    }
  },

  /**
   * Delete a job
   * @param {number} jobId - Job ID
   * @returns {Promise<boolean>} Success status
   */
  async deleteJob(jobId) {
    try {
      const response = await api.delete(`/jobs/${jobId}`);
      return response.data.success;
    } catch (error) {
      console.error(`Error deleting job ${jobId}:`, error);
      throw new Error(
        error.response?.data?.error || 
        error.message || 
        'Failed to delete job'
      );
    }
  },

  /**
   * Trigger the job scraper
   * @returns {Promise<Object>} Scraper result
   */
  async triggerScraper() {
    try {
      console.log('🔄 Triggering job scraper...');
      const response = await api.post('/scrape');
      
      if (response.data.success) {
        console.log('✅ Scraper completed successfully');
        return response.data.data;
      } else {
        throw new Error(response.data.error || 'Scraper failed');
      }
    } catch (error) {
      console.error('Error running scraper:', error);
      throw new Error(
        error.response?.data?.error || 
        error.message || 
        'Failed to run scraper'
      );
    }
  },

  /**
   * Health check endpoint
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw new Error('Backend health check failed');
    }
  },

  /**
   * Get job statistics (if available)
   * @returns {Promise<Object>} Job statistics
   */
  async getJobStats() {
    try {
      const response = await api.get('/jobs/stats');
      if (response.data.success) {
        return response.data.data;
      } else {
        return { total: 0, recent: 0, companies: 0 };
      }
    } catch (error) {
      console.error('Error fetching job statistics:', error);
      // Return default stats on error
      return { total: 0, recent: 0, companies: 0 };
    }
  }
};

/**
 * Utility functions for API data formatting
 */
export const apiUtils = {
  /**
   * Format job data for API submission
   * @param {Object} jobData - Raw job form data
   * @returns {Object} Formatted job data
   */
  formatJobForAPI(jobData) {
    const formatted = { ...jobData };
    
    // Handle tags - ensure it's a string for backend
    if (Array.isArray(formatted.tags)) {
      formatted.tags = formatted.tags.join(', ');
    } else if (!formatted.tags) {
      formatted.tags = '';
    }
    
    // Ensure boolean values are properly formatted
    if (typeof formatted.remote_allowed === 'string') {
      formatted.remote_allowed = formatted.remote_allowed === 'true';
    }
    
    // Ensure posting_date is properly formatted if provided
    if (formatted.posting_date && typeof formatted.posting_date === 'string') {
      try {
        formatted.posting_date = new Date(formatted.posting_date).toISOString();
      } catch (e) {
        delete formatted.posting_date; // Let backend set current date
      }
    }
    
    // Remove empty or undefined fields
    Object.keys(formatted).forEach(key => {
      if (formatted[key] === '' || formatted[key] == null) {
        delete formatted[key];
      }
    });
    
    return formatted;
  },

  /**
   * Format job data from API for display
   * @param {Object} job - Job data from API
   * @returns {Object} Formatted job data
   */
  formatJobFromAPI(job) {
    if (!job) return null;
    
    const formatted = { ...job };
    
    // Format posting date
    if (formatted.posting_date) {
      try {
        formatted.posting_date = new Date(formatted.posting_date);
      } catch (e) {
        formatted.posting_date = new Date();
      }
    }
    
    // Ensure tags is handled properly
    if (typeof formatted.tags === 'string') {
      formatted.tags = formatted.tags
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0);
    } else if (!Array.isArray(formatted.tags)) {
      formatted.tags = [];
    }
    
    // Ensure boolean fields are properly typed
    formatted.remote_allowed = Boolean(formatted.remote_allowed);
    formatted.is_scraped = Boolean(formatted.is_scraped);
    
    return formatted;
  },

  /**
   * Build query parameters for job filtering
   * @param {Object} filters - Filter object
   * @returns {Object} Query parameters
   */
  buildJobQueryParams(filters) {
    const params = {};
    
    if (filters.search && filters.search.trim()) {
      params.search = filters.search.trim();
    }
    
    if (filters.job_type && filters.job_type !== 'All') {
      params.job_type = filters.job_type;
    }
    
    if (filters.location && filters.location.trim()) {
      params.location = filters.location.trim();
    }
    
    if (filters.experience_level && filters.experience_level !== 'All') {
      params.experience_level = filters.experience_level;
    }
    
    if (filters.remote_allowed !== undefined && filters.remote_allowed !== 'All') {
      params.remote_allowed = filters.remote_allowed === 'true' || filters.remote_allowed === true;
    }
    
    if (filters.sort) {
      params.sort = filters.sort;
    }
    
    if (filters.order) {
      params.order = filters.order;
    }
    
    return params;
  },

  /**
   * Format relative time display
   * @param {Date|string} date - Date to format
   * @returns {string} Formatted relative time
   */
  formatRelativeTime(date) {
    if (!date) return 'Unknown';
    
    try {
      const now = new Date();
      const jobDate = new Date(date);
      const diffInSeconds = Math.floor((now - jobDate) / 1000);
      
      if (diffInSeconds < 60) {
        return 'Just now';
      } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
      } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
      } else if (diffInSeconds < 604800) {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} day${days > 1 ? 's' : ''} ago`;
      } else {
        return jobDate.toLocaleDateString();
      }
    } catch (e) {
      return 'Unknown';
    }
  },

  /**
   * Check if backend is reachable
   * @returns {Promise<boolean>} Backend status
   */
  async checkBackendHealth() {
    try {
      await jobAPI.healthCheck();
      return true;
    } catch (error) {
      console.warn('Backend health check failed:', error.message);
      return false;
    }
  }
};

// Legacy export for backwards compatibility
export const jobsAPI = jobAPI;

// Export default API instance
export default api;