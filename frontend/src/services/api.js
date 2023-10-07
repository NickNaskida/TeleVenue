import axios from "axios";


const axiosInstance = axios.create({
  baseURL: `${import.meta.env.VITE_BASE_API_URL}`,
});

export default axiosInstance;