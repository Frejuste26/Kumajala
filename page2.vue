<template>
  <div class="translate-container">
    <header class="header">
      <span class="logo"><img src="@/assets/KUMAJALA-IMAGE.jpg" /></span>
      <span class="settings-icon" @click="goToSettings"
        ><img src="@/assets/KUMAJALA-ICON.jpg" /> <i class="fas fa-cog"></i>
      </span>
    </header>

    <main class="content">
      <div class="translation-card">
        <div class="language-selector-header">
          <div class="lang-selector-group lang-selector-from">
            <button
              class="lang-option-button"
              :class="{ 'active-lang': fromLanguage === 'auto-detect' }"
              @click="selectLanguage('from', 'auto-detect')"
            >
              Auto-detect
            </button>
            <button
              class="lang-option-button"
              :class="{ 'active-lang': fromLanguage !== 'auto-detect' }"
              @click="openLanguagePicker('from')"
            >
              {{ fromLanguageDisplayShort }}
            </button>
          </div>

          <button class="swap-lang-button" @click="swapLanguages">
            <i class="fas fa-exchange-alt"></i>
          </button>

          <div class="lang-selector-group lang-selector-to">
            <button class="lang-option-button active-lang" @click="openLanguagePicker('to')">
              {{ toLanguageDisplayShort }}
            </button>
          </div>
        </div>

        <div class="translation-areas-wrapper">
          <div class="input-section">
            <div class="textarea-container">
              <textarea
                placeholder="Enter text"
                v-model="inputText"
                class="text-input"
                @input="autoTranslate"
              ></textarea>
              <div class="input-actions">
                <button class="action-btn" @click="useMicrophone" title="Voice input">
                  <i class="fas fa-microphone"></i>
                </button>
                <button class="action-btn" @click="useCamera" title="Camera input">
                  <i class="fas fa-camera"></i>
                </button>
              </div>
            </div>
          </div>

          <div class="output-section">
            <div class="textarea-container">
              <textarea
                placeholder="Translation"
                v-model="translatedText"
                class="text-output"
                readonly
              ></textarea>
              <div class="output-actions">
                <button class="action-btn" @click="speakTranslatedText" title="Listen">
                  <i class="fas fa-volume-up"></i>
                </button>
                <button class="action-btn" @click="copyTranslatedText" title="Copy">
                  <i class="fas fa-copy"></i>
                </button>
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
        <div class="modal-header">
          <h3>Select Language</h3>
          <button class="close-modal-btn" @click="showLanguagePicker = false">X</button>
        </div>
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
            @click="selectLanguage(pickerFor, lang.value)"
            class="lang-option"
            :class="{
              'selected-lang-option':
                (pickerFor === 'from' && fromLanguage === lang.value) ||
                (pickerFor === 'to' && toLanguage === lang.value),
            }"
          >
            {{ lang.label }}
          </button>
        </div>
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
        { label: 'Auto-detect', value: 'auto-detect', short: 'Detect' },
        { label: 'Yacouba', value: 'yacouba', short: 'Ycb' },
        { label: 'Guérré', value: 'guerré', short: 'Grr' },
        { label: 'Agni', value: 'agni', short: 'Agn' },
        { label: 'Dida', value: 'dida', short: 'Did' },
        { label: 'Français', value: 'fr', short: 'Fr' },
        { label: 'English', value: 'en', short: 'En' },
        { label: 'Espagnol', value: 'es', short: 'Es' },
        { label: 'Allemand', value: 'de', short: 'De' },
      ],
      recent: [
        { text: 'Assè Man Djou', language: 'Guérré' },
        { text: 'Comment allez vous', language: 'Français' },
      ],
      translateTimeout: null,
    }
  },
  computed: {
    fromLanguageDisplayShort() {
      const lang = this.allLanguages.find((l) => l.value === this.fromLanguage)
      return lang ? lang.short : 'Detect'
    },
    toLanguageDisplayShort() {
      const lang = this.allLanguages.find((l) => l.value === this.toLanguage)
      return lang ? lang.short : 'Fr'
    },
    filteredLanguages() {
      const searchTerm = this.searchLang.toLowerCase()
      // Filter out 'Auto-detect' from the 'to' language list
      return this.allLanguages.filter((lang) =>
        this.pickerFor === 'to' && lang.value === 'auto-detect'
          ? false
          : lang.label.toLowerCase().includes(searchTerm),
      )
    },
  },
  methods: {
    goToSettings() {
      console.log('Go to Settings')
      // this.$router.push('/settings');
    },
    openLanguagePicker(forWhich) {
      this.pickerFor = forWhich
      this.searchLang = ''
      this.showLanguagePicker = true
    },
    selectLanguage(forWhich, langValue) {
      if (forWhich === 'from') {
        this.fromLanguage = langValue
      } else if (forWhich === 'to') {
        this.toLanguage = langValue
      }
      this.showLanguagePicker = false
      this.autoTranslate()
    },
    swapLanguages() {
      const tempFrom = this.fromLanguage
      this.fromLanguage = this.toLanguage
      this.toLanguage = tempFrom
      if (this.fromLanguage === 'auto-detect') {
        // If 'auto-detect' became the 'from' language after swap,
        // ensure 'to' isn't 'auto-detect'. Or handle specifically.
        // For now, simple swap.
      }
      this.autoTranslate()
    },
    autoTranslate() {
      clearTimeout(this.translateTimeout)
      this.translateTimeout = setTimeout(() => {
        if (this.inputText.length > 0) {
          this.translatedText = `[Traduction de "${this.inputText}" de ${this.fromLanguageDisplayShort} vers ${this.toLanguageDisplayShort}]`
          this.addRecentTranslation()
        } else {
          this.translatedText = ''
        }
      }, 500)
    },
    addRecentTranslation() {
      const currentText = this.inputText
      const currentLanguage = this.fromLanguageDisplayShort

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
    },
  },
}
</script>
<style scoped>
/* Variables pour les couleurs inspirées de Google Translate */
:root {
  --google-blue: #4285f4;
  --google-blue-dark: #3367d6;
  --google-gray-light-bg: #f8f9fa; /* Plus clair que google-gray-light pour le fond global */
  --google-gray-medium: #dadce0; /* Bordures fines */
  --google-text-dark: #202124;
  --google-text-light: #5f6368;
  --white: #ffffff;
  --shadow-color-card: rgba(60, 64, 67, 0.15); /* Ombre principale de la carte */
  --shadow-color-header: rgba(0, 0, 0, 0.08); /* Ombre de l'en-tête */
  --border-radius-base: 8px;
  --padding-unit: 16px; /* Unité de padding pour consistency */
  --header-height: 64px;
  --footer-height: 56px;
}

