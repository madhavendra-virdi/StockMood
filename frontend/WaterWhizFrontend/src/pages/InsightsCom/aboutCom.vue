
<script>
export default {
  name: "StockPlot",
  data() {
    return {
      selectedStock: "",
      iframeSrcPlot4: "",
      iframeSrcPlot5: "",
      // Sentiment Meter data:
      sentimentScore: 0,
      needleLength: 90,
      needleWidth: 15,
      tooltipVisible: false,
      tooltipPos: { x: 0, y: 0 },
      sentiment: { stock_details: [] },
      twitterCount: 0,
      redditCount: 0,
      negativeCount: 0,
      positiveCount: 0,
      neutralCount:0
    };
  },
  computed: {
    needleAngle() {
      return Math.PI - (this.sentimentScore + 1) * (Math.PI / 2);
    },
    needleTipCoords() {
      const cx = 150;
      const cy = 150;
      const x = cx + this.needleLength * Math.cos(this.needleAngle);
      const y = cy - this.needleLength * Math.sin(this.needleAngle);
      return { x, y };
    },
    needlePoints() {
      const cx = 150;
      const cy = 100;
      const angle = this.needleAngle;
      const length = this.needleLength;
      const width = this.needleWidth;

      const tipX = cx + length * Math.cos(angle);
      const tipY = cy - length * Math.sin(angle);
      const baseLeftX = cx + (width / 2) * Math.cos(angle + Math.PI / 2);
      const baseLeftY = cy - (width / 2) * Math.sin(angle + Math.PI / 2);
      const baseRightX = cx + (width / 2) * Math.cos(angle - Math.PI / 2);
      const baseRightY = cy - (width / 2) * Math.sin(angle - Math.PI / 2);

      return `${tipX},${tipY} ${baseLeftX},${baseLeftY} ${baseRightX},${baseRightY}`;
    },
    interpolatedColor() {
      const s = (this.sentimentScore + 1) / 2;
      const r = Math.round(255 * (1 - s));
      const g = Math.round(204 * s + 255 * (1 - s));
      return `rgb(${r},${g},0)`;
    }
  },
  mounted() {
    const storedStock = sessionStorage.getItem("selectedStock");
    const sentimentStock = sessionStorage.getItem("stockSentiment");
    if (sentimentStock) {
  this.sentiment = JSON.parse(sentimentStock);

  const twitterCount = this.sentiment.stock_details.filter(
    item => item.platform === 'twitter'
  ).length;

  const redditCount = this.sentiment.stock_details.filter(
    item => item.platform === 'reddit'
  ).length;

  this.twitterCount = twitterCount;
  this.redditCount = redditCount;

  const negativeCount = this.sentiment.stock_details.filter(
    item => item.label === 'negative'
  ).length;

  const positiveCount = this.sentiment.stock_details.filter(
    item => item.label === 'positive'
  ).length;

  const neutralCount = this.sentiment.stock_details.filter(
    item => item.label === 'neutral'
  ).length;

  this.negativeCount = negativeCount;
  this.positiveCount = positiveCount;
  this.neutralCount = negativeCount;

  if (sentimentStock) {
  this.sentiment = JSON.parse(sentimentStock);

  const details = this.sentiment.stock_details;

  if (details.length > 0) {
    const totalScore = details.reduce((acc, item) => {
      let weight = 0;
      if (item.label === 'positive') weight = 1;
      else if (item.label === 'negative') weight = -1;
      // neutral is 0, so no need to assign

      return acc + (item.score * weight);
    }, 0);

    const sentimentScore = totalScore / details.length;
    this.sentimentScore = sentimentScore;

    console.log('Overall sentiment score:', sentimentScore.toFixed(4));  // Rounded to 4 decimals
  } else {
    console.log('No sentiment data available.');
  }
}

  

  console.log('Twitter count:', twitterCount);
  console.log('Reddit count:', redditCount);
}
   

  
  

    if (storedStock) {
      try {
        const parsed = JSON.parse(storedStock);
        this.selectedStock = parsed.Name;

        this.iframeSrcPlot4 =
          "/rapi/plot4?stock_name=" + encodeURIComponent(this.selectedStock);
        this.iframeSrcPlot5 =
          "/rapi/plot5?stock_name=" + encodeURIComponent(this.selectedStock);
      } catch (e) {
        console.error("Invalid stock format in sessionStorage");
      }
    }
  },
  methods: {
    showTooltip() {
      const svgRect = this.$refs.svg.getBoundingClientRect();
      const { x, y } = this.needleTipCoords;

      const absoluteX = svgRect.left + x;
      const absoluteY = svgRect.top + y;

      this.tooltipPos = {
        x: absoluteX - 50, // center tooltip
        y: absoluteY - 40  // place above needle
      };
      this.tooltipVisible = true;
    },
    hideTooltip() {
      this.tooltipVisible = false;
    }
  }
};
</script>


