<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const especialistas = ref([])
const horariosDoMedico = ref([])
const medicoSelecionado = ref('')
const carregando = ref(true)

// Carrega os médicos quando a tela abre.
onMounted(async () => {
  try {
    const res = await api.get('especialistas/')
    especialistas.value = res.data
  } catch (error) {
    console.error("Erro ao carregar médicos:", error)
  } finally {
    carregando.value = false
  }
})

// Busca a agenda completa do médico escolhido.
const buscarHorarios = async () => {
  if (!medicoSelecionado.value) return
  
  try {
    const res = await api.get('horarios/')
    const medicoNome = especialistas.value.find(m => m.id === medicoSelecionado.value).nome
    
    // Filtra para pegar apenas os horários do médico selecionado.
    horariosDoMedico.value = res.data.filter(h => h.especialista_nome === medicoNome)
    
  } catch (error) {
    console.error("Erro ao buscar horários:", error)
  }
}

// Envia a requisição para marcar o horário específico.
const confirmarAgendamento = async (horarioId) => {
  try {
    // Utiliza a rota customizada para reservar e impedir agendamento duplicado.
    await api.patch(`horarios/${horarioId}/reservar/`)

    alert("Consulta agendada com sucesso!")
    router.push('/dashboard')
    
  } catch (error) {
    console.error("Erro ao agendar:", error)
    alert("Não foi possível agendar. Esse horário já foi ocupado.")
  }
}

const voltar = () => {
  router.push('/dashboard')
}
</script>

<template>
  <div class="agendar-container">
    <div class="agendar-card">
      <div class="header">
        <h2>📅 Agendar Nova Consulta</h2>
        <button @click="voltar" class="btn-voltar">Voltar</button>
      </div>

      <p v-if="carregando" class="loading">Carregando médicos...</p>

      <div v-else class="agendar-form">
        
        <!-- SELEÇÃO DO MÉDICO -->
        <div class="form-group">
          <label>1. Escolha o Especialista</label>
          <select v-model="medicoSelecionado" @change="buscarHorarios">
            <option value="" disabled>Selecione o especialista...</option>
            <option v-for="medico in especialistas" :key="medico.id" :value="medico.id">
              {{ medico.nome }} ({{ medico.especialidade }})
            </option>
          </select>
        </div>

        <!-- Lista de Horário ( Livres e Ocupados ) -->
        <div v-if="medicoSelecionado" class="horarios-section">
          <label>2. Escolha o Horário de Atendimento</label>
          
          <div v-if="horariosDoMedico.length === 0" class="sem-horarios">
            Nenhum horário dispónivel para esse especialista no momento.
          </div>
          
          <div class="grid-horarios">
            <button 
              v-for="horario in horariosDoMedico" 
              :key="horario.id"
              @click="confirmarAgendamento(horario.id)"
              :disabled="horario.paciente !== null"
              :class="['btn-horario', horario.paciente !== null ? 'ocupado' : 'livre']"
            >
              <span class="data-hora">{{ horario.data }} - {{ horario.hora }}</span>
              <span class="status-text">
                {{ horario.paciente !== null ? 'Reservado' : 'Disponível' }}
              </span>
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.agendar-container {
  min-height: 100vh; padding: 2rem; background-color: #f3f4f6;
  display: flex; justify-content: center; align-items: flex-start;
}
.agendar-card {
  background-color: white; padding: 2.5rem; border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); width: 100%; max-width: 600px;
}
.header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 2rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 1rem;
}
.header h2 { margin: 0; color: #1f2937; font-size: 1.5rem; }
.btn-voltar { background: none; border: none; color: #6b7280; cursor: pointer; font-weight: bold; text-decoration: underline; }

.form-group { margin-bottom: 1.5rem; display: flex; flex-direction: column; }
.form-group label { margin-bottom: 0.5rem; font-weight: bold; color: #374151; font-size: 1rem; }
.form-group select { padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 1rem; outline: none; }
.form-group select:focus { border-color: #2563eb; }

.horarios-section { margin-top: 2rem; }
.sem-horarios { color: #dc2626; padding: 1rem; background-color: #fee2e2; border-radius: 6px; text-align: center; font-weight: bold; }
.grid-horarios { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1rem; margin-top: 1rem; }

.btn-horario {
  padding: 1rem; border-radius: 8px; font-weight: bold; transition: all 0.2s;
  display: flex; flex-direction: column; align-items: center; gap: 0.5rem;
}
.data-hora { font-size: 1rem; }
.status-text { font-size: 0.8rem; font-weight: normal; }

.btn-horario.livre {
  background-color: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; cursor: pointer;
}
.btn-horario.livre:hover { background-color: #22c55e; color: white; border-color: #16a34a; }

.btn-horario.ocupado {
  background-color: #f3f4f6; color: #9ca3af; border: 1px solid #e5e7eb;
  cursor: not-allowed; opacity: 0.7;
}
</style>