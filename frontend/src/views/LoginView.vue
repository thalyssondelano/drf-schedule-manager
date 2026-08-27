<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = '' 
  
  try {
    const response = await axios.post('http://localhost:8000/api/token/', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    localStorage.setItem('username', username.value)
    
    router.push('/dashboard')
    
  } catch (error) {    
    errorMessage.value = "Credenciais Incorretas. Tente novamente."
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">Login</h2>
      <p class="login-subtitle">Gerenciador de Agendamentos</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        
        <div class="form-group">
          <label for="username">Usuário</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            placeholder="Digite seu usuário"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Senha</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Digite sua senha"
            required
          />
        </div>

        <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>

        <button type="submit" class="btn-submit">Entrar</button>
      
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6; 
}

.login-card {
  background-color: white;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-title {
  margin: 0;
  color: #1f2937;
  font-size: 1.5rem;
  text-align: center;
}

.login-subtitle {
  color: #6b7280;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #374151;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #2563eb; 
}

.btn-submit {
  width: 100%;
  background-color: #2563eb;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-submit:hover {
  background-color: #1d4ed8; 
}

.error-msg {
  color: #dc2626;
  font-size: 0.85rem;
  text-align: center;
  margin-bottom: 1rem;
}
</style>