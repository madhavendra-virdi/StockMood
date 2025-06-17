<template>
  <div style="padding-left: 3%" class="content">
    <!-- <div class="main_box">
      <div class="data_table">
        <div class="table_title">
          <div class="table_title_tag"></div>
          <span> Make Prediction</span>
        </div>
        <Table
          class="table"
          height="400"
          :loading="model_table_flag"
          border
          :columns="columns"
          :data="availableModels"
        >
          <template slot-scope="{ row, index }" slot="Type">
            {{ row.method }}
            <el-tooltip
              class="item"
              effect="dark"
              :content="getContent(row.method)"
              placement="top-start"
            >
              <i style="color:#A9C0E8" class="el-icon-info"></i>
            </el-tooltip>
          </template>
          <template slot-scope="{ row, index }" slot="action">
            <Button
              style="background: #a9c0e8; border-color: #a9c0e8"
              type="success"
              size="default"
              @click="getNextMonthPrediction(index)"
              >Predict</Button
            >
          </template>
        </Table>
      </div>

      <div class="left_box">
        <div class="left_box_item">
          <div class="item_title">Machine Learning Model</div>
          <Select v-model="method">
            <Option value="all">All</Option>
            <Option v-for="item in modelList" :value="item" :key="item">{{
              item
            }}</Option>
          </Select>
        </div>
        <div class="left_box_item">
          <Button
            style="
              background-color: #a9c0e8;
              border-color: #a9c0e8;
              width: 275px;
              height: 40px;
              font-size: 24px;
            "
            type="success"
            shape="circle"
            icon="ios-stats"
            long
            @click="getAvailableMethods"
            >Search</Button
          >
        </div>
      </div>
    </div> -->

    <div id="plot_holder" v-if="plot_loading_flag" style="height: 400px">
      <spin size="large" fix v-if="plot_loading_flag" style="font-size: 20px"
        >Using {{ chosenModel.method }} to
        {{ indicator.toUpperCase() }} predict...</spin
      >
    </div>
    <div v-else id="plot_prediction" style="height: 400px"></div>
  </div>
</template>

