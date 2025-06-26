<template>
  <div class="home_box">
    <div class="banner">
      <div class="video-bg">
        <video autoplay muted loop playsinline class="video-content">
          <source src="@/assets/tryout.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>

      <div class="text_box">
        <div class="text_box_child">
          <div class="title">
            The future of investment
            <br />
            research, fueled by AI.
            <div>
              <div class="search-container">
                <input
                  type="text"
                  class="search-bar"
                  v-model="searchQuery"
                  placeholder="Search your next investment idea..."
                  @focus="showDropdown = true"
                  @blur="hideDropdownWithDelay"
                  @input="debounceFilter"
                />
                <ul v-if="showDropdown && filteredStocks.length > 0" class="dropdown-list">
                  <li v-for="stock in filteredStocks" :key="stock" @mousedown="selectStock(stock)">
                    {{ stock }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="image-container">
      <img class="background-image" src="@/assets/images/home/twitter.png" alt="Twitter" />
      <img class="background-image" src="@/assets/images/home/reddit.png" alt="Reddit" />
      <img class="background-image" src="@/assets/images/home/nse.png" alt="NSE" />
      <img class="background-image" src="@/assets/images/home/et.png" alt="ET" />
      <img class="background-image" src="@/assets/images/home/youtube.png" alt="YouTube" />
    </div>
        

    <!-- FinChat-style Feature Section 1 -->
    <section class="feature_section">
      <div class="feature_content">
        <div class="text_side">
          <span class="tag">FEATURE</span>
          <h2>Accurate global financial data</h2>
          <p>
            Global financial data for public equities, ETFs and funds. With institutional-grade data
            trusted by leading asset managers and individuals alike, StockMood provides everything
            you need to analyze investments effectively.
          </p>
          <button class="cta">↪ Get Started</button>
        </div>
        <div class="image_side">
          <img src="@/assets/images/biotech.png" alt="Financial Data Screenshot" />
        </div>
      </div>
    </section>

    <!-- FinChat-style Feature Section 2 -->
    <section class="feature_section alt">
      <div class="feature_content">
        <div class="image_side">
          <img src="@/assets/images/biotech.png" alt="AI Research Screenshot" />
        </div>
        <div class="text_side">
          <span class="tag">FEATURE</span>
          <h2>Leverage AI to your benefit</h2>
          <p>
            Save time with AI tools and automations. Let the system do the grunt work while you
            focus on strategic thinking. StockMood blends classic financial workflows with next-gen
            AI.
          </p>
          <button class="cta">↪ Get Started</button>
        </div>
      </div>
    </section>
    <!-- Floating CTA Button -->
    <div class="floating-elements">
      <button class="floating-cta" @click="focusSearchBar">
        Try it for free?
      </button>

      <div v-if="showInfoPopup" class="info-popup">
        First select a stock to start
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: '',
      stocks: [],
      selectedStock: [],
      filteredStocks: [],
      showDropdown: false,
      showInfoPopup: false,
      websiteContentData: [
        {
          image: require("@/assets/images/home/Swim2x.png"),
          title: "Sentiment Score",
          content: "Gauge social influence across platforms.",
          router: "/insights?tab=sentimentAnalysis"
        },
        {
          image: require("@/assets/images/home/AI@2x.png"),
          title: "ML Model",
          content: "Train on your fav ratios & predict the future",
          router: "/insights?tab=relativeValuation"
        },
        {
          image: require("@/assets/images/home/qs@2x.png"),
          title: "FCFF Valuation",
          content: "Decrypt traditional finance",
          router: "/insights?tab=modelling"
        }
      ]
    };
  },

  mounted() {
    this.fetchStockList();
  },

  methods: {
    async fetchStockList() {
      try {
        const response = await axios.get('/api/stocks');
        console.log("Fetched stocks:", response.data.stocks); // Debugging
        this.stocks = response.data.stocks;
      } catch (error) {
        console.error('Error fetching stock list:', error);
      }
    },

    debounceFilter() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.filterStocks();
      }, 300);
    },

    filterStocks() {
      if (!this.searchQuery.trim()) {
        this.filteredStocks = [];
        return;
      }

      // Filter stocks starting with the searchQuery
      this.filteredStocks = this.stocks.filter(stock =>
        stock.toLowerCase().startsWith(this.searchQuery.toLowerCase())
      );
    },

    selectStock(stock) {
  this.searchQuery = stock;
  this.showDropdown = false;

  console.log("Selected stock:", stock);

  // Fetch stock details
  axios.get(`/api/stock/${stock}`)
    .then(response => {
      console.log("Stock details response:", response.data);

      if (response.data.stock_details) {
        this.selectedStock = response.data.stock_details[0];
        sessionStorage.setItem('selectedStock', JSON.stringify(response.data.stock_details[0]));

        // 🔹 Fetch sentiment for the selected stock
        axios.get(`/api/sentiment/${encodeURIComponent(stock)}`)
          .then(sentimentResponse => {
            console.log("Stock sentiment response:", sentimentResponse.data);
            sessionStorage.setItem('stockSentiment', JSON.stringify(sentimentResponse.data));
          })
          .catch(sentimentError => {
            console.error('Error fetching sentiment data:', sentimentError);
          });

        // Fetch stocks in the same sub-industry
        const encodedStock = encodeURIComponent(stock);
        axios.get(`/api/stocks/subindustry/${encodedStock}`)
          .then(subResponse => {
            if (subResponse.data.stocks_in_subindustry) {
              const stockNames = subResponse.data.stocks_in_subindustry;

              const stockDetailPromises = stockNames.map(stockName => 
                axios.get(`/api/stock/${encodeURIComponent(stockName)}`)
                  .then(detailResponse => detailResponse.data.stock_details[0])
                  .catch(error => {
                    console.error(`Error fetching details for ${stockName}:`, error);
                    return null;
                  })
              );

              Promise.all(stockDetailPromises).then(stockDetails => {
                const filteredStockDetails = stockDetails.filter(stock => stock !== null);
                sessionStorage.setItem('stocksInSubIndustry', JSON.stringify(filteredStockDetails));
                console.log("Stored stock details in sessionStorage:", filteredStockDetails);

                this.$router.push(`/insights?tab=modelling`);
              });
            } else {
              this.$router.push(`/insights?tab=modelling`);
            }
          })
          .catch(subError => {
            console.error('Error fetching stocks in the same sub-industry:', subError);
            this.$router.push(`/insights?tab=modelling`);
          });
      } else {
        this.$router.push(`/insights?tab=modelling`);
      }
    })
    .catch(error => {
      console.error('Error fetching stock details:', error);
      this.$router.push(`/insights?tab=modelling`);
    });
}

    ,

    hideDropdownWithDelay() {
      setTimeout(() => {
        this.showDropdown = false;
      }, 200);
    },

    toPage(path) {
      this.$router.push(path);
    },
    focusSearchBar() {
      const el = document.querySelector('.search-bar');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.focus();
      }

      this.showInfoPopup = true;
      setTimeout(() => {
        this.showInfoPopup = false;
      }, 3000);
    }

  }
};
</script>



