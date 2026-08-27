<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const username = localStorage.getItem('username') || 'Usuário'

const especialistas = ref([])
const meusAgendamentos = ref([])
const diasDaSemana = ref([])
const carregando = ref(true)

const formEspecialista = ref({ nome: '', especialidade: '' })
const formAgenda = ref({
  especialista: '',
  dias_semana: [],
  data_inicio: '',
  data_fim: '',
  hora_inicio: '',
  hora_fim: '',
  vagas_por_dia: 1
})

onMounted(async () => {
  try {
    // Busca Especialistas e Dias da Semana
    const [resEsp, resDias] = await Promise.all([
      api.get('especialistas/'),
      api.get('dias-semana/')
    ])
    
    especialistas.value = resEsp.data
    diasDaSemana.value = resDias.data
    
    // Busca os horários reservados do paciente logado
    if (username !== 'admin') {
      const resHorarios = await api.get('horarios/?meus=true')
      meusAgendamentos.value = resHorarios.data
    }

  } catch (error) {
    console.error("Erro ao buscar dados:", error)
  } finally {
    carregando.value = false
  }
})

const cadastrarEspecialista = async () => {
  try {
    await api.post('especialistas/', formEspecialista.value)
    alert('Especialista cadastrado com sucesso!')
    formEspecialista.value = { nome: '', especialidade: '' } // Limpa o formulário ao finalizar
    
    // Atualiza a lista de especialistas na tela
    const res = await api.get('especialistas/')
    especialistas.value = res.data
  } catch (error) {
    console.error(error)
    alert('Erro ao cadastrar especialista.')
  }
}

