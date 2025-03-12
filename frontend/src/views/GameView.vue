<template>
  <div class="game-container hoi4-style">
    <!-- Top Bar -->
    <div class="top-bar">
      <div class="date-display">
        <span class="date-icon">📅</span>
        <h2>{{ gameState.date }}</h2>
      </div>
      
      <div class="resource-display">
        <div class="resource">
          <span class="resource-icon">💰</span>
          <span class="resource-value">${{ formatNumber(playerNation?.gdp || 0) }}B</span>
        </div>
        <div class="resource">
          <span class="resource-icon">🛢️</span>
          <span class="resource-value">{{ playerNation?.resources?.oil || 0 }}</span>
        </div>
        <div class="resource">
          <span class="resource-icon">⚙️</span>
          <span class="resource-value">{{ playerNation?.resources?.steel || 0 }}</span>
        </div>
        <div class="resource">
          <span class="resource-icon">🔋</span>
          <span class="resource-value">{{ playerNation?.resources?.electricity || 0 }}</span>
        </div>
      </div>

      <div class="speed-controls">
        <button @click="pauseGame" :class="{ active: !gameRunning }">
          <span v-if="gameRunning">⏸️</span>
          <span v-else>▶️</span>
        </button>
        <button
          @click="changeSpeed('slow')"
          :class="{ active: gameSpeed === 'slow' }"
        >
          1
        </button>
        <button
          @click="changeSpeed('normal')"
          :class="{ active: gameSpeed === 'normal' }"
        >
          2
        </button>
        <button
          @click="changeSpeed('fast')"
          :class="{ active: gameSpeed === 'fast' }"
        >
          3
        </button>
        <button @click="toggleGameMenu" class="menu-button">
          <span>☰ Menu</span>
        </button>
      </div>
    </div>

    <!-- Game Content Area -->
    <div class="main-content">
      <!-- Left Sidebar -->
      <div class="left-sidebar">
        <div class="country-info panel">
          <div class="country-flag" v-if="playerNation">
            <h3>{{ playerNation.name }}</h3>
            <p class="leader-name">{{ playerNation.leader }}</p>
          </div>
          
          <div class="country-stats">
            <div class="stat-item">
              <span class="stat-label">GDP:</span>
              <span class="stat-value">${{ formatNumber(playerNation?.gdp || 0) }}B</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Military Power:</span>
              <span class="stat-value">{{ playerNation?.military_power || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Stability:</span>
              <span class="stat-value">{{ playerNation?.stability || 70 }}%</span>
            </div>
          </div>
        </div>
        
        <div class="action-categories panel">
          <h3>Decision Categories</h3>
          <button class="category-btn">
            <span class="btn-icon">🌐</span>
            <span class="btn-text">Diplomacy</span>
          </button>
          <button class="category-btn">
            <span class="btn-icon">🔬</span>
            <span class="btn-text">Research</span>
          </button>
          <button class="category-btn">
            <span class="btn-icon">⚔️</span>
            <span class="btn-text">Military</span>
          </button>
          <button class="category-btn">
            <span class="btn-icon">��</span>
            <span class="btn-text">Economy</span>
          </button>
          <button class="category-btn">
            <span class="btn-icon">🔍</span>
            <span class="btn-text">Intelligence</span>
          </button>
        </div>
      </div>

      <!-- Map Area -->
      <div class="map-area">
        <Map 
          :nations="gameState.nations" 
          @country-selected="handleCountrySelected"
        />

        <!-- Alerts Bar -->
        <div class="alerts-bar">
          <div class="alert" v-if="gameState.alerts && gameState.alerts.length">
            <span class="alert-icon">⚠️</span>
            <span class="alert-text">{{ gameState.alerts[0] }}</span>
          </div>
          <div class="alert" v-else>
            <span class="alert-icon">✓</span>
            <span class="alert-text">No current alerts</span>
          </div>
        </div>
      </div>

      <!-- Right Sidebar -->
      <div class="right-sidebar">
        <div class="tabs-container">
          <div class="tabs-header">
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
              <div class="nations-header">
                <span class="col">Nation</span>
                <span class="col">GDP</span>
                <span class="col">Military</span>
              </div>
              <div
                v-for="nation in gameState.nations"
                :key="nation.name"
                class="nation-row"
                @click="handleCountrySelected(nation)"
              >
                <span class="col nation-name">{{ nation.name }}</span>
                <span class="col">${{ formatNumber(nation.gdp) }}B</span>
                <span class="col">{{ nation.military_power }}</span>
              </div>
            </div>

            <div v-if="activeTab === 'events'" class="events-list">
              <div class="event" v-if="!gameState.events || !gameState.events.length">
                <p>No recent events</p>
              </div>
              <div 
                v-else
                v-for="(event, index) in gameState.events" 
                :key="index"
                class="event"
              >
                <div class="event-header">
                  <span class="event-date">{{ event.date }}</span>
                  <span class="event-type">{{ event.type }}</span>
                </div>
                <div class="event-content">
                  {{ event.description }}
                </div>
              </div>
            </div>

            <div v-if="activeTab === 'alliances'" class="alliances-list">
              <div class="alliance" v-if="!gameState.alliances || !gameState.alliances.length">
                <p>No current alliances</p>
              </div>
              <div 
                v-else
                v-for="(alliance, index) in gameState.alliances" 
                :key="index"
                class="alliance"
              >
                <div class="alliance-header">
                  <span class="alliance-name">{{ alliance.name }}</span>
                </div>
                <div class="alliance-members">
                  <div 
                    v-for="member in alliance.members" 
                    :key="member"
                    class="alliance-member"
                  >
                    {{ member }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Bar -->
    <div class="bottom-bar">
      <div class="construction-queue">
        <h3>Construction</h3>
        <div class="queue-items">
          <div class="queue-item" v-if="playerNation?.constructionQueue?.length">
            <span class="item-name">Military Factory</span>
            <div class="progress-bar">
              <div class="progress" style="width: 60%"></div>
            </div>
            <span class="time-left">15 days</span>
          </div>
          <div class="empty-queue" v-else>
            <span>No construction in progress</span>
          </div>
        </div>
      </div>
      <div class="production-queue">
        <h3>Production</h3>
        <div class="queue-items">
          <div class="queue-item" v-if="playerNation?.productionQueue?.length">
            <span class="item-name">Main Battle Tanks</span>
            <div class="progress-bar">
              <div class="progress" style="width: 45%"></div>
            </div>
            <span class="time-left">30 days</span>
          </div>
          <div class="empty-queue" v-else>
            <span>No production in progress</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Game Menu Overlay -->
    <div v-if="showGameMenu" class="game-menu-overlay">
      <div class="game-menu">
        <h2>Game Menu</h2>
        <div class="menu-buttons">
          <button @click="resumeGame" class="menu-btn resume-btn">
            <span class="menu-icon">▶️</span>
            Resume Game
          </button>
          <button @click="toggleSaveMenu" class="menu-btn save-btn">
            <span class="menu-icon">💾</span>
            Save/Load Game
          </button>
          <button @click="exitToMenu" class="menu-btn exit-btn">
            <span class="menu-icon">🚪</span>
            Exit to Main Menu
          </button>
        </div>
        <div class="menu-help">
          <p>Press <kbd>ESC</kbd> to toggle menu</p>
          <p>Press <kbd>F5</kbd> for quick save</p>
        </div>
      </div>
    </div>
    
    <!-- Save Game Modal -->
    <div v-if="showSaveMenu" class="save-modal">
      <div class="save-modal-content">
        <h3>Save/Load Game</h3>
        
        <div class="save-section">
          <h4>Save Current Game</h4>
          <div class="save-options">
            <div class="save-input">
              <input 
                v-model="saveName" 
                placeholder="Enter save name" 
                @keyup.enter="saveGame"
              />
              <button @click="saveGame" :disabled="!saveName">Save</button>
            </div>
            <div class="quick-save">
              <button @click="quickSave" class="quick-save-btn">Quick Save</button>
              <span class="quick-save-info" v-if="lastQuickSave">Last: {{ formatSaveDate(lastQuickSave) }}</span>
            </div>
          </div>
        </div>
        
        <div class="load-section">
          <h4>Load Saved Game</h4>
          <div v-if="savedGames.length === 0" class="no-saves">
            No saved games found
          </div>
          <div v-else class="saved-games-list">
            <div 
              v-for="(save, index) in savedGames" 
              :key="index"
              class="saved-game-item"
              :class="{ 'quick-save-item': save.isQuickSave }"
            >
              <div class="save-info">
                <span class="save-name">{{ save.name }}</span>
                <span class="save-date">{{ formatSaveDate(save.date) }}</span>
                <span class="save-details" v-if="save.gameState.date">Game Date: {{ save.gameState.date }}</span>
              </div>
              <div class="save-actions">
                <button @click="loadGame(save.id)">Load</button>
                <button @click="deleteSave(save.id)" class="delete-btn">Delete</button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="toggleSaveMenu" class="close-btn">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import Map from "../components/Map.vue";

const router = useRouter();

// WebSocket connection
const ws = ref(null);
const wsConnected = ref(false);
const reconnectAttempts = ref(0);
const maxReconnectAttempts = 5;

// Connect to WebSocket
const connectWebSocket = () => {
  // Fix WebSocket URL construction
  // When behind an nginx proxy, we need to use the relative path
  const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${wsProtocol}//${window.location.host}/api/ws`;
  
  console.log("Connecting to WebSocket:", wsUrl);
  
  try {
    ws.value = new WebSocket(wsUrl);
    
    ws.value.onopen = () => {
      console.log("WebSocket connected successfully");
      wsConnected.value = true;
      reconnectAttempts.value = 0;
    };
    
    ws.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Received WebSocket data:", data);
        
        // Update game state with the received data
        gameState.value = data;
        
        // Update UI state based on data
        if (data.paused !== undefined) {
          gameRunning.value = !data.paused;
        }
        
        if (data.speed !== undefined) {
          gameSpeed.value = data.speed;
        }
      } catch (error) {
        console.error("Error parsing WebSocket data:", error);
      }
    };
    
    ws.value.onclose = (event) => {
      console.log("WebSocket disconnected:", event.code, event.reason);
      wsConnected.value = false;
      
      // Try to reconnect if not a normal closure
      if (event.code !== 1000 && reconnectAttempts.value < maxReconnectAttempts) {
        reconnectAttempts.value++;
        const timeout = Math.min(1000 * reconnectAttempts.value, 5000);
        console.log(`Attempting to reconnect in ${timeout}ms (attempt ${reconnectAttempts.value}/${maxReconnectAttempts})`);
        
        setTimeout(connectWebSocket, timeout);
      }
    };
    
    ws.value.onerror = (error) => {
      console.error("WebSocket connection error:", error);
    };
  } catch (error) {
    console.error("Failed to create WebSocket connection:", error);
  }
};

// Send command to WebSocket
const sendCommand = (action, data = {}) => {
  if (ws.value && wsConnected.value) {
    const command = { action, ...data };
    ws.value.send(JSON.stringify(command));
    console.log("Sent command:", command);
  } else {
    console.warn("WebSocket not connected, can't send command:", action);
  }
};

// Add class to parent when component is mounted
onMounted(async () => {
  document.querySelector('.app-container').classList.add('game-page');
  
  // Load saved games from localStorage
  loadSavedGamesList();
  
  // Check if we need to load a specific save
  const currentSaveId = localStorage.getItem('geopolitics_current_save');
  if (currentSaveId) {
    // Find the save with the given ID
    const save = savedGames.value.find(s => s.id === currentSaveId);
    if (save) {
      // Load the game state
      gameState.value = save.gameState;
      gameRunning.value = save.gameRunning;
      gameSpeed.value = save.gameSpeed;
      activeTab.value = save.activeTab;
      
      // Clear the current save ID
      localStorage.removeItem('geopolitics_current_save');
      
      console.log('Loaded saved game:', save.name);
    }
  }
  
  // Connect to WebSocket for real-time updates
  connectWebSocket();
  
  // Add keyboard event listener for shortcuts
  window.addEventListener('keydown', handleKeyDown);
  
  // Check for last quick save
  const savedGamesData = localStorage.getItem('geopolitics_saved_games');
  if (savedGamesData) {
    const saves = JSON.parse(savedGamesData);
    const quickSaves = saves.filter(save => save.isQuickSave);
    if (quickSaves.length > 0) {
      lastQuickSave.value = quickSaves[0].date;
    }
  }
});

// Remove class when component is unmounted
onUnmounted(() => {
  document.querySelector('.app-container').classList.remove('game-page');
  
  // Close WebSocket connection
  if (ws.value) {
    ws.value.close();
    ws.value = null;
  }
  
  // Remove keyboard event listener
  window.removeEventListener('keydown', handleKeyDown);
});

// Game state
const gameState = ref({
  date: "January 1, 2025",
  nations: [],
  speed: "normal",
  paused: true,
  events: [],
  alliances: []
});

// Game controls
const gameRunning = ref(false);
const gameSpeed = ref("normal");

// Watch for game control changes and send updates to the server
watch(gameRunning, (running) => {
  sendCommand(running ? 'resume' : 'pause');
});

watch(gameSpeed, (speed) => {
  sendCommand('set_speed', { speed });
});

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

// Handle country selection from the map
const handleCountrySelected = (nation) => {
  if (nation) {
    console.log(`Selected country: ${nation.name}`);
    // You can add additional logic here, like showing more details
    // or focusing on the country in the sidebar
  }
};

// Save/Load game functionality
const showSaveMenu = ref(false);
const saveName = ref("");
const savedGames = ref([]);
const lastQuickSave = ref(null);

const toggleSaveMenu = () => {
  // Close game menu when opening save menu
  if (showGameMenu.value) {
    showGameMenu.value = false;
  }
  
  // Pause the game when opening save menu
  if (!showSaveMenu.value && gameRunning.value) {
    pauseGame();
  }
  
  showSaveMenu.value = !showSaveMenu.value;
  
  // Refresh saved games list when opening the menu
  if (showSaveMenu.value) {
    loadSavedGamesList();
  }
};

const loadSavedGamesList = () => {
  try {
    const savedGamesData = localStorage.getItem('geopolitics_saved_games');
    if (savedGamesData) {
      savedGames.value = JSON.parse(savedGamesData);
    } else {
      savedGames.value = [];
    }
  } catch (error) {
    console.error('Failed to load saved games:', error);
    savedGames.value = [];
  }
};

const saveGame = () => {
  if (!saveName.value.trim()) return;
  
  try {
    // Create a save object with current game state
    const saveData = {
      id: Date.now().toString(),
      name: saveName.value,
      date: new Date().toISOString(),
      gameState: JSON.parse(JSON.stringify(gameState.value)),
      gameRunning: gameRunning.value,
      gameSpeed: gameSpeed.value,
      activeTab: activeTab.value,
      isQuickSave: false
    };
    
    // Save the game
    saveGameToStorage(saveData);
    
    // Clear the input
    saveName.value = '';
    
    // Show success message
    alert('Game saved successfully!');
  } catch (error) {
    console.error('Failed to save game:', error);
    alert('Failed to save game. Please try again.');
  }
};

const quickSave = () => {
  try {
    // Create a quick save object
    const saveData = {
      id: 'quicksave_' + Date.now().toString(),
      name: 'Quick Save',
      date: new Date().toISOString(),
      gameState: JSON.parse(JSON.stringify(gameState.value)),
      gameRunning: gameRunning.value,
      gameSpeed: gameSpeed.value,
      activeTab: activeTab.value,
      isQuickSave: true
    };
    
    // Save the game
    saveGameToStorage(saveData);
    
    // Update last quick save time
    lastQuickSave.value = saveData.date;
    
    // Show brief notification
    const notification = document.createElement('div');
    notification.className = 'quick-save-notification';
    notification.textContent = 'Game saved!';
    document.body.appendChild(notification);
    
    // Remove notification after 2 seconds
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 2000);
  } catch (error) {
    console.error('Failed to quick save game:', error);
    alert('Failed to quick save. Please try again.');
  }
};

