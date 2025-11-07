import { ref, computed } from 'vue';
import { translateService } from '@/api/translate';
import { speechService } from '@/api/speack';
import { languagesService } from '@/api/languages';
import { useNotifications } from './useNotifications';

/**
 * Composable pour gérer les fonctionnalités de traduction
 */
export function useTranslator() {
  const { showSuccess, showError, showInfo, showWarning } = useNotifications();

  // États réactifs
  const inputText = ref('');
  const translatedText = ref('');
  const sourceLanguage = ref('fr');
  const targetLanguage = ref('');
  const languages = ref([]);
  const isLoadingTranslate = ref(false);
  const isLoadingSpeak = ref(false);
  const isLoadingLanguages = ref(false);
  const translationSource = ref('');
  const processingTime = ref('');
  const audioData = ref(null);

  // Computed
  const availableTargetLanguages = computed(() => 
    languages.value.filter(lang => lang.code !== sourceLanguage.value)
  );

  const sourceLanguageInfo = computed(() => 
    languagesService.findByCode(languages.value, sourceLanguage.value)
  );

  const targetLanguageInfo = computed(() => 
    languagesService.findByCode(languages.value, targetLanguage.value)
  );

  const canTranslate = computed(() => 
    inputText.value.trim() && 
    targetLanguage.value && 
    sourceLanguage.value === 'fr' && 
    !isLoadingTranslate.value
  );

  const canSpeak = computed(() => 
    translatedText.value && 
    !isLoadingSpeak.value
  );

  // Méthodes
  const loadLanguages = async () => {
    isLoadingLanguages.value = true;
    try {
      const response = await languagesService.getSupportedLanguages();
      languages.value = response.languages;
      
      // Initialiser les langues par défaut
      if (languages.value.length > 0) {
        const firstLocalLang = languages.value.find(lang => lang.code !== 'fr');
        if (firstLocalLang && !targetLanguage.value) {
          targetLanguage.value = firstLocalLang.code;
        }
      }
      
      showSuccess('Langues chargées', `${languages.value.length} langues disponibles`);
    } catch (error) {
      showError('Erreur de chargement', 'Impossible de charger les langues supportées');
      console.error('Erreur lors du chargement des langues:', error);
    } finally {
      isLoadingLanguages.value = false;
    }
  };

  const translate = async () => {
    if (!canTranslate.value) {
      showWarning('Traduction impossible', 'Vérifiez le texte et la langue cible');
      return;
    }

    isLoadingTranslate.value = true;
    translatedText.value = '';
    translationSource.value = '';
    processingTime.value = '';
    audioData.value = null;

    try {
      const response = await translateService.translateText(inputText.value, targetLanguage.value);
      
      translatedText.value = response.translation;
      translationSource.value = response.source;
      processingTime.value = response.processingTime;
      
      showSuccess('Traduction réussie', `Traduit via ${response.source}`);
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Erreur lors de la traduction';
      showError('Erreur de traduction', errorMessage);
      console.error('Erreur de traduction:', error);
    } finally {
      isLoadingTranslate.value = false;
    }
  };

  const speak = async () => {
    if (!canSpeak.value) {
      showInfo('Aucun texte à lire', 'Traduisez d\'abord un texte');
      return;
    }

    isLoadingSpeak.value = true;

    try {
      const langInfo = targetLanguageInfo.value;
      const ttsCode = langInfo?.code_gtts || langInfo?.code || 'fr';
      
      const response = await speechService.synthesizeSpeech(translatedText.value, ttsCode);
      
      audioData.value = {
        base64: response.audioBase64,
        contentType: response.contentType
      };

      await speechService.playAudio(response.audioBase64, response.contentType);
      showSuccess('Lecture audio', 'La traduction est en cours de lecture');
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Erreur lors de la synthèse vocale';
      showError('Erreur audio', errorMessage);
      console.error('Erreur de synthèse vocale:', error);
    } finally {
      isLoadingSpeak.value = false;
    }
  };

  const swapLanguages = () => {
    const temp = sourceLanguage.value;
    sourceLanguage.value = targetLanguage.value;
    targetLanguage.value = temp;

    // Vider la traduction si la nouvelle source n'est pas le français
    if (sourceLanguage.value !== 'fr') {
      translatedText.value = '';
      showWarning('Source limitée', 'Seul le français est supporté comme langue source');
    } else {
      showInfo('Langues échangées', 'Les langues ont été inversées');
    }
  };

  const copyTranslation = async () => {
    if (!translatedText.value) {
      showInfo('Rien à copier', 'Aucun texte traduit disponible');
      return;
    }

    try {
      // Méthode compatible avec les iframes
      const textarea = document.createElement('textarea');
      textarea.value = translatedText.value;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      
      showSuccess('Copié !', 'Texte copié dans le presse-papiers');
    } catch (error) {
      showError('Erreur de copie', 'Impossible de copier le texte');
      console.error('Erreur de copie:', error);
    }
  };

  const downloadAudio = () => {
    if (!audioData.value) {
      showInfo('Aucun audio', 'Générez d\'abord l\'audio de la traduction');
      return;
    }

    try {
      const filename = `kumajala-${targetLanguage.value}-${Date.now()}.mp3`;
      speechService.downloadAudio(audioData.value.base64, filename, audioData.value.contentType);
      showSuccess('Téléchargement', 'Audio téléchargé avec succès');
    } catch (error) {
      showError('Erreur de téléchargement', 'Impossible de télécharger l\'audio');
      console.error('Erreur de téléchargement:', error);
    }
  };

  const clearAll = () => {
    inputText.value = '';
    translatedText.value = '';
    translationSource.value = '';
    processingTime.value = '';
    audioData.value = null;
    showInfo('Effacé', 'Tous les champs ont été vidés');
  };

  return {
    // États
    inputText,
    translatedText,
    sourceLanguage,
    targetLanguage,
    languages,
    isLoadingTranslate,
    isLoadingSpeak,
    isLoadingLanguages,
    translationSource,
    processingTime,
    audioData,

    // Computed
    availableTargetLanguages,
    sourceLanguageInfo,
    targetLanguageInfo,
    canTranslate,
    canSpeak,

    // Méthodes
    loadLanguages,
    translate,
    speak,
    swapLanguages,
    copyTranslation,
    downloadAudio,
    clearAll
  };
}