import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Translator from '@/views/Translator.vue';
import Setting from '@/views/Setting.vue'; 
import About from '@/views/About.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/translator',
    name: 'Translator',
    component: Translator,
  },
  {
    path: '/settings', 
    name: 'Settings',
    component: Setting,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
