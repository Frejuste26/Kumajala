<script setup>
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { Home as HomeIcon, Info as InfoIcon, Search as SearchIcon, Sun as SunIcon, Moon as MoonIcon, ArrowRight as ArrowRightIcon, Settings as SettingsIcon } from 'lucide-vue-next'; // Import des icônes

// Props
const props = defineProps({
  // Configuration du logo
  logoSrc: {
    type: String,
    default: '/src/assets/logo.png' // Chemin mis à jour pour Vite
  },

  logoAlt: {
    type: String,
    default: 'Logo Kumajala'
  },

  logoHeight: {
    type: String,
    default: '40px'
  },

  // Navigation
  navItems: {
    type: Array,
    default: () => [
      { name: 'Accueil', path: '/', icon: HomeIcon },
      { name: 'À Propos', path: '/about', icon: InfoIcon },
      { name: 'Traducteur', path: '/translator', icon: null },
      { name: 'Paramètres', path: '/settings', icon: SettingsIcon },
    ]
  },

  // Actions (boutons à droite)
  showActions: {
    type: Boolean,
    default: true
  },

  // Variantes de style
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'transparent', 'solid', 'blur'].includes(value)
  },

  // Position
  position: {
    type: String,
    default: 'relative',
    validator: (value) => ['relative', 'sticky', 'fixed'].includes(value)
  },

  // Mobile
  mobileBreakpoint: {
    type: Number,
    default: 768
  },

  // Scroll behavior
  hideOnScroll: {
    type: Boolean,
    default: false
  },

  shrinkOnScroll: {
    type: Boolean,
    default: true
  }
})

// Emits
const emit = defineEmits(['logo-click', 'nav-item-click', 'mobile-menu-toggle'])

// Reactive state
const router = useRouter()
const route = useRoute()

const isMobileMenuOpen = ref(false)
const isScrolled = ref(false)
const isHidden = ref(false)
const isMobile = ref(false)
const lastScrollY = ref(0)
const isDarkMode = ref(false); // État pour le mode sombre

// Computed
const headerClasses = computed(() => [
  'enhanced-header',
  `variant-${props.variant}`,
  `position-${props.position}`,
  {
    'is-scrolled': isScrolled.value,
    'is-hidden': isHidden.value && props.hideOnScroll,
    'is-shrunk': isScrolled.value && props.shrinkOnScroll,
    'mobile-menu-open': isMobileMenuOpen.value
  }
])

const logoClasses = computed(() => [
  'header-logo',
  {
    'is-shrunk': isScrolled.value && props.shrinkOnScroll
  }
])

// Methods
const handleScroll = () => {
  const currentScrollY = window.scrollY

  // Détection du scroll
  isScrolled.value = currentScrollY > 20

  // Masquage au scroll (optionnel)
  if (props.hideOnScroll) {
    isHidden.value = currentScrollY > lastScrollY.value && currentScrollY > 100
  }

  lastScrollY.value = currentScrollY
}

const handleResize = () => {
  isMobile.value = window.innerWidth < props.mobileBreakpoint

  // Fermer le menu mobile si on passe en desktop
  if (!isMobile.value && isMobileMenuOpen.value) {
    isMobileMenuOpen.value = false
  }
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
  emit('mobile-menu-toggle', isMobileMenuOpen.value)

  // Empêcher le scroll du body quand le menu est ouvert
  if (isMobileMenuOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const handleLogoClick = () => {
  emit('logo-click')
  router.push('/')
}

const handleNavItemClick = (item) => {
  emit('nav-item-click', item)

  // Fermer le menu mobile après navigation
  if (isMobileMenuOpen.value) {
    toggleMobileMenu()
  }
}

const isActiveRoute = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

// Fonction pour basculer le mode sombre
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark-mode'); // Appliquer la classe sur html
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark-mode'); // Retirer la classe de html
    localStorage.setItem('theme', 'light');
  }
};

// Lifecycle
onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', handleResize, { passive: true })
  handleResize() // Check initial size

  // Charger le thème depuis localStorage au montage
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    isDarkMode.value = true;
    document.documentElement.classList.add('dark-mode');
  } else {
    isDarkMode.value = false;
    document.documentElement.classList.remove('dark-mode');
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleResize)
  document.body.style.overflow = '' // Cleanup
})

