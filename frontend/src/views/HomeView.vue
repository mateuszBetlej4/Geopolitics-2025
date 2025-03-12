<template>
  <div class="home-container hoi4-style">
    <!-- Header Area -->
    <header class="site-header">
      <h1>GEOPOLITICS 2025</h1>
      <p class="tagline">Shape the future of global politics in this real-time strategy game</p>
      <div class="copyright-info">© 2025 Geopolitics Strategy Game</div>
    </header>
    
    <div class="main-layout">
      <!-- Left Panel - Main Menu -->
      <div class="main-menu-panel">
        <div class="menu-header">
          <h2>MAIN MENU</h2>
        </div>
        
        <div class="menu-actions">
          <button @click="startNewGame" class="menu-btn primary-btn">
            <div class="btn-icon">🌍</div>
            <div class="btn-text">New Game</div>
          </button>
          
          <button @click="toggleSavedGames" class="menu-btn secondary-btn">
            <div class="btn-icon">💾</div>
            <div class="btn-text">
              {{ showSavedGames ? 'Hide Saved Games' : 'Load Game' }}
            </div>
          </button>
          
          <router-link to="/settings" class="menu-btn tertiary-btn">
            <div class="btn-icon">⚙️</div>
            <div class="btn-text">Settings</div>
          </router-link>
          
          <!-- Placeholder for future buttons -->
          <a href="https://github.com/yourusername/geopolitics-2025" target="_blank" class="menu-btn info-btn">
            <div class="btn-icon">ℹ️</div>
            <div class="btn-text">About</div>
          </a>
          
          <button @click="exitGame" class="menu-btn danger-btn">
            <div class="btn-icon">🚪</div>
            <div class="btn-text">Exit</div>
          </button>
        </div>
        
        <div class="version-info">
          <p>Version 0.1 (Alpha)</p>
          <p>© 2025 Geopolitics Team</p>
        </div>
      </div>
      
      <!-- Right Content Area -->
      <div class="content-area">
        <!-- Saved Games Section -->
        <div v-if="showSavedGames" class="content-panel saved-games-panel">
          <div class="panel-header">
            <h2>Saved Games</h2>
          </div>
          
          <div class="panel-content">
            <div v-if="savedGames.length === 0" class="no-saves">
              <p>No saved games found. Start a new game to create a save.</p>
            </div>
            <div v-else class="saved-games-list">
              <div 
                v-for="save in savedGames" 
                :key="save.id"
                class="save-item"
              >
                <div class="save-info">
                  <div class="save-name">{{ save.name }}</div>
                  <div class="save-meta">
                    <span class="save-date">{{ formatSaveDate(save.date) }}</span>
                    <span class="save-details">Game Date: {{ save.gameState.date }}</span>
                  </div>
                </div>
                <div class="save-actions">
                  <button @click="loadGame(save.id)" class="action-btn load-btn">Continue</button>
                  <button @click="deleteSave(save.id)" class="action-btn delete-btn">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Game Info Panel -->
        <div v-if="!showSavedGames" class="content-panel">
          <div class="panel-header">
            <h2>Game Features</h2>
          </div>
          
          <div class="panel-content">
            <div class="features-grid">
              <div class="feature-card">
                <div class="feature-icon">🔫</div>
                <div class="feature-content">
                  <h3>Military Expansion</h3>
                  <p>Build powerful armies, navies, and air forces to project your nation's power globally.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="feature-icon">💰</div>
                <div class="feature-content">
                  <h3>Economic Development</h3>
                  <p>Grow your GDP, establish trade agreements, and impose sanctions on rival nations.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="feature-icon">🤝</div>
                <div class="feature-content">
                  <h3>Diplomacy & Alliances</h3>
                  <p>Form strategic partnerships, negotiate treaties, and manage international relations.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="feature-icon">☢️</div>
                <div class="feature-content">
                  <h3>Nuclear Deterrence</h3>
                  <p>Develop nuclear capabilities as the ultimate deterrent, but use with extreme caution.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Nations Panel -->
        <div class="content-panel nations-panel">
          <div class="panel-header">
            <h2>Playable Nations</h2>
          </div>
          
          <div class="panel-content">
            <div v-if="loadingNations" class="loading-message">Loading nations data...</div>
            <div v-if="nationError" class="error-message">{{ nationError }}</div>
            <div class="nations-grid">
              <div 
                class="nation-card" 
                v-for="nation in nations" 
                :key="nation.name"
                @click="selectNation(nation)"
              >
                <div class="flag-icon">
                  <div class="nation-initial">{{ nation.name.charAt(0) }}</div>
                </div>
                <div class="nation-content">
                  <div class="nation-header">
                    <h3>{{ nation.name }}</h3>
                    <span class="nation-difficulty" :class="nation.difficulty || 'medium'">
                      {{ nation.difficulty || 'Medium' }}
                    </span>
                  </div>
                  <div class="nation-details">
                    <span class="nation-leader">Leader: {{ nation.leader }}</span>
                    <p class="nation-desc">{{ nation.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- World Map Background -->
    <div class="map-background"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const showSavedGames = ref(false);
const savedGames = ref([]);

// Toggle saved games section
const toggleSavedGames = () => {
  showSavedGames.value = !showSavedGames.value;
  if (showSavedGames.value) {
    loadSavedGamesList();
  }
};

// Load saved games from localStorage
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

// Format save date
const formatSaveDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleString();
  } catch (error) {
    return 'Unknown date';
  }
};

