<script setup>
import { onMounted } from 'vue';
import TopBar from '@/components/topBar.vue';
import GetStartedButton from '@/components/getStartedButton.vue';
import SelectLang from '@/components/SelectLang.vue';
import { Volume2 as Volume2Icon, Send as SendIcon, RefreshCw as SwapIcon, Copy as CopyIcon, Download as DownloadIcon, Trash2 as ClearIcon, ArrowRightLeft as ArrowRightLeftIcon } from 'lucide-vue-next';
import { useTranslator } from '@/composables/useTranslator';
import { Home as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon } from 'lucide-vue-next';

const {
  inputText,
  translatedText,
  sourceLanguage,
  targetLanguage,
  languages,
  availableTargetLanguages,
  sourceLanguageInfo,
  targetLanguageInfo,
  isLoadingTranslate,
  isLoadingSpeak,
  isLoadingLanguages,
  translationSource,
  processingTime,
  canTranslate,
  canSpeak,
  loadLanguages,
  translate,
  speak,
  swapLanguages,
  copyTranslation,
  downloadAudio,
  clearAll
} = useTranslator();

const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon },
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

onMounted(() => {
  loadLanguages();
});
</script>

<template>
  <div class="translator-page min-h-screen flex flex-col">
    <TopBar
      :nav-items="navigationItems"
      variant="blur"
      position="sticky"
      :shrink-on-scroll="true"
      :show-actions="false"
    />

    <section class="translator-section">
      <div class="translator-container">
        <div class="header-section">
          <h1 class="page-title">
            <LanguagesIcon class="title-icon" />
            Traducteur <span class="highlight-text">Kumajala</span>
          </h1>
          <p class="page-subtitle">
            Traduisez du français vers les langues africaines locales en temps réel
          </p>
        </div>

        <div class="language-selector-card">
          <div class="language-selector-content">
            <div class="language-select-group">
              <SelectLang
                label="Langue Source"
                v-model="sourceLanguage"
                :options="languages"
                :disabled="isLoadingLanguages"
              />
            </div>

            <button
              class="swap-button"
              @click="swapLanguages"
              :disabled="isLoadingTranslate"
              aria-label="Échanger les langues"
            >
              <ArrowRightLeftIcon class="swap-icon" />
            </button>

            <div class="language-select-group">
              <SelectLang
                label="Langue Cible"
                v-model="targetLanguage"
                :options="availableTargetLanguages"
                :disabled="isLoadingLanguages"
              />
            </div>
          </div>
        </div>

        <div class="translation-workspace">
          <div class="translation-panel input-panel">
            <div class="panel-header">
              <h3 class="panel-title">{{ sourceLanguageInfo?.name || 'Français' }}</h3>
              <GetStartedButton
                variant="ghost"
                size="sm"
                :left-icon="ClearIcon"
                text="Effacer"
                @click="clearAll"
                :disabled="!inputText && !translatedText"
              />
            </div>
            <div class="panel-body">
              <textarea
                v-model="inputText"
                placeholder="Entrez votre texte ici..."
                class="translation-textarea"
                :disabled="isLoadingTranslate"
              />
              <div class="character-count" v-if="inputText">
                {{ inputText.length }} caractères
              </div>
            </div>
          </div>

          <div class="translation-panel output-panel">
            <div class="panel-header">
              <h3 class="panel-title">{{ targetLanguageInfo?.name || 'Langue Cible' }}</h3>
              <div class="panel-actions">
                <button
                  class="icon-button"
                  @click="copyTranslation"
                  :disabled="!translatedText"
                  title="Copier"
                >
                  <CopyIcon width="18" height="18" />
                </button>
                <button
                  class="icon-button"
                  @click="downloadAudio"
                  :disabled="!translatedText"
                  title="Télécharger audio"
                >
                  <DownloadIcon width="18" height="18" />
                </button>
              </div>
            </div>
            <div class="panel-body">
              <div class="translation-result">
                <div v-if="translatedText" class="result-text">
                  {{ translatedText }}
                </div>
                <div v-else-if="isLoadingTranslate" class="result-placeholder loading">
                  <div class="loading-spinner"></div>
                  <p>Traduction en cours...</p>
                </div>
                <div v-else class="result-placeholder">
                  <LanguagesIcon width="48" height="48" class="placeholder-icon" />
                  <p>La traduction s'affichera ici</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="action-section">
          <div class="action-buttons">
            <GetStartedButton
              variant="primary"
              size="lg"
              :loading="isLoadingTranslate"
              :disabled="!canTranslate"
              @click="translate"
              :left-icon="SendIcon"
              text="Traduire"
              class="primary-action"
            />

            <GetStartedButton
              variant="secondary"
              size="lg"
              :loading="isLoadingSpeak"
              :disabled="!canSpeak"
              @click="speak"
              :left-icon="Volume2Icon"
              text="Écouter"
              class="secondary-action"
            />
          </div>

          <div v-if="translatedText && translationSource" class="translation-meta">
            <span class="meta-item">
              <span class="meta-label">Source:</span>
              <span class="meta-value">{{ translationSource }}</span>
            </span>
            <span class="meta-separator">•</span>
            <span class="meta-item">
              <span class="meta-label">Temps:</span>
              <span class="meta-value">{{ processingTime }}</span>
            </span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.translator-page {
  background: linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%);
  transition: var(--transition-color);
}