<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
  align-items: center;
  font-family: Arial, sans-serif;
}

.mentions-summary {
  text-align: center;
}

.mentions-title {
  color: #a9c0e8;
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 10px;
}

.mention-columns {
  display: flex;
  justify-content: center;
  gap: 50px;
}

.mention-source {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.source-name {
  font-weight: 500;
  font-size: 16px;
  margin-bottom: 6px;
}

.mention-count {
  font-size: 18px;
  font-weight: bold;
  color: #2a2a2a;
}

.mention-source.positive .mention-count {
  color: green;
}

.mention-source.neutral .mention-count {
  color: #3f78c4;
}

.mention-source.negative .mention-count {
  color: red;
}

.top-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  gap: 20px;
}

.plot {
  flex: 1;
}

.sankey-width {
  flex: 7;
}

.wordcloud-width {
  flex: 3;
}

.oval-shaped-iframe {
  border-radius: 10px;
}

.sentiment-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 40px;
  gap: 16px;
}

.sentiment-meter {
  width: 100%;
  max-width: 600px;
  background-color: #f9fbfd;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  padding: 20px 10px 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.sentiment-meter svg {
  width: 100%;
  max-width: 400px;
  height: auto;
  transform: none;
}




.tooltip {
  position: fixed;
  padding: 8px 12px;
  color: white;
  font-size: 14px;
  border-radius: 6px;
  pointer-events: none;
  font-weight: 500;
  white-space: nowrap;
  z-index: 100;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
  .top-row {
    flex-direction: column;
  }

  .sankey-width,
  .wordcloud-width {
    width: 100%;
  }
  .plot iframe{
    height: 500px !important;
  }
}

</style>

<template>
  <div class="main-container">
    <!-- Mentions Summary Section -->
    <div class="mentions-summary">
      <h3 class="mentions-title">{{ sentiment.stock_details.length }} online mentions in last week</h3>
      <div class="mention-columns">
        <div class="mention-source">
          <div class="source-name">BSE</div>
          <div class="mention-count">0</div>
        </div>
        <div class="mention-source">
          <div class="source-name">Twitter</div>
          <div class="mention-count">{{ twitterCount }}</div>
        </div>
        <div class="mention-source">
          <div class="source-name">Reddit</div>
          <div class="mention-count">{{ redditCount }}</div>
        </div>
      </div>
    </div>

    <!-- Top Row -->
    <div class="top-row">
      <div v-if="iframeSrcPlot4" class="plot sankey-width">
        <iframe 
          :src="iframeSrcPlot4" 
          width="100%" 
          height="500" 
          frameborder="0" 
          style="border:none; background: transparent;"
        ></iframe>
      </div>
      <div v-else class="plot sankey-width">
        <p>No stock selected.</p>
      </div>

      <div class="plot wordcloud-width">
        <iframe 
          :src="iframeSrcPlot5" 
          width="100%" 
          height="500"  
          frameborder="0" 
          style="border:none; background: transparent;"
          class="oval-shaped-iframe"
        ></iframe>
      </div>
    </div>

    <!-- Sentiment Meter -->
    <!-- Sentiment Summary -->
    <div class="sentiment-block">
      <h3 class="mentions-title">Mention sentiments</h3>
      <div class="mention-columns">
        <div class="mention-source negative">
          <div class="source-name">Negative</div>
          <div class="mention-count">{{ negativeCount }}</div>
        </div>
        <div class="mention-source neutral">
          <div class="source-name">Neutral</div>
          <div class="mention-count">{{ neutralCount }}</div>
        </div>
        <div class="mention-source positive">
          <div class="source-name">Positive</div>
          <div class="mention-count">{{ positiveCount }}</div>
        </div>
      </div>

      <div class="sentiment-meter">
        <svg ref="svg" viewBox="0 0 300 200" preserveAspectRatio="xMidYMid meet">
          <defs>
            <linearGradient id="sentimentGradient" x1="60" y1="150" x2="240" y2="150" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#ff0000" />
              <stop offset="50%" stop-color="#ffff00" />
              <stop offset="100%" stop-color="#00cc00" />
            </linearGradient>
          </defs>

          <path
            d="M60 100 A90 90 0 0 1 240 100"
            stroke="url(#sentimentGradient)"
            stroke-width="16"
            fill="none"
          />

          <polygon
            :points="needlePoints"
            fill="black"
            ref="needle"
            @mouseenter="showTooltip"
            @mouseleave="hideTooltip"
          />

          <circle cx="150" cy="100" r="6" fill="black" />
        </svg>

        <div
          v-if="tooltipVisible"
          class="tooltip"
          :style="{
            top: tooltipPos.y + 'px',
            left: tooltipPos.x + 'px',
            backgroundColor: interpolatedColor
          }"
        >
          Sentiment Score: {{ sentimentScore.toFixed(2) }}
        </div>
      </div>
    </div>

  </div>
</template>

