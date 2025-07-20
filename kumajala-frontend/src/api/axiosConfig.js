import axios from 'axios';

// Définir l'URL de base de votre backend Flask
// Si votre backend Flask tourne sur localhost:5000 et que votre frontend est sur un port différent,
// vous devrez utiliser l'URL complète ici.
// Assurez-vous que cette URL correspond à celle de votre backend.
const API_BASE_URL = 'http://localhost:5000/kumajala-api/v1'; // Ajustez si votre base URL est différente

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Vous pouvez ajouter des intercepteurs ici si nécessaire, par exemple pour gérer les erreurs
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('Erreur de l\'API:', error.response || error.message);
    // Vous pouvez ajouter une logique de gestion d'erreur globale ici,
    // comme afficher une notification à l'utilisateur ou rediriger.
    return Promise.reject(error);
  }
);

export default apiClient;
