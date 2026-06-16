import axios from 'axios'

const baseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const api = axios.create({
  baseURL: `${baseUrl}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
