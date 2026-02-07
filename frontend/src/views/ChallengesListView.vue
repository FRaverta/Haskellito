<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const API_BASE = '/api'
const router = useRouter()

const challenges = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

async function fetchChallenges() {
  try {
    const response = await axios.get(`${API_BASE}/challenges`)
    challenges.value = response.data.challenges
  } catch (error) {
    errorMessage.value = `Failed to load challenges: ${error.message}`
  } finally {
    isLoading.value = false
  }
}

function goToChallenge(id) {
  router.push(`/challenge/${id}`)
}

onMounted(() => {
  fetchChallenges()
})
</script>

<template>
  <div class="challenges-list-view">
    <div class="content">
      <h2>Haskell Challenges</h2>
      <p class="subtitle">Practice your Haskell skills with these coding challenges</p>

      <div v-if="isLoading" class="loading">
        Loading challenges...
      </div>

      <div v-else-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div v-else class="challenges-grid">
        <div 
          v-for="challenge in challenges" 
          :key="challenge.id" 
          class="challenge-card"
          @click="goToChallenge(challenge.id)"
        >
          <h3>{{ challenge.title }}</h3>
          <div class="card-footer">
            <span class="start-btn">Start Challenge →</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.challenges-list-view {
  height: 100%;
  overflow-y: auto;
  background: #1e1e2e;
}

.content {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

h2 {
  color: #89b4fa;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.subtitle {
  color: #6c7086;
  margin-bottom: 2rem;
}

.loading {
  color: #6c7086;
  font-style: italic;
}

.error-message {
  color: #f38ba8;
}

.challenges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.challenge-card {
  background: #181825;
  border: 1px solid #313244;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.challenge-card:hover {
  border-color: #89b4fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.challenge-card h3 {
  color: #cdd6f4;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
}

.start-btn {
  color: #89b4fa;
  font-size: 0.875rem;
  font-weight: 500;
}

.challenge-card:hover .start-btn {
  color: #b4befe;
}
</style>