// Watch route changes to close mobile menu
watch(() => route.path, () => {
  if (isMobileMenuOpen.value) {
    toggleMobileMenu()
  }
})
</script>

<template>
  <header :class="headerClasses">
    <div class="header-container">
      <!-- Logo -->
      <div class="header-brand">
        <button
          class="logo-button"
          @click="handleLogoClick"
          :aria-label="`Aller à l'accueil - ${logoAlt}`"
        >
          <img
            :src="logoSrc"
            :alt="logoAlt"
            :class="logoClasses"
            :style="{ height: logoHeight }"
            loading="lazy"
          />
        </button>
      </div>

      <!-- Navigation Desktop -->
      <nav class="desktop-nav" aria-label="Navigation principale">
        <ul class="nav-list">
          <li
            v-for="item in navItems"
            :key="item.path"
            class="nav-item"
          >
            <RouterLink
              :to="item.path"
              class="nav-link"
              :class="{ 'is-active': isActiveRoute(item.path) }"
              @click="handleNavItemClick(item)"
            >
              <!-- Icône si fournie -->
              <component
                :is="item.icon"
                v-if="item.icon"
                class="nav-icon"
              />
              <span>{{ item.name }}</span>

              <!-- Indicateur d'état actif -->
              <span
                v-if="isActiveRoute(item.path)"
                class="active-indicator"
                aria-hidden="true"
              ></span>
            </RouterLink>
          </li>
        </ul>
      </nav>

      <!-- Actions (boutons, recherche, etc.) -->
      <div v-if="showActions" class="header-actions">
        <slot name="actions">
          <!-- Bouton de thème -->
          <button class="action-button theme-toggle" @click="toggleDarkMode" :aria-label="isDarkMode ? 'Passer en mode clair' : 'Passer en mode sombre'">
            <component :is="isDarkMode ? MoonIcon : SunIcon" width="20" height="20" />
          </button>

          <!-- Bouton de recherche (si vous le gardez) -->
          <button class="action-button search-button" aria-label="Rechercher">
            <SearchIcon width="20" height="20" />
          </button>

          <!-- Lien vers les paramètres (si vous le gardez) -->
          <RouterLink to="/settings" class="action-button" aria-label="Paramètres">
            <SettingsIcon width="20" height="20" />
          </RouterLink>
          
          <RouterLink to="/translator" class="cta-button">
            <span>Commencer</span>
            <ArrowRightIcon width="16" height="16" />
          </RouterLink>
        </slot>
      </div>

      <!-- Bouton menu mobile -->
      <button
        class="mobile-menu-button"
        @click="toggleMobileMenu"
        :aria-expanded="isMobileMenuOpen"
        :aria-label="isMobileMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
      >
        <span class="hamburger-line" :class="{ 'is-open': isMobileMenuOpen }"></span>
        <span class="hamburger-line" :class="{ 'is-open': isMobileMenuOpen }"></span>
        <span class="hamburger-line" :class="{ 'is-open': isMobileMenuOpen }"></span>
      </button>
    </div>

    <!-- Menu Mobile -->
    <Transition name="mobile-menu">
      <div v-show="isMobileMenuOpen" class="mobile-menu">
        <div class="mobile-menu-backdrop" @click="toggleMobileMenu"></div>
        <nav class="mobile-nav" aria-label="Navigation mobile">
          <ul class="mobile-nav-list">
            <li
              v-for="(item, index) in navItems"
              :key="item.path"
              class="mobile-nav-item"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <RouterLink
                :to="item.path"
                class="mobile-nav-link"
                :class="{ 'is-active': isActiveRoute(item.path) }"
                @click="handleNavItemClick(item)"
              >
                <component
                  :is="item.icon"
                  v-if="item.icon"
                  class="mobile-nav-icon"
                />
                <span>{{ item.name }}</span>
              </RouterLink>
            </li>
          </ul>

          <!-- Actions mobiles -->
          <div class="mobile-actions">
            <slot name="mobile-actions">
              <RouterLink to="/translator" class="mobile-cta-button">
                Commencer
              </RouterLink>
            </slot>
          </div>
        </nav>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
