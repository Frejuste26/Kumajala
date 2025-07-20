<script setup>
import EnhancedHeader from '@/components/topBar.vue';
import { Home as HomeIcon, Info as InfoIcon, Languages as LanguagesIcon, Settings as SettingsIcon } from 'lucide-vue-next'; 
import Footer from '@/components/Footer.vue'; 
const navigationItems = [
    { name: 'Accueil', path: '/', icon: HomeIcon }, 
    { name: 'À Propos', path: '/about', icon: InfoIcon },
    { name: 'Traducteur', path: '/translator', icon: LanguagesIcon },
    { name: 'Paramètres', path: '/settings', icon: SettingsIcon }
];

const handleLogoClick = () => {
    console.log('Logo clicked!');
};

const handleNavClick = (item) => {
    console.log('Nav item clicked:', item.name);
};
</script>

<template>
  <div>
    <EnhancedHeader
      :nav-items="navigationItems"
      variant="blur"
      position="sticky"
      :shrink-on-scroll="true"
      @logo-click="handleLogoClick"
      @nav-item-click="handleNavClick"
    />

    <!-- SECTION ABOUT -->
    <section class="about-hero">
      <h1>À propos de <span class="highlight">Kumajala</span></h1>
      <p>Une vision, un engagement, une équipe dédiée à l’avenir de l’environnement et de la technologie.</p>
    </section>

    <section class="about-content">
      <h2>Notre mission</h2>
      <p>
        Chez Kumajala, nous croyons que la technologie peut être un levier puissant pour améliorer la gestion de l’environnement et la qualité de vie des communautés.
        Notre objectif est d’offrir des solutions modernes, accessibles et adaptées aux défis écologiques actuels.
      </p>

      <h2>Notre vision</h2>
      <p>
        Créer une plateforme numérique intuitive, humaine et durable, qui facilite l’adoption des bonnes pratiques environnementales au quotidien.
      </p>

      <h2>Nos valeurs</h2>
      <ul>
        <li>🌿 Respect de l’environnement</li>
        <li>💡 Innovation responsable</li>
        <li>🤝 Collaboration et transparence</li>
        <li>📈 Excellence et qualité</li>
      </ul>
    </section>

    <Footer />
  </div>
</template>

<style scoped>
.about-hero {
  padding: 120px 20px;
  text-align: center;
  background: linear-gradient(to bottom, #f5f5f5, #eaeaea);
}

.about-hero h1 {
  font-size: 2.8rem;
  color: var(--cl-primary);
}

.about-hero .highlight {
  background: linear-gradient(90deg, var(--cl-primary), var(--cl-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.about-hero p {
  font-size: 1.2rem;
  color: var(--cl-secondary);
  margin-top: 1rem;
}

.about-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 80px 20px;
  line-height: 1.7;
  color: var(--cl-tertiary);
}

.about-content h2 {
  font-size: 1.8rem;
  color: var(--cl-primary);
  margin-bottom: 0.5rem;
}

.about-content p {
  margin-bottom: 2rem;
  color: var(--cl-secondary);
}

.about-content ul {
  list-style: none;
  padding: 0;
}

.about-content li {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}


</style>
