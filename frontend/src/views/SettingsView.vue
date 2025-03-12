<template>
  <div class="settings-container hoi4-style">
    <!-- Header Area -->
    <header class="site-header">
      <h1>GEOPOLITICS 2025</h1>
      <p class="tagline">Game Settings</p>
      <div class="copyright-info">© 2025 Geopolitics Strategy Game</div>
    </header>
    
    <div class="main-layout">
      <!-- Left Panel - Settings Categories -->
      <div class="settings-nav-panel">
        <div class="panel-header">
          <h2>SETTINGS</h2>
        </div>
        
        <div class="settings-nav-links">
          <button @click="activeTab = 'game'" 
              :class="['settings-nav-btn', activeTab === 'game' ? 'active' : '']">
            <div class="btn-icon">🎮</div>
            <div class="btn-text">Game Options</div>
          </button>
          
          <button @click="activeTab = 'graphics'" 
              :class="['settings-nav-btn', activeTab === 'graphics' ? 'active' : '']">
            <div class="btn-icon">🖥️</div>
            <div class="btn-text">Graphics</div>
          </button>
          
          <button @click="activeTab = 'audio'" 
              :class="['settings-nav-btn', activeTab === 'audio' ? 'active' : '']">
            <div class="btn-icon">🔊</div>
            <div class="btn-text">Audio</div>
          </button>
          
          <button @click="activeTab = 'controls'" 
              :class="['settings-nav-btn', activeTab === 'controls' ? 'active' : '']">
            <div class="btn-icon">⌨️</div>
            <div class="btn-text">Controls</div>
          </button>
          
          <router-link to="/" class="settings-nav-btn return-btn">
            <div class="btn-icon">🔙</div>
            <div class="btn-text">Back to Menu</div>
          </router-link>
        </div>
      </div>
      
      <!-- Right Content Area -->
      <div class="content-area">
        <!-- Game Options Panel -->
        <div v-if="activeTab === 'game'" class="content-panel">
          <div class="panel-header">
            <h2>Game Options</h2>
          </div>
          
          <div class="panel-content">
            <div class="settings-grid">
              <div class="setting-item">
                <label for="difficulty">Difficulty Level</label>
                <select id="difficulty" v-model="settings.difficulty" class="hoi4-select">
                  <option value="easy">Easy</option>
                  <option value="normal">Normal</option>
                  <option value="hard">Hard</option>
                  <option value="expert">Expert</option>
                </select>
              </div>
              
              <div class="setting-item">
                <label for="gameSpeed">Default Game Speed</label>
                <select id="gameSpeed" v-model="settings.gameSpeed" class="hoi4-select">
                  <option value="slow">Slow</option>
                  <option value="normal">Normal</option>
                  <option value="fast">Fast</option>
                </select>
              </div>
              
              <div class="setting-item checkbox">
                <label for="autoPause">
                  <input type="checkbox" id="autoPause" v-model="settings.autoPauseEvents" 
                      class="hoi4-checkbox" />
                  <span>Auto-pause on major events</span>
                </label>
              </div>
              
              <div class="setting-item checkbox">
                <label for="tutorialMode">
                  <input type="checkbox" id="tutorialMode" v-model="settings.tutorialMode" 
                      class="hoi4-checkbox" />
                  <span>Enable tutorial mode</span>
                </label>
              </div>
              
              <div class="setting-item checkbox">
                <label for="ironmanMode">
                  <input type="checkbox" id="ironmanMode" v-model="settings.ironmanMode" 
                      class="hoi4-checkbox" />
                  <span>Ironman Mode (No save scumming)</span>
                </label>
              </div>
              
              <div class="setting-item">
                <label for="aiAggressiveness">AI Aggressiveness</label>
                <div class="slider-container">
                  <input type="range" id="aiAggressiveness" v-model="settings.aiAggressiveness" 
                      min="0" max="100" class="hoi4-slider" />
                  <span>{{ settings.aiAggressiveness }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Graphics Panel -->
        <div v-if="activeTab === 'graphics'" class="content-panel">
          <div class="panel-header">
            <h2>Graphics Options</h2>
          </div>
          
          <div class="panel-content">
            <div class="settings-grid">
              <div class="setting-item">
                <label for="resolution">Resolution</label>
                <select id="resolution" v-model="settings.resolution" class="hoi4-select">
                  <option value="1280x720">1280 x 720</option>
                  <option value="1920x1080">1920 x 1080</option>
                  <option value="2560x1440">2560 x 1440</option>
                  <option value="3840x2160">3840 x 2160</option>
                </select>
              </div>
              
              <div class="setting-item">
                <label for="displayMode">Display Mode</label>
                <select id="displayMode" v-model="settings.displayMode" class="hoi4-select">
                  <option value="windowed">Windowed</option>
                  <option value="borderless">Borderless</option>
                  <option value="fullscreen">Fullscreen</option>
                </select>
              </div>
              
              <div class="setting-item">
                <label for="mapStyle">Map Style</label>
                <select id="mapStyle" v-model="settings.mapStyle" class="hoi4-select">
                  <option value="political">Political</option>
                  <option value="satellite">Satellite</option>
                  <option value="terrain">Terrain</option>
                </select>
              </div>
              
              <div class="setting-item">
                <label for="graphicsQuality">Graphics Quality</label>
                <select id="graphicsQuality" v-model="settings.graphicsQuality" class="hoi4-select">
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="ultra">Ultra</option>
                </select>
              </div>
              
              <div class="setting-item">
                <label for="uiScale">UI Scale</label>
                <div class="slider-container">
                  <input type="range" id="uiScale" v-model="settings.uiScaleValue" 
                      min="50" max="150" class="hoi4-slider" />
                  <span>{{ settings.uiScaleValue }}%</span>
                </div>
              </div>
              
              <div class="setting-item checkbox">
                <label for="darkMode">
                  <input type="checkbox" id="darkMode" v-model="settings.darkMode" 
                      class="hoi4-checkbox" />
                  <span>Dark Mode (Default)</span>
                </label>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Audio Panel -->
        <div v-if="activeTab === 'audio'" class="content-panel">
          <div class="panel-header">
            <h2>Audio Settings</h2>
          </div>
          
          <div class="panel-content">
            <div class="settings-grid">
              <div class="setting-item">
                <label for="masterVolume">Master Volume</label>
                <div class="slider-container">
                  <input type="range" id="masterVolume" v-model="settings.masterVolume" 
                      min="0" max="100" class="hoi4-slider" />
                  <span>{{ settings.masterVolume }}%</span>
                </div>
              </div>
              
              <div class="setting-item">
                <label for="musicVolume">Music Volume</label>
                <div class="slider-container">
                  <input type="range" id="musicVolume" v-model="settings.musicVolume" 
                      min="0" max="100" class="hoi4-slider" />
                  <span>{{ settings.musicVolume }}%</span>
                </div>
              </div>
              
              <div class="setting-item">
                <label for="sfxVolume">Sound Effects Volume</label>
                <div class="slider-container">
                  <input type="range" id="sfxVolume" v-model="settings.sfxVolume" 
                      min="0" max="100" class="hoi4-slider" />
                  <span>{{ settings.sfxVolume }}%</span>
                </div>
              </div>
              
              <div class="setting-item">
                <label for="uiSoundVolume">UI Sound Volume</label>
                <div class="slider-container">
                  <input type="range" id="uiSoundVolume" v-model="settings.uiSoundVolume" 
                      min="0" max="100" class="hoi4-slider" />
                  <span>{{ settings.uiSoundVolume }}%</span>
                </div>
              </div>
              
              <div class="setting-item checkbox">
                <label for="muteAll">
                  <input type="checkbox" id="muteAll" v-model="settings.muteAll" 
                      class="hoi4-checkbox" />
                  <span>Mute All</span>
                </label>
              </div>
              
              <div class="setting-item checkbox">
                <label for="playMusic">
                  <input type="checkbox" id="playMusic" v-model="settings.playMusic" 
                      class="hoi4-checkbox" />
                  <span>Play Music in Menu</span>
                </label>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Controls Panel -->
        <div v-if="activeTab === 'controls'" class="content-panel">
          <div class="panel-header">
            <h2>Controls Settings</h2>
          </div>
          
          <div class="panel-content">
            <div class="settings-grid">
              <div class="hotkey-section">
                <h3>Map Navigation</h3>
                <div class="hotkey-item">
                  <span class="action">Pan Map</span>
                  <span class="key">WASD or Arrow Keys</span>
                </div>
                <div class="hotkey-item">
                  <span class="action">Zoom In/Out</span>
                  <span class="key">Mouse Wheel or +/-</span>
                </div>
                <div class="hotkey-item">
                  <span class="action">Rotate Map</span>
                  <span class="key">Q / E</span>
                </div>
              </div>
              
              <div class="hotkey-section">
                <h3>Game Controls</h3>
                <div class="hotkey-item">
                  <span class="action">Pause/Resume</span>
                  <span class="key">Space</span>
                </div>
                <div class="hotkey-item">
                  <span class="action">Speed Up</span>
                  <span class="key">+</span>
                </div>
                <div class="hotkey-item">
                  <span class="action">Slow Down</span>
                  <span class="key">-</span>
                </div>
              </div>
              
              <div class="hotkey-section">
                <h3>Interface</h3>
                <div class="hotkey-item">
                  <span class="action">Toggle UI</span>
                  <span class="key">F10</span>
                </div>
                <div class="hotkey-item">
                  <span class="action">Economic View</span>
                  <span class="key">F1</span>
                </div>
                <div class="hotkey-item">
                  <span class="action">Military View</span>
                  <span class="key">F2</span>
                </div>
                <div class="hotkey-item">
                  <span class="action">Diplomatic View</span>
                  <span class="key">F3</span>
                </div>
              </div>
              
              <div class="control-options">
                <div class="setting-item checkbox">
                  <label for="edgeScrolling">
                    <input type="checkbox" id="edgeScrolling" v-model="settings.edgeScrolling" 
                        class="hoi4-checkbox" />
                    <span>Edge Scrolling</span>
                  </label>
                </div>
                
                <div class="setting-item">
                  <label for="scrollSpeed">Map Scroll Speed</label>
                  <div class="slider-container">
                    <input type="range" id="scrollSpeed" v-model="settings.scrollSpeed" 
                        min="1" max="10" class="hoi4-slider" />
                    <span>{{ settings.scrollSpeed }}</span>
                  </div>
                </div>
                
                <div class="setting-item checkbox">
                  <label for="invertYAxis">
                    <input type="checkbox" id="invertYAxis" v-model="settings.invertYAxis" 
                        class="hoi4-checkbox" />
                    <span>Invert Y-Axis</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Save Button Panel -->
        <div class="content-panel action-panel">
          <div class="settings-actions">
            <button @click="saveSettings" class="hoi4-btn primary-btn">Save Settings</button>
            <button @click="resetSettings" class="hoi4-btn secondary-btn">Reset to Default</button>
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

// Default settings
const defaultSettings = {
  // Game options
  difficulty: "normal",
  gameSpeed: "normal",
  autoPauseEvents: true,
  tutorialMode: false,
  ironmanMode: false,
  aiAggressiveness: 50,
  
  // Graphics options
  resolution: "1920x1080",
  displayMode: "borderless",
  mapStyle: "political",
  graphicsQuality: "high",
  uiScale: "medium",
  uiScaleValue: 100,
  darkMode: true,
  
  // Audio options
  masterVolume: 80,
  musicVolume: 70,
  sfxVolume: 90,
  uiSoundVolume: 85,
  muteAll: false,
  playMusic: true,
  
  // Controls options
  edgeScrolling: true,
  scrollSpeed: 5,
  invertYAxis: false
};

// Current tab
const activeTab = ref('game');

// Settings state
const settings = ref({ ...defaultSettings });

// Load settings from localStorage on mount
onMounted(() => {
  const savedSettings = localStorage.getItem("gameSettings");
  if (savedSettings) {
    try {
      const parsedSettings = JSON.parse(savedSettings);
      settings.value = { ...defaultSettings, ...parsedSettings };
    } catch (error) {
      console.error("Failed to parse saved settings:", error);
    }
  }
});

// Save settings to localStorage
const saveSettings = () => {
  localStorage.setItem("gameSettings", JSON.stringify(settings.value));
  alert("Settings saved successfully!");
};

// Reset settings to default
const resetSettings = () => {
  if (confirm("Are you sure you want to reset all settings to default?")) {
    settings.value = { ...defaultSettings };
    localStorage.removeItem("gameSettings");
  }
};
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
.settings-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--hoi4-bg-color);
  position: relative;
  z-index: 0;
  overflow: hidden;
}

