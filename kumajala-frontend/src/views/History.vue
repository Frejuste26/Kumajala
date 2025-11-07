<script setup>
import { ref, onMounted, computed } from 'vue';
import TopBar from '@/components/topBar.vue';
import GetStartedButton from '@/components/getStartedButton.vue';
import { History as HistoryIcon, Search as SearchIcon, ListFilter as FilterIcon, Download as DownloadIcon, Trash2 as DeleteIcon, Volume2 as SpeakIcon, Copy as CopyIcon, Calendar as CalendarIcon } from 'lucide-vue-next';
import { Hop as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon } from 'lucide-vue-next';
import { useNotifications } from '@/composables/useNotifications';
import { speechService } from '@/api/speack';

const { showSuccess, showError, showInfo } = useNotifications();

// Configuration de la navigation
const navigationItems = [
  { name: 'Accueil', path: '/', icon: HomeIcon },
  { name: 'À Propos', path: '/about', icon: InfoIcon },
  { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
  { name: 'Historique', path: '/history', icon: HistoryIcon },
  { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

// États réactifs
const translations = ref([]);
const searchQuery = ref('');
const selectedLanguage = ref('');
const sortBy = ref('date'); // 'date', 'source', 'target'
const sortOrder = ref('desc'); // 'asc', 'desc'
const isLoading = ref(false);
const selectedTranslations = ref(new Set());

// Computed
const filteredTranslations = computed(() => {
  let filtered = translations.value;

  // Filtrage par recherche
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(t => 
      t.originalText.toLowerCase().includes(query) ||
      t.translatedText.toLowerCase().includes(query) ||
      t.targetLanguage.toLowerCase().includes(query)
    );
  }

  // Filtrage par langue
  if (selectedLanguage.value) {
    filtered = filtered.filter(t => t.targetLanguage === selectedLanguage.value);
  }

  // Tri
  filtered.sort((a, b) => {
    let aValue, bValue;
    
    switch (sortBy.value) {
      case 'date':
        aValue = new Date(a.timestamp);
        bValue = new Date(b.timestamp);
        break;
      case 'source':
        aValue = a.originalText.toLowerCase();
        bValue = b.originalText.toLowerCase();
        break;
      case 'target':
        aValue = a.translatedText.toLowerCase();
        bValue = b.translatedText.toLowerCase();
        break;
      default:
        return 0;
    }

    if (sortOrder.value === 'asc') {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  return filtered;
});

const availableLanguages = computed(() => {
  const languages = [...new Set(translations.value.map(t => t.targetLanguage))];
  return languages.sort();
});

const hasSelections = computed(() => selectedTranslations.value.size > 0);

// Méthodes
const loadHistory = () => {
  isLoading.value = true;
  try {
    // Charger depuis localStorage pour le MVP
    const saved = localStorage.getItem('kumajala-history');
    if (saved) {
      translations.value = JSON.parse(saved);
    }
    showInfo('Historique chargé', `${translations.value.length} traductions trouvées`);
  } catch (error) {
    showError('Erreur de chargement', 'Impossible de charger l\'historique');
    console.error('Erreur lors du chargement de l\'historique:', error);
  } finally {
    isLoading.value = false;
  }
};

const saveToHistory = (originalText, translatedText, targetLanguage, source) => {
  const translation = {
    id: Date.now().toString(),
    originalText,
    translatedText,
    targetLanguage,
    source,
    timestamp: new Date().toISOString()
  };

  translations.value.unshift(translation);
  
  // Limiter à 100 traductions
  if (translations.value.length > 100) {
    translations.value = translations.value.slice(0, 100);
  }

  // Sauvegarder dans localStorage
  try {
    localStorage.setItem('kumajala-history', JSON.stringify(translations.value));
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error);
  }
};

const deleteTranslation = (id) => {
  translations.value = translations.value.filter(t => t.id !== id);
  selectedTranslations.value.delete(id);
  
  try {
    localStorage.setItem('kumajala-history', JSON.stringify(translations.value));
    showSuccess('Supprimé', 'Traduction supprimée de l\'historique');
  } catch (error) {
    showError('Erreur', 'Impossible de supprimer la traduction');
  }
};

const deleteSelected = () => {
  const count = selectedTranslations.value.size;
  translations.value = translations.value.filter(t => !selectedTranslations.value.has(t.id));
  selectedTranslations.value.clear();
  
  try {
    localStorage.setItem('kumajala-history', JSON.stringify(translations.value));
    showSuccess('Supprimé', `${count} traductions supprimées`);
  } catch (error) {
    showError('Erreur', 'Impossible de supprimer les traductions');
  }
};

const clearHistory = () => {
  if (confirm('Êtes-vous sûr de vouloir effacer tout l\'historique ?')) {
    translations.value = [];
    selectedTranslations.value.clear();
    localStorage.removeItem('kumajala-history');
    showSuccess('Historique effacé', 'Toutes les traductions ont été supprimées');
  }
};

const copyText = async (text) => {
  try {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showSuccess('Copié', 'Texte copié dans le presse-papiers');
  } catch (error) {
    showError('Erreur', 'Impossible de copier le texte');
  }
};

const speakText = async (text, language) => {
  try {
    const response = await speechService.synthesizeSpeech(text, language);
    await speechService.playAudio(response.audioBase64, response.contentType);
    showSuccess('Lecture', 'Texte en cours de lecture');
  } catch (error) {
    showError('Erreur audio', 'Impossible de lire le texte');
  }
};

const exportHistory = () => {
  try {
    const dataStr = JSON.stringify(translations.value, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `kumajala-history-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showSuccess('Export réussi', 'Historique exporté avec succès');
  } catch (error) {
    showError('Erreur d\'export', 'Impossible d\'exporter l\'historique');
  }
};

const toggleSelection = (id) => {
  if (selectedTranslations.value.has(id)) {
    selectedTranslations.value.delete(id);
  } else {
    selectedTranslations.value.add(id);
  }
};

const selectAll = () => {
  if (selectedTranslations.value.size === filteredTranslations.value.length) {
    selectedTranslations.value.clear();
  } else {
    filteredTranslations.value.forEach(t => selectedTranslations.value.add(t.id));
  }
};

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString('fr-FR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Exposer la fonction pour l'utiliser depuis d'autres composants
window.kumajalaAddToHistory = saveToHistory;

onMounted(() => {
  loadHistory();
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

    <section class="history-section container mx-auto p-space-4 flex-1">
      <div class="header-section mb-space-8">
        <h1 class="text-4xl md:text-5xl font-extrabold text-tertiary mb-space-4">
          <HistoryIcon class="inline-block mr-space-3" width="48" height="48" />
          Historique des traductions
        </h1>
        
        <!-- Barre de recherche et filtres -->
        <div class="filters-section bg-white rounded-lg p-space-6 shadow-sm">
          <div class="flex flex-col md:flex-row gap-space-4 mb-space-4">
            <!-- Recherche -->
            <div class="flex-1 relative">
              <SearchIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" width="20" height="20" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Rechercher dans les traductions..."
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-primary"
              />
            </div>
            
            <!-- Filtre par langue -->
            <select
              v-model="selectedLanguage"
              class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-primary"
            >
              <option value="">Toutes les langues</option>
              <option v-for="lang in availableLanguages" :key="lang" :value="lang">
                {{ lang }}
              </option>
            </select>
            
            <!-- Tri -->
            <select
              v-model="sortBy"
              class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-primary"
            >
              <option value="date">Trier par date</option>
              <option value="source">Trier par texte source</option>
              <option value="target">Trier par traduction</option>
            </select>
            
            <button
              @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
              class="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:border-primary"
              :title="sortOrder === 'asc' ? 'Croissant' : 'Décroissant'"
            >
              {{ sortOrder === 'asc' ? '↑' : '↓' }}
            </button>
          </div>
          
          <!-- Actions -->
          <div class="flex flex-wrap gap-space-3">
            <GetStartedButton
              variant="outline"
              size="sm"
              @click="selectAll"
              text="Tout sélectionner"
            />
            
            <GetStartedButton
              variant="outline"
              size="sm"
              :left-icon="DownloadIcon"
              @click="exportHistory"
              text="Exporter"
              :disabled="translations.length === 0"
            />
            
            <GetStartedButton
              variant="danger"
              size="sm"
              :left-icon="DeleteIcon"
              @click="deleteSelected"
              text="Supprimer sélection"
              :disabled="!hasSelections"
            />
            
            <GetStartedButton
              variant="danger"
              size="sm"
              @click="clearHistory"
              text="Tout effacer"
              :disabled="translations.length === 0"
            />
          </div>
        </div>
      </div>

      <!-- Liste des traductions -->
      <div class="translations-list">
        <div v-if="isLoading" class="text-center py-space-12">
          <p class="text-gray-500">Chargement de l'historique...</p>
        </div>
        
        <div v-else-if="filteredTranslations.length === 0" class="text-center py-space-12">
          <HistoryIcon class="mx-auto mb-space-4 text-gray-400" width="64" height="64" />
          <p class="text-gray-500 text-lg">
            {{ translations.length === 0 ? 'Aucune traduction dans l\'historique' : 'Aucun résultat pour cette recherche' }}
          </p>
        </div>
        
        <div v-else class="space-y-space-4">
          <div
            v-for="translation in filteredTranslations"
            :key="translation.id"
            class="translation-card bg-white rounded-lg p-space-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
          >
            <div class="flex items-start gap-space-4">
              <!-- Checkbox de sélection -->
              <input
                type="checkbox"
                :checked="selectedTranslations.has(translation.id)"
                @change="toggleSelection(translation.id)"
                class="mt-1 w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary"
              />
              
              <!-- Contenu principal -->
              <div class="flex-1">
                <div class="flex flex-col md:flex-row md:items-start gap-space-4">
                  <!-- Texte source -->
                  <div class="flex-1">
                    <h3 class="font-semibold text-gray-800 mb-space-2">Français</h3>
                    <p class="text-gray-700 bg-gray-50 p-space-3 rounded-md">
                      {{ translation.originalText }}
                    </p>
                  </div>
                  
                  <!-- Flèche -->
                  <div class="flex-shrink-0 text-primary text-2xl font-bold">
                    →
                  </div>
                  
                  <!-- Texte traduit -->
                  <div class="flex-1">
                    <h3 class="font-semibold text-gray-800 mb-space-2">{{ translation.targetLanguage }}</h3>
                    <p class="text-gray-700 bg-primary/5 p-space-3 rounded-md">
                      {{ translation.translatedText }}
                    </p>
                  </div>
                </div>
                
                <!-- Métadonnées -->
                <div class="flex flex-wrap items-center gap-space-4 mt-space-4 text-sm text-gray-500">
                  <span class="flex items-center gap-space-1">
                    <CalendarIcon width="14" height="14" />
                    {{ formatDate(translation.timestamp) }}
                  </span>
                  <span class="px-2 py-1 bg-gray-100 rounded-full">
                    Source: {{ translation.source }}
                  </span>
                </div>
              </div>
              
              <!-- Actions -->
              <div class="flex flex-col gap-space-2">
                <button
                  @click="copyText(translation.translatedText)"
                  class="p-2 text-gray-500 hover:text-primary hover:bg-primary/10 rounded-md transition-colors"
                  title="Copier la traduction"
                >
                  <CopyIcon width="16" height="16" />
                </button>
                
                <button
                  @click="speakText(translation.translatedText, translation.targetLanguage)"
                  class="p-2 text-gray-500 hover:text-primary hover:bg-primary/10 rounded-md transition-colors"
                  title="Écouter la traduction"
                >
                  <SpeakIcon width="16" height="16" />
                </button>
                
                <button
                  @click="deleteTranslation(translation.id)"
                  class="p-2 text-gray-500 hover:text-error hover:bg-error/10 rounded-md transition-colors"
                  title="Supprimer"
                >
                  <DeleteIcon width="16" height="16" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.translation-card {
  transition: all var(--transition-base);
}

.translation-card:hover {
  transform: translateY(-1px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .history-section {
    padding: var(--space-4) var(--space-3);
  }
  
  .filters-section {
    padding: var(--space-4);
  }
  
  .translation-card {
    padding: var(--space-4);
  }
  
  .flex.flex-col.md\\:flex-row.md\\:items-start.gap-space-4 {
    flex-direction: column;
  }
  
  .flex-shrink-0.text-primary.text-2xl.font-bold {
    transform: rotate(90deg);
    align-self: center;
  }
}
</style>