body,
html {
  margin: 0;
  padding: 0;
  overflow: hidden; /* Empêche le défilement inutile de la page */
}

.translate-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* Prend toute la hauteur de la fenêtre */
  background-color: var(--google-gray-light-bg);
  font-family: 'Google Sans', 'Roboto', Arial, sans-serif;
  color: var(--google-text-dark);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 var(--padding-unit);
  height: var(--header-height);
  background-color: var(--white);
  box-shadow: 0 1px 4px var(--shadow-color-header); /* Ombre de l'en-tête */
  z-index: 100;
  flex-shrink: 0;
}

.KUMAJALA-IMAGE {
  height: 40px; /* Ajustez la taille de l'image du logo */
  width: 200px; /* Ajustez la largeur de l'image du logo */
  object-fit: contain; /* Assure que l'image garde ses proportions */
  margin-right: 12px; /* Espace entre le logo et le texte */
}
.KUMAJALA-icon{
  height: 20px; /* Ajustez la taille de l'icône */
  width: 20px; /* Ajustez la largeur de l'icône */
  object-fit: contain; /* Assure que l'icône garde ses proportions */
  margin-left: 12px; /* Espace entre le texte et l'icône */
  vertical-align: middle; /* Aligne l'icône avec le texte */
}
.settings-icon {
  font-size: 1.4em;
  cursor: pointer;
  color: var(--google-text-light);
  transition: color 0.2s ease;
}
.settings-icon:hover {
  color: var(--google-blue);
}

