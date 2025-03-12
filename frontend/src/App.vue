<template>
  <div :class="['app-container', isFullScreenPage ? 'fullscreen-page' : '']">
    <header class="app-header" v-if="!isFullScreenPage">
      <h1>Geopolitics 2025</h1>
      <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/game">Play Game</router-link> |
        <router-link to="/settings">Settings</router-link>
      </nav>
    </header>

    <main class="app-content">
      <router-view />
    </main>

    <footer class="app-footer" v-if="!isFullScreenPage">
      <p>&copy; 2025 Geopolitics Strategy Game</p>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// Check if current page should be fullscreen (no header/footer)
const isFullScreenPage = computed(() => {
  return route.path === '/game' || route.path === '/settings' || route.path === '/';
});
</script>

<style>
/* Global styles */
:root {
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --accent-color: #e74c3c;
  --background-color: #f5f5f5;
  --text-color: #333;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Arial", sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  line-height: 1.6;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  height: 100vh;
  overflow: hidden;
}

.app-header {
  background-color: var(--primary-color);
  color: white;
  padding: 0.5rem;
  text-align: center;
  height: 60px;
}

.app-header h1 {
  margin-bottom: 0.5rem;
}

.app-header nav {
  margin-top: 0.5rem;
}

.app-header a {
  color: white;
  text-decoration: none;
  margin: 0 0.5rem;
}

.app-header a.router-link-active {
  font-weight: bold;
  color: var(--secondary-color);
}

.app-content {
  flex: 1;
  padding: 0;
  max-width: 100%;
  margin: 0;
  width: 100%;
  overflow: hidden;
  display: flex;
}

.app-footer {
  background-color: var(--primary-color);
  color: white;
  text-align: center;
  padding: 0.5rem;
  height: 40px;
}

/* Fullscreen page styling (no header/footer) */
.fullscreen-page .app-content {
  height: 100vh;
}
</style>
