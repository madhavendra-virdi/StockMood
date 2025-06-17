<template>
  <div>
    <!-- Shiny Container -->
    <div style="display: flex; width: 100%; box-sizing: border-box;">
  <!-- Left: Market Share Donut Chart -->
  <div style="width: 50%; padding-right: 10px; box-sizing: border-box;">
    <h3>Market Share Donut Chart</h3>
    <div v-if="iframeSrc" class="plot-container">
  <iframe :src="iframeSrc" width="100%" height="600" frameborder="0"></iframe>
</div>
<div v-else>
  <p>No visualization available for the selected stock.</p>
</div>
  </div>

  <!-- Right: DE Plot -->
  <div style="width: 50%; padding-left: 10px; box-sizing: border-box;">
    <h3>Debt-to-Equity (DE) Chart</h3>
    <div v-if="iframeSrc2" class="plot-container">
  <iframe :src="iframeSrc2" width="100%" height="600" frameborder="0"></iframe>
</div>
<div v-else>
  <p>No visualization available for the selected stock.</p>
</div>
  </div>
</div>



    <h1>Industry Relative ML Model Prediction</h1>
    <h2>Select Columns to Train Model</h2>


    <div id="table-container">
      <el-table :data="tableData" border id="data-table">
        <el-table-column 
          v-for="col in tableColumns" 
          :key="col" 
          :prop="col" 
          :label="col" 
          sortable
          header-align="center" 
          align="center">
          <template #header>
            <div @click="toggleColumnSelection(col)" class="checkbox-header">
              <img v-if="selectedColumns.includes(col)" class="checkbox" src="@/assets/images/Calculator/Checkbox-Input-选中@2x.png" />
              <img v-else class="checkbox" src="@/assets/images/Calculator/Checkbox-Input-默认@2x.png" />
              <span>{{ col }}</span>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <h2>Selected columns : {{ selectedColumns }}</h2>

    <div class="calculator_btn">
      <el-button @click="toSubmit" type="primary">Predict</el-button>
    </div>

    <h3 v-if="predictedPrice !== null">Predicted Price: {{ predictedPrice }}</h3>
  </div>
</template>

<script>
import axios from 'axios'; // Ensure axios is imported for API requests
import Plotly from 'plotly.js-dist';

export default {
  name: "BiotechComponent",
  
  data() {
    return {
      stocksInSubIndustry: null,
      tableColumns: [],
      tableData: [],
      selectedColumns: [],
      predictedPrice: null,  // Store the predicted price
      selectedStock: null,
      plotUrl: null,
      iframeSrc: null
    };
  },
  mounted() {
    // Fetch data from sessionStorage when component is mounted
    const storedStocks = sessionStorage.getItem('stocksInSubIndustry');
    let selectedStock = sessionStorage.getItem('selectedStock');

    if (selectedStock) {
  const parsedStock = JSON.parse(selectedStock);
  this.selectedStock = parsedStock.Name;
  let rawStockName = parsedStock.Name.trim();
  const encodedStockName = encodeURIComponent(rawStockName);


  this.iframeSrc = rawStockName ? `/rapi/plot2?stock_name=${encodeURIComponent(rawStockName)}` : ''
  this.iframeSrc2 = rawStockName ? `/rapi/plot3?stock_name=${encodeURIComponent(rawStockName)}` : ''
  console.log("plotUrl:", this.iframeSrc);
  console.log("plotde:", this.iframeSrc2);


}

    if (storedStocks) {
      let parsedData = JSON.parse(storedStocks);

      // Define the columns you want to keep
      const selectedColumns = [
        "Name", "Price", "Kd", "Ke", "DE", "debt_ratio", "debt_percent_2024", "PE", 
        "EV2EBITDA",'ROE','ROC_2024','sales_CAGR','EV2invested_capital','price2sales','EV2sales'
      ];

      // Filter only selected columns
      this.tableColumns = selectedColumns;
      this.tableData = parsedData.map(row => {
        let filteredRow = {};
        selectedColumns.forEach(col => {
          if (row[col] !== undefined) {
            filteredRow[col] = row[col];
          }
        });
        return filteredRow;
      });

      // Initialize selectedColumns with all selected by default
      this.selectedColumns = [...selectedColumns];
    }
  },
  methods: {
    
    toggleColumnSelection(col) {
      const index = this.selectedColumns.indexOf(col);
      if (index > -1) {
        this.selectedColumns.splice(index, 1);
      } else {
        this.selectedColumns.push(col);
      }
    },
    async toSubmit() {
      // Prepare the data for submission (remove the 'Name' column as it's not a predictor)
      const dataToSend = this.tableData.map(row => {
        const filteredRow = { ...row };
        // delete filteredRow.Name; // Don't send the 'Name' column as it's not a predictor
        return filteredRow;
      });

      console.log("Data being sent to /predict:", JSON.stringify({
  data: dataToSend,
  selectedStock: this.selectedStock
}, null, 2)); // Print the data


      try {
        // Send a POST request with the selected data
        const response = await axios.post('/api/predict', {
          data: dataToSend,
          selectedStock: this.selectedStock // Send selected stock name
        });

        // Get the predicted price from the backend response
        // const predictedPrice = response.data.predicted_price;
        const predictedPrice = response.data

        // Store the predicted price in the component's state
        this.predictedPrice = predictedPrice;

      } catch (error) {
        console.error('Error during prediction:', error);
        alert('Prediction failed. Please try again.');
      }
    }
  }
};
</script>

<style scoped>
.checkbox-header {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.checkbox {
  width: 16px;
  height: 16px;
  margin-right: 5px;
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
</style>
