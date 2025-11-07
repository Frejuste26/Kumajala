import apiClient from './axiosConfig';

/**
 * Service pour les opérations de synthèse vocale
 */
export const speechService = {
  /**
   * Génère l'audio d'un texte traduit
   * @param {string} text - Texte à synthétiser
   * @param {string} languageCode - Code de langue pour la synthèse
   * @returns {Promise} Réponse de l'API avec l'audio en base64
   */
  async synthesizeSpeech(text, languageCode = 'fr') {
    try {
      const response = await apiClient.post('/speak', {
        text: text.trim(),
        languageCode: languageCode
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la synthèse vocale:', error);
      throw error;
    }
  },

  /**
   * Joue l'audio à partir des données base64
   * @param {string} audioBase64 - Audio encodé en base64
   * @param {string} contentType - Type de contenu (ex: 'audio/mpeg')
   * @returns {Promise<HTMLAudioElement>} Element audio
   */
  async playAudio(audioBase64, contentType = 'audio/mpeg') {
    try {
      const audioSrc = `data:${contentType};base64,${audioBase64}`;
      const audio = new Audio(audioSrc);
      
      return new Promise((resolve, reject) => {
        audio.onloadeddata = () => resolve(audio);
        audio.onerror = (error) => reject(error);
        audio.play().catch(reject);
      });
    } catch (error) {
      console.error('Erreur lors de la lecture audio:', error);
      throw error;
    }
  },

  /**
   * Télécharge l'audio en tant que fichier
   * @param {string} audioBase64 - Audio encodé en base64
   * @param {string} filename - Nom du fichier
   * @param {string} contentType - Type de contenu
   */
  downloadAudio(audioBase64, filename = 'kumajala-audio.mp3', contentType = 'audio/mpeg') {
    try {
      const audioSrc = `data:${contentType};base64,${audioBase64}`;
      const link = document.createElement('a');
      link.href = audioSrc;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Erreur lors du téléchargement audio:', error);
      throw error;
    }
  }
};

export default speechService;