/* Header Styling */
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
  margin-bottom: 1rem; /* Reduced since footer is removed */
}

/* Settings Navigation Panel */
.settings-nav-panel {
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

.panel-header {
  background-color: var(--hoi4-panel-header);
  padding: 0.7rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
}

.panel-header h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.settings-nav-links {
  padding: 0.8rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.settings-nav-btn {
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

.settings-nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.settings-nav-btn.active {
  background-color: var(--hoi4-accent);
  border-color: var(--hoi4-accent);
}

.return-btn {
  margin-top: 1rem;
  border-color: var(--hoi4-panel-border);
}

.btn-icon {
  font-size: 1.3rem;
  margin-right: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
}

/* Content Area */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  max-height: calc(100vh - 8rem); /* Adjusted since footer is removed */
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

.panel-content {
  padding: 1rem;
  overflow: hidden;
}

/* Settings Grid */
.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.2rem;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.setting-item label {
  font-weight: 600;
  color: var(--hoi4-text);
  font-size: 0.9rem;
}

.setting-item.checkbox label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

/* Sliders */
.slider-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.slider-container span {
  width: 3rem;
  text-align: right;
  font-size: 0.9rem;
  color: var(--hoi4-accent);
}

.hoi4-slider {
  flex: 1;
  height: 8px;
  -webkit-appearance: none;
  appearance: none;
  background: var(--hoi4-panel-light);
  border-radius: 4px;
  outline: none;
}

.hoi4-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: var(--hoi4-accent);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid var(--hoi4-text);
}

.hoi4-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: var(--hoi4-accent);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid var(--hoi4-text);
}

/* Select elements */
.hoi4-select {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: var(--hoi4-panel-content);
  border: 1px solid var(--hoi4-panel-border);
  color: var(--hoi4-text);
  font-size: 0.9rem;
  width: 100%;
  cursor: pointer;
}

.hoi4-select option {
  background-color: var(--hoi4-panel-bg);
  color: var(--hoi4-text);
}

/* Checkbox */
.hoi4-checkbox {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border: 2px solid var(--hoi4-panel-border);
  border-radius: 4px;
  background-color: var(--hoi4-panel-content);
  cursor: pointer;
  position: relative;
  flex-shrink: 0;
}

.hoi4-checkbox:checked {
  background-color: var(--hoi4-accent);
  border-color: var(--hoi4-accent);
}

.hoi4-checkbox:checked::after {
  content: "✓";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.8rem;
}

/* Hotkey Sections */
.hotkey-section {
  margin-bottom: 1.5rem;
}

.hotkey-section h3 {
  color: var(--hoi4-accent);
  margin-top: 0;
  margin-bottom: 0.8rem;
  font-size: 1rem;
  border-bottom: 1px solid var(--hoi4-panel-border);
  padding-bottom: 0.3rem;
}

.hotkey-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(61, 67, 80, 0.3);
}

