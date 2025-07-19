<template>
  <div class="translate-container">
    <header class="header">
      <span class="logo">KUMANJALA Translate</span>
      <span class="settings-icon" @click="goToSettings"> ⚙️ </span>
    </header>

    <main class="content">
      <div class="translation-card">
        <div class="language-selection-bar">
          <button class="lang-button" @click="openLanguagePicker('from')">
            {{ fromLanguageDisplay }}
          </button>
          <button class="swap-lang-button" @click="swapLanguages">&#x21C6;</button>
          <button class="lang-button" @click="openLanguagePicker('to')">
            {{ toLanguageDisplay }}
          </button>
        </div>

        <div class="translation-areas-wrapper">
          <div class="input-section">
            <div class="textarea-wrapper">
              <textarea
                placeholder="Enter text"
                v-model="inputText"
                class="text-input"
                @input="autoTranslate"
              ></textarea>
              <div class="input-actions">
                <button class="action-btn" @click="useMicrophone" title="Voice input">🎤</button>
                <button class="action-btn" @click="useCamera" title="Camera input">📷</button>
              </div>
            </div>
          </div>

          <div class="output-section">
            <div class="textarea-wrapper">
              <textarea
                placeholder="Translation"
                v-model="translatedText"
                class="text-output"
                readonly
              ></textarea>
              <div class="output-actions">
                <button class="action-btn" @click="speakTranslatedText" title="Listen">🔊</button>
                <button class="action-btn" @click="copyTranslatedText" title="Copy">📋</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="footer-nav">
      <button class="nav-item active" @click="goToHome">
        <span class="nav-icon">🏠</span> Home
      </button>
      <button class="nav-item" @click="goToFavorites">
        <span class="nav-icon">🔖</span> Favorites
      </button>
      <button class="nav-item" @click="goToSettings">
        <span class="nav-icon">⚙️</span> Settings
      </button>
    </footer>

    <div v-if="showLanguagePicker" class="language-picker-modal">
      <div class="modal-content">
        <h3>Select Language</h3>
        <input
          type="text"
          v-model="searchLang"
          placeholder="Search language..."
          class="search-lang-input"
        />
        <div class="lang-list">
          <button
            v-for="lang in filteredLanguages"
            :key="lang.value"
            @click="selectLanguage(lang.value)"
            class="lang-option"
          >
            {{ lang.label }}
          </button>
        </div>
        <button class="close-modal-btn" @click="showLanguagePicker = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TranslatePage',
  data() {
    return {
      inputText: '',
      translatedText: '',
      fromLanguage: 'auto-detect',
      toLanguage: 'fr',
      pickerFor: null,
      showLanguagePicker: false,
      searchLang: '',
      allLanguages: [
        { label: 'Auto-detect', value: 'auto-detect' },
        { label: 'Yacouba', value: 'yacouba' },
        { label: 'Guérré', value: 'guerré' },
        { label: 'Agni', value: 'agni' },
        { label: 'Dida', value: 'dida' },
        { label: 'Français', value: 'fr' },
        { label: 'English', value: 'en' },
        { label: 'Espagnol', value: 'es' },
        { label: 'Allemand', value: 'de' },
      ],
      recent: [
        { text: 'Assè Man Djou', language: 'Guérré' },
        { text: 'Comment allez vous', language: 'Français' },
      ],
      translateTimeout: null, // Pour le debounce de la traduction
    }
  },
  computed: {
    fromLanguageDisplay() {
      const lang = this.allLanguages.find((l) => l.value === this.fromLanguage)
      return lang ? lang.label : 'Auto-detect'
    },
    toLanguageDisplay() {
      const lang = this.allLanguages.find((l) => l.value === this.toLanguage)
      return lang ? lang.label : 'Français'
    },
    filteredLanguages() {
      const searchTerm = this.searchLang.toLowerCase()
      return this.allLanguages.filter((lang) => lang.label.toLowerCase().includes(searchTerm))
    },
  },
  methods: {
    goToSettings() {
      console.log('Go to Settings')
      // this.$router.push('/settings');
    },
    openLanguagePicker(forWhich) {
      this.pickerFor = forWhich
      this.searchLang = '' // Reset search
      this.showLanguagePicker = true
    },
    selectLanguage(langValue) {
      if (this.pickerFor === 'from') {
        this.fromLanguage = langValue
      } else if (this.pickerFor === 'to') {
        this.toLanguage = langValue
      }
      this.showLanguagePicker = false
      this.autoTranslate() // Translate immediately after language selection
    },
    swapLanguages() {
      const tempFrom = this.fromLanguage
      this.fromLanguage = this.toLanguage
      this.toLanguage = tempFrom
      if (this.fromLanguage === 'auto-detect') {
        // Example fallback
        this.fromLanguage = 'en'
      }
      this.autoTranslate() // Re-translate after swap
    },
    autoTranslate() {
      clearTimeout(this.translateTimeout)
      this.translateTimeout = setTimeout(() => {
        if (this.inputText.length > 0) {
          this.translatedText = `[Traduction de "${this.inputText}" de ${this.fromLanguageDisplay} vers ${this.toLanguageDisplay}]`
          this.addRecentTranslation()
        } else {
          this.translatedText = ''
        }
      }, 500)
    },
    addRecentTranslation() {
      const currentText = this.inputText
      const currentLanguage = this.fromLanguageDisplay

      if (currentText && (!this.recent[0] || this.recent[0].text !== currentText)) {
        this.recent.unshift({
          text: currentText,
          language: currentLanguage,
        })
        if (this.recent.length > 5) {
          this.recent.pop()
        }
      }
    },
    useMicrophone() {
      alert('Microphone activated!')
      console.log('Use Microphone')
    },
    useCamera() {
      alert('Camera activated!')
      console.log('Use Camera')
    },
    speakTranslatedText() {
      if (this.translatedText) {
        alert(`Speaking: "${this.translatedText}"`)
        console.log('Speak translated text')
      }
    },
    copyTranslatedText() {
      if (this.translatedText) {
        navigator.clipboard
          .writeText(this.translatedText)
          .then(() => alert('Translation copied!'))
          .catch((err) => console.error('Failed to copy text: ', err))
      }
    },
    viewRecent(item) {
      console.log('Viewing recent item:', item)
      this.inputText = item.text
      this.autoTranslate()
    },
    goToHome() {
      console.log('Go to Home')
      this.$emit('go-to-onboarding')
    },
    goToFavorites() {
      console.log('Go to Favorites')
      // this.$router.push('/favorites');
    },
  },
  mounted() {
    this.autoTranslate()
  },
}
</script>

