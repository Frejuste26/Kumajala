<script setup>
import { RouterView } from 'vue-router';
import NotificationToast from '@/components/NotificationToast.vue'; // Import du composant de notification
import { useNotifications } from '@/composables/useNotifications'; // Import du composable

const { notifications, removeNotification } = useNotifications();
</script>

<template>
  <div id="app">
    <!-- Conteneur principal pour les transitions de page -->
    <RouterView v-slot="{ Component }">
      <Transition name="page-fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>

    <!-- Conteneur des notifications -->
    <div class="notification-container">
      <TransitionGroup name="notification-list">
        <NotificationToast
          v-for="notification in notifications"
          :key="notification.id"
          :id="notification.id"
          :message="notification.message"
          :type="notification.type"
          :details="notification.details"
          :duration="notification.duration"
          @close="removeNotification(notification.id)"
        />
      </TransitionGroup>
    </div>
  </div>
</template>

<style>
/* Styles globaux pour l'application si nécessaire, sinon main.css suffit */
body {
  margin: 0;
  padding: 0;
  font-family: var(--font-primary); /* Utilise la variable de base.css */
  background-color: var(--cl-gray-100); /* Utilise la variable de base.css */
  color: var(--cl-black); /* Couleur de texte par défaut */
  transition: var(--transition-color); /* Transition pour le mode sombre */
}

/* Conteneur des notifications */
.notification-container {
  position: fixed;
  top: var(--space-6);
  right: var(--space-6);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  max-width: 320px; /* Limite la largeur des toasts */
  pointer-events: none; /* Permet de cliquer à travers le conteneur */
}

.notification-container > * {
  pointer-events: auto; /* Mais les toasts eux-mêmes sont cliquables */
}

/* Transitions pour la liste des notifications */
.notification-list-enter-active,
.notification-list-leave-active {
  transition: all 0.5s ease;
}
.notification-list-enter-from,
.notification-list-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
.notification-list-move {
  transition: transform 0.5s ease;
}

/* Responsive pour les notifications */
@media (max-width: 640px) {
  .notification-container {
    top: auto;
    bottom: var(--space-4);
    left: var(--space-4);
    right: var(--space-4);
    max-width: calc(100% - var(--space-8));
  }
}

/* Styles pour les transitions de page */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateX(20px); /* Glisse légèrement depuis la droite */
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px); /* Glisse légèrement vers la gauche */
}
</style>
