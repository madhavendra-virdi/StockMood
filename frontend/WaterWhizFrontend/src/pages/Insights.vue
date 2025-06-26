<template>
  <div>
    <div class="insights_box">
      <div class="banner">
        <img
          :src="getImage(selectedStock ? selectedStock['Sub_Industry'] : '')"
          style="
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 36px 36px 36px 36px;
          "
        />
        <div class="text_box">
          
          <div class="text_box_child"> 
            <div class="title">{{ selectedStock ? selectedStock.Name : 'N/A' }}
              <i 
                class="star-icon" 
                :class="isFavorited ? 'fas fa-star' : 'far fa-star'" 
                @click="toggleFavorite"
              ></i>
            </div>
            <div class="content">{{ selectedStock ? selectedStock.Price : 'N/A' }}</div>
            <div class="content" >{{ selectedStock ? selectedStock.Industry : 'N/A' }}</div>
            <div class="content">{{ selectedStock ? selectedStock['Sub_Industry'] : 'N/A' }}
            </div>
          </div>

        </div>
      </div>
      <div class="insights_content">
        <div class="left_box">
          <div
            :key="index"
            v-for="(item, index) in leftData"
            :class="item.isactive ? 'left_box_item active' : ''"
            class="left_box_item"
            @click="clickItem(item)"
          >
            {{ item.title }}

            <img
              v-if="item.isactive"
              src="@/assets/images/education/jiantou_isactive.png"
            />
            <img v-else src="@/assets/images/education/jiantou.png" />
          </div>
        </div>

        <div class="right_box">
          <overviewCom v-if="leftData[0].isactive"></overviewCom>
          <aboutCom v-if="leftData[1].isactive"></aboutCom>
          <streetCom v-if="leftData[2].isactive"></streetCom>
          <homeCom v-if="leftData[3].isactive"></homeCom>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import overviewCom from "./InsightsCom/overview.vue";
import aboutCom from "./InsightsCom/aboutCom.vue";

import homeCom from "./InsightsCom/homeCom.vue";
import streetCom from "./InsightsCom/streetCom.vue";
import axios from 'axios';

export default {
  components: {
    aboutCom,
    homeCom,
    overviewCom,
    streetCom
  },
  data() {
    return {
      selectedStock: JSON.parse(sessionStorage.getItem('selectedStock')) || null,
      stocks: [],
      isFavorited: false,
      leftData: [
        { title: "Overview",
          key: "overview",
          isactive: true  },
        {
          title: "Sentiment Analysis",
          isactive: true,
          key: "sentimentAnalysis"
        },
        {
          title: "Relative Valuation",
          isactive: false,
          key: "relativeValuation"
        },
        {
          title: "Modelling",
          isactive: false,
          key: "modelling"
        }
      ]
    };
  },
  mounted() {
    const querySymbol = this.$route.query.stock;
    const fallback = sessionStorage.getItem('selectedStock');

    if (querySymbol) {
      // Try fetching from backend using ?stock=
      this.loadStockFromBackend(querySymbol).then(() => {
        this.setActiveTabFromRoute();
      });
    } else if (fallback) {
      this.selectedStock = JSON.parse(fallback);
      this.checkIfFavorited();
      this.setActiveTabFromRoute();
    } else {
      console.warn("❌ No selected stock found via route or sessionStorage.");
    }
  },
  watch: {
    "$route.query.tab": function () {
      this.setActiveTabFromRoute();
    },
    "$route.query.stock"(newSymbol) {
      if (newSymbol) {
        this.loadStockFromBackend(newSymbol);
      }
    },
    "$route.query.tab"(tabKey) {
      this.setActiveTabFromRoute();
    }
  },
  methods: {
    async fetchStockList() {
      try {
        const response = await axios.get('/api/stocks');
        console.log("Fetched stocks:", response.data.stocks);
        this.stocks = response.data.stocks;
      } catch (error) {
        console.error('Error fetching stock list:', error);
      }
    },
    clickItem(item) {
      this.leftData.forEach((tab) => (tab.isactive = false));
      item.isactive = true;
      this.$router.push({ query: { tab: item.key } });
    },
    setActiveTabFromRoute() {
      const tabKey = this.$route.query.tab;

      // Always reset all to inactive first
      this.leftData.forEach(tab => tab.isactive = false);

      if (tabKey) {
        const found = this.leftData.find(tab => tab.key === tabKey);
        if (found) {
          found.isactive = true;
        }
      } else {
      // Fallback: activate the first tab (Overview) by default
      this.leftData[0].isactive = true;
      }
    },
    checkIfFavorited() {
      const user = localStorage.getItem('loggedInUser');
      if (!user || !this.selectedStock) return;

      axios.get(`/api/user-favorites/${user}`)
        .then(res => {
           this.isFavorited = res.data.includes(this.selectedStock.Name);
        })
        .catch(err => {
          console.error("Error checking favorite:", err);
        });
    },
    
    loadStockFromBackend(symbol) {
      if (!symbol) {
        console.warn("No stock symbol provided in route query.");
        return;
      }

      const decodedSymbol = decodeURIComponent(symbol);
      console.log("🔍 Fetching stock:", decodedSymbol);

      return axios.get(`/api/stock/${encodeURIComponent(decodedSymbol)}`)
        .then(res => {
          if (res.data && res.data.stock_details && res.data.stock_details.length > 0) {
            this.selectedStock = res.data.stock_details[0];
            sessionStorage.setItem('selectedStock', JSON.stringify(this.selectedStock));
            this.checkIfFavorited();
          } else {
            console.warn("⚠️ No stock details found for:", decodedSymbol);
            this.selectedStock = null;
          }
        })
        .catch(err => {
          console.error("❌ Failed to fetch stock from backend:", err);
          this.selectedStock = null;
        });
    },


    toggleFavorite() {
      const user = localStorage.getItem('loggedInUser');
      if (!user) {
        this.$message.warning("Please login to favorite a stock.");
        this.$router.push('/login');
        return;
      }
      if (!this.selectedStock) return;
      const endpoint = this.isFavorited ? '/api/unfavorite-stock' : '/api/favorite-stock';
      axios.post(`${endpoint}`, {
        username: user,
        stock_symbol: this.selectedStock.Name
      }).then(() => {
        this.isFavorited = !this.isFavorited;
      }).catch(err => {
        console.error("Error toggling favorite:", err);
      });
    },
    getImage(subIndustry) {
  const industryImages = {
    "Biotech": require('@/assets/images/biotech2.png'),
    "Software": require('@/assets/images/software.jpg'),
    "Pharmaceuticals": require('@/assets/images/biotech2.png'),
    "Technology": require('@/assets/images/biotech2.png'),
    "Energy": require('@/assets/images/biotech2.png'),
    "Automotive": require('@/assets/images/biotech2.png'),
    "Healthcare": require('@/assets/images/biotech2.png'),
    "Finance": require('@/assets/images/biotech2.png'),
    "Retail": require('@/assets/images/biotech2.png'),
    "Telecommunications": require('@/assets/images/biotech2.png')
  };

  return industryImages[subIndustry] || require('@/assets/images/biotech2.png');
}
  }
};
</script>