const saveGameToStorage = (saveData) => {
  // Get existing saves or initialize empty array
  let saves = [];
  const savedGamesData = localStorage.getItem('geopolitics_saved_games');
  if (savedGamesData) {
    saves = JSON.parse(savedGamesData);
  }
  
  // If this is a quick save, remove any previous quick saves
  if (saveData.isQuickSave) {
    saves = saves.filter(save => !save.isQuickSave);
  }
  
  // Add new save
  saves.push(saveData);
  
  // Save back to localStorage
  localStorage.setItem('geopolitics_saved_games', JSON.stringify(saves));
  
  // Update the list
  savedGames.value = saves;
};

const loadGame = (id) => {
  try {
    // Find the save with the given ID
    const save = savedGames.value.find(s => s.id === id);
    if (!save) {
      alert('Save not found!');
      return;
    }
    
    // Load the game state
    gameState.value = save.gameState;
    gameRunning.value = save.gameRunning;
    gameSpeed.value = save.gameSpeed;
    activeTab.value = save.activeTab;
    
    // Close the save menu
    showSaveMenu.value = false;
    
    // Show success message
    alert('Game loaded successfully!');
  } catch (error) {
    console.error('Failed to load game:', error);
    alert('Failed to load game. Please try again.');
  }
};

const deleteSave = (id) => {
  try {
    // Confirm deletion
    if (!confirm('Are you sure you want to delete this save?')) {
      return;
    }
    
    // Filter out the save with the given ID
    const filteredSaves = savedGames.value.filter(s => s.id !== id);
    
    // Update localStorage
    localStorage.setItem('geopolitics_saved_games', JSON.stringify(filteredSaves));
    
    // Update the list
    savedGames.value = filteredSaves;
    
    // Show success message
    alert('Save deleted successfully!');
  } catch (error) {
    console.error('Failed to delete save:', error);
    alert('Failed to delete save. Please try again.');
  }
};

const formatSaveDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleString();
  } catch (error) {
    return 'Unknown date';
  }
};

// Game menu state
const showGameMenu = ref(false);

const toggleGameMenu = () => {
  // Pause the game when opening menu
  if (!showGameMenu.value && gameRunning.value) {
    pauseGame();
  }
  showGameMenu.value = !showGameMenu.value;
  
  // Close save menu if it's open
  if (showGameMenu.value && showSaveMenu.value) {
    showSaveMenu.value = false;
  }
};

const resumeGame = () => {
  showGameMenu.value = false;
  if (!gameRunning.value) {
    pauseGame(); // Resume the game
  }
};

const exitToMenu = () => {
  // Confirm exit if game is running
  if (gameRunning.value) {
    if (!confirm('Exit without saving? Your progress since the last save will be lost.')) {
      return;
    }
  }
  
  // Navigate to home page
  router.push('/');
};

// Add keyboard shortcuts for quick save and menu
onMounted(() => {
  // Add keyboard event listener
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  // Remove keyboard event listener
  window.removeEventListener('keydown', handleKeyDown);
});

const handleKeyDown = (event) => {
  // F5 for quick save
  if (event.key === 'F5') {
    event.preventDefault();
    quickSave();
  }
  
  // Escape for game menu
  if (event.key === 'Escape') {
    event.preventDefault();
    if (showSaveMenu.value) {
      showSaveMenu.value = false;
    } else {
      toggleGameMenu();
    }
  }
};
</script>

