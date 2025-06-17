<template>
  <div>
    <div id="container">
      <div id="map2"></div>
    </div>
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">Loading...</div>
    </div>
  </div>
</template>

<script>
import axios2 from "axios";
axios2.defaults.baseURL = "";
const localAxios = axios2.create({});
export default {
  name: "MapComponent",
  data() {
    return {
      map2: null,
      showMap: false,
      loading: false
    };
  },
  mounted() {
    this.showMap = false;
    let that = this;
    that.initMap();
  },
  methods: {
    initMap() {
      // Initialize Leaflet map
      this.map2 = L.map("map2", {
        center: [-37.8136, 144.9631], // Center the map on Melbourne
        zoom: 9,
        layers: []
      });

      // Add tile layer
      L.tileLayer(
        "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        {
          attribution: "Map data © OpenStreetMap contributors, CartoDB"
        }
      ).addTo(this.map2);

      // Load GeoJSON data
      localAxios
        .get(
          "/static/Catchments_-_Major_Catchments_of_Melbourne's_River_Basins.geojson"
        )
        .then(response => {
          const data = response.data;
          console.log(data, data.features.length, "datadata");
          // Loop through each feature in the GeoJSON data
          data.features.forEach(feature => {
            // Extract the first set of coordinates (longitude, latitude)
            let coordinates = feature.geometry.coordinates[0][0]; // Assuming it's a Polygon
            if (feature.geometry.coordinates[0][0].length > 2) {
              coordinates = feature.geometry.coordinates[0][0][0];
            }
            console.log(coordinates, "coordinates");
            // Extract the property value to determine color
            const propertyValue = feature.properties.AREA_SQ_KM; // Example: based on area size

            // Create a marker with the custom icon and add it to the map
            const marker = L.marker([coordinates[1], coordinates[0]]).addTo(
              this.map2
            );

            // Get the catchment name from properties
            const catchmentName =
              feature.properties.MAJOR_CATCHMENT_NAME || "Unknown Catchment";
            // Add click event to marker to fetch and display weather info
            marker.on("click", () => {
              // Fetch weather information based on coordinates
              this.getWeatherForecast(coordinates[1], coordinates[0]).then(
                weatherForecast => {
                  // Update the popup with weather information
                  const popupContent = `
              <strong style="font-weight:bold;font-size:20px"> ${catchmentName}</strong><br><br>
              <strong style="font-weight:bold;font-size:16px">Today:</strong> ${this.getstatus(
                    weatherForecast.today.precipitation
                  )}<br>
                 <strong style="font-weight:bold;font-size:16px">Tomorrow:</strong> ${this.getstatus(
                    weatherForecast.tomorrow.precipitation
                  )}<br>
                 <strong style="font-weight:bold;font-size:16px">Day After Tomorrow:</strong> ${this.getstatus(
                    weatherForecast.dayAfter.precipitation
                  )}<br>
             
            `;

                  marker.bindPopup(popupContent).openPopup();
                }
              );
            });
          });
        })
        .catch(error => {
          console.error("Error loading GeoJSON data:", error);
        });
    },
    getstatus(precipitation) {
      //       0 to 24mm ： good
      // 25 to 99mm ：Fair
      // 100mm + ：poor.
      if (precipitation <= 0.2) {
        return `<div style='font-weight: bold;font-size: 20px;color: #000000;display: flex;align-items: center;'><div style='width: 11px;height: 11px;background: #56E5C9;border-radius: 47px 47px 47px 47px;'></div>
        <div style='margin-left:10px'>GOOD</div>
        </div>`;
      } else if (precipitation <= 1 && precipitation > 0.2) {
        return `<div style='font-weight: bold;font-size: 20px;color: #000000;display: flex;align-items: center;'><div style='width: 11px;height: 11px;background: #F1CF27;border-radius: 47px 47px 47px 47px;'></div>
        <div style='margin-left:10px'>Fair</div>
        </div>`;
      } else {
        return `<div style='font-weight: bold;font-size: 20px;color: #000000;display: flex;align-items: center;'><div style='width: 11px;height: 11px;background: #E25D4E;border-radius: 47px 47px 47px 47px;'></div>
        <div style='margin-left:10px'>POOR</div>
        </div>`;
      }
    },
    getWeatherForecast(lat, lon) {
      this.loading = true; // Show loading spinner
      const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,precipitation&forecast_days=3`;

      return localAxios.get(apiUrl).then(response => {
        const weatherData = response.data;

        // Extracting forecast for today, tomorrow, and the day after
        const today = {
          // temp: weatherData.hourly.temperature_2m[0], // Assuming the first value is for today
          precipitation: weatherData.hourly.precipitation[0] // Assuming the first value is for today
        };

        const tomorrow = {
          // temp: weatherData.hourly.temperature_2m[24], // 24 hours later
          precipitation: weatherData.hourly.precipitation[24] // 24 hours later
        };

        const dayAfter = {
          // temp: weatherData.hourly.temperature_2m[48], // 48 hours later
          precipitation: weatherData.hourly.precipitation[48] // 48 hours later
        };
        this.loading = false; // Hide loading spinner after data is loaded

        return {
          today,
          tomorrow,
          dayAfter
        };
      });
    }
  }
  // Function to fetch 3-day weather forecast using Open-Meteo API
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  margin: 0;
  padding: 0;
}

#container {
  width: 100%;
  max-width: 1400px;
  display: flex;
  position: relative;
  justify-content: center;
}

#map2 {
  height: 635px;
  width: 1200px;
  margin-bottom: 10px;
  border-radius: 32px;
}

#chart {
  width: 1000px;
  height: 400px;
  margin: 0 auto;
}

#sidebar {
  width: 154px;
  margin-left: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 5px;
  position: absolute;
  right: -190px;
  top: 0;
  z-index: 10;
}

.color-box {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.color-box div {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}

#description {
  font-size: 18px;
  margin-bottom: 20px;
  text-align: center;
  width: 100%;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.loading-spinner {
  font-size: 20px;
  color: #333;
}
</style>
