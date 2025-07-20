<template>
    <footer class="site-footer">
      <p>&copy; 2025 Kumajala | Développé par VFC Crew</p>
      <ul>
        <li>
          <a href="https://github.com/Frejuste26" target="_blank">Kei Prince Frejuste</a>
        </li>
        <li>
          <a href="https://github.com/nango-vital" target="_blank">Nango Ebrotié Vital</a>
        </li>
        <li>
          <a href="https://github.com/sannetia" target="_blank">Sanné-Tia Chrys</a>
        </li>
      </ul>
    </footer>
</template>
<style scoped>
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
</style>