<style scoped>
/* HOI4 Style UI */
.hoi4-style {
  --hoi4-bg-color: #282c34;
  --hoi4-panel-bg: #1e2128;
  --hoi4-panel-border: #3d4350;
  --hoi4-accent: #4a90e2;
  --hoi4-warning: #e2a14a;
  --hoi4-danger: #e24a4a;
  --hoi4-success: #4ae24a;
  --hoi4-text: #e6e6e6;
  --hoi4-text-dim: #a0a0a0;
  --hoi4-panel-header: #3d4350;
  --hoi4-panel-content: #282c34;
  color: var(--hoi4-text);
}

.game-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--hoi4-bg-color);
}

/* Top Bar */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--hoi4-panel-bg);
  border-bottom: 2px solid var(--hoi4-panel-border);
  padding: 0.5rem;
  height: 50px;
  color: var(--hoi4-text);
}

.date-display {
  display: flex;
  align-items: center;
  font-size: 1.2rem;
  margin-left: 1rem;
}

.date-icon {
  margin-right: 0.5rem;
}

.resource-display {
  display: flex;
  gap: 1.5rem;
}

.resource {
  display: flex;
  align-items: center;
  background-color: var(--hoi4-panel-content);
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  border: 1px solid var(--hoi4-panel-border);
}

