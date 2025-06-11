import axios from 'axios';
import { RefactorRequest, RefactorResponse } from '@/types';

// Get API token from environment variable
const API_TOKEN = process.env.NEXT_PUBLIC_API_TOKEN;

// Configure axios instance
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 60000, // 60 second timeout
  headers: {
    'Content-Type': 'application/json',
    // Add authentication header if token is available
    ...(API_TOKEN && { 'Authorization': `Bearer ${API_TOKEN}` })
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('🚀 Making API request:', config.method?.toUpperCase(), config.url);
    console.log('📤 Request data:', config.data);
    
    // Log authentication status
    if (config.headers.Authorization) {
      console.log('🔐 Authentication: Bearer token included');
    } else {
      console.log('🔓 Authentication: No token provided');
    }
    
    return config;
  },
  (error) => {
    console.error('❌ Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('✅ API response received:', response.status, response.config.url);
    console.log('📥 Response data:', response.data);
    return response;
  },
  (error) => {
    console.error('❌ API error:', error);
    
    // Handle different types of errors
    if (error.response) {
      // Server response error
      console.error('Server response error:', error.response.status, error.response.data);
      
      // Handle authentication errors specifically
      if (error.response.status === 401) {
        const message = 'Authentication failed: Please check your API token or contact the administrator.';
        throw new Error(message);
      }
      
      const message = error.response.data?.detail || error.response.data?.message || 'Server error';
      throw new Error(`Server Error (${error.response.status}): ${message}`);
    } else if (error.request) {
      // Network error
      console.error('Network error - no response received:', error.request);
      throw new Error('Network error: Unable to connect to the server. Please check if the backend is running.');
    } else {
      // Other errors
      console.error('Request setup error:', error.message);
      throw new Error(`Request error: ${error.message}`);
    }
  }
);

// API functions
export const refactorCode = async (data: RefactorRequest): Promise<RefactorResponse> => {
  try {
    console.log('🔄 Starting refactor request with data:', data);
    const response = await api.post<RefactorResponse>('/refactor', data);
    console.log('✨ Refactor completed successfully');
    return response.data;
  } catch (error) {
    console.error('💥 Refactor API error:', error);
    throw error;
  }
};

// Health check
export const healthCheck = async (): Promise<{ status: string }> => {
  try {
    console.log('🏥 Performing health check...');
    const response = await api.get<{ status: string }>('/health');
    console.log('💚 Health check passed:', response.data);
    return response.data;
  } catch (error) {
    console.error('💔 Health check error:', error);
    throw error;
  }
};

// Check authentication status
export const checkAuthStatus = async (): Promise<{ authenticated: boolean; user?: Record<string, unknown>; message?: string }> => {
  try {
    console.log('🔐 Checking authentication status...');
    const response = await api.get('/auth/status');
    console.log('✅ Authentication check passed:', response.data);
    return response.data;
  } catch (error) {
    console.error('🚫 Authentication check failed:', error);
    // Return a formatted response for auth failures
    if (error instanceof Error && error.message.includes('Authentication failed')) {
      return { 
        authenticated: false, 
        message: error.message 
      };
    }
    throw error;
  }
};

export default api; 