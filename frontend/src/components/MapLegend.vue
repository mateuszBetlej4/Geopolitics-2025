<template>
  <div class="map-legend">
    <h4>Military Power</h4>
    <div class="legend-items">
      <div class="legend-item">
        <div class="color-box" style="background-color: #FF5733;"></div>
        <span>Strong (90+)</span>
      </div>
      <div class="legend-item">
        <div class="color-box" style="background-color: #FFC300;"></div>
        <span>Medium-Strong (70-90)</span>
      </div>
      <div class="legend-item">
        <div class="color-box" style="background-color: #DAF7A6;"></div>
        <span>Medium (50-70)</span>
      </div>
      <div class="legend-item">
        <div class="color-box" style="background-color: #C4E1FF;"></div>
        <span>Weaker (< 50)</span>
      </div>
      <div class="legend-item">
        <div class="color-box" style="background-color: #CCCCCC;"></div>
        <span>No Data</span>
      </div>
    </div>
  </div>
</template>

<script setup>
// No props or state needed for this simple component
</script>

<style scoped>
.map-legend {
  position: absolute;
  bottom: 50px;
  right: 20px;
  background-color: white;
  padding: 8px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 900;
  max-width: 180px;
  font-size: 11px;
  opacity: 0.9;
}

.map-legend h4 {
  margin-top: 0;
  margin-bottom: 6px;
  font-size: 13px;
  color: var(--primary-color);
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.color-box {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .map-legend {
    bottom: 40px;
    right: 10px;
    padding: 6px;
    max-width: 150px;
    font-size: 10px;
  }
  
  .map-legend h4 {
    font-size: 12px;
    margin-bottom: 4px;
  }
  
  .color-box {
    width: 12px;
    height: 12px;
  }
}
</style> 