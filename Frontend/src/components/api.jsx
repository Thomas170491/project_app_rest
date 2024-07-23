import axios from 'axios';
import { alignPropType } from 'react-bootstrap/esm/types';

const api = axios.create({
  baseURL: 'http://localhost:5000', // Remplacez par l'URL de votre API
});

export const loginUser = async (username, password) => {
  try {
    const response = await api.post('/users/login', { username, password });

    // Check if response is in expected format
    if (response.data && response.data.token) {
      return response.data;
    } else {
      // Handle unexpected response structure
      throw new Error('Unexpected response format');
    }
  } catch (error) {
    // Handle error responses and network errors
    if (error.response) {
      // Return detailed error message from server if available
      return {
        status: error.response.status,
        message: error.response.data.message || 'An error occurred',
      };
    } else {
      // Throw a network error if no response is available
      throw new Error('Network error'); }
    }
  }


export const getUserDashboard = async () => {
  const token = localStorage.getItem('acces_token')
  try {
    const response = await api.get(`/users/dashboard`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;  // Handle the response data accordingly
} catch (error) {
    console.error('Failed to fetch dashboard data:', error);
    throw error;  // Rethrow error to be handled in your component
}
};
export const getDriverDashboard = async () => {
    
    const response = await api.get('/drivers/dashboard')
    return response.data
    }
export const getAdminDashboard = async () => {
  const response = await api.get('/admins/dashboard')
  return response.data
}
export const deleteUser = async (user_id) => {
  const response = await api.post("/admins/delete-user/${user_id}")
  return response.data
}



export default api;