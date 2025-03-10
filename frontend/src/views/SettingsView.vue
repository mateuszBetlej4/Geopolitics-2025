<template>
  <div class="settings-container">
    <h1>Game Settings</h1>

    <div class="settings-section">
      <h2>Game Options</h2>

      <div class="setting-item">
        <label for="difficulty">Difficulty Level</label>
        <select id="difficulty" v-model="settings.difficulty">
          <option value="easy">Easy</option>
          <option value="normal">Normal</option>
          <option value="hard">Hard</option>
          <option value="expert">Expert</option>
        </select>
      </div>

      <div class="setting-item">
        <label for="gameSpeed">Default Game Speed</label>
        <select id="gameSpeed" v-model="settings.gameSpeed">
          <option value="slow">Slow</option>
          <option value="normal">Normal</option>
          <option value="fast">Fast</option>
        </select>
      </div>

      <div class="setting-item checkbox">
        <input
          type="checkbox"
          id="autoPause"
          v-model="settings.autoPauseEvents"
        />
        <label for="autoPause">Auto-pause on major events</label>
      </div>

      <div class="setting-item checkbox">
        <input
          type="checkbox"
          id="tutorialMode"
          v-model="settings.tutorialMode"
        />
        <label for="tutorialMode">Enable tutorial mode</label>
      </div>
    </div>

    <div class="settings-section">
      <h2>Display Settings</h2>

      <div class="setting-item">
        <label for="mapStyle">Map Style</label>
        <select id="mapStyle" v-model="settings.mapStyle">
          <option value="political">Political</option>
          <option value="satellite">Satellite</option>
          <option value="terrain">Terrain</option>
        </select>
      </div>

      <div class="setting-item">
        <label for="uiScale">UI Scale</label>
        <select id="uiScale" v-model="settings.uiScale">
          <option value="small">Small</option>
          <option value="medium">Medium</option>
          <option value="large">Large</option>
        </select>
      </div>

      <div class="setting-item checkbox">
        <input type="checkbox" id="darkMode" v-model="settings.darkMode" />
        <label for="darkMode">Dark Mode</label>
      </div>
    </div>

    <div class="settings-section">
      <h2>Audio Settings</h2>

      <div class="setting-item">
        <label for="masterVolume">Master Volume</label>
        <input
          type="range"
          id="masterVolume"
          v-model="settings.masterVolume"
          min="0"
          max="100"
        />
        <span>{{ settings.masterVolume }}%</span>
      </div>

      <div class="setting-item">
        <label for="musicVolume">Music Volume</label>
        <input
          type="range"
          id="musicVolume"
          v-model="settings.musicVolume"
          min="0"
          max="100"
        />
        <span>{{ settings.musicVolume }}%</span>
      </div>

      <div class="setting-item">
        <label for="sfxVolume">Sound Effects Volume</label>
        <input
          type="range"
          id="sfxVolume"
          v-model="settings.sfxVolume"
          min="0"
          max="100"
        />
        <span>{{ settings.sfxVolume }}%</span>
      </div>

      <div class="setting-item checkbox">
        <input type="checkbox" id="muteAll" v-model="settings.muteAll" />
        <label for="muteAll">Mute All</label>
      </div>
    </div>

    <div class="settings-actions">
      <button @click="saveSettings" class="btn-primary">Save Settings</button>
      <button @click="resetSettings" class="btn-secondary">
        Reset to Default
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

// Default settings
const defaultSettings = {
  difficulty: "normal",
  gameSpeed: "normal",
  autoPauseEvents: true,
  tutorialMode: false,
  mapStyle: "political",
  uiScale: "medium",
  darkMode: false,
  masterVolume: 80,
  musicVolume: 70,
  sfxVolume: 90,
  muteAll: false,
};

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
.settings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

h1 {
  color: var(--primary-color);
  margin-bottom: 2rem;
  text-align: center;
}

.settings-section {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.settings-section h2 {
  color: var(--primary-color);
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.setting-item {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.setting-item label {
  flex: 1;
  font-weight: bold;
}

.setting-item select,
.setting-item input[type="range"] {
  width: 200px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.setting-item span {
  margin-left: 1rem;
  width: 50px;
  text-align: right;
}

.setting-item.checkbox {
  display: flex;
  align-items: center;
}

.setting-item.checkbox input {
  margin-right: 0.5rem;
  width: auto;
}

.setting-item.checkbox label {
  flex: 1;
}

.settings-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

button {
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  border: none;
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

@media (max-width: 768px) {
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .setting-item label {
    margin-bottom: 0.5rem;
  }

  .setting-item select,
  .setting-item input[type="range"] {
    width: 100%;
  }

  .setting-item.checkbox {
    flex-direction: row;
  }
}
</style>