.translator-section {
  padding: var(--space-12) var(--space-6);
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
}

.translator-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  text-align: center;
  margin-bottom: var(--space-10);
  animation: fadeInDown 0.6s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-title {
  font-size: var(--fs-4xl);
  font-weight: var(--fw-extrabold);
  color: var(--cl-tertiary);
  margin-bottom: var(--space-3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  transition: var(--transition-color);
}

.title-icon {
  width: 40px;
  height: 40px;
  color: var(--cl-primary);
}

.highlight-text {
  background: linear-gradient(135deg, var(--cl-primary), var(--cl-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: var(--fs-lg);
  color: var(--cl-gray-600);
  font-weight: var(--fw-normal);
  transition: var(--transition-color);
}

.language-selector-card {
  background: var(--cl-white);
  border-radius: var(--radius-2xl);
  padding: var(--space-8);
  box-shadow: var(--shadow-lg);
  margin-bottom: var(--space-8);
  animation: fadeInUp 0.6s ease-out 0.2s both;
  transition: var(--transition-color);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.language-selector-content {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: var(--space-6);
  align-items: end;
}

.language-select-group {
  flex: 1;
}

.swap-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, var(--cl-primary), var(--cl-secondary));
  border: none;
  border-radius: var(--radius-full);
  color: var(--cl-white);
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-md);
  margin-bottom: var(--space-1);
}

.swap-button:hover:not(:disabled) {
  transform: scale(1.1) rotate(180deg);
  box-shadow: var(--shadow-lg);
}

.swap-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.swap-icon {
  width: 24px;
  height: 24px;
  transition: transform var(--transition-base);
}

.translation-workspace {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
  margin-bottom: var(--space-8);
  animation: fadeInUp 0.6s ease-out 0.4s both;
}

.translation-panel {
  background: var(--cl-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  transition: all var(--transition-base);
}

.translation-panel:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-5);
  background: linear-gradient(135deg, var(--cl-gray-50), var(--cl-gray-100));
  border-bottom: 2px solid var(--cl-gray-200);
  transition: var(--transition-color);
}

.panel-title {
  font-size: var(--fs-lg);
  font-weight: var(--fw-semibold);
  color: var(--cl-tertiary);
  transition: var(--transition-color);
}

.panel-actions {
  display: flex;
  gap: var(--space-2);
}

.icon-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: transparent;
  border: 1px solid var(--cl-gray-300);
  border-radius: var(--radius-lg);
  color: var(--cl-gray-600);
  cursor: pointer;
  transition: all var(--transition-base);
}

.icon-button:hover:not(:disabled) {
  background: var(--cl-primary);
  color: var(--cl-white);
  border-color: var(--cl-primary);
  transform: scale(1.05);
}

.icon-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.panel-body {
  padding: var(--space-6);
  position: relative;
}

.translation-textarea {
  width: 100%;
  min-height: 300px;
  padding: var(--space-4);
  border: 2px solid var(--cl-gray-200);
  border-radius: var(--radius-lg);
  background: var(--cl-gray-50);
  font-size: var(--fs-base);
  font-family: var(--font-primary);
  color: var(--cl-gray-800);
  resize: vertical;
  transition: all var(--transition-base);
  line-height: 1.6;
}

.translation-textarea:focus {
  outline: none;
  border-color: var(--cl-primary);
  background: var(--cl-white);
  box-shadow: 0 0 0 4px rgba(241, 137, 14, 0.1);
}

