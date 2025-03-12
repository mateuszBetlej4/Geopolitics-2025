<template>
  <div class="map-container">
    <div v-if="loading" class="map-loading">
      <div class="spinner"></div>
      <p>Loading map...</p>
    </div>
    <div id="map" ref="mapContainer"></div>
    <div class="map-controls">
      <button @click="zoomIn" class="map-btn">+</button>
      <button @click="zoomOut" class="map-btn">-</button>
      <button @click="resetView" class="map-btn">
        <span class="reset-icon">⟲</span>
      </button>
    </div>
    <div v-if="selectedCountry" class="country-info">
      <h3>{{ selectedCountry.name }}</h3>
      <p v-if="selectedCountry.leader">
        <strong>Leader:</strong> {{ selectedCountry.leader }}
      </p>
      <p v-if="selectedCountry.gdp">
        <strong>GDP:</strong> ${{ formatNumber(selectedCountry.gdp) }} billion
      </p>
      <p v-if="selectedCountry.military_power">
        <strong>Military Power:</strong> {{ selectedCountry.military_power }}
      </p>
      <button @click="selectCountry(null)" class="close-btn">×</button>
    </div>
    <MapLegend v-if="showLegend" />
    <button @click="toggleLegend" class="legend-toggle">
      {{ showLegend ? 'Hide Legend' : 'Show Legend' }}
    </button>
    <div class="map-style-control">
      <button 
        v-for="style in mapStyles" 
        :key="style.id" 
        @click="changeMapStyle(style.id)" 
        class="style-btn"
        :class="{ active: currentStyle === style.id }"
      >
        {{ style.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import MapLegend from './MapLegend.vue';
import * as turf from '@turf/turf';

// Import country GeoJSON data
// We'll use a CDN for now, but you can replace this with your own GeoJSON file
const GEOJSON_URL =
  "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json";

// Props
const props = defineProps({
  nations: {
    type: Array,
    default: () => [],
  },
  initialCenter: {
    type: Array,
    default: () => [0, 30],
  },
  initialZoom: {
    type: Number,
    default: 2,
  },
});

// Emits
const emit = defineEmits(["country-selected"]);

// Refs
const mapContainer = ref(null);
const map = ref(null);
const geojsonData = ref(null);
const selectedCountry = ref(null);
const showLegend = ref(true); // Show legend by default
const loading = ref(true); // Loading state
const currentStyle = ref('streets');

// Map styles
const mapStyles = [
  { id: 'streets', name: 'Streets', url: 'https://demotiles.maplibre.org/style.json' },
  { id: 'satellite', name: 'Satellite', url: 'https://api.maptiler.com/maps/hybrid/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL' },
  { id: 'terrain', name: 'Terrain', url: 'https://api.maptiler.com/maps/topo/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL' }
];

// Get color based on military power
const getCountryColor = (nation) => {
  // Color countries based on their military power
  if (!nation || !nation.military_power) return "#CCCCCC";

  if (nation.military_power > 90) return "#FF5733"; // Strong military (red)
  if (nation.military_power > 70) return "#FFC300"; // Medium-strong military (yellow)
  if (nation.military_power > 50) return "#DAF7A6"; // Medium military (light green)
  return "#C4E1FF"; // Weaker military (light blue)
};

// Helper functions
const getNationByCode = (code) => {
  if (!code) return null;

  // Map ISO country codes to nation names
  const codeToName = {
    US: "United States",
    CN: "China",
    RU: "Russia",
    IN: "India",
    FR: "France",
    DE: "Germany",
    GB: "United Kingdom",
    PL: "Poland",
    UA: "Ukraine",
    KP: "North Korea",
  };

  const name = codeToName[code];
  return props.nations.find((nation) => nation.name === name);
};

const getNationByName = (name) => {
  return props.nations.find((nation) => nation.name === name);
};

const formatNumber = (num) => {
  return num.toLocaleString();
};

// Map control functions
const zoomIn = () => {
  if (map.value) {
    map.value.zoomIn();
  }
};

const zoomOut = () => {
  if (map.value) {
    // Only zoom out if current zoom is greater than minimum zoom
    if (map.value.getZoom() > map.value.getMinZoom()) {
      map.value.zoomOut();
    }
  }
};

const resetView = () => {
  if (map.value) {
    map.value.flyTo({
      center: [props.initialCenter[1], props.initialCenter[0]], // MapLibre uses [lng, lat]
      zoom: props.initialZoom,
      essential: true
    });
  }
};

// Country selection
const selectCountry = (nation) => {
  selectedCountry.value = nation;
  emit("country-selected", nation);
};

// Set up geojson layer styling
const setupGeoJsonLayer = () => {
  if (!map.value || !geojsonData.value) return;
  
  // Add a geojson source
  if (!map.value.getSource('countries')) {
    map.value.addSource('countries', {
      type: 'geojson',
      data: geojsonData.value
    });
  } else {
    map.value.getSource('countries').setData(geojsonData.value);
  }

  // Add a layer for country fills
  if (!map.value.getLayer('country-fills')) {
    map.value.addLayer({
      id: 'country-fills',
      type: 'fill',
      source: 'countries',
      layout: {},
      paint: {
        'fill-color': [
          'match',
          ['get', 'iso_a2'],
          ...props.nations.flatMap(nation => {
            const code = Object.keys(codeToName).find(
              key => codeToName[key] === nation.name
            );
            return code ? [code, getCountryColor(nation)] : [];
          }),
          '#CCCCCC' // Default color
        ],
        'fill-opacity': 0.7
      }
    });
  }

  // Add a layer for country borders
  if (!map.value.getLayer('country-borders')) {
    map.value.addLayer({
      id: 'country-borders',
      type: 'line',
      source: 'countries',
      layout: {},
      paint: {
        'line-color': '#2A2A2A',
        'line-width': 2,
        'line-opacity': 1
      }
    });
  }

  // Add a layer for highlighted country
  if (!map.value.getLayer('country-highlighted')) {
    map.value.addLayer({
      id: 'country-highlighted',
      type: 'line',
      source: 'countries',
      layout: {},
      paint: {
        'line-color': '#FFFFFF',
        'line-width': 3,
        'line-opacity': [
          'case',
          ['boolean', ['feature-state', 'hover'], false],
          1,
          0
        ]
      }
    });
  }
};

// Handle country hover and click events
const setupCountryInteractions = () => {
  let hoveredStateId = null;

  // When the mouse moves over the country-fills layer, update the feature state
  map.value.on('mousemove', 'country-fills', (e) => {
    if (e.features.length > 0) {
      if (hoveredStateId !== null) {
        map.value.setFeatureState(
          { source: 'countries', id: hoveredStateId },
          { hover: false }
        );
      }
      hoveredStateId = e.features[0].id;
      map.value.setFeatureState(
        { source: 'countries', id: hoveredStateId },
        { hover: true }
      );
    }
  });

  // When the mouse leaves the country-fills layer, reset the feature state
  map.value.on('mouseleave', 'country-fills', () => {
    if (hoveredStateId !== null) {
      map.value.setFeatureState(
        { source: 'countries', id: hoveredStateId },
        { hover: false }
      );
    }
    hoveredStateId = null;
  });

  // When a country is clicked, select it
  map.value.on('click', 'country-fills', (e) => {
    if (e.features.length > 0) {
      const feature = e.features[0];
      const countryCode = feature.properties.iso_a2;
      const nation = getNationByCode(countryCode);

      if (nation) {
        selectCountry(nation);
        
        // Fly to the country's bounds
        const bbox = turf.bbox(feature.geometry);
        map.value.fitBounds([
          [bbox[0], bbox[1]],
          [bbox[2], bbox[3]]
        ], { padding: 50 });
      }
    }
  });

  // Change cursor on hover
  map.value.on('mouseenter', 'country-fills', () => {
    map.value.getCanvas().style.cursor = 'pointer';
  });

  map.value.on('mouseleave', 'country-fills', () => {
    map.value.getCanvas().style.cursor = '';
  });
};

// Add capital markers
const addCapitalMarkers = () => {
  // Define capital cities for major nations
  const capitals = [
    { name: 'Washington D.C.', country: 'United States', coords: [38.8951, -77.0364] },
    { name: 'Beijing', country: 'China', coords: [39.9042, 116.4074] },
    { name: 'Moscow', country: 'Russia', coords: [55.7558, 37.6173] },
    { name: 'New Delhi', country: 'India', coords: [28.6139, 77.2090] },
    { name: 'Paris', country: 'France', coords: [48.8566, 2.3522] },
    { name: 'Berlin', country: 'Germany', coords: [52.5200, 13.4050] },
    { name: 'London', country: 'United Kingdom', coords: [51.5074, -0.1278] },
    { name: 'Warsaw', country: 'Poland', coords: [52.2297, 21.0122] },
    { name: 'Kyiv', country: 'Ukraine', coords: [50.4501, 30.5234] },
    { name: 'Pyongyang', country: 'North Korea', coords: [39.0392, 125.7625] }
  ];

  // Add marker elements for capitals
  capitals.forEach(capital => {
    const nation = getNationByName(capital.country);
    
    // Create a marker element
    const marker = document.createElement('div');
    marker.className = 'capital-marker';
    marker.innerHTML = '<div class="capital-icon"></div>';
    
    // Add the marker to the map
    const markerObj = new maplibregl.Marker(marker)
      .setLngLat([capital.coords[1], capital.coords[0]]) // MapLibre uses [lng, lat]
      .addTo(map.value);
    
    // Add a popup with the capital name
    const popup = new maplibregl.Popup({
      closeButton: false,
      closeOnClick: false,
      className: 'capital-tooltip'
    }).setText(`${capital.name} (${capital.country})`);
    
    // Show popup on hover
    marker.addEventListener('mouseenter', () => {
      markerObj.setPopup(popup);
      popup.addTo(map.value);
    });
    
    marker.addEventListener('mouseleave', () => {
      popup.remove();
    });
    
    // Select nation on click
    marker.addEventListener('click', () => {
      if (nation) {
        selectCountry(nation);
      }
    });
  });
};

// Change map style
const changeMapStyle = (styleId) => {
  if (map.value && styleId !== currentStyle.value) {
    const style = mapStyles.find(s => s.id === styleId);
    if (style) {
      currentStyle.value = styleId;
      map.value.setStyle(style.url);
      
      // Re-add data sources and layers when style is loaded
      map.value.once('styledata', () => {
        setupGeoJsonLayer();
        addCapitalMarkers();
      });
    }
  }
};

// Initialize map
const initMap = async () => {
  loading.value = true;

  try {
    // Fetch GeoJSON data
    const response = await fetch(GEOJSON_URL);
    geojsonData.value = await response.json();
    
    // Give each feature a unique id
    geojsonData.value.features.forEach((feature, index) => {
      feature.id = index;
    });
    
    // Create the map
    map.value = new maplibregl.Map({
      container: mapContainer.value,
      style: mapStyles.find(s => s.id === currentStyle.value).url,
      center: [props.initialCenter[1], props.initialCenter[0]], // MapLibre uses [lng, lat]
      zoom: props.initialZoom,
      minZoom: 2,
      maxZoom: 10,
      attributionControl: true
    });
    
    // Add navigation controls (without the default zoom buttons as we have custom ones)
    const navControl = new maplibregl.NavigationControl({
      showCompass: true,
      showZoom: false,
      visualizePitch: true
    });
    map.value.addControl(navControl, 'top-left');
    
    // Add a fullscreen control
    map.value.addControl(new maplibregl.FullscreenControl(), 'top-left');
    
    // Wait for the map to load before adding layers
    map.value.on('load', () => {
      setupGeoJsonLayer();
      setupCountryInteractions();
      addCapitalMarkers();
      loading.value = false;
    });
    
  } catch (error) {
    console.error('Error loading map data:', error);
    loading.value = false;
  }
};

// Update layers when nations data changes
watch(
  () => props.nations,
  () => {
    setupGeoJsonLayer();
  },
  { deep: true }
);

// Toggle legend visibility
const toggleLegend = () => {
  showLegend.value = !showLegend.value;
};

// Lifecycle hooks
onMounted(() => {
  initMap();
});

onUnmounted(() => {
  if (map.value) {
    map.value.remove();
  }
});

// Map ISO country codes to nation names - needed for layer styling
const codeToName = {
  US: "United States",
  CN: "China",
  RU: "Russia",
  IN: "India",
  FR: "France",
  DE: "Germany",
  GB: "United Kingdom",
  PL: "Poland",
  UA: "Ukraine",
  KP: "North Korea",
};
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#map {
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* Position zoom controls in the top-right with more space */
.map-controls {
  position: absolute;
  top: 70px; /* Move down to avoid overlap with navigation controls */
  right: 10px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.map-btn {
  width: 30px;
  height: 30px;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ccc;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.map-btn:hover {
  background-color: white;
}

.reset-icon {
  font-size: 14px;
}

/* Style switcher */
.map-style-control {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.style-btn {
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 5px 8px;
  font-size: 12px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.style-btn:hover {
  background-color: white;
}

.style-btn.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* Position country info in the bottom-left */
.country-info {
  position: absolute;
  bottom: 40px; /* Move up to avoid overlap with attribution */
  left: 20px;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 250px; /* Slightly smaller to fit better */
  z-index: 900;
}

.country-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: var(--primary-color);
  font-size: 16px; /* Slightly smaller font */
}

.country-info p {
  margin: 5px 0;
  font-size: 14px; /* Slightly smaller font */
}

.close-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

/* Position legend toggle button */
.legend-toggle {
  position: absolute;
  bottom: 20px;
  right: 20px; /* Adjusted position */
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 5px 10px;
  font-size: 12px;
  cursor: pointer;
  z-index: 900;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.legend-toggle:hover {
  background-color: white;
}

/* Capital marker styles */
.capital-marker {
  width: 12px;
  height: 12px;
  cursor: pointer;
}

.capital-icon {
  width: 8px;
  height: 8px;
  background-color: white;
  border: 2px solid #333;
  border-radius: 50%;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.4);
}

/* Loading animation */
.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--secondary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Media queries for responsive design */
@media (max-width: 768px) {
  .country-info {
    max-width: 200px;
    padding: 10px;
    font-size: 12px;
  }
  
  .country-info h3 {
    font-size: 14px;
  }
  
  .country-info p {
    font-size: 12px;
  }
  
  .legend-toggle {
    bottom: 10px;
    right: 10px;
    padding: 3px 8px;
    font-size: 10px;
  }
  
  .map-controls {
    top: 60px;
  }
  
  .map-btn {
    width: 26px;
    height: 26px;
  }
  
  .style-btn {
    padding: 3px 6px;
    font-size: 10px;
  }
}
</style>