.content {
  flex-grow: 1; /* Permet au contenu de prendre tout l'espace restant */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--padding-unit); /* Padding autour de la carte */
  overflow: hidden; /* Empêche le défilement du content lui-même si la carte défile */
  box-sizing: border-box;
}

.translation-card {
  background-color: var(--white);
  border-radius: var(--border-radius-base);
  box-shadow: 0 2px 5px 0 var(--shadow-color-card); /* Ombre plus douce pour la carte */
  width: 100%; /* Prend toute la largeur disponible dans le content */
  max-width: 960px; /* Largeur maximale pour les grands écrans */
  height: 100%; /* Prend toute la hauteur disponible dans le content */
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Section supérieure des sélecteurs de langue */
.language-selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* Google Translate n'a pas de bordure autour de cette barre, juste un séparateur en bas */
  padding: 8px var(--padding-unit);
  border-bottom: 1px solid var(--google-gray-medium); /* Séparateur subtil */
  background-color: var(--white);
  flex-shrink: 0; /* Ne pas réduire cette section */
}

.lang-selector-group {
  display: flex;
  flex-grow: 1;
  /* Google Translate a souvent un padding ou un espace subtil ici */
  padding: 0 4px;
}

.lang-option-button {
  background: none;
  border: none;
  font-size: 1em;
  font-weight: 500;
  color: var(--google-text-light); /* Couleur par défaut */
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
  flex-grow: 1; /* Permet aux boutons de prendre l'espace */
  text-align: center;
  position: relative; /* Pour la barre bleue active */
}
.lang-option-button.active-lang {
  color: var(--google-blue); /* Couleur bleue pour l'actif */
  font-weight: 600;
}
.lang-option-button.active-lang::after {
  content: '';
  position: absolute;
  bottom: -9px; /* Position sous le texte */
  left: 0;
  width: 100%;
  height: 3px; /* Épaisseur de la barre */
  background-color: var(--google-blue);
  border-radius: 2px 2px 0 0; /* Arrondi sur le dessus */
}

.lang-option-button:hover {
  background-color: rgba(66, 133, 244, 0.05);
}

.swap-lang-button {
  background: var(--white); /* Fond blanc comme sur Google Translate */
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
    border-color 0.2s ease,
    transform 0.2s ease;
  margin: 0 10px;
  flex-shrink: 0;
}
.swap-lang-button:hover {
  background-color: var(--google-gray-light-bg);
  border-color: var(--google-blue);
  transform: rotate(180deg); /* Animation de rotation */
}
.swap-lang-button i {
  font-size: 0.8em; /* Ajustement de la taille de l'icône si FontAwesome */
}

/* Wrapper pour les zones de texte */
.translation-areas-wrapper {
  display: flex;
  flex-direction: column; /* Mobile First: vertical */
  flex-grow: 1; /* Prend l'espace restant dans la carte */
}

.input-section,
.output-section {
  padding: var(--padding-unit); /* Padding interne des sections */
  flex-grow: 1; /* Les deux sections prennent une part égale de l'espace vertical */
  min-height: 150px; /* Hauteur minimale pour chaque section */
  display: flex; /* Permet au textarea-container de s'étirer */
  flex-direction: column;
}

.input-section {
  border-bottom: 1px solid var(--google-gray-medium); /* Séparateur entre input et output sur mobile */
}
.output-section {
  border-bottom: none;
}

.textarea-container {
  position: relative;
  height: 100%; /* Prend toute la hauteur de la section parent */
  display: flex;
  flex-direction: column; /* Pour que le textarea puisse s'étirer */
}

.text-input,
.text-output {
  width: 100%;
  height: 100%; /* Prend toute la hauteur du container */
  border: none; /* AUCUNE BORDURE ICI POUR IMITER GOOGLE TRANSLATE */
  background: transparent;
  resize: none;
  font-size: 1.1em;
  color: var(--google-text-dark);
  outline: none; /* Retire l'outline au focus */
  padding: 0; /* Aucun padding ici, le padding est sur input-section/output-section */
  box-sizing: border-box;
  display: block;
}

