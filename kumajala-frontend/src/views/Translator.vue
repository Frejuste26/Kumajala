<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api/axiosConfig';
import TopBar from '@/components/topBar.vue';
import GetStartedButton from '@/components/getStartedButton.vue';
import SelectLang from '@/components/SelectLang.vue';
import Screen from '@/components/Screen.vue';
import { Volume2 as Volume2Icon, Send as SendIcon, RefreshCw as SwapIcon, Copy as CopyIcon } from 'lucide-vue-next'; // Import de CopyIcon
import { useNotifications } from '@/composables/useNotifications';
import { Home as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon } from 'lucide-vue-next'; // Import des nouvelles icônes

const { showSuccess, showError, showInfo, showWarning } = useNotifications(); // Utilisation des fonctions de notification

// États réactifs pour l'interface utilisateur
const inputText = ref('');
const translatedText = ref('');
const sourceLanguage = ref(''); // Nouvelle ref pour la langue source
const selectedLanguage = ref('');
const languages = ref([]);
const audioSrc = ref(null);
const isLoadingTranslate = ref(false);
const isLoadingSpeak = ref(false);
const source = ref('');
const processingTime = ref('');

// Configuration de la barre de navigation pour cette page
const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon },
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon }, // Utilisation de LanguagesIcon
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon } // Utilisation de SettingsIcon
];

// Fonction pour récupérer les langues supportées depuis le backend
const fetchLanguages = async () => {
  try {
    const response = await apiClient.get('/languages');
    languages.value = response.data.languages;
    if (languages.value.length > 0) {
      const frenchLang = languages.value.find(lang => lang.code === 'fr');
      sourceLanguage.value = frenchLang ? frenchLang.code : languages.value[0].code;

      // Initialise selectedLanguage avec la première langue locale différente du français
      const firstLocalLang = languages.value.find(lang => lang.code !== 'fr');
      selectedLanguage.value = firstLocalLang ? firstLocalLang.code : languages.value[0].code;
    }
  } catch (err) {
    console.error('Erreur lors de la récupération des langues:', err);
    showError('Erreur de chargement', err.response?.data?.error || 'Impossible de charger les langues.');
  }
};

// Fonction pour traduire le texte
const translate = async () => {
  isLoadingTranslate.value = true;
  audioSrc.value = null;

  if (!inputText.value.trim()) {
    showError('Texte manquant', 'Veuillez entrer un texte à traduire.');
    isLoadingTranslate.value = false;
    return;
  }
  if (!selectedLanguage.value) {
    showError('Langue cible manquante', 'Veuillez sélectionner une langue cible.');
    isLoadingTranslate.value = false;
    return;
  }

  // Vérification que la langue source est bien le français
  if (sourceLanguage.value !== 'fr') {
    translatedText.value = ''; // Clear previous translation
    showError('Source non supportée', 'La traduction est actuellement supportée uniquement du Français vers les langues locales.');
    isLoadingTranslate.value = false;
    return;
  }

  try {
    const response = await apiClient.post('/translate', {
      text: inputText.value,
      targetLanguage: selectedLanguage.value,
    });
    translatedText.value = response.data.translation;
    source.value = response.data.source;
    processingTime.value = response.data.processingTime;
    showSuccess('Traduction réussie !', `Texte traduit via ${source.value}.`);
  } catch (err) {
    console.error('Erreur lors de la traduction:', err);
    translatedText.value = '';
    source.value = '';
    processingTime.value = '';
    showError('Erreur de traduction', err.response?.data?.error || 'Une erreur est survenue lors de la traduction.');
  } finally {
    isLoadingTranslate.value = false;
  }
};

// Fonction pour lire l'audio du texte traduit
const speak = async () => {
  if (!translatedText.value) {
    showInfo('Aucun texte à lire', 'Veuillez traduire un texte d\'abord.');
    return;
  }
  isLoadingSpeak.value = true;
  audioSrc.value = null;

  try {
    const lang_meta = languages.value.find(lang => lang.code === selectedLanguage.value);
    const gtts_code = lang_meta ? (lang_meta.code_gtts || lang_meta.code) : 'fr';

    const response = await apiClient.post('/speak', {
      text: translatedText.value,
      languageCode: gtts_code
    });
    const audioBase64 = response.data.audioBase64;
    const contentType = response.data.contentType;
    audioSrc.value = `data:${contentType};base64,${audioBase64}`;

    const audio = new Audio(audioSrc.value);
    audio.play();
    showSuccess('Lecture audio', 'La traduction est en cours de lecture.');

  } catch (err) {
    console.error('Erreur lors de la lecture audio:', err);
    audioSrc.value = null;
    showError('Erreur audio', err.response?.data?.error || 'Impossible de générer l\'audio.');
  } finally {
    isLoadingSpeak.value = false;
  }
};

// Fonction pour échanger les langues source et cible
const swapLanguages = () => {
  const tempLang = sourceLanguage.value;
  sourceLanguage.value = selectedLanguage.value;
  selectedLanguage.value = tempLang;

  // Si la nouvelle langue source n'est pas le français, vider la traduction et afficher un avertissement
  if (sourceLanguage.value !== 'fr') {
    translatedText.value = '';
    showWarning('Source limitée', 'La traduction est actuellement supportée uniquement du Français vers les langues locales. Veuillez choisir le Français comme langue source.');
  } else {
    showInfo('Langues échangées', 'Les langues source et cible ont été échangées.');
  }
};