<style scoped lang="less">

.search-container {
    margin-top: 20px;
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


.home_box {
  padding: 0 21px;

  //   width: 1180px;
  margin: 0 auto;

  // .text_remark {
  //   margin-top: 50px;
  //   font-size: 26px;
  //   text-align: center;
  //   font-weight: bold;
  //   width: 1180px;
  //   margin: 50px auto;
  // }

  // .calculate_button {
  //   margin-top: 50px;
  //   width: fit-content;
  //   margin: 50px auto;
  //   text-align: center;

  //   .button_class {
  //     display: inline-block;
  //     text-align: center;
  //     padding: 20px;
  //     font-weight: bold;
  //     font-size: 34px;
  //     color: #ffffff;

  //     background: #a9c0e8;
  //     border-radius: 24px 24px 24px 24px;
  //   }

  //   .button_class:hover {
  //     cursor: pointer;
  //     box-shadow: 0px 0px 10px 0px #a9c0e8;
  //   }
  // }

  // .image_box {
  //   justify-content: center;
  //   margin-top: 50px;
  //   width: 1180px;
  //   margin: 50px auto;

  //   text-align: center;

  //   .calculate_button {
  //     margin-top: 10px;
  //     text-align: center;

  //     .button_class2 {
  //       font-size: 26px;

  //       background: linear-gradient(90deg, #133700 0%, #0e0e0e 100%);
  //       color: white;
  //       border-radius: 10px;
  //       display: inline-block;
  //       text-align: center;
  //       padding: 10px;
  //       width: 262px;
  //       font-weight: bold;
  //       font-size: 34px;

  //       background: #a9c0e8;
  //       border-radius: 24px 24px 24px 24px;
  //     }

  //     .button_class2:hover {
  //       cursor: pointer;
  //       box-shadow: 0px 0px 10px 0px #a9c0e8;
  //     }
  //   }
  // }

  
  
  .website_box {
    margin-top: 250px;

    .website_title {
      font-size: 40px;
      text-align: center;
    
      // font-weight: bold;
    }

    .website_content_box {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      width: 1280px;
      margin: 50px auto;
      justify-content: start;

      .website_content_item {
        width: 378px;
        height: 291px;
        margin: 0 20px;
        padding-bottom: 20px;
        border-radius: 20px;
        margin-bottom: 40px;
        background: #f4f4f4;

        position: relative;

        .img_box {
          width: 378px;
          height: 298px;
          position: absolute;
          right: 0;
          bottom: 0;
        }

        .content_box {
          display: flex;
          padding: 20px;

          .title_content {
            flex: 1;
            width: 50%;

            .title {
              font-size: 26px;
              font-weight: bold;
            }

            .content {
              font-size: 20px;
              margin-top: 20px;
              width: 50%;
              white-space: pre-wrap;
            }
          }

          .index_content {
            width: 50px;
            height: 50px;
            background: #6fcd3e;
            border-radius: 50%;
            text-align: center;
            line-height: 50px;
            color: white;
            font-size: 26px;
            font-weight: bold;
            margin-left: 20px;
          }
        }
      }

      .website_content_item:hover {
        background: #a9c0e8;
        color: #fff;
        cursor: pointer;

        .img_box {
          transform: scale(1.2);
          transition: all 0.5s ease-in-out;
        }
      }
    }
  }
}
.video-bg {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
  z-index: 0;
}

.video-bg iframe {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 177.77vh; /* 100 * (16/9) */
  height: 100vh;
  transform: translate(-50%, -50%);
  pointer-events: none;
  border: none;
}

.banner {
  width: 100%;

  height: 600px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  overflow: hidden;
  z-index: 1;

  .text_box {
    position: relative;
    top: 172px;
    color: #ae0f0f;
    //   width: 100%;
    text-align: center;
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 0;
    z-index: 1;

    .text_box_child {
      // backdrop-filter: blur(5px);
      color: #a9c0e8;
      width: fit-content;
      padding: 20px;
      text-align: left;
    }

    .title {
      font-size: 64px;
      // width: 100px;
      text-align: center;
    }

    .content {
      font-size: 32px;
      width: 410px;
      text-align: center;
    }
  }
}

// .ToChatAIButton {
//   width: 447px;
//   height: 65px;
//   border-radius: 34px 34px 34px 34px;
//   border: 2px solid #a9c0e8;
//   display: flex;
//   align-items: center;
//   margin: 50px auto;
//   font-size: 26px;
//   justify-content: center;

//   span {
//     font-family: PingFang SC, PingFang SC;
//     font-weight: 100;
//     font-size: 30px;
//     color: #000000;
//     margin-left: 36px;
//   }
// }

// .ToChatAIButton:hover {
//   cursor: pointer;
//   background: #a9c0e8;

//   span {
//     color: #ffffff;
//   }
// }
// screen
.image-container {
  position: relative;
  width: 100%;
  height: 120px;
  margin: 40px 0;
  overflow: hidden;
}

.background-image {
  position: absolute;
  width: 100px;
  height: 100px;
  object-fit: cover;
  animation: moveHorizontal 5s infinite linear;
  opacity: 0.8;
  top: 10px;
}

/* Adjust each child’s animation delay */
.background-image:nth-child(1) { left: -150px; animation-delay: 0s; }
.background-image:nth-child(2) { left: -150px; animation-delay: 1s; }
.background-image:nth-child(3) { left: -150px; animation-delay: 2s; }
.background-image:nth-child(4) { left: -150px; animation-delay: 3s; }
.background-image:nth-child(5) { left: -150px; animation-delay: 4s; }

/* Horizontal motion animation */
@keyframes moveHorizontal {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(calc(110vw+100px)); /* Move completely off-screen to the right */
  }
}