const criarAgenda = async () => {
  if (formAgenda.value.dias_semana.length === 0) {
    alert("Selecione pelo menos um dia da semana!")
    return
  }
  try {
    await api.post('agendas/', formAgenda.value)
    alert('Agenda criada e horários gerados com sucesso!')
    // Limpa o formulário ao finalizar
    formAgenda.value = { especialista: '', dias_semana: [], data_inicio: '', data_fim: '', hora_inicio: '', hora_fim: '', vagas_por_dia: 1 }
  } catch (error) {
    console.error(error)
    
    if (error.response && error.response.data) {
      const dadosErro = error.response.data
      
      const mensagensErro = Object.values(dadosErro)
        .flat()
        .join('\n\n')   
        
      alert(`⚠️ Não foi possível criar a agenda:\n\n${mensagensErro}`)
      
    } else {
      alert('⚠️ Erro de conexão.')
    }
  }
}

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
      <div class="header">
        <h1 class="welcome-title">Olá, {{ username }}!</h1>
        <button @click="handleLogout" class="btn-logout">Sair</button>
      </div>
      
      <!-- Visao do Administrador -->
      <div v-if="username === 'admin'" class="admin-panel">
        <span class="role-badge admin">Administrador</span>
        
        <div class="admin-grid">
          <!-- Cadastrar Especialista -->
          <div class="admin-box">
            <h3>👨‍⚕️ Novo Especialista</h3>
            <form @submit.prevent="cadastrarEspecialista" class="form-basico">
              <input type="text" v-model="formEspecialista.nome" placeholder="Nome" required>
              <input type="text" v-model="formEspecialista.especialidade" placeholder="Especialidade" required>
              <button type="submit" class="btn-submit">Salvar Especialista</button>
            </form>
          </div>

          <!-- Criar Agenda -->
          <div class="admin-box">
            <h3>📅 Criar Agenda de Atendimento</h3>
            <form @submit.prevent="criarAgenda" class="form-basico">
              
              <select v-model="formAgenda.especialista" required>
                <option value="" disabled>Selecione o Especialista...</option>
                <option v-for="med in especialistas" :key="med.id" :value="med.id">{{ med.nome }}</option>
              </select>

              <div class="dias-checkbox">
                <label>Dias de Atendimento:</label>
                <div class="checkbox-grid">
                  <!-- Empilha os IDs em um array automaticamente -->
                  <label v-for="dia in diasDaSemana" :key="dia.id" class="check-item">
                    <input type="checkbox" :value="dia.id" v-model="formAgenda.dias_semana">
                    {{ dia.nome_dia || dia.dia }}
                  </label>
                </div>
              </div>

              <div class="input-row">
                <div class="input-col"><label>Início</label><input type="date" v-model="formAgenda.data_inicio" required></div>
                <div class="input-col"><label>Fim</label><input type="date" v-model="formAgenda.data_fim" required></div>
              </div>
              
              <div class="input-row">
                <div class="input-col"><label>Hora Início</label><input type="time" v-model="formAgenda.hora_inicio" required></div>
                <div class="input-col"><label>Hora Fim</label><input type="time" v-model="formAgenda.hora_fim" required></div>
              </div>

              <div class="input-col" style="margin-bottom: 1rem;">
                <label>Vagas por Dia</label>
                <input type="number" v-model="formAgenda.vagas_por_dia" min="1" required>
              </div>

              <button type="submit" class="btn-submit">Gerar Horários</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Visao do Paciente -->
      <div v-else class="patient-panel">
        <span class="role-badge patient">Paciente</span>
        <div class="header-paciente">
          <h2>Minhas Consultas</h2>
          <button @click="router.push('/agendar')" class="btn-action">📅 Agendar</button>
        </div>
        
        <p v-if="carregando">Carregando consultas...</p>
        
        <ul v-else-if="meusAgendamentos.length > 0" class="lista-consultas">
          <li v-for="consulta in meusAgendamentos" :key="consulta.id" class="card-consulta">
            <div class="consulta-info">
              <strong>{{ consulta.especialista_nome }}</strong>
              <span class="data">{{ consulta.data }} às {{ consulta.hora }}</span>
            </div>
            <span class="badge-status">Confirmada</span>
          </li>
        </ul>
        <div v-else class="sem-dados">Você ainda não tem consultas agendadas.</div>
      </div>

      <!-- Lista de Especialistas -->
      <div class="content">
        <hr class="divider" />
        <h3>Corpo Clínico</h3>
        <ul v-if="especialistas.length > 0" class="lista-especialistas">
          <li v-for="medico in especialistas" :key="medico.id" class="card-medico">
            <strong>{{ medico.nome }}</strong> 
            <span class="badge">{{ medico.especialidade }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container { min-height: 100vh; padding: 2rem; background-color: #f3f4f6; display: flex; justify-content: center; align-items: flex-start; }
.dashboard-card { background-color: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); width: 100%; max-width: 900px; }
.header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e5e7eb; padding-bottom: 1rem; margin-bottom: 2rem; }
.welcome-title { color: #1f2937; margin: 0; font-size: 1.5rem; }
.btn-logout { background-color: #dc2626; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; font-weight: bold; cursor: pointer; }
.role-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.8rem; font-weight: bold; margin-bottom: 1rem; }
.role-badge.admin { background-color: #fef08a; color: #854d0e; }
.role-badge.patient { background-color: #dcfce7; color: #166534; }
.divider { border: 0; border-top: 1px solid #e5e7eb; margin: 2rem 0; }

.admin-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }
@media (max-width: 768px) { .admin-grid { grid-template-columns: 1fr; } }
.admin-box { background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1.5rem; border-radius: 8px; }
.admin-box h3 { margin-top: 0; color: #334155; font-size: 1.1rem; border-bottom: 2px solid #cbd5e1; padding-bottom: 0.5rem; margin-bottom: 1rem; }
.form-basico { display: flex; flex-direction: column; gap: 1rem; }
.form-basico input[type="text"], .form-basico select, .form-basico input[type="date"], .form-basico input[type="time"], .form-basico input[type="number"] {
  padding: 0.6rem; border: 1px solid #cbd5e1; border-radius: 6px; width: 100%; font-size: 0.9rem;
}
.input-row { display: flex; gap: 1rem; }
.input-col { flex: 1; display: flex; flex-direction: column; gap: 0.3rem; font-size: 0.85rem; font-weight: bold; color: #475569; }
.dias-checkbox label { font-size: 0.85rem; font-weight: bold; color: #475569; margin-bottom: 0.5rem; display: block; }
.checkbox-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
.check-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem; font-weight: normal; color: #334155; cursor: pointer; }
.btn-submit { background-color: #2563eb; color: white; border: none; padding: 0.75rem; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }
.btn-submit:hover { background-color: #1d4ed8; }

.header-paciente { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.btn-action { background-color: #2563eb; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; font-weight: bold; cursor: pointer; }
.lista-consultas, .lista-especialistas { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 1rem; }
.card-consulta { padding: 1rem; border: 1px solid #bbf7d0; background-color: #f0fdf4; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
.consulta-info { display: flex; flex-direction: column; }
.consulta-info strong { color: #166534; font-size: 1.1rem; }
.consulta-info .data { color: #15803d; font-size: 0.9rem; }
.badge-status { background-color: #22c55e; color: white; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.75rem; font-weight: bold; }
.card-medico { padding: 1rem; border: 1px solid #d1d5db; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
.badge { background-color: #e0f2fe; color: #0369a1; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; font-weight: bold; }
.sem-dados { color: #6b7280; font-style: italic; }
</style>