<script>
export default {
  name: "WaterPrediction",
  data() {
    return {
      method: "all",
      modelList: [],
      availableModels: [],
      prediction: "",
      chosenModel: {},
      model_table_flag: false,
      plot_loading_flag: false,
      plotWaterQualities: [],
      plotDates: [],
      plotWaterQualitiesSecond: [],
      columns: [
        {
          title: "Type",
          key: "method",
          slot: "Type",
          align: "center"
        },
        {
          title: "RMSE",
          key: "rmse",
          align: "center",
          sortable: "true"
        },

        {
          title: "Training Date",
          key: "date",
          align: "center",
          sortable: "true"
        },
        {
          title: "Operation",
          slot: "action",
          align: "center"
        }
      ]
    };
  },
  watch: {
    indicator: function(newValue, oldValue) {
      // this.getAllMethods();
      this.getNextMonthPrediction();
    }
  },
  props: {
    indicator: {
      type: String,
      default: "ph"
    }
  },
  mounted() {
    // this.getAllMethods();
    this.getNextMonthPrediction();
  },

  methods: {
    getContent(method) {
      if (method === "SVM") {
        return "Fast Predictions (Quick insights, speed-first)";
      } else if (method === "ADABOOST") {
        return "Precision Focused (Highest accuracy, takes more time)";
      } else if (method === "RVM") {
        return "Consistent Results (Best for varied data quality)";
      } else if (method === "LSTM") {
        return "Forecast long-term trends (Greater than 5 years)";
      } else if (method === "BP") {
        return "Balanced and Dependable (Good balance of speed and accuracy)";
      } else if (method === "OPTIMIZATION") {
        return "Optimized for Performance (Best overall results, fine-tuned)";
      }
    },

    fomartDate(date) {
      var date = new Date(date);
      var year = date.getFullYear();
      var month = date.getMonth() + 1;
      var day = date.getDate();

      return year + "-" + month + "-" + day;
    },
    getAvailableMethods() {
      let _this = this;
      this.model_table_flag = true;

      this.axios
        .get("/model/available", {
          params: {
            indicator: _this.indicator,
            method: _this.method
          }
        })
        .then(function(response) {
          _this.availableModels = response.data;
          for (var i = 0; i < _this.availableModels.length; i++) {
            _this.availableModels[i].user =
              _this.availableModels[i].user.username;
            _this.availableModels[i].date = new Date(
              _this.availableModels[i].date
            );
            _this.availableModels[i].date = _this.fomartDate(
              _this.availableModels[i].date
            );
          }
          _this.getNextMonthPrediction(0);
          _this.model_table_flag = false;
        });
    },
    getAllMethods() {
      let _this = this;
      this.model_table_flag = true;
      this.axios
        .get("model/list", {
          params: {
            indicator: _this.indicator
          }
        })
        .then(function(response) {
          _this.modelList = response.data;
          _this.method = "all";
          _this.getAvailableMethods();
        });
    },

    deleteModel(index) {
      let _this = this;
      this.chosenModel = this.availableModels[index];
      this.axios
        .post("model/delete/" + this.chosenModel.id.toString())
        .then(function(response) {
          if (response.data.status === "success") {
            _this.$Message.success("Delete succeed!");
            _this.getAvailableMethods();
          } else if (response.data.status === "deny") {
            _this.$Message.error(
              "Permission denied, please contact the administrator!"
            );
          } else {
            _this.$Message.error("Delete failed!");
          }
        });
    },

    getNextMonthPrediction(index) {
      let _this = this;
      this.plot_loading_flag = true;

      // this.chosenModel = this.availableModels[index];
      let id =
        this.indicator == "ph" ? 193 : this.indicator == "do" ? 193 : 207;
      this.axios
        .get("model/prediction", {
          params: {
            id: id,
            indicator: _this.indicator
          }
        })
        .then(function(response) {
          let body = response.data;
          _this.plot_loading_flag = false;
          _this.$nextTick(function() {
            let charts = document.getElementById("plot_prediction");
            if (body.status === "success") {
              _this.prediction = body.pred;
              _this.plotWaterQualities = body.forPlot;
              _this.plotWaterQualitiesSecond = [
                "-",
                "-",
                "-",
                "-",
                _this.plotWaterQualities[4],
                _this.prediction
              ];
              _this.plotWaterQualities[5] = "-";
              _this.plotDates = body.dates;
              charts.style.height = "400px";
              _this.plot();
            } else {
              charts.style.visibility = "visible";
              charts.style.height = "400px";

              _this.$Message.error("Predict failed！");
            }
          });
        });
    },
    plot() {
      let _this = this;
      let chart = this.echarts.init(document.getElementById("plot_prediction"));
      let option = {
        title: {
          left: "center",
          text:
            _this.indicator.toUpperCase() +
            "Predication for Next Month: " +
            _this.prediction
          // subtext:
          //   "Predicted by " +
          //   _this.chosenModel.method +
          //   " model " +
          //   "which is trained by " +
          //   _this.chosenModel.user +
          //   " on " +
          //   _this.chosenModel.date
        },
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
        grid: {
          left: "3%",
          right: "0",
          bottom: "3%",
          containLabel: true
        },
        xAxis: {
          type: "category",
          data: _this.plotDates
        },
        yAxis: {
          type: "value",
          scale: true
        },
        series: [
          {
            data: _this.plotWaterQualities,
            lineStyle: {
              normal: {
                color: "#C66C71"
              }
            },
            label: {
              show: false,
              position: "top",
              textStyle: {
                color: "#C66C71"
              }
            },

            itemStyle: {
              color: "#C66C71",
              borderColor: "#C66C71",
              borderWidth: 2
            },
            type: "line",
            areaStyle: {
              normal: {
                color: new this.echarts.graphic.LinearGradient(
                  0,
                  0,
                  0,
                  1,
                  [
                    {
                      offset: 0,
                      color: " rgba(244,229,230,1)"
                    },
                    {
                      offset: 1,
                      color: "rgba(242,191,161,0)"
                    }
                  ],
                  false
                ),
                shadowColor: "rgba(244,229,230,0.54)",
                shadowBlur: 20
              }
            }
          },
          {
            data: _this.plotWaterQualitiesSecond,
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
                color: new this.echarts.graphic.LinearGradient(
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
            }
          }
        ]
      };
      chart.setOption(option);
      var charts = document.getElementById("plot_prediction");
      charts.style.visibility = "visible";
      _this.plot_loading_flag = false;
    }
  }
};
</script>

<style scoped>
.query {
  margin-top: 20px;
}

.queryline {
  line-height: 32px;
}

.data_table {
  margin-top: 20px;
  margin-bottom: 15px;
  padding-left: 30px;
  padding-right: 30px;
}

.table_title {
  margin-bottom: 10px;
  font-size: 16px;
  display: flex;
  align-items: center;
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
.plot_title {
  margin-bottom: 15px;
  font-size: 18px;
}

#plot_holder {
  position: relative;
  margin-left: 30px;
  margin-right: 30px;
}

/*#plot {*/
/*position: relative;*/
/*}*/

.main_box {
  display: flex;
  align-items: center;
}
.data_table {
  flex: 1;
  width: 65%;
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
  margin-bottom: 50px;
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
