<script setup>
</script>

<template>
  <div class="container-principal">
    <div class="card">
      <h1 class="titulo">
        Vue.js + Django
      </h1>
      <p class="texto">
        SETUP FRONTEND
      </p>
    </div>
  </div>
</template>

<style scoped>

:global(body) {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f3f4f6;
}

.container-principal {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 450px;
}

.titulo {
  color: #2563eb;
  font-size: 1.8rem;
  margin-top: 0;
  margin-bottom: 1rem;
}

.texto {
  color: #4b5563;
  font-size: 1rem;
  line-height: 1.5;
  margin: 0;
}
</style>