<template>
  <div class="onboarding-container">
    <header class="header">
      <span class="logo">
        <img src="@/assets/KUMAJALA-IMAGE.jpg" alt="KUMAJALA Logo" class="kumajala-logo-image" />
      </span>
      <span class="language-switcher" @click="toggleLanguage">
        <img
          src="@/assets/KUMAJALA-ICON.jpg"
          alt="Icône de sélection de langue"
          class="kumajala-language-icon"
        />
      </span>
    </header>

    <main class="content">
      <div class="main-content-wrapper">
        <div class="dots-navigation">
          <span class="dot active"></span>
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>

        <h1 class="title">Connect Across Cultures</h1>
        <p class="description">
          Translate languages, share insights, and build a global community.
        </p>

        <button class="get-started-button" @click="getStarted">Get Started</button>
      </div>
    </main>

    <footer class="footer"></footer>
  </div>
</template>

<script>
export default {
  name: 'pageOne', // Nom cohérent avec le fichier page1.vue
  methods: {
    toggleLanguage() {
      console.log('Changer de langue cliqué !')
      alert("Changement de langue non implémenté pour l'instant.")
    },
    getStarted() {
      console.log('Bouton "Get Started" cliqué ! Émission de l\'événement "get-started".')
      this.$emit('get-started') // Émet un événement personnalisé nommé 'get-started'
    },
  },
}
</script>

<style scoped>
/* Variables pour les couleurs et espacements */
:root {
  --primary-blue: #f08910; /* Bleu standard pour les accents */
  --primary-blue-hover: #0056b3; /* Bleu plus foncé pour l'effet de survol */
  --bg-main-color: #f08910; /* Couleur de fond principale, vive et opaque */
  --text-color-light: #f08910; /* Couleur de texte claire pour les titres et boutons */
  --text-color-medium: #f08910 /* Couleur de texte pour les descriptions, légèrement transparente */
    --dot-inactive-color: #f08910 /* Couleur des points de navigation inactifs */
    --dot-active-color: #f08910; /* Couleur du point de navigation actif */
  --shadow-color: #f08910; /* Couleur standard pour les ombres */
  --placeholder-bg: #f08910 /* Fond du placeholder de l'image (légèrement transparent) */;
}

.onboarding-container {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  min-height: 100vh;
  background-color: var(--bg-main-color); /* Couleur de fond PLEINE et opaque */
  font-family: Arial, sans-serif;
  color: var(--text-color-light); /* Couleur de texte par défaut pour le conteneur */
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden; /* Empêche les barres de défilement indésirables */
}

/* Pseudo-élément pour l'image de fond "Afrique.png" (semi-transparente) */
.onboarding-container::before {
  content: ''; /* Essentiel pour que le pseudo-élément soit affiché */
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  background-repeat: no-repeat;
  background-position: center top; /* Positionnement au centre en haut */
  background-size: 50% auto; /* Ajuste la taille de l'image de fond */
  opacity: 0.1; /* Opacité faible pour un effet de filigrane, APPLIQUÉE UNIQUEMENT ICI */
  filter: drop-shadow(0 8px 24px rgba(0, 0, 0, 0.1)); /* Ombre portée légère */
  z-index: 1; /* Place le fond derrière le contenu */
  pointer-events: none; /* Permet aux clics de traverser le pseudo-élément */
}

/* Assurez-vous que le contenu principal est toujours au-dessus du fond */
.header,
.content,
.footer {
  position: relative; /* Nécessaire pour que z-index fonctionne */
  z-index: 2; /* Place le contenu au-dessus du pseudo-élément de fond */
}

/* Styles pour les images KUMAJALA dans l'en-tête */
.kumajala-logo-image {
  width: 175px; /* Agrandissement du logo principal */
  height: 60px; /* Maintient les proportions */

  margin-right: 12px; /* Espace entre le logo et le texte */
}

.kumajala-language-icon {
  width: 55px; /* Agrandissement de l'icône de langue */
  height: 64px; /* Taille carrée pour l'icône */
  object-fit: contain;
  border-radius: 75%;
  margin-left: 12px; /* Espace entre le texte et l'icône de langue */
  vertical-align: middle;
}

/* Header */
.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}

.logo {
  font-weight: bold;
  font-size: 1.8em; /* Taille de police plus grande pour le nom KUMANJALA */
  color: var(--text-color-light); /* Texte en blanc plein */
  display: flex; /* Permet l'alignement des éléments internes */
  align-items: center; /* Alignement vertical centré pour les images et le texte */
  gap: 8px; /* Espace général entre les éléments du logo */
}

.language-switcher {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Main Content */
.content {
  flex-grow: 1; /* Permet au contenu de prendre l'espace disponible */
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  justify-content: center; /* Centre le contenu verticalement */
  padding-bottom: 80px; /* Espace pour le footer */
  width: 100%;
  padding-top: 20px; /* Espace en haut du contenu */
}

.image-placeholder {
  width: min(80vw, 300px); /* Taille du cadre du téléphone */
  height: auto;
  aspect-ratio: 1/1.4; /* Ratio d'aspect pour conserver la forme du téléphone */
  background-color: var(--placeholder-bg); /* Fond légèrement transparent pour le placeholder */
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 40px;
  box-shadow: 0 10px 20px var(--shadow-color); /* Ombre portée */
  position: relative;
  overflow: hidden;
}

.phone-mockup-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Couvre tout le cadre sans déformation */
  border-radius: 20px; /* Coins arrondis pour l'image du téléphone */
}
.get-started-button {
  background-color: #f08910;
  color:white ; /* Couleur du texte du bouton */
  border: lightblue 1px solid; /* Bordure légère pour le bouton */
  border-radius: 30px; /* Coins arrondis pour le bouton */
  padding: 12px 24px; /* Espace interne du bouton */
  font-size: 1.2em; /* Taille de police du texte du bouton */
  cursor: pointer;
  font-weight: bold; /* Texte en gras pour le bouton */
  transition:
    background-color 0.3s ease,
    color 0.3s ease,
    box-shadow 0.3s ease,
    transform 0.2s ease,
    border-radius 0.3s ease; /* Transition pour les effets de survol */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Ombre portée pour le bouton */
}
.get-started-button:hover {
  background-color: var(--primary-blue-hover); /* Couleur de fond au survol */
  color: #f08910; /* Couleur du texte au survol */
  transform: scale(1.05); /* Légère augmentation de la taille au survol */
}
.title {
  color: #f08910;
  text-decoration: solid;
}
.description {
  color: #f08910;
}
</style>