// Load a saved game
const loadGame = (id) => {
  try {
    // Store the save ID in localStorage
    localStorage.setItem('geopolitics_current_save', id);
    
    // Navigate to the game page
    router.push('/game');
  } catch (error) {
    console.error('Failed to load game:', error);
    alert('Failed to load game. Please try again.');
  }
};

// Delete a saved game
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
  } catch (error) {
    console.error('Failed to delete save:', error);
    alert('Failed to delete save. Please try again.');
  }
};

// Exit game
const exitGame = () => {
  if (confirm('Are you sure you want to exit?')) {
    window.close();
  }
};

// Select nation (placeholder for future functionality)
const selectNation = (nation) => {
  console.log(`Selected nation: ${nation.name}`);
  // Future: Could be used to pre-select a nation before starting a new game
};

// Start a new game
const startNewGame = () => {
  // Set flag to indicate this is a new game
  localStorage.setItem('geopolitics_new_game', 'true');
  
  // Clear any current save ID to prevent automatic loading
  localStorage.removeItem('geopolitics_current_save');
  
  // Navigate to the game page
  router.push('/game');
};

// Sample data for nations
const nations = ref([]);
const loadingNations = ref(false);
const nationError = ref(null);

// Fetch playable nations from API
const fetchPlayableNations = async () => {
  loadingNations.value = true;
  nationError.value = null;
  
  try {
    console.log("Fetching playable nations...");
    // Use the nginx proxy path to access the backend
    const apiUrl = '/api/playable-nations';
    console.log("API URL:", apiUrl);
    
    const response = await fetch(apiUrl);
    console.log("Response status:", response.status);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch playable nations: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log("Fetched data:", data);
    
    // Check if we got valid data
    if (!data || !Array.isArray(data) || data.length === 0) {
      throw new Error("No nation data received from API");
    }
    
    nations.value = data;
  } catch (error) {
    console.error('Error fetching playable nations:', error);
    nationError.value = `Failed to load nation data: ${error.message}. Using fallback data.`;
    
    // Fallback to hardcoded data
    nations.value = [
      {
        name: "United States",
        leader: "Donald Trump",
        difficulty: "easy",
        description: "Nuclear power with powerful military and massive economy."
      },
      {
        name: "China",
        leader: "Li Qiang",
        difficulty: "medium",
        description: "Nuclear power with powerful military and substantial economy."
      },
      {
        name: "Russia",
        leader: "Vladimir Putin",
        difficulty: "medium",
        description: "Nuclear power with strong military and substantial economy."
      },
      {
        name: "India",
        leader: "Narendra Modi",
        difficulty: "hard",
        description: "Nuclear power with developing military and growing economy."
      }
    ];
  } finally {
    loadingNations.value = false;
  }
};

// Check for saved games on component mount
onMounted(() => {
  loadSavedGamesList();
  fetchPlayableNations();
  
  // Add class to body for full-page background
  document.body.classList.add('home-page');
  
  return () => {
    // Remove class when component unmounts
    document.body.classList.remove('home-page');
  };
});
</script>

