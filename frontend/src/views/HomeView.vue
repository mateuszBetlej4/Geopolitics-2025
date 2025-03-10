<template>
  <div class="home-container">
    <div class="hero-section">
      <h1>Geopolitics 2025</h1>
      <p class="tagline">
        Shape the future of global politics in this real-time strategy game
      </p>
      <div class="cta-buttons">
        <router-link to="/game" class="btn btn-primary">Start Game</router-link>
        <router-link to="/settings" class="btn btn-secondary"
          >Settings</router-link
        >
      </div>
    </div>

    <div class="features-section">
      <h2>Game Features</h2>
      <div class="features-grid">
        <div class="feature-card">
          <h3>Military Expansion</h3>
          <p>
            Build powerful armies, navies, and air forces to project your
            nation's power globally.
          </p>
        </div>
        <div class="feature-card">
          <h3>Economic Development</h3>
          <p>
            Grow your GDP, establish trade agreements, and impose sanctions on
            rival nations.
          </p>
        </div>
        <div class="feature-card">
          <h3>Diplomacy & Alliances</h3>
          <p>
            Form strategic partnerships, negotiate treaties, and manage
            international relations.
          </p>
        </div>
        <div class="feature-card">
          <h3>Nuclear Deterrence</h3>
          <p>
            Develop nuclear capabilities as the ultimate deterrent, but use with
            extreme caution.
          </p>
        </div>
      </div>
    </div>

    <div class="nations-section">
      <h2>Playable Nations</h2>
      <div class="nations-grid">
        <div class="nation-card" v-for="nation in nations" :key="nation.name">
          <h3>{{ nation.name }}</h3>
          <p><strong>Leader:</strong> {{ nation.leader }}</p>
          <p>{{ nation.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// Sample data for nations
const nations = ref([
  {
    name: "United States",
    leader: "Donald Trump",
    description:
      "Global superpower with the strongest military and largest economy.",
  },
  {
    name: "China",
    leader: "Li Qiang",
    description:
      "Rising economic powerhouse with growing military capabilities.",
  },
  {
    name: "Russia",
    leader: "Vladimir Putin",
    description:
      "Military power with vast nuclear arsenal and resource-rich territory.",
  },
  {
    name: "India",
    leader: "Narendra Modi",
    description:
      "Rapidly developing nation with large population and growing influence.",
  },
]);
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.hero-section {
  text-align: center;
  margin-bottom: 3rem;
  padding: 3rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border-radius: 8px;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.tagline {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: var(--secondary-color);
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.features-section,
.nations-section {
  margin-bottom: 3rem;
}

.features-section h2,
.nations-section h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--primary-color);
}

.features-grid,
.nations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card,
.nation-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.feature-card h3,
.nation-card h3 {
  color: var(--primary-color);
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2rem;
  }

  .tagline {
    font-size: 1.2rem;
  }

  .features-grid,
  .nations-grid {
    grid-template-columns: 1fr;
  }
}
</style>
