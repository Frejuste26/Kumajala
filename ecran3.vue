<template>
  <div
    class="relative flex size-full min-h-screen flex-col bg-white justify-between group/design-root overflow-x-hidden"
    style='--select-button-svg: url(&apos;data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2724px%27 height=%2724px%27 fill=%27rgb(96,117,138)%27 viewBox=%270 0 256 256%27%3e%3cpath d=%27M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z%27%3e%3c/path%3e%3c/svg%3e&apos;); font-family: "Spline Sans", "Noto Sans", sans-serif;'
  >
    <div>
      <div class="flex items-center bg-white p-4 pb-2 justify-between">
        <button @click="goBack" class="text-[#111418] flex size-12 shrink-0 items-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
            <path
              d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z"
            ></path>
          </svg>
        </button>
        <h2 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">Translate</h2>
      </div>

      <h3 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">From</h3>
      <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
        <label class="flex flex-col min-w-40 flex-1">
          <select
            v-model="fromLanguage"
            class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#111418] focus:outline-0 focus:ring-0 border border-[#dbe0e6] bg-white focus:border-[#dbe0e6] h-14 bg-[image:--select-button-svg] placeholder:text-[#60758a] p-[15px] text-base font-normal leading-normal"
          >
            <option value="auto-detect">Auto-detect</option>
            <option value="yacouba">Yacouba</option>
            <option value="guerré">Guérré</option>
            <option value="agni">Agni</option>
            <option value="dida">Dida</option>
            <option value="fr">Français</option>
            <option value="en">English</option>
            <option value="es">Espagnol</option>
            <option value="de">Allemand</option>
          </select>
        </label>
      </div>

      <h3 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">To</h3>
      <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
        <label class="flex flex-col min-w-40 flex-1">
          <select
            v-model="toLanguage"
            class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#111418] focus:outline-0 focus:ring-0 border border-[#dbe0e6] bg-white focus:border-[#dbe0e6] h-14 bg-[image:--select-button-svg] placeholder:text-[#60758a] p-[15px] text-base font-normal leading-normal"
          >
            <option value="fr">Français</option>
            <option value="en">English</option>
            <option value="es">Espagnol</option>
            <option value="de">Allemand</option>
            <option value="yacouba">Yacouba</option>
            <option value="guerré">Guérré</option>
            <option value="agni">Agni</option>
            <option value="dida">Dida</option>
          </select>
        </label>
      </div>
    </div>

    <div>
      <div class="flex gap-2 border-t border-[#f0f2f5] bg-white px-4 pb-3 pt-2">
        <button @click="goToHome" class="just flex flex-1 flex-col items-center justify-end gap-1 rounded-full text-[#111418]">
          <div class="text-[#111418] flex h-8 items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M224,115.55V208a16,16,0,0,1-16,16H168a16,16,0,0,1-16-16V168a8,8,0,0,0-8-8H112a8,8,0,0,0-8,8v40a16,16,0,0,1-16,16H48a16,16,0,0,1-16-16V115.55a16,16,0,0,1,5.17-11.78l80-75.48.11-.11a16,16,0,0,1,21.53,0,1.14,1.14,0,0,0,.11.11l80,75.48A16,16,0,0,1,224,115.55Z"
              ></path>
            </svg>
          </div>
          <p class="text-[#111418] text-xs font-medium leading-normal tracking-[0.015em]">Home</p>
        </button>
        <button @click="goToFavorites" class="just flex flex-1 flex-col items-center justify-end gap-1 text-[#60758a]">
          <div class="text-[#60758a] flex h-8 items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M184,32H72A16,16,0,0,0,56,48V224a8,8,0,0,0,12.24,6.78L128,193.43l59.77,37.35A8,8,0,0,0,200,224V48A16,16,0,0,0,184,32Zm0,16V161.57l-51.77-32.35a8,8,0,0,0-8.48,0L72,161.56V48ZM132.23,177.22a8,8,0,0,0-8.48,0L72,209.57V180.43l56-35,56,35v29.14Z"
              ></path>
            </svg>
          </div>
          <p class="text-[#60758a] text-xs font-medium leading-normal tracking-[0.015em]">Favorites</p>
        </button>
        <button @click="goToSettings" class="just flex flex-1 flex-col items-center justify-end gap-1 text-[#60758a]">
          <div class="text-[#60758a] flex h-8 items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M128,80a48,48,0,1,0,48,48A48.05,48.05,0,0,0,128,80Zm0,80a32,32,0,1,1,32-32A32,32,0,0,1,128,160Zm88-29.84q.06-2.16,0-4.32l14.92-18.64a8,8,0,0,0,1.48-7.06,107.21,107.21,0,0,0-10.88-26.25,8,8,0,0,0-6-3.93l-23.72-2.64q-1.48-1.56-3-3L186,40.54a8,8,0,0,0-3.94-6,107.71,107.71,0,0,0-26.25-10.87,8,8,0,0,0-7.06,1.49L130.16,40Q128,40,125.84,40L107.2,25.11a8,8,0,0,0-7.06-1.48A107.6,107.6,0,0,0,73.89,34.51a8,8,0,0,0-3.93,6L67.32,64.27q-1.56,1.49-3,3L40.54,70a8,8,0,0,0-6,3.94,107.71,107.71,0,0,0-10.87,26.25,8,8,0,0,0,1.49,7.06L40,125.84Q40,128,40,130.16L25.11,148.8a8,8,0,0,0-1.48,7.06,107.21,107.21,0,0,0,10.88,26.25,8,8,0,0,0,6,3.93l23.72,2.64q1.49,1.56,3,3L70,215.46a8,8,0,0,0,3.94,6,107.71,107.71,0,0,0,26.25,10.87,8,8,0,0,0,7.06-1.49L125.84,216q2.16.06,4.32,0l18.64,14.92a8,8,0,0,0,7.06,1.48,107.21,107.21,0,0,0,26.25-10.88,8,8,0,0,0,3.93-6l2.64-23.72q1.56-1.48,3-3L215.46,186a8,8,0,0,0,6-3.94,107.71,107.71,0,0,0,10.87-26.25,8,8,0,0,0-1.49-7.06Zm-16.1-6.5a73.93,73.93,0,0,1,0,8.68,8,8,0,0,0,1.74,5.48l14.19,17.73a91.57,91.57,0,0,1-6.23,15L187,173.11a8,8,0,0,0-5.1,2.64,74.11,74.11,0,0,1-6.14,6.14,8,8,0,0,0-2.64,5.1l-2.51,22.58a91.32,91.32,0,0,1-15,6.23l-17.74-14.19a8,8,0,0,0-5-1.75h-.48a73.93,73.93,0,0,1-8.68,0,8,8,0,0,0-5.48,1.74L100.45,215.8a91.57,91.57,0,0,1-15-6.23L82.89,187a8,8,0,0,0-2.64-5.1,74.11,74.11,0,0,1-6.14-6.14,8,8,0,0,0-5.1-2.64L46.43,170.6a91.32,91.32,0,0,1-6.23-15l14.19-17.74a8,8,0,0,0,1.74-5.48,73.93,73.93,0,0,1,0-8.68,8,8,0,0,0-1.74-5.48L40.2,100.45a91.57,91.57,0,0,1,6.23-15L69,82.89a8,8,0,0,0,5.1-2.64,74.11,74.11,0,0,1,6.14-6.14A8,8,0,0,0,82.89,69L85.4,46.43a91.32,91.32,0,0,1,15-6.23l17.74,14.19a8,8,0,0,0,5.48,1.74,73.93,73.93,0,0,1,8.68,0,8,8,0,0,0,5.48-1.74L155.55,40.2a91.57,91.57,0,0,1,15,6.23L173.11,69a8,8,0,0,0,2.64,5.1,74.11,74.11,0,0,1,6.14,6.14,8,8,0,0,0,5.1,2.64l22.58,2.51a91.32,91.32,0,0,1,6.23,15l-14.19,17.74A8,8,0,0,0,199.87,123.66Z"
              ></path>
            </svg>
          </div>
          <p class="text-[#60758a] text-xs font-medium leading-normal tracking-[0.015em]">Settings</p>
        </button>
      </div>
      <div class="h-5 bg-white"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TranslatePageSimple', // Nom distinct pour ce composant
  data() {
    return {
      // Langues par défaut, correspondant aux options HTML
      fromLanguage: 'auto-detect', // Ou 'fr' si vous voulez une détection automatique au démarrage
      toLanguage: 'fr',
      
      // La liste complète des langues pour l'affichage (similaire à page2.vue)
      // Note: Le HTML actuel n'utilise pas cette liste pour générer les <option>,
      // il faudrait une boucle v-for si vous vouliez la rendre dynamique.
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
    };
  },
  computed: {
    // Affiche le nom complet de la langue "From"
    fromLanguageDisplay() {
      const lang = this.allLanguages.find(l => l.value === this.fromLanguage);
      return lang ? lang.label : 'Auto-detect'; // Fallback si non trouvé
    },
    // Affiche le nom complet de la langue "To"
    toLanguageDisplay() {
      const lang = this.allLanguages.find(l => l.value === this.toLanguage);
      return lang ? lang.label : 'Français'; // Fallback si non trouvé
    },
  },
  methods: {
    // Méthode pour le bouton "X" en haut à gauche
    goBack() {
      console.log('Action: Go back or close translate view');
      // Ici, vous mettriez this.$router.back() ou this.$emit('close')
    },
    // Méthodes de navigation pour le footer
    goToHome() {
      console.log('Navigate to Home');
      // this.$router.push('/'); ou this.$emit('go-to-home')
    },
    goToFavorites() {
      console.log('Navigate to Favorites');
      // this.$router.push('/favorites');
    },
    goToSettings() {
      console.log('Navigate to Settings');
      // this.$router.push('/settings');
    },
    // Note: Les méthodes openLanguagePicker, selectLanguage, swapLanguages,
    // autoTranslate, addRecentTranslation, useMicrophone, useCamera,
    // speakTranslatedText, copyTranslatedText, viewRecent de page2.vue
    // ne sont pas présentes ici car les éléments HTML correspondants
    // (boutons d'échange, champs de texte, modale) sont absents du HTML fourni.
  },
  // La section <style scoped> n'est pas nécessaire ici car Tailwind gère tout avec les classes.
  // Cependant, si vous aviez des styles personnalisés en plus de Tailwind, ils iraient ici.
};
</script>

<style scoped>
/*
  Comme ce HTML utilise principalement Tailwind CSS, la section <style scoped>
  est moins essentielle que dans le précédent fichier .vue qui utilisait des classes
  CSS personnalisées et des variables.

  Cependant, si vous avez des styles qui NE SONT PAS couverts par Tailwind
  ou des surcharges spécifiques au composant, vous les placeriez ici.

  Par exemple, le style '--select-button-svg' qui est directement dans l'attribut style
  du div racine pourrait être géré via CSS pur si vous le souhaitiez.
*/
</style>