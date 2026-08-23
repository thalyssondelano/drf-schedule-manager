<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const username = localStorage.getItem('username') || 'Usuário'

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('username')
  router.push('/')
}
</script>

<template>
  <div class="dashboard-container">
    <div class="dashboard-card">
      <h1 class="welcome-title">Bem-vindo, {{ username }}! 🚀</h1>
      <p class="welcome-text">Você fez login com sucesso no sistema da clínica.</p>
      
      <button @click="handleLogout" class="btn-logout">Sair do Sistema</button>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
}

.dashboard-card {
  background-color: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.welcome-title {
  color: #1f2937;
  margin-top: 0;
  font-size: 1.8rem;
}

.welcome-text {
  color: #6b7280;
  margin-bottom: 2rem;
}

.btn-logout {
  background-color: #dc2626;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-logout:hover {
  background-color: #b91c1c;
}
</style>