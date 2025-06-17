<template>
  <div>
    <div class="table_title">
      <div class="table_title_tag"></div>
      <span>Train Models</span>
    </div>
    <div class="content">
      <div class="right_box">
        <div
          id="plot_holder_train"
          v-if="plot_loading_flag"
          style="height: 400px"
        >
          <spin
            size="large"
            fix
            v-if="plot_loading_flag"
            style="font-size: 20px"
            >Training {{ method }} model...</spin
          >
        </div>
        <div v-else id="plot_train" style="height: 400px"></div>
      </div>
      <div class="left_box">
        <div class="left_box_item">
          <div class="item_title">Machine Learning Model</div>
          <Select v-model="method">
            <Option value="LSTM">LSTM</Option>
            <Option value="SVM">SVM</Option>
            <Option value="RVM">RVM</Option>
            <Option value="Adaboost">Adaboost</Option>
            <Option value="BP">BP</Option>
            <Option value="Optimization">Optimization</Option>
          </Select>
        </div>
        <div class="left_box_item">
          <Button
            style="
              background-color: #a9c0e8;
              border-color: #a9c0e8;
              width: 275px;
              height: 56px;
              font-size: 24px;
            "
            type="success"
            shape="circle"
            icon="ios-stats"
            long
            @click="trainModel"
            >Train Model</Button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ModelTraining",
  data() {
    return {
      method: "LSTM",
      rmse: "",
      pred: [],
      real: [],
      plot_loading_flag: false,
      currentUser: {
        id: 1,
      },
    };
  },
  props: {
    indicator: {
      type: String,
      default: "ph",
    },
  },
  watch: {
    indicator: function (newValue, oldValue) {
      this.trainModel();
    },
  },
  created() {
    // this.getCurrentUser();
  },
  methods: {
    trainModel() {
      let _this = this;

      _this.plot_loading_flag = true;
      this.axios
        .get("model/training", {
          params: {
            indicator: _this.indicator,
            method: _this.method,
            uid: _this.currentUser.id,
          },
        })
        .then(function (response) {
          let body = response.data;
          _this.plot_loading_flag = false;
          _this.$nextTick(function () {
            let charts = document.getElementById("plot_train");

            if (body.status === "success") {
              _this.rmse = body.data.rmse;
              _this.pred = body.data.pred;
              _this.real = body.data.real;

              _this.plot();
            } else if (body.status === "deny") {
              _this.plot_loading_flag = false;
              _this.$Message.error(
                "\n" + "Permission denied, please contact the administrator"
              );

              charts.style.visibility = "visible";
            } else {
              _this.plot_loading_flag = false;
              _this.$Message.error("Training failed！");

              charts.style.visibility = "visible";
            }
          });
        });
    },

    getCurrentUser() {
      let _this = this;
      this.axios.get("/user/current").then(function (response) {
        _this.currentUser = response.data;
      });
    },

    plot() {
      let _this = this;
      let chart = this.echarts.init(document.getElementById("plot_train"));
      let x = new Array(_this.pred.length);
      for (var i = 0; i < _this.pred.length; i++) {
        x[i] = i + 1;
      }
      let option = {
        title: {
          left: "center",
          text:
            "Training Result of" +
            " " +
            _this.method +
            " Model on " +
            _this.indicator.toUpperCase(),
          subtext: "The RMSE on test set is " + _this.rmse,
        },
        legend: {
          data: ["Predication", "Actual value"],
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
                    color: "red",
                  },
                  {
                    offset: 0.5,
                    color: "red",
                  },
                  {
                    offset: 1,
                    color: "red",
                  },
                ],
                global: false,
              },
            },
          },
        },
        xAxis: {
          type: "category",
          data: x,
        },
        yAxis: {
          type: "value",
          scale: true,
        },
        series: [
          {
            data: _this.pred,
            lineStyle: {
              normal: {
                color: "#6682D6",
              },
            },
            label: {
              show: false,
              position: "top",
              textStyle: {
                color: "#6682D6",
              },
            },

            itemStyle: {
              color: "#6682D6",
              borderColor: "#6682D6",
              borderWidth: 2,
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
                      color: "rgba(197,224,253,1)",
                    },
                    {
                      offset: 1,
                      color: "rgba(179,216,255,0)",
                    },
                  ],
                  false
                ),
              },
            },
          },
          {
            data: _this.real,
            lineStyle: {
              normal: {
                color: "#EE742F",
              },
            },
            label: {
              show: false,
              position: "top",
              textStyle: {
                color: "#EE742F",
              },
            },

            itemStyle: {
              color: "#EE742F",
              borderColor: "#EE742F",
              borderWidth: 2,
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
                      color: "rgba(242,191,161,1)",
                    },
                    {
                      offset: 1,
                      color: "rgba(242,191,161,0)",
                    },
                  ],
                  false
                ),
                shadowColor: "rgba(242,191,161,0.54)",
                shadowBlur: 20,
              },
            },
          },
        ],
      };
      chart.setOption(option);
      var charts = document.getElementById("plot_train");
      charts.style.visibility = "visible";
      _this.plot_loading_flag = false;
    },
  },
};
</script>

<style scoped>
.content {
  display: flex;
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
.query {
  margin-top: 20px;
  margin-bottom: 20px;
}

.queryline {
  line-height: 32px;
}

#plot_holder_train {
  position: relative;
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