.text-input::placeholder,
.text-output::placeholder {
  color: var(--google-text-light); /* Couleur du placeholder */
  opacity: 1; /* S'assure que le placeholder n'est pas transparent */
}

.text-output {
  color: var(--google-text-dark);
}

.input-actions,
.output-actions {
  position: absolute;
  /* Top-right ou bottom-right selon le design de Google Translate (souvent bottom-right) */
  right: 12px;
  bottom: 12px;
  display: flex;
  gap: 8px;
  z-index: 1;
}

.action-btn {
  background: none;
  border: none;
  font-size: 1.3em;
  color: var(--google-text-light);
  cursor: pointer;
  width: 36px; /* Taille légèrement plus grande pour l'icône */
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
}
.action-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--google-blue); /* La couleur de l'icône change au survol */
}
.action-btn i {
  font-size: 0.9em; /* Ajuster la taille de l'icône si FontAwesome */
}

/* Footer / Navbar */
.footer-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  padding: 10px 0;
  background-color: var(--white);
  border-top: 1px solid var(--google-gray-medium); /* Séparateur subtil */
  box-shadow: 0 -1px 4px var(--shadow-color-header); /* Ombre légère vers le haut */
  position: sticky;
  bottom: 0;
  z-index: 90;
  flex-shrink: 0;
  height: var(--footer-height);
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
  padding: var(--padding-unit);
  border-radius: var(--border-radius-base);
  box-shadow: 0 4px 8px var(--shadow-color-card);
  width: 90%;
  max-width: 400px;
  max-height: 80vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.modal-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: var(--google-text-dark);
}
.close-modal-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  color: var(--google-text-light);
  cursor: pointer;
  padding: 5px;
  line-height: 1; /* Pour aligner le X */
  transition: color 0.2s ease;
}
.close-modal-btn:hover {
  color: var(--google-blue);
}

.search-lang-input {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid var(--google-gray-medium);
  border-radius: 5px;
  font-size: 1em;
  outline: none;
  box-sizing: border-box;
}
.search-lang-input:focus {
  border-color: var(--google-blue);
}

.lang-list {
  display: flex;
  flex-direction: column;
  gap: 0; /* Pas d'espacement direct entre les options */
}

.lang-option {
  background: none;
  border: none;
  padding: 12px 0; /* Plus de padding pour les options */
  text-align: left;
  font-size: 1em;
  color: var(--google-text-dark);
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid var(--google-gray-light-bg); /* Séparateur très léger */
}
.lang-option:last-child {
  border-bottom: none;
}
.lang-option:hover {
  background-color: var(--google-gray-light-bg); /* Hover sur fond très léger */
}
.lang-option.selected-lang-option {
  background-color: var(--google-blue);
  color: var(--white);
  font-weight: bold;
}
.lang-option.selected-lang-option:hover {
  background-color: var(--google-blue-dark); /* Darker blue on hover for selected */
}

/* Media Queries pour le responsive design */

/* Disposition horizontale pour les tablettes et desktops (à partir de 768px de largeur) */
@media (min-width: 768px) {
  .translation-card {
    /* La hauteur de la carte remplit l'espace vertical disponible */
    height: calc(100vh - var(--header-height) - var(--footer-height) - (var(--padding-unit) * 2));
    flex-direction: column; /* Main card structure remains column */
  }

  .translation-areas-wrapper {
    flex-direction: row; /* Input and Output sections side-by-side */
    flex-grow: 1; /* Takes up remaining height in translation-card */
  }

  .input-section,
  .output-section {
    border-bottom: none; /* No bottom border for horizontal layout */
    border-right: 1px solid var(--google-gray-medium); /* Vertical divider */
    height: 100%; /* Take full height of parent wrapper */
    min-height: auto; /* Supprimer la hauteur minimale pour laisser flexbox gérer */
  }
  .output-section {
    border-right: none;
  }

  .textarea-container {
    height: 100%;
  }
}
</style>
