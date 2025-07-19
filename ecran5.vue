<template>
  <div
    class="relative flex size-full min-h-screen flex-col bg-white justify-between group/design-root overflow-x-hidden"
    style='font-family: "Spline Sans", "Noto Sans", sans-serif;'
  >
    <div>
      <div class="flex items-center bg-white p-4 pb-2 justify-between">
        <h2 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pl-12">Saved</h2>
        <div class="flex w-12 items-center justify-end">
          <button
            @click="addNewItem"
            class="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-12 bg-transparent text-[#111418] gap-2 text-base font-bold leading-normal tracking-[0.015em] min-w-0 p-0"
          >
            <div class="text-[#111418]">
              <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                <path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path>
              </svg>
            </div>
          </button>
        </div>
      </div>

      <div class="pb-3">
        <div class="flex border-b border-[#dbe0e6] px-4 gap-8">
          <button
            @click="setActiveTab('words')"
            :class="[
              'flex flex-col items-center justify-center pb-[13px] pt-4',
              activeTab === 'words' ? 'border-b-[3px] border-b-[#111418] text-[#111418]' : 'border-b-[3px] border-b-transparent text-[#60758a]'
            ]"
          >
            <p :class="['text-sm font-bold leading-normal tracking-[0.015em]', activeTab === 'words' ? 'text-[#111418]' : 'text-[#60758a]']">Words</p>
          </button>
          <button
            @click="setActiveTab('phrases')"
            :class="[
              'flex flex-col items-center justify-center pb-[13px] pt-4',
              activeTab === 'phrases' ? 'border-b-[3px] border-b-[#111418] text-[#111418]' : 'border-b-[3px] border-b-transparent text-[#60758a]'
            ]"
          >
            <p :class="['text-sm font-bold leading-normal tracking-[0.015em]', activeTab === 'phrases' ? 'text-[#111418]' : 'text-[#60758a]']">Phrases</p>
          </button>
          <button
            @click="setActiveTab('themes')"
            :class="[
              'flex flex-col items-center justify-center pb-[13px] pt-4',
              activeTab === 'themes' ? 'border-b-[3px] border-b-[#111418] text-[#111418]' : 'border-b-[3px] border-b-transparent text-[#60758a]'
            ]"
          >
            <p :class="['text-sm font-bold leading-normal tracking-[0.015em]', activeTab === 'themes' ? 'text-[#111418]' : 'text-[#60758a]']">Themes</p>
          </button>
        </div>
      </div>

      <div v-if="filteredItems.length">
        <div
          v-for="item in filteredItems"
          :key="item.id"
          class="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2 border-b border-[#f0f2f5] last:border-b-0"
          @click="selectItem(item)"
        >
          <div class="text-[#111418] flex items-center justify-center rounded-lg bg-[#f0f2f5] shrink-0 size-12">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M239.2,97.29a16,16,0,0,0-13.81-11L166,81.17,142.72,25.81h0a15.95,15.95,0,0,0-29.44,0L90.07,81.17,30.61,86.32a16,16,0,0,0-9.11,28.06L66.61,153.8,53.09,212.34a16,16,0,0,0,23.84,17.34l51-31,51.11,31a16,16,0,0,0,23.84-17.34l-13.51-58.6,45.1-39.36A16,16,0,0,0,239.2,97.29Zm-15.22,5-45.1,39.36a16,16,0,0,0-5.08,15.71L187.35,216v0l-51.07-31a15.9,15.9,0,0,0-16.54,0l-51,31h0L82.2,157.4a16,16,0,0,0-5.08-15.71L32,102.35a.37.37,0,0,1,0-.09l59.44-5.14a16,16,0,0,0,13.35-9.75L128,32.08l23.2,55.29a16,16,0,0,0,13.35,9.75L224,102.26S224,102.32,224,102.33Z"
              ></path>
            </svg>
          </div>
          <div class="flex flex-col justify-center flex-1">
            <p class="text-[#111418] text-base font-medium leading-normal line-clamp-1">{{ item.text }}</p>
            <p class="text-[#60758a] text-sm font-normal leading-normal line-clamp-2">{{ item.language }}</p>
          </div>
        </div>
      </div>
      <div v-else class="text-center text-[#60758a] p-8">
        No items saved for {{ activeTab }} yet.
      </div>
    </div>

    <div>
      <div class="flex gap-2 border-t border-[#f0f2f5] bg-white px-4 pb-3 pt-2">
        <button @click="goToHome" class="just flex flex-1 flex-col items-center justify-end gap-1 text-[#60758a]">
          <div class="text-[#60758a] flex h-8 items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M218.83,103.77l-80-75.48a1.14,1.14,0,0,1-.11-.11,16,16,0,0,0-21.53,0l-.11.11L37.17,103.77A16,16,0,0,0,32,115.55V208a16,16,0,0,0,16,16H96a16,16,0,0,0,16-16V160h32v48a16,16,0,0,0,16,16h48a16,16,0,0,0,16-16V115.55A16,16,0,0,0,218.83,103.77ZM208,208H160V160a16,16,0,0,0-16-16H112a16,16,0,0,0-16,16v48H48V115.55l.11-.1L128,40l79.9,75.43.11.1Z"
              ></path>
            </svg>
          </div>
          <p class="text-[#60758a] text-xs font-medium leading-normal tracking-[0.015em]">Home</p>
        </button>
        <button @click="goToFavorites" class="just flex flex-1 flex-col items-center justify-end gap-1 rounded-full text-[#111418]">
          <div class="text-[#111418] flex h-8 items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M234.5,114.38l-45.1,39.36,13.51,58.6a16,16,0,0,1-23.84,17.34l-51.11-31-51,31a16,16,0,0,1-23.84-17.34L66.61,153.8,21.5,114.38a16,16,0,0,1,9.11-28.06l59.46-5.15,23.21-55.36a15.95,15.95,0,0,1,29.44,0h0L166,81.17l59.44,5.15a16,16,0,0,1,9.11,28.06Z"
              ></path>
            </svg>
          </div>
          <p class="text-[#111418] text-xs font-medium leading-normal tracking-[0.015em]">Favorites</p>
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
  name: 'SavedItemsPage',
  data() {
    return {
      activeTab: 'words', // 'words', 'phrases', 'themes'
      savedItems: [
        { id: 1, type: 'words', text: 'Hola', language: 'Spanish' },
        { id: 2, type: 'words', text: 'Bonjour', language: 'French' },
        { id: 3, type: 'words', text: 'Hallo', language: 'German' },
        { id: 4, type: 'words', text: 'Ciao', language: 'Italian' },
        { id: 5, type: 'words', text: 'Konnichiwa', language: 'Japanese' },
        { id: 6, type: 'phrases', text: 'How are you?', language: 'English' },
        { id: 7, type: 'phrases', text: 'Comment allez-vous?', language: 'French' },
        { id: 8, type: 'themes', text: 'Travel Greetings', language: 'General' },
      ],
    };
  },
  computed: {
    // Filtrer les éléments affichés en fonction de l'onglet actif
    filteredItems() {
      return this.savedItems.filter(item => item.type === this.activeTab);
    }
  },
  methods: {
    addNewItem() {
      // Simule l'ajout d'un nouvel élément
      const newItem = prompt(`Add a new ${this.activeTab} (e.g., "Hello,English"):`);
      if (newItem) {
        const [text, language] = newItem.split(',');
        if (text && language) {
          this.savedItems.push({
            id: this.savedItems.length + 1,
            type: this.activeTab,
            text: text.trim(),
            language: language.trim()
          });
          alert(`"${text.trim()}" added to ${this.activeTab}!`);
        } else {
          alert('Invalid format. Please use "Text,Language".');
        }
      }
      console.log('Add new item');
    },
    setActiveTab(tabName) {
      this.activeTab = tabName;
      console.log(`Active tab set to: ${tabName}`);
    },
    selectItem(item) {
      alert(`Selected: "${item.text}" (${item.language}) - Type: ${item.type}`);
      console.log('Selected item:', item);
      // Ici, vous implémenteriez la logique pour afficher les détails de l'élément
      // ou effectuer une autre action (par exemple, naviguer vers une page de détails).
    },
    goToHome() {
      console.log('Navigate to Home');
      // this.$router.push('/');
    },
    goToFavorites() {
      console.log('Navigate to Favorites');
      // this.$router.push('/favorites'); // Note: This page IS the favorites/saved page.
                                        // This would likely navigate to a main dashboard or home.
    },
    goToSettings() {
      console.log('Navigate to Settings');
      // this.$router.push('/settings');
    },
  },
};
</script>

<style scoped>
/*
  Comme les exemples précédents, ce composant utilise principalement Tailwind CSS.
  La section <style scoped> est ici pour des ajouts spécifiques si nécessaire,
  mais la mise en page et l'apparence de base sont gérées par les classes utilitaires.
*/
</style>