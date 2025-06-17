<template>
  <div>
    <div class="title_box">Associated Health Risks</div>

    <div class="main_content_box1">
      <div
        v-for="(item, index) in mainContentData1"
        :key="index"
        class="main_content_item1"
        :class="item.isactive ? 'active' : ''"
        @click="clickItem(item)"
      >
        <div>
          <img :src="item.img" />
        </div>
        <div class="title_box">{{ item.title }}</div>
      </div>
    </div>
    <br />
    <el-dialog
      :title="indicator.title"
      :visible.sync="dialogVisible"
      width="30%"
      center
    >
      <span style="font-size:18px">{{ indicator.remark }}</span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mainContentData1: [
        {
          title: "Severe astrointestinal Issues",
          remark: `Significant symptoms like persistent diarrhea, vomiting, or stomach cramps from high bacterial counts`,
          img: require("@/assets/images/planning/Severe astrointestinal Issues@2x.png")
        },
        {
          title: "Intense Skin Reactions",
          remark: `Severe rashes, eczema flare-ups, or bacterial infections from increased pollutants.`,
          img: require("@/assets/images/planning/Intense Skin Reactions@2x.png")
        },
        {
          title: "Acute Ear Infections",
          remark: `Risk of conjunctivitis or other serious eye conditions from high levels of contaminants`,
          img: require("@/assets/images/planning/Acute Ear Infections@2x.png")
        },
        {
          remark: `Elevated risk of swimmer’s ear requiring medical treatment`,
          title: "Serious Eye Infections",
          img: require("@/assets/images/planning/Serious Eye Infections@2x.png")
        }
      ],
      dialogVisible: false,
      indicator: {}
    };
  },
  methods: {
    clickItem(item) {
      for (let index = 0; index < this.mainContentData1.length; index++) {
        const element = this.mainContentData1[index];
        element.isactive = false;
      }
      item.isactive = !item.isactive;
      this.indicator = item;
      this.dialogVisible = true;
      this.$forceUpdate();
    }
  }
};
</script>

<style lang="less" scoped>
.title_box {
  font-weight: bold;
  font-size: 36px;
}
.sub_title_box {
  font-weight: 400;
  font-size: 20px;
  color: #000000;
}
.main_content_box {
  margin-top: 20px;
  .main_content_item {
    display: flex;
    align-items: center;
    margin-bottom: 40px;
    img {
      width: 48px;
      height: 48px;
    }
    .content_box {
      margin-left: 16px;
      .content_1 {
        font-weight: bold;
        font-size: 20px;
        color: #000000;
        margin-bottom: 5px;
      }
      .content_2 {
        font-size: 16px;
        color: #000000;
        margin-bottom: 10px;
      }
    }
  }
}
.main_content_box1 {
  display: flex;
  justify-content: space-between;
  .main_content_item1 {
    width: 276px;
    height: 200px;
    text-align: center;
    background: #ffffff;
    border-radius: 12px 12px 12px 12px;
    border: 1px solid rgba(0, 0, 0, 0.05);
    padding: 35px 10px;
    margin-right: 30px;
    img {
      width: 78px;
      height: 78px;
    }
    .title_box {
      font-weight: bold;
      font-size: 20px;

      margin-top: 12px;
    }
    .content_box {
      margin-top: 12px;

      font-weight: 400;
      font-size: 20px;
    }
  }
  .main_content_item1:hover {
    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.05);
    cursor: pointer;
  }
  .active {
    background: #a9c0e8;
    color: #ffffff !important;
  }
}
</style>
