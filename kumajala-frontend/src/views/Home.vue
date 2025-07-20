<script setup>
import { useRouter } from 'vue-router'; 
import TopBar from '@/components/topBar.vue'; 
import GetStartedButton from '@/components/getStartedButton.vue'; 
import { Home as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon } from 'lucide-vue-next'; 
import Footer from '@/components/Footer.vue'; 

const router = useRouter();

const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon }, 
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

const handleLogoClick = () => {
    router.push('/'); // Utilisation de router.push
};

const handleNavClick = (item) => {
    console.log('Nav item clicked:', item.name);
    // Le router.push est déjà géré par RouterLink dans TopBar
};

const handleGetStarted = () => {
    router.push('/translator'); // Utilisation de router.push
};
</script>

<template>
  <div>
    <TopBar
      :nav-items="navigationItems"
      variant="blur"
      position="sticky"
      :shrink-on-scroll="true"
      @logo-click="handleLogoClick"
      @nav-item-click="handleNavClick"
    />

    <!-- SECTION HERO -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          Bienvenue sur <span class="highlight">Kumajala</span>
        </h1>
        <p class="hero-subtitle">
          Votre voyage vers un environnement plus sain commence ici.
        </p>
        <GetStartedButton variant="primary" size="lg" @click="handleGetStarted">
          Commencer l'aventure
        </GetStartedButton>
      </div>
    </section>

    <!-- SECTION AVANTAGES / FONCTIONNALITÉS -->
    <section class="features">
      <h2>Pourquoi choisir Kumajala ?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <h3>🌱 Écologique</h3>
          <p>Réduisez votre impact environnemental en toute simplicité.</p>
        </div>
        <div class="feature-card">
          <h3>⚡ Rapide</h3>
          <p>Optimisé pour des performances rapides et fluides.</p>
        </div>
        <div class="feature-card">
          <h3>🛡️ Sécurisé</h3>
          <p>Vos données sont protégées avec les dernières technologies.</p>
        </div>
      </div>
    </section>
    <Footer />
  </div>
</template>

<style scoped>
/* --- HERO --- */
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 120px 20px;
  background: linear-gradient(to bottom right, var(--cl-gray-100), var(--cl-gray-200)); /* Utilisation des variables */
  min-height: calc(100vh - 100px); /* Ajuster pour la hauteur de l'en-tête */
}

.hero-content {
  max-width: 600px;
}

.hero-title {
  font-size: var(--fs-5xl); /* Utilisation des variables */
  color: var(--cl-primary);
  margin-bottom: var(--space-4); /* Utilisation des variables */
}

.highlight {
  background: linear-gradient(90deg, var(--cl-primary), var(--cl-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: var(--fs-lg); /* Utilisation des variables */
  color: var(--cl-secondary);
  margin-bottom: var(--space-8); /* Utilisation des variables */
}

/* --- FEATURES --- */
.features {
  padding: var(--space-20) var(--space-4); /* Utilisation des variables */
  text-align: center;
  background-color: var(--cl-white);
}

.features h2 {
  font-size: var(--fs-4xl); /* Utilisation des variables */
  margin-bottom: var(--space-10); /* Utilisation des variables */
  color: var(--cl-tertiary); /* Couleur ajustée pour la cohérence */
}

.features-grid {
  display: grid;
  gap: var(--space-8); /* Utilisation des variables */
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  max-width: 960px; /* Limiter la largeur de la grille */
  margin: 0 auto;
}

.feature-card {
  background: var(--cl-white);
  padding: var(--space-8); /* Utilisation des variables */
  border-radius: var(--radius-lg); /* Utilisation des variables */
  box-shadow: var(--shadow-md);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: var(--cl-primary);
  margin-bottom: var(--space-4); /* Utilisation des variables */
}

.feature-card p {
  color: var(--cl-gray-700); /* Couleur ajustée pour la lisibilité */
}

/* --- FOOTER --- */
.site-footer {
  padding: var(--space-10) var(--space-4); /* Utilisation des variables */
  background-color: var(--cl-black); /* Couleur ajustée pour un contraste */
  text-align: center;
  color: var(--cl-white); /* Texte blanc sur fond sombre */
  font-size: var(--fs-sm); /* Utilisation des variables */
}

.site-footer ul {
  list-style: none;
  padding: 0;
  margin-top: var(--space-3); /* Utilisation des variables */
  display: flex;
  justify-content: center;
  gap: var(--space-4); /* Utilisation des variables */
}

.site-footer a {
  color: var(--cl-secondary); /* Couleur pour les liens */
  text-decoration: none;
  transition: color var(--transition-base);
}

.site-footer a:hover {
  color: var(--cl-primary);
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .hero {
    padding: 80px 20px;
    min-height: calc(100vh - 80px);
  }
  .hero-title {
    font-size: var(--fs-4xl);
  }
  .hero-subtitle {
    font-size: var(--fs-base);
  }
  .features {
    padding: 60px 20px;
  }
  .features h2 {
    font-size: var(--fs-3xl);
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: var(--fs-3xl);
  }
  .hero-subtitle {
    font-size: var(--fs-sm);
  }
  .features h2 {
    font-size: var(--fs-2xl);
  }
  .feature-card {
    padding: var(--space-6);
  }
  .site-footer {
    padding: var(--space-6) var(--space-3);
  }
}
</style>
