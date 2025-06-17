<template>
  <div>
    <div class="table_title">
      <div class="table_title_tag"></div>
      <span> Data Trend</span>
    </div>
    <div class="content">
      <div class="right_box">
        <div id="plot_holder" v-if="plot_loading_flag" style="height: 400px">
          <spin size="large" fix v-if="plot_loading_flag" style="font-size: 20px">Loading...</spin>
        </div>
        <div v-else id="plot" style="height: 400px"></div>
      </div>

      <div class="left_box">
        <div class="left_box_item">
          <div class="item_title">Suburb</div>

          <Select v-model="station" placeholder="0">
            <Option v-for="item in stationList" :value="item.num" :key="item.num">{{ item.text }}</Option>
          </Select>
          <div style="font-size :14px">
            {{ getContent(station) }}
          </div>
        </div>

        <div class="left_box_item">
          <div class="item_title">Time</div>
          <Select v-model="period" placeholder="One Year">
            <Option value="1">Last Year</Option>
            <Option value="3">Last 3 Years</Option>
            <Option value="5">Last 5 Years</Option>
          </Select>
        </div>
        <div class="left_box_item">
          <Button style="
              background-color: #a9c0e8;
              border-color: #a9c0e8;
              width: 275px;
              height: 40px;
              font-size: 24px;
            " type="success" shape="circle" icon="ios-stats" long @click="getQueriedDataForPlot">Show Trend</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WaterTrend",
  data() {
    return {
      // stationList: [0, 1, 3, 4, 5, 6, 7, 8, 10],
      stationList: [
        {
          num: 0,
          text: "Docklands"
        },
        {
          num: 1,
          text: "Southbank"
        },
        {
          num: 3,
          text: "Carlton"
        },
        {
          num: 4,
          text: "Albert Park"
        },
        {
          num: 5,
          text: "Werribee"
        },
        {
          num: 6,
          text: "Box Hill"
        },
        {
          num: 7,
          text: "Burwood"
        },
        {
          num: 8,
          text: "Preston"
        },
        {
          num: 10,
          text: "Bendigo"
        }
      ],
      station: 0,
      period: "1",
      // indicator: "ph",
      plot_loading_flag: true,
      waterQualities: [],
      dates: []
    };
  },
  props: {
    indicator: {
      type: String,
      default: "ph"
    }
  },
  watch: {
    indicator: function (newValue, oldValue) {
      this.getQueriedDataForPlot();
    }
  },
  mounted() {
    // this.getAllStations();
    this.getQueriedDataForPlot();
  },
  methods: {
    getContent(station) {
      //       0     Docklands (Melbourne) – Near the Yarra River and various stormwater systems.
      // 1     Southbank (Melbourne) – Close to the Yarra River.
      // 3     Carlton (Melbourne) – Close to the Yarra River and associated catchments.
      // 4     Albert Park (Melbourne) – Includes Albert Park Lake.
      // 5     Werribee (Western Suburbs) – Close to the Werribee River.
      // 6     Box Hill (Eastern Suburbs) – Near Gardiners Creek.
      // 7     Burwood (Eastern Suburbs) – Close to local creeks.
      // 8     Preston (Northern Suburbs) – Close to Darebin Creek.
      // 10    Bendigo (Regional Victoria) – Near local creeks and rivers.
      if (station == 0) {
        return "Docklands (Melbourne) – Near the Yarra River and various stormwater systems.";
      } else if (station == 1) {
        return "Southbank (Melbourne) – Close to the Yarra River.";
      } else if (station == 3) {
        return "Carlton (Melbourne) – Close to the Yarra River and associated catchments.";
      } else if (station == 4) {
        return "Albert Park (Melbourne) – Includes Albert Park Lake";
      } else if (station == 5) {
        return "Werribee (Western Suburbs) – Close to the Werribee River.";
      } else if (station == 6) {
        return "Box Hill (Eastern Suburbs) – Near Gardiners Creek.";
      } else if (station == 7) {
        return "Burwood (Eastern Suburbs) – Close to local creeks.";
      } else if (station == 8) {
        return "Preston (Northern Suburbs) – Close to Dare";
      } else if (station == 10) {
        return " Bendigo (Regional Victoria) – Near local creeks and rivers.";
      }
    },
    getAllStations() {
      let _this = this;
      this.axios.get("waterquality/station").then(function (response) {
        _this.stationList = response.data;
      });
    },
    getQueriedDataForPlot() {
      let _this = this;

      this.axios
        .get("waterquality/plot", {
          params: {
            station: _this.station,
            period: _this.period,
            indicator: _this.indicator
          }
        })
        .then(function (response) {
          let data = response.data;
          _this.waterQualities = data.waterquality;
          _this.dates = data.dates;
          _this.plot_loading_flag = false;
          _this.$nextTick(function () {
            _this.plot();
          });
        });
    },
    plot() {
      let _this = this;

      let chart = this.echarts.init(document.getElementById("plot"));

      let markline =
        this.indicator == "ph"
          ? { yAxis: 7.5, name: "ph= 7.5\nSafety value" }
          : this.indicator == "do"
            ? { yAxis: 6, name: "do = 6\nSafety value" }
            : { yAxis: 0.5, name: "nh3n = 0.5\nSafety value" };

      let option = {
        tooltip: {
          trigger: "axis",
          backgroundColor: "#fff",

          axisPointer: {
            lineStyle: {
              color: {
                type: "linear",
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: "red"
                  },
                  {
                    offset: 0.5,
                    color: "red"
                  },
                  {
                    offset: 1,
                    color: "red"
                  }
                ],
                global: false
              }
            }
          }
        },
        xAxis: {
          type: "category",
          data: _this.dates
        },
        yAxis: {
          type: "value",
          scale: true
        },
        series: [
          {
            data: _this.waterQualities,
            lineStyle: {
              normal: {
                color: "#77C8C8"
              }
            },
            label: {
              show: false,
              position: "top",
              textStyle: {
                color: "#77C8C8"
              }
            },

            itemStyle: {
              color: "#77C8C8",
              borderColor: "#77C8C8",
              borderWidth: 2
            },
            type: "line",
            areaStyle: {
              normal: {
                color: this.echarts.graphic.LinearGradient(
                  0,
                  0,
                  0,
                  1,
                  [
                    {
                      offset: 0,
                      color: " rgba(217,246,246,1)"
                    },
                    {
                      offset: 1,
                      color: "rgba(183,231,231,0)"
                    }
                  ],
                  false
                ),
                shadowColor: "rgba(183,231,231,0.54)",
                shadowBlur: 20
              }
            },
            markLine: {
              silent: true,
              data: [markline],
              lineStyle: {
                type: "dashed",
                color: "#FF0000" // The color can be changed as needed
              },
              label: {
                formatter: "{b}" // Labels that display horizontal lines
              }
            }
          }
        ]
      };
      chart.setOption(option);
    }
  }
};
</script>

<style scoped>
.query {
  margin-top: 20px;
}

.table_title {
  margin-bottom: 10px;
  font-size: 16px;
  display: flex;
  align-items: center;
  padding-left: 5%;
}

.table_title span {
  margin-left: 16px;
  font-weight: 100;
  font-size: 24px;
  color: #000000;
}

.table_title_tag {
  width: 6px;
  height: 27px;
  background: #a9c0e8;
  border-radius: 33px 33px 33px 33px;
}

#plot_holder {
  position: relative;
  margin-top: 20px;
  margin-left: 30px;
  margin-right: 30px;
}

.content {
  display: flex;
  align-items: center;
}

.right_box {
  flex: 1;
}

.left_box {
  width: 300px;
  background: #f4f4f4;
  height: 300px;
  border-radius: 30px;
  padding: 20px;
}

.left_box_item {
  display: flex;

  flex-direction: column;
  margin-bottom: 10px;
}

.left_box_item .item_title {
  font-weight: bold;
  font-size: 20px;
  color: #000000;
  text-align: left;
  font-style: normal;
  text-transform: none;
  margin-bottom: 10px;
}
</style>