<style scoped>
/* Variables pour les couleurs inspirées de Google Translate */
:root {
  --google-blue: #4285f4;
  --google-blue-dark: #3367d6;
  --google-gray-light: #f5f5f5;
  --google-gray-medium: #dadce0;
  --google-text-dark: #202124;
  --google-text-light: #5f6368;
  --white: #ffffff;
  --shadow-color: rgba(0, 0, 0, 0.1);
  --border-radius-base: 8px;
  --padding-base: 16px;
}

.translate-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--google-gray-light);
  font-family: 'Google Sans', 'Roboto', Arial, sans-serif;
  color: var(--google-text-dark);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--padding-base);
  background-color: var(--white);
  box-shadow: 0 2px 4px var(--shadow-color);
  z-index: 100;
}

.logo {
  font-size: 1.5em;
  font-weight: bold;
  color: var(--google-blue);
}

.settings-icon {
  font-size: 1.4em;
  cursor: pointer;
  color: var(--google-text-light);
}

.content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--padding-base);
  overflow-y: auto;
}

.translation-card {
  background-color: var(--white);
  border-radius: var(--border-radius-base);
  box-shadow:
    0 1px 3px var(--shadow-color),
    0 1px 2px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 960px; /* Plus large pour la disposition horizontale */
  margin-bottom: var(--padding-base);
  display: flex; /* Utilise flex pour le layout interne */
  flex-direction: column; /* Par défaut en colonne pour mobile */
  overflow: hidden;
}

/* Bandeau des sélecteurs de langue */
.language-selection-bar {
  display: flex;
  border: black 1px solid; /* Bordure pour le bandeau */
  border-radius: 3px;
  justify-content: space-around; /* ou space-between */
  align-items: center;
  padding: 8px var(--padding-base);
  border-bottom: 1px solid var(--google-gray-light);
  background-color: var(--white);
}

.lang-button {
  background: none;
  border: none;
  font-size: 1em;
  font-weight: 500;
  color: var(--google-blue);
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
  flex-grow: 1; /* Permet aux boutons de langue de prendre de l'espace */
  text-align: center;
}
.lang-button:hover {
  background-color: rgba(66, 133, 244, 0.1);
}

.swap-lang-button {
  background: none;
  border: 1px solid var(--google-gray-medium);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2em;
  color: var(--google-text-light);
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    border-color 0.2s ease;
  margin: 0 10px; /* Espacement entre les boutons de langue */
  flex-shrink: 0; /* Ne pas réduire la taille */
}
.swap-lang-button:hover {
  background-color: var(--google-gray-light);
  border-color: var(--google-blue);
}

