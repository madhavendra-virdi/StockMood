<template>
  <div>
    <div id="container">
      <div id="map"></div>
      <div id="sidebar">
        <div class="legend">
          <h3>Priority Level</h3>
          <div class="color-box">
            <div style="background-color:#08306b;"></div>
            &nbsp;&nbsp; 6 ML/Year
          </div>
          <div class="color-box">
            <div style="background-color:#2171b5;"></div>
            4 - 6 ML/Year
          </div>
          <div class="color-box">
            <div style="background-color:#6baed6;"></div>
            2 - 4 ML/Year
          </div>
          <div class="color-box">
            <div style="background-color:#c6dbef;"></div>
            1 - 2 ML/Year
          </div>
          <div class="color-box">
            <div style="background-color:#eff3ff;"></div>
            0 - 1 ML/Year
          </div>
        </div>
        <div class="legend">
          <h3>Measure Names</h3>
          <div class="color-box">
            <div style="background-color:rgba(54, 162, 235, 0.8);"></div>
            Harvesting
          </div>
          <div class="color-box">
            <div style="background-color:rgba(75, 192, 192, 0.8);"></div>
            Infiltration
          </div>
        </div>
      </div>
    </div>
    <div id="description">Harvesting and Infiltration at each Catchment</div>
    <canvas id="chart"></canvas>
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
      map: null,
      myChart: null
    };
  },
  mounted() {
    this.initMap();
    this.initChart();
  },
  methods: {
    initMap() {
      // Initialize Leaflet map
      this.map = L.map("map", {
        center: [-37.8136, 144.9631],
        zoom: 9,
        layers: []
      });

      // Add tile layer
      L.tileLayer(
        "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        {
          attribution: "Map data © OpenStreetMap contributors, CartoDB"
        }
      ).addTo(this.map);

      // Load GeoJSON data and apply styles and click events
      localAxios
        .get(
          "/static/STORMWATER_PRIORITY_AREAS_HWS_3367393708685921605.geojson"
        )
        .then(response => {
          console.log(response);
          const data = response.data;
          console.log(data);
          L.geoJSON(data, {
            style: feature => {
              const harvesting = feature.properties.HARV_ML_Y_IMP_HA || 0;
              return {
                fillColor: this.getColorBasedOnHarvesting(harvesting),
                weight: 2,
                color: "white",
                fillOpacity: 0.7
              };
            },
            onEachFeature: (feature, layer) => {
              layer.on("click", () => {
                const properties = feature.properties;
                const popupContent =
                  "<b>Catchment:</b> " +
                  (properties.CATCHMENT || "Unknown") +
                  "<br/><b>Harvesting (ML/Year):</b> " +
                  (properties.HARV_ML_Y_IMP_HA || "Unknown") +
                  "<br/><b>Infiltration (ML/Year):</b> " +
                  (properties.INF_ML_Y_IMP_HA || "Unknown") +
                  "<br/><b>Subcatchment:</b> " +
                  (properties.SUBCATCHMENT || "Unknown") +
                  "<br/><b>Subcatch Id:</b> " +
                  (properties.SUBCATCH_ID || "Unknown");
                layer.bindPopup(popupContent).openPopup();
                // Update chart
                this.updateChart(
                  properties.CATCHMENT,
                  properties.HARV_ML_Y_IMP_HA,
                  properties.INF_ML_Y_IMP_HA
                );
              });
            }
          }).addTo(this.map);
        });
    },

    getColorBasedOnHarvesting(harvesting) {
      return harvesting > 6
        ? "#08306b"
        : harvesting > 4
        ? "#2171b5"
        : harvesting > 2
        ? "#6baed6"
        : harvesting > 1
        ? "#c6dbef"
        : "#eff3ff";
    },
    initChart() {
      const ctx = document.getElementById("chart").getContext("2d");
      this.myChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: [
            "Dandenong",
            "Maribyrnong",
            "Werribee",
            "Westernport",
            "Yarra"
          ],
          datasets: [
            {
              label: "Harvesting",
              data: [5, 3, 4, 2, 6],
              backgroundColor: "rgba(54, 162, 235, 0.8)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1
            },
            {
              label: "Infiltration",
              data: [2, 2, 3, 4, 5],
              backgroundColor: "rgba(75, 192, 192, 0.8)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },
    updateChart(catchmentName, harvesting, infiltration) {
      if (harvesting && infiltration) {
        this.myChart.data.datasets[0].data = [harvesting];
        this.myChart.data.datasets[1].data = [infiltration];
        this.myChart.data.labels = [catchmentName];
        this.myChart.update();
      }
    }
  }
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
#map {
  height: 635px;
  width: 1000px;
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
</style>
