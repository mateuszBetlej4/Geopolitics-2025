<template>
  <div class="game-container">
    <div class="game-header">
      <div class="game-date">
        <h2>{{ gameState.date }}</h2>
      </div>
      <div class="game-controls">
        <button @click="pauseGame" :class="{ active: !gameRunning }">
          <span v-if="gameRunning">Pause</span>
          <span v-else>Resume</span>
        </button>
        <button
          @click="changeSpeed('slow')"
          :class="{ active: gameSpeed === 'slow' }"
        >
          Slow
        </button>
        <button
          @click="changeSpeed('normal')"
          :class="{ active: gameSpeed === 'normal' }"
        >
          Normal
        </button>
        <button
          @click="changeSpeed('fast')"
          :class="{ active: gameSpeed === 'fast' }"
        >
          Fast
        </button>
      </div>
    </div>

    <div class="game-content">
      <div class="sidebar">
        <div class="player-info">
          <h3>Your Nation</h3>
          <div class="nation-details" v-if="playerNation">
            <p><strong>Name:</strong> {{ playerNation.name }}</p>
            <p><strong>Leader:</strong> {{ playerNation.leader }}</p>
            <p>
              <strong>GDP:</strong> ${{
                formatNumber(playerNation.gdp)
              }}
              billion
            </p>
            <p>
              <strong>Military Power:</strong> {{ playerNation.military_power }}
            </p>
          </div>
        </div>

        <div class="actions-panel">
          <h3>Actions</h3>
          <button class="action-btn">Military</button>
          <button class="action-btn">Economy</button>
          <button class="action-btn">Diplomacy</button>
          <button class="action-btn">Research</button>
          <button class="action-btn">Intelligence</button>
        </div>
      </div>

      <div class="main-view">
        <div class="world-map">
          <!-- This would be replaced with an actual map component -->
          <div class="map-placeholder">
            <p>World Map</p>
            <p>Interactive map will be displayed here</p>
          </div>
        </div>
      </div>

      <div class="info-panel">
        <div class="tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="{ active: activeTab === tab.id }"
          >
            {{ tab.name }}
          </button>
        </div>

        <div class="tab-content">
          <div v-if="activeTab === 'nations'" class="nations-list">
            <h3>World Nations</h3>
            <div
              v-for="nation in gameState.nations"
              :key="nation.name"
              class="nation-item"
            >
              <h4>{{ nation.name }}</h4>
              <p><strong>Leader:</strong> {{ nation.leader }}</p>
              <p>
                <strong>GDP:</strong> ${{ formatNumber(nation.gdp) }} billion
              </p>
              <p><strong>Military:</strong> {{ nation.military_power }}</p>
            </div>
          </div>

          <div v-if="activeTab === 'events'" class="events-list">
            <h3>Recent Events</h3>
            <p>No events yet</p>
          </div>

          <div v-if="activeTab === 'alliances'" class="alliances-list">
            <h3>Current Alliances</h3>
            <p>No alliances formed yet</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";

// Game state
const gameState = ref({
  date: "January 1, 2025",
  nations: [],
});

// Game controls
const gameRunning = ref(false);
const gameSpeed = ref("normal");

// UI state
const activeTab = ref("nations");
const tabs = [
  { id: "nations", name: "Nations" },
  { id: "events", name: "Events" },
  { id: "alliances", name: "Alliances" },
];

// Computed properties
const playerNation = computed(() => {
  return gameState.value.nations.find(
    (nation) => nation.name === "United States"
  );
});

// Methods
const pauseGame = () => {
  gameRunning.value = !gameRunning.value;
};

const changeSpeed = (speed) => {
  gameSpeed.value = speed;
};

const formatNumber = (num) => {
  return num.toLocaleString();
};

// Fetch initial game state
onMounted(async () => {
  try {
    const response = await fetch("/api/game-state");
    const data = await response.json();
    gameState.value = data;
  } catch (error) {
    console.error("Failed to fetch game state:", error);
  }
});
</script>

<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--primary-color);
  color: white;
}

.game-controls button {
  background-color: #34495e;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
}

.game-controls button.active {
  background-color: var(--secondary-color);
}

.game-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  background-color: #ecf0f1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.player-info,
.actions-panel {
  margin-bottom: 1.5rem;
}

.action-btn {
  display: block;
  width: 100%;
  padding: 0.8rem;
  margin-bottom: 0.5rem;
  background-color: var(--secondary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-align: left;
}

.action-btn:hover {
  background-color: #2980b9;
}

.main-view {
  flex: 1;
  padding: 1rem;
  overflow: hidden;
}

.world-map {
  height: 100%;
  background-color: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.map-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: #ddd;
  color: #555;
  font-size: 1.5rem;
  text-align: center;
}

.info-panel {
  width: 300px;
  background-color: #ecf0f1;
  display: flex;
  flex-direction: column;
}

.tabs {
  display: flex;
  background-color: #34495e;
}

.tabs button {
  flex: 1;
  background-color: transparent;
  color: white;
  border: none;
  padding: 0.8rem;
  cursor: pointer;
}

.tabs button.active {
  background-color: var(--secondary-color);
}

.tab-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.nation-item {
  background-color: white;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nation-item h4 {
  margin-bottom: 0.5rem;
  color: var(--primary-color);
}

@media (max-width: 1200px) {
  .game-content {
    flex-direction: column;
  }

  .sidebar,
  .info-panel {
    width: 100%;
    max-height: 200px;
  }

  .main-view {
    height: 400px;
  }
}
</style>