.feature_section {
  padding: 100px 40px;
  background-color: #f9f9f9;

  &.alt {
    background-color: white;
  }

  .feature_content {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;

    .text_side {
      flex: 1 1 500px;
      padding-right: 40px;

      .tag {
        display: inline-block;
        background: #eeeeee;
        color: #333;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
      }

      h2 {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 20px;
        color: #111827;
      }

      p {
        font-size: 18px;
        color: #4b5563;
        margin-bottom: 30px;
        line-height: 1.6;
      }

      .cta {
        background: black;
        color: white;
        font-size: 16px;
        font-weight: 600;
        padding: 14px 24px;
        border-radius: 30px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .cta:hover {
        background: #1f2937;
      }
    }

    .image_side {
      flex: 1 1 600px;
      text-align: center;

      img {
        max-width: 100%;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
      }
    }
  }
}

// .container {
//   text-align: center;
//   animation: fadeIn 2s ease-in-out;
// }

// h1 {
//   font-size: 72px;
//   color: #58a4db;
//   margin: 0;
//   animation: float 3s ease-in-out infinite;
// }

// p {
//   font-size: 20px;
//   color: #666;
//   margin: 10px 0 20px 0;
//   animation: fadeIn 3s ease-in-out;
// }

// a {
//   color: #58a4db;
//   text-decoration: none;
//   padding: 10px 20px;
//   border: 2px solid #58a4db;
//   border-radius: 25px;
//   font-size: 18px;
//   transition: background-color 0.3s ease, color 0.3s ease;
//   animation: slideIn 1.5s ease-in-out;
// }

// a:hover {
//   background-color: #58a4db;
//   color: white;
// }

// @keyframes fadeIn {
//   from {
//     opacity: 0;
//   }
//   to {
//     opacity: 1;
//   }
// }

// @keyframes float {
//   0%,
//   100% {
//     transform: translateY(0);
//   }
//   50% {
//     transform: translateY(-10px);
//   }
// }

// @keyframes slideIn {
//   from {
//     transform: translateY(20px);
//     opacity: 0;
//   }
//   to {
//     transform: translateY(0);
//     opacity: 1;
//   }
// }

@media (max-width: 768px) {
  .text_box {
    flex-direction: column;
    align-items: center;
    padding: 0 1rem;
    top: 100px;

    .text_box_child {
      width: 100%;
      text-align: center;

      .title {
        font-size: 2rem;
        line-height: 1.3;
        margin-bottom: 1rem;
      }

      .search-container {
        margin: 1rem auto 0;
        width: 90%;

        .search-bar {
          width: 100%;
          font-size: 1rem;
        }
      }
    }
  }
}



@media (max-width: 768px) {
  .image-container {
    position: relative;
    width: 100%;
    height: 80px;
    margin: 20px 0;
    overflow: hidden;
  }

  .background-image {
    width: 50px;
    height: 50px;
    object-fit: contain;
    position: absolute;
    opacity: 0.9;
    animation: moveHorizontal 5s infinite linear;
    top: 15px;
  }

  .background-image:nth-child(1) { left: -150px; animation-delay: 0s; }
  .background-image:nth-child(2) { left: -150px; animation-delay: 1s; }
  .background-image:nth-child(3) { left: -150px; animation-delay: 2s; }
  .background-image:nth-child(4) { left: -150px; animation-delay: 3s; }
  .background-image:nth-child(5) { left: -150px; animation-delay: 4s; }
}

.video-content {
  width: 100%;
  height: 100%;
  object-fit: cover;
}




.video-content {
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
  position: absolute;
}


.floating-elements {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  pointer-events: none; // makes sure container doesn’t interfere
}

.floating-cta {
  pointer-events: auto;
  background-color: #a9c0e8;
  color: white;
  font-size: 16px;
  padding: 14px 24px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  transition: background 0.3s ease;
}

.floating-cta:hover {
  background-color: #88aee0;
}

.info-popup {
  margin-top: 10px;
  background: #111827;
  color: white;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
  white-space: nowrap;
  animation: fadeInOut 3s ease-in-out;
  pointer-events: auto;
}

@keyframes fadeInOut {
  0%   { opacity: 0; transform: translateY(10px); }
  10%  { opacity: 1; transform: translateY(0); }
  90%  { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(10px); }
}




</style>
