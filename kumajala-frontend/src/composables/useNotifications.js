import { ref } from 'vue';

// Stockage global des notifications
const notifications = ref([]);
let nextId = 0;

/**
 * Composant pour gérer les notifications toast dans l'application.
 * Fournit des méthodes pour afficher différents types de notifications.
 */
export function useNotifications() {

  /**
   * Affiche une notification.
   * @param {string} message - Le message principal de la notification.
   * @param {string} type - Le type de notification ('success', 'error', 'warning', 'info').
   * @param {string} [details=null] - Des détails supplémentaires pour la notification.
   * @param {number} [duration=5000] - La durée en millisecondes avant la fermeture automatique (0 pour permanent).
   */
  const showNotification = (message, type, details = null, duration = 5000) => {
    const id = `notification-${nextId++}`;
    const newNotification = { id, message, type, details, duration };
    notifications.value.push(newNotification);

    // Supprime la notification après sa durée, sauf si elle est permanente
    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, duration);
    }
  };

  /**
   * Supprime une notification par son ID.
   * @param {string} id - L'ID de la notification à supprimer.
   */
  const removeNotification = (id) => {
    notifications.value = notifications.value.filter(n => n.id !== id);
  };

  /**
   * Affiche une notification de succès.
   * @param {string} message - Le message de succès.
   * @param {string} [details=null] - Des détails supplémentaires.
   * @param {number} [duration=5000] - Durée.
   */
  const showSuccess = (message, details = null, duration = 5000) => {
    showNotification(message, 'success', details, duration);
  };

  /**
   * Affiche une notification d'erreur.
   * @param {string} message - Le message d'erreur.
   * @param {string} [details=null] - Des détails supplémentaires.
   * @param {number} [duration=0] - Durée (par défaut permanent pour les erreurs).
   */
  const showError = (message, details = null, duration = 0) => {
    showNotification(message, 'error', details, duration);
  };

  /**
   * Affiche une notification d'information.
   * @param {string} message - Le message d'information.
   * @param {string} [details=null] - Des détails supplémentaires.
   * @param {number} [duration=5000] - Durée.
   */
  const showInfo = (message, details = null, duration = 5000) => {
    showNotification(message, 'info', details, duration);
  };

  /**
   * Affiche une notification d'avertissement.
   * @param {string} message - Le message d'avertissement.
   * @param {string} [details=null] - Des détails supplémentaires.
   * @param {number} [duration=8000] - Durée.
   */
  const showWarning = (message, details = null, duration = 8000) => {
    showNotification(message, 'warning', details, duration);
  };

  return {
    notifications,
    showSuccess,
    showError,
    showInfo,
    showWarning,
    removeNotification
  };
}
