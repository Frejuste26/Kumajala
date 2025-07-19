<template>
  <div
    class="relative flex size-full min-h-screen flex-col bg-white justify-between group/design-root overflow-x-hidden"
    style='font-family: "Spline Sans", "Noto Sans", sans-serif;'
  >
    <div>
      <div class="flex items-center bg-white p-4 pb-2 justify-between">
        <button @click="goBack" class="text-[#111418] flex size-12 shrink-0 items-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
            <path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path>
          </svg>
        </button>
        <h2 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">Settings</h2>
      </div>

      <h3 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Appearance</h3>
      <button @click="changeTheme" class="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2 justify-between w-full">
        <div class="flex flex-col justify-center text-left">
          <p class="text-[#111418] text-base font-medium leading-normal line-clamp-1">Theme</p>
          <p class="text-[#60758a] text-sm font-normal leading-normal line-clamp-2">System</p>
        </div>
        <div class="shrink-0"><p class="text-[#111418] text-base font-normal leading-normal">{{ currentTheme }}</p></div>
      </button>

      <h3 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Language</h3>
      <button @click="changeAppLanguage" class="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2 justify-between w-full">
        <div class="flex flex-col justify-center text-left">
          <p class="text-[#111418] text-base font-medium leading-normal line-clamp-1">App language</p>
          <p class="text-[#60758a] text-sm font-normal leading-normal line-clamp-2">{{ appLanguageDisplay }}</p>
        </div>
        <div class="shrink-0"><p class="text-[#111418] text-base font-normal leading-normal">{{ appLanguageDisplay }}</p></div>
      </button>

      <h3 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Audio</h3>
      <button @click="togglePlayAudio" class="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2 justify-between w-full">
        <div class="flex flex-col justify-center text-left">
          <p class="text-[#111418] text-base font-medium leading-normal line-clamp-1">Play audio</p>
          <p class="text-[#60758a] text-sm font-normal leading-normal line-clamp-2">{{ playAudioStatus }}</p>
        </div>
        <div class="shrink-0"><p class="text-[#111418] text-base font-normal leading-normal">{{ playAudioStatus }}</p></div>
      </button>
      <button @click="changeVoice" class="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2 justify-between w-full">
        <div class="flex flex-col justify-center text-left">
          <p class="text-[#111418] text-base font-medium leading-normal line-clamp-1">Voice</p>
          <p class="text-[#60758a] text-sm font-normal leading-normal line-clamp-2">System</p>
        </div>
        <div class="shrink-0"><p class="text-[#111418] text-base font-normal leading-normal">{{ currentVoice }}</p></div>
      </button>

      <h3 class="text-[#111418] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Offline</h3>
      <button @click="downloadLanguages" class="flex items-center gap-4 bg-white px-4 min-h-14 justify-between w-full">
        <p class="text-[#111418] text-base font-normal leading-normal flex-1 truncate text-left">Download languages</p>
        <div class="shrink-0 text-[#111418] flex size-7 items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
            <path d="M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z"></path>
          </svg>
        </div>
      </button>
    </div>

    <div>
      <div class="flex gap-2 border-t border-[#f0f2f5] bg-white px-4 pb-3 pt-2">
        <button @click="goToHome" :class="['just flex flex-1 flex-col items-center justify-end gap-1', activeFooterTab === 'home' ? 'text-[#111418]' : 'text-[#60758a]']">
          <div :class="['flex h-8 items-center justify-center', activeFooterTab === 'home' ? 'text-[#111418]' : 'text-[#60758a]']">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M218.83,103.77l-80-75.48a1.14,1.14,0,0,1-.11-.11,16,16,0,0,0-21.53,0l-.11.11L37.17,103.77A16,16,0,0,0,32,115.55V208a16,16,0,0,0,16,16H96a16,16,0,0,0,16-16V160h32v48a16,16,0,0,0,16,16h48a16,16,0,0,0,16-16V115.55A16,16,0,0,0,218.83,103.77ZM208,208H160V160a16,16,0,0,0-16-16H112a16,16,0,0,0-16,16v48H48V115.55l.11-.1L128,40l79.9,75.43.11.1Z"
              ></path>
            </svg>
          </div>
          <p :class="['text-xs font-medium leading-normal tracking-[0.015em]', activeFooterTab === 'home' ? 'text-[#111418]' : 'text-[#60758a]']">Home</p>
        </button>
        <button @click="goToFavorites" :class="['just flex flex-1 flex-col items-center justify-end gap-1', activeFooterTab === 'favorites' ? 'text-[#111418]' : 'text-[#60758a]']">
          <div :class="['flex h-8 items-center justify-center', activeFooterTab === 'favorites' ? 'text-[#111418]' : 'text-[#60758a]']">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M184,32H72A16,16,0,0,0,56,48V224a8,8,0,0,0,12.24,6.78L128,193.43l59.77,37.35A8,8,0,0,0,200,224V48A16,16,0,0,0,184,32Zm0,16V161.57l-51.77-32.35a8,8,0,0,0-8.48,0L72,161.56V48ZM132.23,177.22a8,8,0,0,0-8.48,0L72,209.57V180.43l56-35,56,35v29.14Z"
              ></path>
            </svg>
          </div>
          <p :class="['text-xs font-medium leading-normal tracking-[0.015em]', activeFooterTab === 'favorites' ? 'text-[#111418]' : 'text-[#60758a]']">Favorites</p>
        </button>
        <button @click="goToSettings" :class="['just flex flex-1 flex-col items-center justify-end gap-1 rounded-full', activeFooterTab === 'settings' ? 'text-[#111418]' : 'text-[#60758a]']">
          <div :class="['flex h-8 items-center justify-center', activeFooterTab === 'settings' ? 'text-[#111418]' : 'text-[#60758a]']">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path
                d="M216,130.16q.06-2.16,0-4.32l14.92-18.64a8,8,0,0,0,1.48-7.06,107.6,107.6,0,0,0-10.88-26.25,8,8,0,0,0-6-3.93l-23.72-2.64q-1.48-1.56-3-3L186,40.54a8,8,0,0,0-3.94-6,107.29,107.29,0,0,0-26.25-10.86,8,8,0,0,0-7.06,1.48L130.16,40Q128,40,125.84,40L107.2,25.11a8,8,0,0,0-7.06-1.48A107.6,107.6,0,0,0,73.89,34.51a8,8,0,0,0-3.93,6L67.32,64.27q-1.56,1.49-3,3L40.54,70a8,8,0,0,0-6,3.94,107.71,107.71,0,0,0-10.87,26.25,8,8,0,0,0,1.49,7.06L40,125.84Q40,128,40,130.16L25.11,148.8a8,8,0,0,0-1.48,7.06,107.6,107.6,0,0,0,10.88,26.25,8,8,0,0,0,6,3.93l23.72,2.64q1.49,1.56,3,3L70,215.46a8,8,0,0,0,3.94,6,107.71,107.71,0,0,0,26.25,10.87,8,8,0,0,0,7.06-1.49L125.84,216q2.16.06,4.32,0l18.64,14.92a8,8,0,0,0,7.06,1.48,107.21,107.21,0,0,0,26.25-10.88,8,8,0,0,0,3.93-6l2.64-23.72q1.56-1.48,3-3L215.46,186a8,8,0,0,0,6-3.94,107.71,107.71,0,0,0,10.87-26.25,8,8,0,0,0-1.49-7.06ZM128,168a40,40,0,1,1,40-40A40,40,0,0,1,128,168Z"
              ></path>
            </svg>
          </div>
          <p :class="['text-xs font-medium leading-normal tracking-[0.015em]', activeFooterTab === 'settings' ? 'text-[#111418]' : 'text-[#60758a]']">Settings</p>
        </button>
      </div>
      <div class="h-5 bg-white"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsPage',
  data() {
    return {
      currentTheme: 'Light', // Could be 'Light', 'Dark', 'System'
      appLanguage: 'en',     // Could be 'en', 'fr', 'es', etc.
      playAudio: true,       // Boolean for toggle
      currentVoice: 'System', // Could be 'System', 'Male', 'Female', etc.
      activeFooterTab: 'settings', // To highlight the active tab in the footer
    };
  },
  computed: {
    appLanguageDisplay() {
      // Return a more user-friendly string based on the appLanguage code
      const languages = {
        'en': 'English',
        'fr': 'French',
        'es': 'Spanish',
        // Add more as needed
      };
      return languages[this.appLanguage] || 'Unknown';
    },
    playAudioStatus() {
      return this.playAudio ? 'Always' : 'Never';
    }
  },
  methods: {
    goBack() {
      console.log('Navigating back...');
      // In a real Vue app with Vue Router, you would use:
      // this.$router.go(-1); or this.$router.back();
    },
    changeTheme() {
      // Simulate changing theme; in a real app, this would open a modal/selection
      const themes = ['Light', 'Dark', 'System'];
      const currentIndex = themes.indexOf(this.currentTheme);
      this.currentTheme = themes[(currentIndex + 1) % themes.length];
      alert(`Theme changed to: ${this.currentTheme}`);
    },
    changeAppLanguage() {
      // Simulate changing language; in a real app, this would open a language selection list
      const languages = ['en', 'fr', 'es'];
      const currentIndex = languages.indexOf(this.appLanguage);
      this.appLanguage = languages[(currentIndex + 1) % languages.length];
      alert(`App language changed to: ${this.appLanguageDisplay}`);
    },
    togglePlayAudio() {
      this.playAudio = !this.playAudio;
      alert(`Play audio set to: ${this.playAudioStatus}`);
    },
    changeVoice() {
      // Simulate changing voice; in a real app, this would open a voice selection list
      const voices = ['System', 'Male', 'Female', 'Assistant'];
      const currentIndex = voices.indexOf(this.currentVoice);
      this.currentVoice = voices[(currentIndex + 1) % voices.length];
      alert(`Voice changed to: ${this.currentVoice}`);
    },
    downloadLanguages() {
      console.log('Navigating to Download Languages section/page...');
      alert('Opening language download options...');
      // In a real app, this might navigate to a specific page or open a modal
      // this.$router.push('/settings/download-languages');
    },
    goToHome() {
      this.activeFooterTab = 'home';
      console.log('Navigate to Home');
      // this.$router.push('/');
    },
    goToFavorites() {
      this.activeFooterTab = 'favorites';
      console.log('Navigate to Favorites');
      // this.$router.push('/favorites');
    },
    goToSettings() {
      this.activeFooterTab = 'settings'; // Already on settings, but good for explicit state
      console.log('Navigate to Settings');
      // this.$router.push('/settings');
    },
  },
};
</script>

<style scoped>
/* Tailwind CSS is used for styling. No additional scoped CSS needed for this structure. */
</style>