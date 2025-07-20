<template>
  <div :class="['notification-toast', `notification-${type}`]">
    <div class="notification-icon">
      <component :is="iconComponent" width="20" height="20" />
    </div>
    <div class="notification-content">
      <p class="notification-message">{{ message }}</p>
      <span v-if="details" class="notification-details">{{ details }}</span>
    </div>
    <button class="notification-close-button" @click="$emit('close')" aria-label="Fermer la notification">
      <XIcon width="16" height="16" />
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { CheckCircle as CheckCircleIcon, XCircle as XCircleIcon, Info as InfoIcon, AlertTriangle as AlertTriangleIcon, X as XIcon } from 'lucide-vue-next';

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: 'info', // 'success', 'error', 'warning', 'info'
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value),
  },
  details: {
    type: String,
    default: null,
  },
  duration: {
    type: Number,
    default: 5000, // Durée en ms avant fermeture automatique
  },
});

const emit = defineEmits(['close']);

const iconComponent = computed(() => {
  switch (props.type) {
    case 'success':
      return CheckCircleIcon;
    case 'error':
      return XCircleIcon;
    case 'warning':
      return AlertTriangleIcon;
    case 'info':
    default:
      return InfoIcon;
  }
});

// Auto-fermeture
let timeoutId;
if (props.duration > 0) {
  timeoutId = setTimeout(() => {
    emit('close');
  }, props.duration);
}

// Nettoyage du timeout si le composant est démonté manuellement
import { onUnmounted } from 'vue';
onUnmounted(() => {
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
});
</script>

<style scoped>
.notification-toast {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  color: var(--cl-white);
  font-family: var(--font-primary);
  font-size: var(--fs-sm);
  position: relative;
  overflow: hidden;
  animation: slideInFromRight 0.3s ease-out forwards;
  transition: background-color var(--transition-base), border-color var(--transition-base), color var(--transition-base);
}

@keyframes slideInFromRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-toast.notification-leave-active {
  animation: slideOutToRight 0.3s ease-in forwards;
}

@keyframes slideOutToRight {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

.notification-success {
  background-color: var(--cl-success);
}

.notification-error {
  background-color: var(--cl-error);
}

.notification-warning {
  background-color: var(--cl-warning);
}

.notification-info {
  background-color: var(--cl-info);
}

.notification-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-content {
  flex-grow: 1;
}

.notification-message {
  font-weight: var(--fw-semibold);
  margin-bottom: var(--space-1);
}

.notification-details {
  font-size: var(--fs-xs);
  opacity: 0.8;
}

.notification-close-button {
  background: none;
  border: none;
  color: var(--cl-white);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
}

.notification-close-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

/* Dark mode adjustments */
html.dark-mode .notification-toast {
  color: var(--cl-black); /* Texte sombre sur fond coloré */
}
html.dark-mode .notification-success {
  background-color: var(--cl-success); /* Utilise la couleur du dark mode */
}
html.dark-mode .notification-error {
  background-color: var(--cl-error); /* Utilise la couleur du dark mode */
}
html.dark-mode .notification-warning {
  background-color: var(--cl-warning); /* Utilise la couleur du dark mode */
}
html.dark-mode .notification-info {
  background-color: var(--cl-info); /* Utilise la couleur du dark mode */
}
html.dark-mode .notification-close-button {
  color: var(--cl-black);
}
html.dark-mode .notification-close-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}
</style>