/* ===== BASE HEADER ===== */
.enhanced-header {
  position: relative;
  width: 100%;
  z-index: 1000;
  transition: all var(--transition-base);
  font-family: var(--font-primary);
}

.position-sticky {
  position: sticky;
  top: 0;
}

.position-fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.header-container {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  transition: all var(--transition-base);
}

/* ===== VARIANTES ===== */
.variant-default {
  background-color: var(--cl-white);
  border-bottom: 1px solid var(--cl-gray-200);
  transition: var(--transition-color); /* Ajouté */
}

.variant-transparent {
  background-color: transparent;
  transition: var(--transition-color); /* Ajouté */
}

.variant-solid {
  background-color: var(--cl-primary);
  color: var(--cl-white);
  transition: var(--transition-color); /* Ajouté */
}

.variant-blur {
  background-color: rgba(255, 255, 239, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(196, 196, 196, 0.2);
  transition: var(--transition-color); /* Ajouté */
}

/* ===== ÉTATS DE SCROLL ===== */
.is-scrolled .header-container {
  padding: var(--space-2) var(--space-6);
}

.is-scrolled.variant-transparent,
.is-scrolled.variant-blur {
  background-color: var(--cl-white); /* Utilise la variable du mode actuel */
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--cl-gray-200); /* Utilise la variable du mode actuel */
  box-shadow: var(--shadow-sm);
}

.is-hidden {
  transform: translateY(-100%);
}

.is-shrunk .header-logo {
  height: 32px !important;
}

/* ===== LOGO ===== */
.header-brand {
  flex-shrink: 0;
}

.logo-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
}

.logo-button:hover {
  background-color: var(--cl-gray-100); /* Utilise la variable du mode actuel */
  transform: scale(1.05);
}

.logo-button:focus-visible {
  outline: 2px solid var(--cl-primary);
  outline-offset: 2px;
}

.header-logo {
  display: block;
  transition: all var(--transition-base);
  max-width: 100%;
}

/* ===== NAVIGATION DESKTOP ===== */
.desktop-nav {
  display: flex;
  align-items: center;
}

.nav-list {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-item {
  position: relative;
}

.nav-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-4);
  font-size: var(--fs-base);
  font-weight: var(--fw-medium);
  text-decoration: none;
  color: var(--cl-tertiary); /* Utilise la variable du mode actuel */
  border-radius: var(--radius-lg);
  transition: var(--transition-color); /* Ajouté */
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--cl-primary), var(--cl-secondary));
  opacity: 0;
  transition: opacity var(--transition-base);
  border-radius: inherit;
}

.nav-link:hover::before {
  opacity: 0.1;
}

.nav-link:hover {
  color: var(--cl-primary); /* Utilise la variable du mode actuel */
  transform: translateY(-1px);
}

.nav-link.is-active {
  color: var(--cl-primary); /* Utilise la variable du mode actuel */
  font-weight: var(--fw-semibold);
}

.nav-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.active-indicator {
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 6px;
  background-color: var(--cl-primary); /* Utilise la variable du mode actuel */
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ===== ACTIONS ===== */
.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: none;
  border: none;
  border-radius: var(--radius-lg);
  color: var(--cl-tertiary); /* Utilise la variable du mode actuel */
  cursor: pointer;
  transition: var(--transition-color); /* Ajouté */
}

.action-button:hover {
  background-color: var(--cl-gray-100); /* Utilise la variable du mode actuel */
  color: var(--cl-primary); /* Utilise la variable du mode actuel */
  transform: scale(1.1);
}