// Fonction pour copier le texte traduit
const copyTranslatedText = async () => {
  if (translatedText.value) {
    try {
      // Utilisation de document.execCommand('copy') pour la compatibilité iframe
      const textarea = document.createElement('textarea');
      textarea.value = translatedText.value;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      showSuccess('Copié !', 'Le texte traduit a été copié dans le presse-papiers.');
    } catch (err) {
      console.error('Erreur lors de la copie:', err);
      showError('Erreur de copie', 'Impossible de copier le texte.');
    }
  } else {
    showInfo('Rien à copier', 'Aucun texte traduit à copier.');
  }
};

onMounted(() => {
  fetchLanguages();
});
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <TopBar
      :nav-items="navigationItems"
      variant="default"
      position="relative"
      :shrink-on-scroll="false"
      :show-actions="false"
    />

    <section class="translator-section container mx-auto p-space-4 flex-1 flex flex-col items-center justify-center">
      <h1 class="text-4xl md:text-5xl font-extrabold text-tertiary mb-space-2">
        Kumajala <span class="text-primary">Translate</span>
      </h1>

      <div class="lang-select-container flex flex-col md:flex-row justify-center items-center gap-space-8 w-full max-w-2xl mb-space-8">
        <SelectLang
          label="Langue Source"
          v-model="sourceLanguage"
          :options="languages"
          class="flex-1 w-full md:w-auto"
        />

        <GetStartedButton
          variant="ghost"
          size="md"
          :left-icon="SwapIcon"
          text="Échanger"
          @click="swapLanguages"
          class="mt-space-4 md:mt-0"
        />

        <SelectLang
          label="Traduire vers:"
          v-model="selectedLanguage"
          :options="languages.filter(lang => lang.code !== sourceLanguage)"
          class="flex-1 w-full md:w-auto"
        />
      </div>

      <div class="screens-container flex flex-col md:flex-row gap-space-8 w-full max-w-4xl mb-space-8">
        <Screen :title="languages.find(l => l.code === sourceLanguage)?.name || 'Langue Source'">
          <textarea
            v-model="inputText"
            placeholder="Écrivez ici..."
            rows="8"
            class="w-full p-space-4 font-normal text-base border border-gray-300 rounded-lg resize-vertical bg-gray-50 focus:outline-none focus:border-primary transition"
          />
        </Screen>

        <Screen :title="languages.find(l => l.code === selectedLanguage)?.name || 'Langue Cible'">
          <div class="translated-result min-h-[180px] p-space-4 bg-gray-100 rounded-lg border border-gray-200 text-left font-normal text-base text-gray-700 whitespace-pre-line overflow-auto">
            <p v-if="translatedText">{{ translatedText }}</p>
            <p v-else class="placeholder text-tertiary opacity-70 italic">Le texte traduit s'affichera ici.</p>
          </div>
        </Screen>
      </div>

      <div class="flex flex-col md:flex-row gap-space-4 justify-center items-center w-full max-w-4xl">
        <GetStartedButton
          variant="primary"
          size="lg"
          :loading="isLoadingTranslate"
          :disabled="!inputText.trim() || sourceLanguage !== 'fr'"
          @click="translate"
          :left-icon="SendIcon"
          text="Traduire"
          class="w-full md:w-auto flex-1"
        />

        <GetStartedButton
          variant="secondary"
          size="lg"
          :loading="isLoadingSpeak"
          :disabled="!translatedText"
          @click="speak"
          :left-icon="Volume2Icon"
          text="Écouter la traduction"
          class="w-full md:w-auto flex-1"
        />

        <GetStartedButton
          variant="outline"
          size="lg"
          :disabled="!translatedText"
          @click="copyTranslatedText"
          :left-icon="CopyIcon"
          text="Copier"
          class="w-full md:w-auto flex-1"
        />
      </div>

      <div v-if="translatedText" class="text-sm text-gray-600 mt-space-4 flex flex-col md:flex-row gap-space-2 md:gap-space-8 justify-center w-full max-w-2xl">
        <span>Source: <span class="font-medium text-tertiary">{{ source }}</span></span>
        <span>Temps de traitement: <span class="font-medium text-tertiary">{{ processingTime }}</span></span>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Les styles spécifiques à cette page */
textarea:focus, select:focus {
  border-color: var(--cl-primary);
  box-shadow: 0 0 0 3px rgba(var(--cl-primary-rgb, 241, 137, 14), 0.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .translator-section {
    padding-top: var(--space-12);
    padding-bottom: var(--space-12);
  }
  .lang-select-container,
  .screens-container {
    flex-direction: column;
    gap: var(--space-4);
  }
  .lang-select-container > *,
  .screens-container > * {
    width: 100%;
  }
  .flex-col.md\:flex-row.gap-space-4 > .w-full.md\:w-auto.flex-1 {
    width: 100%; /* Ensure buttons stack on mobile */
  }
}
</style>