.hotkey-item .action {
  color: var(--hoi4-text);
  font-size: 0.9rem;
}

.hotkey-item .key {
  background-color: var(--hoi4-panel-light);
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  color: var(--hoi4-text);
  font-family: monospace;
  border: 1px solid var(--hoi4-panel-border);
}

/* Action Panel */
.action-panel {
  margin-top: 1rem;
}

.settings-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  padding: 1rem;
}

.hoi4-btn {
  padding: 0.7rem 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  border: 1px solid var(--hoi4-panel-border);
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.primary-btn {
  background-color: var(--hoi4-accent);
  color: var(--hoi4-text);
}

.primary-btn:hover {
  background-color: #3a80d2;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.secondary-btn {
  background-color: var(--hoi4-panel-light);
  color: var(--hoi4-text);
}

.secondary-btn:hover {
  background-color: #424855;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-layout {
    flex-direction: column;
    padding: 1rem;
  }
  
  .settings-nav-panel {
    width: 100%;
    min-width: 0;
  }
  
  .site-header h1 {
    font-size: 2.2rem;
  }
  
  .content-area {
    max-height: none;
    overflow: visible;
  }
  
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .site-header h1 {
    font-size: 1.8rem;
  }
  
  .tagline {
    font-size: 0.8rem;
  }
  
  .panel-header h2 {
    font-size: 1.1rem;
  }
  
  .settings-actions {
    flex-direction: column;
    gap: 0.8rem;
  }
  
  .hoi4-btn {
    width: 100%;
  }
}
</style>