<style scoped>
/* HOI4 Style Variables */
.hoi4-style {
  --hoi4-bg-color: #1a1e24;
  --hoi4-panel-bg: #282c34;
  --hoi4-panel-light: #363b47;
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

/* Main Layout */
.home-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--hoi4-bg-color);
  position: relative;
  z-index: 0;
  overflow: hidden;
}

/* New Header Styling */
.site-header {
  background-color: rgba(26, 30, 36, 0.9);
  border-bottom: 1px solid var(--hoi4-panel-border);
  padding: 0.8rem 0;
  text-align: center;
  position: relative;
  z-index: 10;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.site-header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0 0 0.2rem 0;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--hoi4-text);
  text-shadow: 0 0 10px rgba(74, 144, 226, 0.7), 0 0 20px rgba(0, 0, 0, 0.5);
}

.site-header .tagline {
  font-size: 0.9rem;
  color: var(--hoi4-text-dim);
  max-width: 600px;
  margin: 0 auto;
  margin-bottom: 0.2rem;
}

.copyright-info {
  font-size: 0.7rem;
  color: var(--hoi4-text-dim);
  opacity: 0.7;
}

/* Map Background */
.map-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/assets/world-map-fade.png');
  background-size: cover;
  background-position: center;
  opacity: 0.15;
  z-index: -1;
}

/* Main Layout */
.main-layout {
  display: flex;
  flex: 1;
  padding: 1rem 2rem;
  gap: 1.5rem;
  margin-bottom: 1rem; /* Reduced from 4.5rem since footer is removed */
}

/* Menu Panel */
.main-menu-panel {
  width: 250px;
  min-width: 250px;
  background-color: var(--hoi4-panel-bg);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: fit-content;
}

