<script setup>
import { ref, onMounted, watch } from 'vue';
import TopBar from '@/components/topBar.vue';
import Screen from '@/components/Screen.vue';
import GetStartedButton from '@/components/getStartedButton.vue';
import { Moon as MoonIcon, Sun as SunIcon, Save as SaveIcon } from 'lucide-vue-next'; 
import { Home as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon } from 'lucide-vue-next'; 
import { useNotifications } from '@/composables/useNotifications';


// Configuration de la barre de navigation pour cette page
const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon }, 
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

const { showSuccess, showError } = useNotifications(); // Utilisation des fonctions de notification

// États réactifs pour les paramètres
const isDarkMode = ref(false);

// Fonction pour charger les paramètres (depuis le localStorage pour le MVP)
const loadSettings = () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    isDarkMode.value = true;
  } else {
    isDarkMode.value = false;
  }
};

// Fonction pour sauvegarder les paramètres (dans le localStorage pour le MVP)
const saveSettings = () => {
  try {
    if (isDarkMode.value) {
      localStorage.setItem('theme', 'dark');
    } else {
      localStorage.setItem('theme', 'light');
    }
    showSuccess('Paramètres sauvegardés !', 'Vos préférences ont été enregistrées avec succès.');
  } catch (e) {
    showError('Erreur de sauvegarde', 'Impossible d\'enregistrer les paramètres.');
    console.error('Erreur lors de la sauvegarde des paramètres:', e);
  }
};

// Appliquer la classe 'dark-mode' au html en fonction de isDarkMode
watch(isDarkMode, (newValue) => {
  if (newValue) {
    document.documentElement.classList.add('dark-mode');
  } else {
    document.documentElement.classList.remove('dark-mode');
  }
}, { immediate: true });

// Charger les paramètres au montage du composant
onMounted(() => {
  loadSettings();
});
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <TopBar
      :nav-items="navigationItems"
      variant="blur"
      position="sticky"
      :shrink-on-scroll="false"
      :show-actions="false"
    />

    <section class="settings-section container mx-auto p-space-4 flex-1 flex flex-col items-center justify-center">
      <h1 class="text-4xl md:text-5xl font-extrabold text-tertiary mb-space-10 text-center">
        Paramètres de l'Application
      </h1>

      <Screen title="Préférences Générales" class="w-full max-w-2xl mb-space-8">
        <div class="setting-item flex items-center justify-between p-space-4 border-b border-gray-200 last:border-b-0">
          <label for="darkModeToggle" class="text-lg font-medium text-gray-800 flex items-center gap-space-2">
            <component :is="isDarkMode ? MoonIcon : SunIcon" class="text-primary" />
            Mode Sombre
          </label>
          <label class="switch">
            <input type="checkbox" id="darkModeToggle" v-model="isDarkMode">
            <span class="slider round"></span>
          </label>
        </div>
      </Screen>

      <div class="flex justify-center w-full max-w-2xl">
        <GetStartedButton
          variant="primary"
          size="lg"
          @click="saveSettings"
          :left-icon="SaveIcon"
          text="Sauvegarder les paramètres"
          class="w-full md:w-auto"
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
.settings-section {
  padding-top: var(--space-16);
  padding-bottom: var(--space-16);
}

.setting-item {
  /* Styles pour chaque ligne de paramètre */
}

/* Styles pour le toggle switch (inspiré de CSS pur) */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--cl-gray-400);
  transition: .4s;
  transition: var(--transition-color);
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: var(--cl-white);
  transition: .4s;
  transition: var(--transition-color);
}

input:checked + .slider {
  background-color: var(--cl-primary);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--cl-primary);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .settings-section {
    padding-top: var(--space-12);
    padding-bottom: var(--space-12);
  }
}
</style>
