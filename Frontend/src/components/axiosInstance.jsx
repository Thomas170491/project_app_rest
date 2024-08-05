import axios from "axios";

const baseUrl = import.meta.env.VITE_REACT_APP_BASE_URL;
const axiosInstance = axios.create({
  baseURL: `http://${baseUrl}/`,
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
