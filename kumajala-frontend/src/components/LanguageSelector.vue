<template>
  <div class="language-selector">
    <label v-if="label" :for="inputId" class="selector-label">
      {{ label }}
      <span v-if="required" class="required-indicator">*</span>
    </label>
    
    <div class="selector-wrapper" :class="{ 'is-disabled': disabled, 'has-error': hasError }">
      <select
        :id="inputId"
        :value="modelValue"
        @change="handleChange"
        :disabled="disabled"
        :required="required"
        class="language-select"
        :aria-describedby="hasError ? `${inputId}-error` : undefined"
      >
        <option value="" disabled>{{ placeholder }}</option>
        <optgroup 
          v-for="(groupLanguages, region) in groupedLanguages" 
          :key="region" 
          :label="region"
        >
          <option 
            v-for="language in groupLanguages" 
            :key="language.code" 
            :value="language.code"
            :disabled="language.disabled"
          >
            {{ language.name }}
            <span v-if="showRegion && language.region !== region"> ({{ language.region }})</span>
          </option>
        </optgroup>
        
        <!-- Fallback si pas de groupement -->
        <option 
          v-if="!groupByRegion"
          v-for="language in filteredLanguages" 
          :key="language.code" 
          :value="language.code"
          :disabled="language.disabled"
        >
          {{ language.name }}
          <span v-if="showRegion && language.region"> ({{ language.region }})</span>
        </option>
      </select>
      
      <!-- Icône de dropdown -->
      <div class="dropdown-icon">
        <ChevronDownIcon width="16" height="16" />
      </div>
    </div>
    
    <!-- Message d'erreur -->
    <div v-if="hasError" :id="`${inputId}-error`" class="error-message">
      {{ errorMessage }}
    </div>
    
    <!-- Informations sur la langue sélectionnée -->
    <div v-if="selectedLanguageInfo && showInfo" class="language-info">
      <div class="info-item">
        <span class="info-label">Région:</span>
        <span class="info-value">{{ selectedLanguageInfo.region }}</span>
      </div>
      <div v-if="selectedLanguageInfo.code_gtts" class="info-item">
        <span class="info-label">Code TTS:</span>
        <span class="info-value">{{ selectedLanguageInfo.code_gtts }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { ChevronDown as ChevronDownIcon } from 'lucide-vue-next';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  
  languages: {
    type: Array,
    required: true,
    default: () => []
  },
  
  label: {
    type: String,
    default: ''
  },
  
  placeholder: {
    type: String,
    default: 'Sélectionnez une langue'
  },
  
  disabled: {
    type: Boolean,
    default: false
  },
  
  required: {
    type: Boolean,
    default: false
  },
  
  groupByRegion: {
    type: Boolean,
    default: true
  },
  
  showRegion: {
    type: Boolean,
    default: false
  },
  
  showInfo: {
    type: Boolean,
    default: false
  },
  
  excludeLanguages: {
    type: Array,
    default: () => []
  },
  
  errorMessage: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

// ID unique pour l'accessibilité
const inputId = ref(`language-selector-${Math.random().toString(36).substr(2, 9)}`);

// Computed
const hasError = computed(() => !!props.errorMessage);

const filteredLanguages = computed(() => {
  return props.languages.filter(lang => 
    !props.excludeLanguages.includes(lang.code)
  );
});

const groupedLanguages = computed(() => {
  if (!props.groupByRegion) return {};
  
  return filteredLanguages.value.reduce((groups, language) => {
    const region = language.region || 'Autres';
    if (!groups[region]) {
      groups[region] = [];
    }
    groups[region].push(language);
    return groups;
  }, {});
});

const selectedLanguageInfo = computed(() => {
  return props.languages.find(lang => lang.code === props.modelValue) || null;
});

// Méthodes
const handleChange = (event) => {
  const value = event.target.value;
  emit('update:modelValue', value);
  emit('change', {
    value,
    language: selectedLanguageInfo.value
  });
};
</script>

<style scoped>
.language-selector {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.selector-label {
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
  color: var(--cl-gray-700);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.required-indicator {
  color: var(--cl-error);
  font-weight: var(--fw-bold);
}

.selector-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.language-select {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  padding-right: var(--space-10); /* Espace pour l'icône */
  border: 2px solid var(--cl-gray-300);
  border-radius: var(--radius-lg);
  background-color: var(--cl-white);
  font-size: var(--fs-base);
  font-family: var(--font-primary);
  color: var(--cl-gray-800);
  cursor: pointer;
  transition: var(--transition-color);
  appearance: none; /* Supprime le style par défaut */
}

.language-select:focus {
  outline: none;
  border-color: var(--cl-primary);
  box-shadow: 0 0 0 3px rgba(241, 137, 14, 0.1);
}

.language-select:disabled {
  background-color: var(--cl-gray-100);
  color: var(--cl-gray-500);
  cursor: not-allowed;
}

.selector-wrapper.is-disabled {
  opacity: 0.6;
}

.selector-wrapper.has-error .language-select {
  border-color: var(--cl-error);
}

.dropdown-icon {
  position: absolute;
  right: var(--space-3);
  pointer-events: none;
  color: var(--cl-gray-500);
  transition: var(--transition-color);
}

.selector-wrapper.is-disabled .dropdown-icon {
  color: var(--cl-gray-400);
}

.error-message {
  font-size: var(--fs-sm);
  color: var(--cl-error);
  font-weight: var(--fw-medium);
}

.language-info {
  padding: var(--space-3);
  background-color: var(--cl-gray-50);
  border-radius: var(--radius-md);
  border: 1px solid var(--cl-gray-200);
  font-size: var(--fs-sm);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-1);
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-label {
  font-weight: var(--fw-medium);
  color: var(--cl-gray-600);
}

.info-value {
  color: var(--cl-gray-800);
  font-weight: var(--fw-semibold);
}

/* Styles pour les optgroups */
.language-select optgroup {
  font-weight: var(--fw-semibold);
  color: var(--cl-primary);
  font-style: normal;
}

.language-select option {
  font-weight: var(--fw-normal);
  color: var(--cl-gray-800);
  padding: var(--space-2);
}

.language-select option:disabled {
  color: var(--cl-gray-400);
  font-style: italic;
}

/* Responsive */
@media (max-width: 768px) {
  .language-select {
    padding: var(--space-4);
    font-size: var(--fs-lg);
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-1);
  }
}

/* Mode sombre */
html.dark-mode .language-select {
  background-color: var(--cl-gray-50);
  border-color: var(--cl-gray-300);
  color: var(--cl-gray-800);
}

html.dark-mode .language-select:focus {
  border-color: var(--cl-primary);
  box-shadow: 0 0 0 3px rgba(255, 179, 71, 0.1);
}

html.dark-mode .language-info {
  background-color: var(--cl-gray-100);
  border-color: var(--cl-gray-300);
}
</style>