<style scoped lang="less">
.star-icon {
  margin-left: 20px;
  cursor: pointer;
  color: #ccc;
  font-size: 28px;
  transition: color 0.3s ease;
}
.star-icon.fas {
  color: #f4c542; // Yellow color for filled star
}
.search-container {
    margin-top: 120px;
    margin-bottom: 120px;
    text-align: center;
  }

  .search-bar {
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    border-radius: 25px;
    width: 100%;
    background: linear-gradient(to right, #e784ee, #a9c0e8); /* Dark yellow to orange gradient */
    color: white;
    transition: background 0.5s ease;
  }

  .search-bar::placeholder {
    color: #f3f3f3; /* Grey placeholder */
  }

  .search-bar:focus {
    background: linear-gradient(to right, #ffad15, #d97700); /* Slightly brighter orange when focused */
    outline: none;
  }
  .dropdown-list {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 25px;
  width: 52.5%;
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  max-height: 200px;
  overflow-y: auto;
  list-style-type: none;
  padding: 0;
  margin: 0;
  z-index: 10;
}

.dropdown-list li {
  padding: 10px;
  cursor: pointer;
}

.dropdown-list li:hover {
  background: lightgray;
}

.insights_box {
  padding: 0 21px;

  // padding: 20px 120px;
  //   width: 1180px;
  margin: 0 auto;
  .banner {
    width: 100%;
    height: 220px;
    position: relative;
    .text_box {
      position: absolute;
      top: 10%;
      color: #0c0c0c;
      //   width: 100%;
      text-align: center;
      display: flex;
      padding-left: 100px;
      margin-top: 0;
      .text_box_child {
        // backdrop-filter: blur(5px);
        color: #8ca6db;
        padding: 10px 20px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 16px;
        backdrop-filter: blur(6px);
      }
      .title {
        font-size: 36px;
        font-weight: 600;
      }
      .content {
        font-size: 20px;
        font-weight: 500;
        margin-top: 6px;
      }
    }
  }
  .insights_text {
    margin-top: 50px;
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    width: 1380px;
    margin: 50px auto;
  }
  .insights_remark {
    margin-top: 50px;
    font-size: 24px;
    // background: #a9c0e8;
    color: #000;
    width: 1380px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin: 30px auto;
  }
  .insights_content {
    display: flex;
    flex-direction: column; // instead of row
    width: 100%;
    margin: 20px auto;
    align-items: center;
    .left_box {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      padding: 10px 0;
      margin-bottom: 20px;

      .left_box_item {
        padding: 10px 22px;
        font-size: 16px;
        font-weight: 500;
        border-radius: 999px;
        border: 1px solid transparent;
        background-color: #f3f3f3;
        color: #333;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);

        display: flex;
        align-items: center;
        gap: 10px;

        img {
          width: 12px;
          height: 12px;
        }

        &:hover {
          background-color: #e4e4e4;
          cursor: pointer;
        }
      }

      .active {
        background-color: #a9c0e8;
        color: white;
        font-weight: 600;
        border: 1px solid #a9c0e8;
        box-shadow: 0 2px 10px rgba(169, 192, 232, 0.4);
      }
    }


    .right_box {
      width: 90%;
      margin-top: 20px;
      background: #fff;
    }
  }
}
</style>