.cta-button {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: linear-gradient(135deg, var(--cl-primary), var(--cl-secondary));
  color: var(--cl-white);
  border: none;
  border-radius: var(--radius-lg);
  font-weight: var(--fw-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* ===== MENU MOBILE ===== */
.mobile-menu-button {
  display: none;
  flex-direction: column;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.mobile-menu-button:hover {
  background-color: var(--cl-gray-100); /* Utilise la variable du mode actuel */
}

.hamburger-line {
  display: block;
  width: 24px;
  height: 2px;
  background-color: var(--cl-tertiary); /* Utilise la variable du mode actuel */
  border-radius: 2px;
  transition: all var(--transition-base);
  transform-origin: center;
}

.hamburger-line:not(:last-child) {
  margin-bottom: 4px;
}

.hamburger-line.is-open:nth-child(1) {
  transform: rotate(45deg) translate(3px, 3px);
}

.hamburger-line.is-open:nth-child(2) {
  opacity: 0;
  transform: rotate(180deg) scale(0.1);
}

.hamburger-line.is-open:nth-child(3) {
  transform: rotate(-45deg) translate(3px, -3px);
}

.mobile-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 999;
  display: flex;
}

.mobile-menu-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.mobile-nav {
  position: relative;
  width: 280px;
  height: 100%;
  background-color: var(--cl-white); /* Utilise la variable du mode actuel */
  padding: var(--space-8) var(--space-6);
  box-shadow: var(--shadow-xl);
  overflow-y: auto;
  margin-left: auto;
  transition: var(--transition-color); /* Ajouté */
}

.mobile-nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.mobile-nav-item {
  margin-bottom: var(--space-2);
  opacity: 0;
  transform: translateX(20px);
  animation: slideInRight 0.3s ease-out forwards;
}

@keyframes slideInRight {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  font-size: var(--fs-lg);
  font-weight: var(--fw-medium);
  text-decoration: none;
  color: var(--cl-tertiary); /* Utilise la variable du mode actuel */
  border-radius: var(--radius-lg);
  transition: var(--transition-color); /* Ajouté */
}

.mobile-nav-link:hover,
.mobile-nav-link.is-active {
  background-color: rgba(var(--cl-primary-rgb, 241, 137, 14), 0.1); /* Utilise la variable du mode actuel */
  color: var(--cl-primary); /* Utilise la variable du mode actuel */
}

.mobile-nav-icon {
  width: 20px;
  height: 20px;
}

.mobile-actions {
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 1px solid var(--cl-gray-200); /* Utilise la variable du mode actuel */
  transition: var(--transition-color); /* Ajouté */
}

.mobile-cta-button {
  width: 100%;
  padding: var(--space-4) var(--space-6);
  background: linear-gradient(135deg, var(--cl-primary), var(--cl-secondary));
  color: var(--cl-white);
  border: none;
  border-radius: var(--radius-lg);
  font-size: var(--fs-lg);
  font-weight: var(--fw-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.mobile-cta-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* ===== TRANSITIONS ===== */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from .mobile-menu-backdrop,
.mobile-menu-leave-to .mobile-menu-backdrop {
  opacity: 0;
}

.mobile-menu-enter-from .mobile-nav,
.mobile-menu-leave-to .mobile-nav {
  transform: translateX(100%);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }

  .mobile-menu-button {
    display: flex;
  }

  .header-actions {
    display: none;
  }

  .header-container {
    padding: var(--space-3) var(--space-4);
  }

  .is-scrolled .header-container {
    padding: var(--space-2) var(--space-4);
  }
}

@media (max-width: 480px) {
  .mobile-nav {
    width: 100%;
  }

  .header-container {
    padding: var(--space-3);
  }
}

/* ===== VARIANTE SOLID ADJUSTMENTS ===== */
/* Ces styles sont déjà dynamiques via les variables en mode sombre */
/* et ne nécessitent pas de ciblage spécifique 'html.dark-mode' */
.variant-solid .nav-link {
  color: rgba(255, 255, 255, 0.9);
}

.variant-solid .nav-link:hover,
.variant-solid .nav-link.is-active {
  color: var(--cl-white);
}

.variant-solid .action-button {
  color: rgba(255, 255, 255, 0.9);
}

.variant-solid .action-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: var(--cl-white);
}

.variant-solid .hamburger-line {
  background-color: var(--cl-white);
}

/* ===== ACCESSIBILITY ===== */
@media (prefers-reduced-motion: reduce) {
  .enhanced-header,
  .nav-link,
  .action-button,
  .mobile-nav-item {
    transition: none;
    animation: none;
  }
}

/* Focus styles for keyboard navigation */
.nav-link:focus-visible,
.action-button:focus-visible,
.mobile-nav-link:focus-visible {
  outline: 2px solid var(--cl-primary);
  outline-offset: 2px;
}
</style>