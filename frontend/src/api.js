import axios from 'axios'

// Instancia o AXIOS
const api = axios.create({
  baseURL: 'http://localhost:8000/api/'
})

// Toda requisicao passa por aqui
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  
  // Se existir um token salvo, ele anexa como um cracha de acesso
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api