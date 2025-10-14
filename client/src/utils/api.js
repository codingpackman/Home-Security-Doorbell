// API utility functions - simplify authenticated API requests

const API_BASE_URL = 'http://localhost:5050';

// Get stored token
const getToken = () => {
    return localStorage.getItem('authToken');
};

// Create authenticated request headers
const getAuthHeaders = () => {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
};

// Generic API request function
export const apiRequest = async (endpoint, options = {}) => {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        ...options,
        headers: {
            ...getAuthHeaders(),
            ...options.headers,
        },
    };

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            // If token expired, clear local storage
            if (response.status === 401) {
                localStorage.removeItem('authToken');
                localStorage.removeItem('user');
                window.location.href = '/login';
            }
            throw new Error(data.message || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
};

// Specific API call functions
export const api = {
    // Get current user info
    getCurrentUser: () => apiRequest('/record/me'),
    
    // Get all records
    getAllRecords: () => apiRequest('/record'),
    
    // Get single record
    getRecordById: (id) => apiRequest(`/record/${id}`),
    
    // Update record
    updateRecord: (id, data) => apiRequest(`/record/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
    }),
    
    // Delete record
    deleteRecord: (id) => apiRequest(`/record/${id}`, {
        method: 'DELETE',
    }),
};

export default api;

