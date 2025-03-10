import { createRouter, createWebHistory } from 'vue-router';

// Import views
// We'll use lazy loading for better performance
const HomeView = () => import('../views/HomeView.vue');
const GameView = () => import('../views/GameView.vue');
const SettingsView = () => import('../views/SettingsView.vue');

// Define routes
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Home - Geopolitics 2025' }
  },
  {
    path: '/game',
    name: 'game',
    component: GameView,
    meta: { title: 'Play Game - Geopolitics 2025' }
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
    meta: { title: 'Settings - Geopolitics 2025' }
  },
  {
    // Catch-all route for 404
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard to set page title
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Geopolitics 2025';
  next();
});

export default router; 