/* Wrapper pour les zones de texte */
.translation-areas-wrapper {
  display: flex; /* Utilise Flexbox pour les deux zones de texte */
  flex-direction: column; /* Par défaut en colonne pour mobile */
  flex-grow: 1;
}

.input-section,
.output-section {
  padding: var(--padding-base);
  flex-grow: 1; /* Permet aux sections de texte de prendre de l'espace */
  flex-basis: 50%; /* Essaye de leur donner une base de 50% sur desktop */
}
.input-section {
  border-bottom: 1px solid var(--google-gray-light); /* Séparateur pour mobile */
}
.output-section {
  border-bottom: none; /* Pas de bordure en bas de la dernière section */
}

.textarea-wrapper {
  position: relative;
  height: 180px; /* Hauteur plus grande pour les zones de texte */
}

.text-input,
.text-output {
  width: 100%;
  height: 100%; /* Prend toute la hauteur du wrapper */
  border: none;
  background: transparent;
  resize: none;
  font-size: 1.1em;
  color: var(--google-text-dark);
  outline: none;
  padding-right: 40px; /* Espace pour les icônes */
  box-sizing: border-box;
}

.text-output {
  color: var(--google-text-dark);
}

.input-actions,
.output-actions {
  position: absolute;
  right: 10px;
  bottom: 10px;
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: none;
  font-size: 1.3em;
  color: var(--google-text-light);
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}
.action-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* Footer / Navbar */
.footer-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  padding: 10px 0;
  background-color: var(--white);
  border-top: 1px solid var(--google-gray-light);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  position: sticky;
  bottom: 0;
  z-index: 90;
}

.nav-item {
  background: none;
  border: none;
  color: var(--google-text-light);
  font-size: 0.9em;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 8px;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}
.nav-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}
.nav-item.active {
  color: var(--google-blue);
  font-weight: bold;
}
.nav-icon {
  font-size: 1.5em;
}

/* Modals pour le sélecteur de langue */
.language-picker-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}

.modal-content {
  background-color: var(--white);
  padding: 25px;
  border-radius: var(--border-radius-base);
  box-shadow: 0 4px 8px var(--shadow-color);
  width: 90%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.modal-content h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: var(--google-text-dark);
}

.search-lang-input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid var(--google-gray-medium);
  border-radius: 5px;
  font-size: 1em;
  outline: none;
}
.search-lang-input:focus {
  border-color: var(--google-blue);
}

.lang-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.lang-option {
  background: none;
  border: none;
  padding: 10px 0;
  text-align: left;
  font-size: 1em;
  color: var(--google-text-dark);
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid var(--google-gray-light);
}
.lang-option:last-child {
  border-bottom: none;
}
.lang-option:hover {
  background-color: var(--google-gray-light);
}

.close-modal-btn {
  background-color: var(--google-blue);
  color: var(--white);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s ease;
  margin-top: 10px;
}
.close-modal-btn:hover {
  background-color: var(--google-blue-dark);
}

/* Media Queries pour le responsive design */

/* Par défaut, la disposition est verticale pour les petits écrans (mobile first) */

/* Disposition horizontale pour les tablettes et desktops (à partir de 768px de largeur) */
@media (min-width: 768px) {
  .translation-card {
    flex-direction: column; /* Garde la direction colonne pour la carte principale, pour que les barres restent empilées */
    height: 400px; /* Hauteur fixe pour la carte de traduction sur desktop */
  }

  /* Nouvelle zone pour les deux sections de texte côte à côte */
  .translation-areas-wrapper {
    flex-direction: row; /* Les sections d'entrée et de sortie côte à côte */
    flex-grow: 1; /* Permet à ce wrapper de prendre l'espace restant */
  }

  .input-section,
  .output-section {
    border-bottom: none; /* Pas de bordure en bas pour la disposition horizontale */
    border-right: 1px solid var(--google-gray-light); /* Bordure verticale entre les deux zones */
    height: 100%; /* Prend toute la hauteur disponible */
  }
  .output-section {
    border-right: none; /* Pas de bordure à droite pour la dernière section */
  }

  .textarea-wrapper {
    height: 100%; /* Prend toute la hauteur du parent */
  }
}

/* Ajustements pour les très grands écrans (facultatif) */
@media (min-width: 1024px) {
  .translation-card {
    max-width: 1000px;
    height: 450px; /* Encore plus de hauteur */
  }
}
</style>
