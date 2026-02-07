import { reactive, ref } from 'vue'

/**
 * In-memory store for challenge progress (code + test results) per challenge id.
 * Persists when switching between Playground and Challenges.
 */
const progressByChallenge = reactive({})

/** Last challenge page the user was on (e.g. "factorial"). Used so "Challenges" nav returns to it. */
export const lastViewedChallengeId = ref(null)

export function getChallengeProgress(challengeId) {
  return progressByChallenge[challengeId] ?? null
}

export function setChallengeProgress(challengeId, { code, results }) {
  if (!progressByChallenge[challengeId]) {
    progressByChallenge[challengeId] = { code: '', results: [] }
  }
  if (code !== undefined) {
    progressByChallenge[challengeId].code = String(code)
  }
  if (results !== undefined) {
    progressByChallenge[challengeId].results = Array.isArray(results)
      ? [...results]
      : []
  }
}

export function setLastViewedChallengeId(challengeId) {
  lastViewedChallengeId.value = challengeId
}