.resource-icon {
  margin-right: 0.5rem;
}

.speed-controls {
  display: flex;
  gap: 0.5rem;
  margin-right: 1rem;
}

.speed-controls button {
  background-color: var(--hoi4-panel-content);
  color: var(--hoi4-text);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  padding: 0.3rem 0.7rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.speed-controls button:hover {
  background-color: var(--hoi4-accent);
}

.speed-controls button.active {
  background-color: var(--hoi4-accent);
  color: white;
}

.menu-button {
  background-color: var(--hoi4-panel-content) !important;
  font-weight: bold;
  padding: 0.3rem 0.8rem !important;
  margin-left: 0.5rem;
}

/* Main Content Area */
.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Left Sidebar */
.left-sidebar {
  width: 230px;
  background-color: var(--hoi4-panel-bg);
  border-right: 2px solid var(--hoi4-panel-border);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0.8rem;
  overflow-y: auto;
}

.panel {
  background-color: var(--hoi4-panel-content);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  padding: 0.8rem;
  margin-bottom: 0.8rem;
}

.country-info {
  display: flex;
  flex-direction: column;
}

.country-flag {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 0.8rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.leader-name {
  color: var(--hoi4-text-dim);
  font-style: italic;
}

.country-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
}

.action-categories {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.action-categories h3 {
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.category-btn {
  display: flex;
  align-items: center;
  background-color: var(--hoi4-panel-bg);
  color: var(--hoi4-text);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  padding: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
  text-align: left;
}

.category-btn:hover {
  background-color: var(--hoi4-accent);
}

.btn-icon {
  margin-right: 0.5rem;
}

/* Map Area */
.map-area {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.alerts-bar {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: var(--hoi4-panel-bg);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  z-index: 100;
}

.alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Right Sidebar */
.right-sidebar {
  width: 280px;
  background-color: var(--hoi4-panel-bg);
  border-left: 2px solid var(--hoi4-panel-border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.tabs-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.tabs-header {
  display: flex;
  background-color: var(--hoi4-panel-header);
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.tabs-header button {
  flex: 1;
  background-color: transparent;
  color: var(--hoi4-text);
  border: none;
  padding: 0.8rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.tabs-header button.active {
  background-color: var(--hoi4-accent);
  color: white;
}

.tab-content {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.nations-list, .events-list, .alliances-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nations-header {
  display: flex;
  padding: 0.5rem;
  background-color: var(--hoi4-panel-header);
  font-weight: bold;
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.nation-row {
  display: flex;
  padding: 0.5rem;
  background-color: var(--hoi4-panel-content);
  border: 1px solid var(--hoi4-panel-border);
  cursor: pointer;
  transition: background-color 0.2s;
}

.nation-row:hover {
  background-color: var(--hoi4-accent);
}

.col {
  flex: 1;
}

.nation-name {
  font-weight: bold;
}

.event, .alliance {
  background-color: var(--hoi4-panel-content);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  padding: 0.8rem;
}

.event-header, .alliance-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.event-content {
  color: var(--hoi4-text);
}

.alliance-members {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

/* Bottom Bar */
.bottom-bar {
  display: flex;
  height: 100px;
  background-color: var(--hoi4-panel-bg);
  border-top: 2px solid var(--hoi4-panel-border);
  padding: 0.8rem;
}

.construction-queue, .production-queue {
  flex: 1;
  padding: 0 1rem;
}

.construction-queue h3, .production-queue h3 {
  margin-bottom: 0.8rem;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.queue-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.queue-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-bar {
  flex: 1;
  height: 12px;
  background-color: var(--hoi4-panel-content);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 6px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: var(--hoi4-accent);
}

.empty-queue {
  color: var(--hoi4-text-dim);
  font-style: italic;
}

/* Game Menu Overlay */
.game-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100;
  overflow: auto;
}

.game-menu {
  background-color: var(--hoi4-panel-bg);
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  color: var(--hoi4-text);
  text-align: center;
  border: 3px solid var(--hoi4-panel-border);
  max-height: 90vh;
  overflow-y: auto;
  margin: 20px;
  position: relative;
}

.game-menu h2 {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.menu-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.menu-btn {
  padding: 1rem;
  background-color: var(--hoi4-panel-content);
  color: var(--hoi4-text);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.menu-btn:hover {
  background-color: var(--hoi4-accent);
  transform: translateY(-2px);
}

.menu-btn:active {
  transform: translateY(1px);
}

.menu-icon {
  font-size: 1.3rem;
}

.resume-btn {
  background-color: var(--hoi4-success);
}

.exit-btn {
  background-color: var(--hoi4-danger);
  margin-top: 0.5rem;
}

.menu-help {
  margin-top: 2rem;
  font-size: 0.9rem;
  color: var(--hoi4-text-dim);
}

.menu-help kbd {
  background-color: var(--hoi4-panel-content);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
  font-size: 0.9em;
  border: 1px solid var(--hoi4-panel-border);
}

/* Save Modal */
.save-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  overflow: auto;
}

.save-modal-content {
  background-color: var(--hoi4-panel-bg);
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  margin: 20px;
  color: var(--hoi4-text);
  border: 2px solid var(--hoi4-panel-border);
}

.save-modal-content h3 {
  color: var(--hoi4-text);
  margin-bottom: 1rem;
  text-align: center;
  font-size: 1.5rem;
}

.save-section, .load-section {
  margin-bottom: 1.5rem;
}

.save-section h4, .load-section h4 {
  color: var(--hoi4-text);
  margin-bottom: 0.75rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
  padding-bottom: 0.5rem;
}

.save-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.save-input {
  display: flex;
  gap: 0.5rem;
}

.save-input input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  background-color: var(--hoi4-panel-content);
  color: var(--hoi4-text);
}

.save-input button, 
.save-actions button, 
.modal-footer button,
.quick-save-btn {
  padding: 0.5rem 1rem;
  background-color: var(--hoi4-panel-content);
  color: var(--hoi4-text);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-input button:hover, 
.save-actions button:hover, 
.modal-footer button:hover,
.quick-save-btn:hover {
  background-color: var(--hoi4-accent);
}

.quick-save {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.saved-games-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.saved-game-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--hoi4-panel-content);
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid var(--hoi4-panel-border);
}

.save-info {
  display: flex;
  flex-direction: column;
}

.save-name {
  font-weight: bold;
  color: var(--hoi4-text);
}

.save-date {
  font-size: 0.8rem;
  color: var(--hoi4-text-dim);
}

.save-actions {
  display: flex;
  gap: 0.5rem;
}

.delete-btn {
  background-color: var(--hoi4-danger) !important;
}

.modal-footer {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.close-btn {
  padding: 0.5rem 2rem;
}

.no-saves {
  padding: 1rem;
  text-align: center;
  color: var(--hoi4-text-dim);
  font-style: italic;
}

.quick-save-info {
  font-size: 0.8rem;
  color: var(--hoi4-text-dim);
  font-style: italic;
}

.quick-save-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: var(--hoi4-accent);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 2000;
  animation: fadeInOut 2s ease-in-out;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(-20px); }
  20% { opacity: 1; transform: translateY(0); }
  80% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-20px); }
}

/* Responsive Design */
@media (max-width: 1200px) {
  .left-sidebar {
    width: 200px;
  }
  
  .right-sidebar {
    width: 250px;
  }
  
  .bottom-bar {
    height: 80px;
  }
}

@media (max-width: 992px) {
  .main-content {
    flex-direction: column;
  }
  
  .left-sidebar, .right-sidebar {
    width: 100%;
    height: 200px;
    border: none;
  }
  
  .left-sidebar {
    border-bottom: 2px solid var(--hoi4-panel-border);
  }
  
  .right-sidebar {
    border-top: 2px solid var(--hoi4-panel-border);
  }
  
  .map-area {
    flex: 1;
    min-height: 300px;
  }
}

@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    height: auto;
    padding: 0.5rem;
  }
  
  .resource-display {
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
    margin: 0.5rem 0;
  }
  
  .date-display {
    margin: 0;
  }
  
  .speed-controls {
    margin: 0.5rem 0 0 0;
  }
  
  .bottom-bar {
    flex-direction: column;
    height: auto;
  }
  
  .construction-queue, .production-queue {
    padding: 0.5rem 0;
  }
  
  .left-sidebar, .right-sidebar {
    height: 150px;
  }
}

/* Remove floating menu button */
.floating-menu-btn {
  display: none; /* Hide the floating menu button */
}
</style>
