import apiClient from './axiosConfig';

/**
 * Service pour les opérations liées aux langues
 */
export const languagesService = {
  /**
   * Récupère la liste des langues supportées
   * @returns {Promise} Liste des langues avec leurs métadonnées
   */
  async getSupportedLanguages() {
    try {
      const response = await apiClient.get('/languages');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des langues:', error);
      throw error;
    }
  },

  /**
   * Récupère les informations d'une langue spécifique
   * @param {string} languageCode - Code de la langue
   * @returns {Promise} Informations de la langue
   */
  async getLanguageInfo(languageCode) {
    try {
      const response = await apiClient.get(`/languages/${languageCode}`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la récupération des infos pour ${languageCode}:`, error);
      throw error;
    }
  },

  /**
   * Récupère toutes les traductions disponibles pour une langue cible
   * @param {string} targetLanguageCode - Code de la langue cible
   * @returns {Promise} Traductions disponibles
   */
  async getLanguageTranslations(targetLanguageCode) {
    try {
      const response = await apiClient.get(`/languages/${targetLanguageCode}/translations`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la récupération des traductions pour ${targetLanguageCode}:`, error);
      throw error;
    }
  },

  /**
   * Filtre les langues par région
   * @param {Array} languages - Liste des langues
   * @param {string} region - Région à filtrer
   * @returns {Array} Langues filtrées
   */
  filterByRegion(languages, region) {
    return languages.filter(lang => 
      lang.region && lang.region.toLowerCase().includes(region.toLowerCase())
    );
  },

  /**
   * Trouve une langue par son code
   * @param {Array} languages - Liste des langues
   * @param {string} code - Code de la langue
   * @returns {Object|null} Langue trouvée ou null
   */
  findByCode(languages, code) {
    return languages.find(lang => lang.code === code) || null;
  },

  /**
   * Groupe les langues par région
   * @param {Array} languages - Liste des langues
   * @returns {Object} Langues groupées par région
   */
  groupByRegion(languages) {
    return languages.reduce((groups, lang) => {
      const region = lang.region || 'Autre';
      if (!groups[region]) {
        groups[region] = [];
      }
      groups[region].push(lang);
      return groups;
    }, {});
  }
};

export default languagesService;