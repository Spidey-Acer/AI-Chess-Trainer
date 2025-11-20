import axios from 'axios';

// Default to localhost, will be updated if running in Electron
let API_URL = 'http://127.0.0.1:5000';

// Initialize API URL if running in Electron
if (window.electronAPI) {
  window.electronAPI.getApiUrl().then(url => {
    API_URL = url;
    api.defaults.baseURL = url;
  });
}

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const healthCheck = () => api.get('/api/health');

export const analyzePosition = (fen, depth = 20) =>
  api.post('/api/analyze/position', { fen, depth });

export const analyzeGame = (pgn, depth = 20, generateFeedback = false) =>
  api.post('/api/analyze/game', { pgn, depth, generate_feedback: generateFeedback });

export const getTrainingPosition = (difficulty = 'intermediate', focus = 'general') =>
  api.post('/api/train/position', { difficulty, focus });

export const checkMove = (fen, move) =>
  api.post('/api/train/check-move', { fen, move });

export const listGames = (limit = 10, offset = 0) =>
  api.get('/api/games', { params: { limit, offset } });

export const getGame = (gameId) =>
  api.get(`/api/games/${gameId}`);

export const getStats = () =>
  api.get('/api/stats');

export const importPGN = (pgn, analyze = false) =>
  api.post('/api/import/pgn', { pgn, analyze });

export default api;
