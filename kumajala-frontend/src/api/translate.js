import apiClient from './axiosConfig';

/**
 * Service pour les opérations de traduction
 */
export const translateService = {
  /**
   * Traduit un texte vers une langue cible
   * @param {string} text - Texte à traduire
   * @param {string} targetLanguage - Code de la langue cible
   * @returns {Promise} Réponse de l'API
   */
  async translateText(text, targetLanguage) {
    try {
      const response = await apiClient.post('/translate', {
        text: text.trim(),
        targetLanguage: targetLanguage.toLowerCase()
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la traduction:', error);
      throw error;
    }
  },

  /**
   * Traduit plusieurs textes en une seule requête
   * @param {string[]} texts - Tableau de textes à traduire
   * @param {string} targetLanguage - Code de la langue cible
   * @returns {Promise} Réponse de l'API
   */
  async translateBatch(texts, targetLanguage) {
    try {
      const response = await apiClient.post('/translate/batch', {
        texts: texts.map(text => text.trim()),
        targetLanguage: targetLanguage.toLowerCase()
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la traduction batch:', error);
      throw error;
    }
  },

  /**
   * Ajoute ou modifie manuellement une traduction
   * @param {string} frenchText - Texte français
   * @param {string} targetLanguage - Langue cible
   * @param {string} newTranslation - Nouvelle traduction
   * @returns {Promise} Réponse de l'API
   */
  async manageTranslation(frenchText, targetLanguage, newTranslation) {
    try {
      const response = await apiClient.post('/translations/manage', {
        frenchText: frenchText.trim(),
        targetLanguage: targetLanguage.toLowerCase(),
        newTranslation: newTranslation.trim()
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la gestion de traduction:', error);
      throw error;
    }
  }
};

export default translateService;