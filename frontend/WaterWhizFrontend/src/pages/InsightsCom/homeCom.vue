<template>
  <div>
    <!-- Display Selected Stock Name -->
    <div id="table-note" v-if="selectedStock">
      <p>About : {{ selectedStock.About }}</p>
      <br>
      <p>Growth in operating income : {{ selectedStock.growth_in_operating_income }}   xxxxxxxxxxxxxxxxxxxxxxxxxxxxx  Best ROIC yr10: {{ parsedData.BestROCE }}</p>
      <p>Total reinvestment: {{ parsedData.TotalReinvestment }}  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  Industry ROIC: {{ selectedStock.Industry_ROIC }}</p>
      <p>Best scenario: {{ parsedData.best_scenario }}  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  Scenario: {{ selectedStock.Scenario_Behaviour_Description }}</p>
      <p>Equity capital: {{ parsedData.equity_capital_2024 }}  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  Reserves: {{ selectedStock.reserves_2024 }}</p>
      <p>Promoters involvement: {{ parsedData.PromoterHold }}</p>
      <p>P/E: {{ parsedData.PE }}</p>
      <p>MCap: {{ parsedData.MCap }}  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  Category: {{ selectedStock.MCap_category }}</p>
      <br>
    </div>

    <!-- Table Container -->
    <div id="table-container" v-if="selectedStock">
      <table id="data-table">
        <thead>
          <tr>
            <th>Year</th>
            <th v-for="year in years" :key="year">{{ year }}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Growth Rates (%)</td>
            <td v-for="(value, index) in parsedData.Revenue_Growth_Rates" :key="index">{{ value }}</td>
          </tr>
          <tr>
            <td>Revenues</td>
            <td v-for="(value, index) in parsedData.Forecasted_Revenues" :key="index">{{ value }}</td>
          </tr>
          <tr>
            <td>Operating Margin</td>
            <td v-for="(value, index) in parsedData.Operating_Margin_Forecast" :key="index" :style="{ color: value < 0 ? 'red' : 'black' }">
              {{ value }}
            </td>
          </tr>
          <tr>
            <td>Post-tax EBIT</td>
            <td v-for="(value, index) in parsedData.Forecasted_EBIT" :key="index">{{ value }}</td>
          </tr>
          <tr>
            <td>Reinvestment</td>
            <td v-for="(value, index) in parsedData.Reinvestment" :key="index">{{ value }}</td>
          </tr>
          <tr>
            <td>FCFF</td>
            <td v-for="(value, index) in parsedData.fcff" :key="index">{{ formatDecimal(value) }}</td>
          </tr>
          <tr>
            <td>WACC(%)</td>
            <td v-for="(value, index) in parsedData.WACC" :key="index">{{ value }}</td>
          </tr>
          <tr>
            <td>PV(FCFF)</td>
            <td v-for="(value, index) in parsedData.PV_FCFF" :key="index" :style="{ color: value < 0 ? 'red' : 'black' }">
              {{ formatDecimal(value) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

     <!-- Lower Section with Left Table for Stock Summary -->
     <div id="lower-section" v-if="selectedStock">
      <div id="left-table-container">
        <table id="left-data-table">
          <tbody>
            <tr><td>PV (Terminal Value)</td><td>{{ formatDecimal(parsedData.PV_FCFF.slice(-1)[0]) }}</td></tr>
            <tr><td>PV (10 Yr CFs)</td><td>{{ formatDecimal(parsedData.PV_FCFF.slice(0, -1).reduce((a, b) => a + b, 0)) }}</td></tr>
            <tr><td>Sum of PV_FCFF</td><td>{{ formatDecimal(parsedData.PV_FCFF.reduce((a, b) => a + b, 0)) }}</td></tr>
            <tr><td>- Debt Value</td><td>{{ formatDecimal(selectedStock.borrowings_2024) }}</td></tr>
            <tr><td>+ Cash Value</td><td>{{ formatDecimal(selectedStock.cash) }}</td></tr>
            <tr><td>+ Non-Operating Assets</td><td>{{ formatDecimal(selectedStock.other_assets_2024) }}</td></tr>
            <tr><td>Value of Equity</td>
  <td>
    {{ 
      formatDecimal(
        parsedData.PV_FCFF.map(x => Number(x)).reduce((a, b) => a + b, 0)
        - Number(selectedStock.borrowings_2024)
        + Number(selectedStock.cash)
        + Number(selectedStock.other_assets_2024)
      )
    }}
  </td>
</tr>            <tr><td>Number of Shares</td><td>{{ selectedStock.shares_outstanding }}</td></tr>
            <tr class="blue-row"><td>Estimated/Intrinsic Value</td><td>{{ formatDecimal(selectedStock.share_price) }}</td></tr>
          </tbody>
        </table>
      </div>
    <!-- Visualization Container -->
     <!-- Visualization Container -->
<div v-if="iframeSrc" class="plot-container">
  <iframe :src="iframeSrc" width="100%" height="600" frameborder="0"></iframe>
</div>
<div v-else>
  <p>No visualization available for the selected stock.</p>
</div>

     
    </div>
  </div>
</template>

<script>
import axios2 from "axios";

axios2.defaults.baseURL = "";
const localAxios = axios2.create({});

export default {
  name: "StockDetailsComponent",
  data() {
  let selectedStock = JSON.parse(sessionStorage.getItem('selectedStock')) || null;
  
  return {
    selectedStock,
    parsedData: selectedStock ? this.parseStockData(selectedStock) : {},
    years: ["BASE YEAR", ...Array.from({ length: 10 }, (_, i) => `${2025 + i}E`)],
    plotUrl: '',
    iframeSrc: selectedStock ? `/rapi/plot1?stock_name=${encodeURIComponent(selectedStock.Name)}` : ''
  };
}
,

  
  mounted() {
  },




  methods: {
    parseStockData(stock) {
      let parsedStock = { ...stock };

      // Convert stringified arrays to actual arrays
      ["Revenue_Growth_Rates", "Forecasted_Revenues", "Operating_Margin_Forecast", "Forecasted_EBIT", "fcff", "PV_FCFF"].forEach(key => {
        if (typeof parsedStock[key] === "string") {
          try {
            parsedStock[key] = JSON.parse(parsedStock[key]);
          } catch (e) {
            parsedStock[key] = []; // If parsing fails, set it as an empty array
          }
        }
      });

      // Determine the best scenario
      let bestScenario = Math.round(parsedStock.best_scenario);

      // Assign Reinvestment based on the best scenario
      parsedStock.Reinvestment = JSON.parse(parsedStock[`Forecasted_Reinvestment_Scenario_${bestScenario}`] || "[]");

      parsedStock.TotalReinvestment = JSON.parse(parsedStock[`total_reinvestment_${bestScenario}`] || "[]");

      parsedStock.BestROCE = JSON.parse(parsedStock[`Year_10_ROIC_${bestScenario}`] || "[]");


    
      // Compute WACC with 11 equal intervals
      let waccValue = Math.round(parsedStock.WACC);
      parsedStock.WACC = Array(11).fill(waccValue);

      return parsedStock;
    },
    formatDecimal(value) {
      return Number(value).toFixed(2);
    }
  }
};
</script>


<style scoped>



#lower-section {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1480px;
  margin-top: 20px;
}

#left-table-container {
  width: 45%;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 16px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* padding: 16px; */
}

#left-data-table {
  width: 100%;
  /* border-collapse: collapse; */
  background: #fff;
  color: #333;
}

#left-data-table td {
  /* border: 1px solid #ddd; */
  padding: 16px;
  text-align: left;
  font-size: 14px;
}

#left-data-table tr:nth-child(even) {
  background: #f9f9f9;
}

#left-data-table tr:hover {
  background: #e8f0fe;
  cursor: pointer;
  transition: background 0.3s ease-out;
}

#table-container {
  width: 100%;
  max-width: 1480px;
  overflow-y: auto;
  overflow-x: auto;
  margin-bottom: 50px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 16px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

#data-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  color: #333;
}

#data-table th, #data-table td {
  border: 1px solid #ddd;
  padding: 16px;
  text-align: center;
  font-size: 14px;
}

#data-table th {
  background: #f3f3f3;
  color: #333;
  text-transform: uppercase;
  font-weight: bold;
}

#data-table tr:nth-child(even) {
  background: #f9f9f9;
}

#data-table tr:hover {
  background: #e8f0fe;
  cursor: pointer;
  transition: background 0.3s ease-out;
}

.blue-row {
  background: #e8f0fe !important;
}
</style>