.translation-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.character-count {
  position: absolute;
  bottom: var(--space-2);
  right: var(--space-3);
  font-size: var(--fs-xs);
  color: var(--cl-gray-500);
  background: var(--cl-white);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.translation-result {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-text {
  padding: var(--space-4);
  font-size: var(--fs-lg);
  line-height: 1.8;
  color: var(--cl-gray-800);
  background: linear-gradient(135deg, rgba(241, 137, 14, 0.05), rgba(227, 170, 27, 0.05));
  border-radius: var(--radius-lg);
  border: 2px solid var(--cl-primary);
  font-weight: var(--fw-medium);
  transition: var(--transition-color);
  white-space: pre-line;
}

.result-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  color: var(--cl-gray-400);
  text-align: center;
}

.placeholder-icon {
  opacity: 0.3;
}

.result-placeholder.loading {
  gap: var(--space-4);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--cl-gray-200);
  border-top-color: var(--cl-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.action-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-6);
  animation: fadeInUp 0.6s ease-out 0.6s both;
}

.action-buttons {
  display: flex;
  gap: var(--space-4);
  width: 100%;
  max-width: 600px;
}

.primary-action,
.secondary-action {
  flex: 1;
}

.translation-meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--fs-sm);
  color: var(--cl-gray-600);
  background: var(--cl-white);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-color);
}

.meta-item {
  display: flex;
  gap: var(--space-2);
}

.meta-label {
  font-weight: var(--fw-medium);
  color: var(--cl-gray-500);
}

.meta-value {
  font-weight: var(--fw-semibold);
  color: var(--cl-primary);
}

.meta-separator {
  color: var(--cl-gray-400);
}

@media (max-width: 1024px) {
  .translator-section {
    padding: var(--space-8) var(--space-4);
  }

  .page-title {
    font-size: var(--fs-3xl);
  }

  .title-icon {
    width: 32px;
    height: 32px;
  }

  .translation-workspace {
    gap: var(--space-4);
  }
}

@media (max-width: 768px) {
  .translator-section {
    padding: var(--space-6) var(--space-3);
    min-height: auto;
  }

  .page-title {
    font-size: var(--fs-2xl);
    flex-direction: column;
    gap: var(--space-2);
  }

  .title-icon {
    width: 28px;
    height: 28px;
  }

  .page-subtitle {
    font-size: var(--fs-base);
  }

  .language-selector-card {
    padding: var(--space-6);
  }

  .language-selector-content {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }

  .swap-button {
    width: 48px;
    height: 48px;
    margin: 0 auto;
    transform: rotate(90deg);
  }

  .swap-button:hover:not(:disabled) {
    transform: rotate(90deg) scale(1.1);
  }

  .translation-workspace {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }

  .translation-textarea {
    min-height: 200px;
  }

  .translation-result {
    min-height: 200px;
  }

  .panel-header {
    padding: var(--space-4);
  }

  .panel-body {
    padding: var(--space-4);
  }

  .action-buttons {
    flex-direction: column;
  }

  .translation-meta {
    flex-direction: column;
    gap: var(--space-2);
    text-align: center;
  }

  .meta-separator {
    display: none;
  }
}

html.dark-mode .translator-page {
  background: linear-gradient(135deg, var(--cl-gray-900) 0%, var(--cl-gray-800) 100%);
}

html.dark-mode .language-selector-card,
html.dark-mode .translation-panel,
html.dark-mode .translation-meta {
  background: var(--cl-gray-100);
  border: 1px solid var(--cl-gray-200);
}

html.dark-mode .panel-header {
  background: linear-gradient(135deg, var(--cl-gray-50), var(--cl-gray-100));
  border-bottom-color: var(--cl-gray-300);
}

html.dark-mode .translation-textarea {
  background: var(--cl-gray-50);
  border-color: var(--cl-gray-300);
  color: var(--cl-gray-800);
}

html.dark-mode .translation-textarea:focus {
  background: var(--cl-gray-100);
  border-color: var(--cl-primary);
}

html.dark-mode .result-text {
  background: linear-gradient(135deg, rgba(255, 179, 71, 0.1), rgba(255, 215, 0, 0.1));
  color: var(--cl-gray-800);
}

html.dark-mode .character-count {
  background: var(--cl-gray-100);
  color: var(--cl-gray-600);
}

html.dark-mode .icon-button {
  border-color: var(--cl-gray-400);
  color: var(--cl-gray-700);
}

html.dark-mode .icon-button:hover:not(:disabled) {
  background: var(--cl-primary);
  color: var(--cl-white);
}
</style>