.menu-header {
  background-color: var(--hoi4-panel-header);
  padding: 0.7rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.menu-header h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.menu-actions {
  padding: 0.8rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-btn {
  display: flex;
  align-items: center;
  padding: 0.7rem 1rem;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  background-color: var(--hoi4-panel-content);
  color: var(--hoi4-text);
  border: 1px solid var(--hoi4-panel-border);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.menu-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn-icon {
  font-size: 1.3rem;
  margin-right: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
}

.primary-btn {
  background-color: var(--hoi4-accent);
}

.primary-btn:hover {
  background-color: #3a80d2;
}

.secondary-btn:hover {
  background-color: var(--hoi4-panel-light);
}

.tertiary-btn {
  border-color: var(--hoi4-accent);
}

.tertiary-btn:hover {
  background-color: var(--hoi4-panel-light);
}

.danger-btn {
  border-color: var(--hoi4-danger);
}

.danger-btn:hover {
  background-color: var(--hoi4-danger);
}

.version-info {
  padding: 0.4rem;
  border-top: 1px solid var(--hoi4-panel-border);
  font-size: 0.65rem;
  color: var(--hoi4-text-dim);
  text-align: center;
}

/* Content Area */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  max-height: calc(100vh - 8rem); /* Adjusted for header without footer */
  overflow: auto;
  padding-right: 0.5rem;
  padding-bottom: 1.5rem; /* Add extra padding at the bottom */
}

.content-panel {
  background-color: var(--hoi4-panel-bg);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  flex-shrink: 1;
  margin-bottom: 0.5rem;
}

.panel-header {
  background-color: var(--hoi4-panel-header);
  padding: 0.5rem 0.8rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.panel-header h2 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.panel-content {
  padding: 0.6rem;
  overflow: hidden;
}

/* Features Grid */
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.6rem;
}

.feature-card {
  background-color: var(--hoi4-panel-content);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 6px;
  padding: 0.5rem;
  transition: transform 0.2s ease;
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
}

.feature-icon {
  font-size: 1.2rem;
  background-color: var(--hoi4-panel-light);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-content {
  flex: 1;
}

.feature-card:hover {
  transform: translateY(-3px);
}

.feature-card h3 {
  color: var(--hoi4-accent);
  margin: 0 0 0.3rem 0;
  font-size: 0.9rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
  padding-bottom: 0.2rem;
}

.feature-card p {
  color: var(--hoi4-text-dim);
  margin: 0;
  line-height: 1.2;
  font-size: 0.75rem;
}

/* Nations Grid */
.nations-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.4rem;
}

.nation-card {
  background-color: var(--hoi4-panel-content);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 4px;
  padding: 0.4rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
  position: relative;
}

.flag-icon {
  width: 24px;
  height: 24px;
  background-color: var(--hoi4-panel-light);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid var(--hoi4-panel-border);
}

.nation-initial {
  font-weight: bold;
  font-size: 0.9rem;
  color: var(--hoi4-accent);
}

.nation-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.nation-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.1rem;
  border-bottom: 1px dotted var(--hoi4-panel-border);
  padding-bottom: 0.1rem;
}

.nation-card h3 {
  color: var(--hoi4-text);
  margin: 0;
  font-size: 0.8rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 65%;
}

.nation-difficulty {
  font-size: 0.6rem;
  padding: 0.1rem 0.3rem;
  border-radius: 2px;
  background-color: var(--hoi4-panel-light);
  color: var(--hoi4-text-dim);
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.nation-difficulty.easy {
  background-color: var(--hoi4-success);
  color: var(--hoi4-bg-color);
}

.nation-difficulty.medium {
  background-color: var(--hoi4-warning);
  color: var(--hoi4-bg-color);
}

.nation-difficulty.hard {
  background-color: var(--hoi4-danger);
  color: var(--hoi4-text);
}

.nation-details {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.nation-leader {
  color: var(--hoi4-accent);
  font-size: 0.7rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-left: 0.1rem;
}

.nation-desc {
  color: var(--hoi4-text-dim);
  margin: 0;
  font-size: 0.65rem;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Saved Games List */
.saved-games-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.save-item {
  background-color: var(--hoi4-panel-content);
  border: 1px solid var(--hoi4-panel-border);
  border-radius: 6px;
  padding: 0.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.save-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--hoi4-text);
  margin-bottom: 0.2rem;
}

.save-meta {
  display: flex;
  flex-direction: column;
  font-size: 0.8rem;
  color: var(--hoi4-text-dim);
}

.save-actions {
  display: flex;
  gap: 0.8rem;
}

.action-btn {
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  background-color: var(--hoi4-panel-light);
  border: 1px solid var(--hoi4-panel-border);
  color: var(--hoi4-text);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8rem;
}

.load-btn {
  background-color: var(--hoi4-accent);
}

.load-btn:hover {
  background-color: #3a80d2;
}

.delete-btn {
  border-color: var(--hoi4-danger);
}

.delete-btn:hover {
  background-color: var(--hoi4-danger);
}

.no-saves {
  text-align: center;
  padding: 1.5rem;
  color: var(--hoi4-text-dim);
  font-style: italic;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-layout {
    flex-direction: column;
    padding: 1rem;
  }
  
  .main-menu-panel {
    width: 100%;
    min-width: 0;
  }
  
  .site-header h1 {
    font-size: 2.2rem;
  }
  
  .menu-actions {
    padding: 0.8rem;
  }
  
  .content-area {
    max-height: none;
    overflow: visible;
  }
}

@media (max-width: 768px) {
  .site-header h1 {
    font-size: 1.8rem;
  }
  
  .features-grid, 
  .nations-grid {
    grid-template-columns: 1fr;
  }
  
  .tagline {
    font-size: 0.8rem;
  }
  
  .save-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }
  
  .save-actions {
    width: 100%;
    justify-content: space-between;
  }
}

/* Nations Section */
.nations-panel {
  margin-bottom: 1rem; /* Extra space at the bottom */
}

.loading-message {
  text-align: center;
  padding: 1.5rem;
  color: var(--hoi4-text-dim);
  font-style: italic;
}

.error-message {
  text-align: center;
  padding: 1.5rem;
  color: var(--hoi4-danger);
  font-weight: bold;
}

/* Nations Panel specific styles */
.nations-panel .panel-content {
  max-height: 40vh; /* Set a maximum height */
  overflow-y: auto; /* Enable vertical scrolling */
  padding-right: 0.8rem; /* Add extra padding for the scrollbar */
}

/* Add a subtle scrollbar style */
.nations-panel .panel-content::-webkit-scrollbar {
  width: 8px;
}

.nations-panel .panel-content::-webkit-scrollbar-track {
  background: var(--hoi4-panel-content);
  border-radius: 4px;
}

.nations-panel .panel-content::-webkit-scrollbar-thumb {
  background: var(--hoi4-panel-border);
  border-radius: 4px;
}

.nations-panel .panel-content::-webkit-scrollbar-thumb:hover {
  background: var(--hoi4-accent);
}
</style>
