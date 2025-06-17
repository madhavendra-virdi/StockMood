<template>
  <div>
    <div class="title_box">Stay Safe While Enjoying Fair Water Quality</div>

    <div class="main_content_box1">
      <div
        v-for="(item, index) in mainContentData1"
        :key="index"
        class="main_content_item1"
      >
        <div>
          <img :src="item.img" />
        </div>
        <div class="title_box">{{ item.title }}</div>
        <div class="content_box">{{ item.sub_title }}</div>
      </div>
    </div>
    <br />
    <div class="title_box">Plan Your Swim Safely</div>
    <div class="sub_title_box">
      You’ve chosen a great spot for swimming! To ensure a safe and enjoyable
      day, follow these tips for a successful outing while protecting the water
      quality:
    </div>
    <div class="main_content_box">
      <div
        v-for="(item, index) in mainContentData"
        :key="index"
        class="main_content_item"
      >
        <img :src="item.img" />
        <div class="content_box">
          <div class="content_1">{{ item.title }}</div>
          <div class="content_2">{{ item.sub_title }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mainContentData1: [
        {
          title: "Keep Your Mouth Closed",
          sub_title: "Avoid swallowing water while swimming to stay healthy.",
          img: require("@/assets/images/planning/Keep Your Mouth Closed@2x.png")
        },
        {
          title: "Rinse Off After Swimming",
          sub_title:
            "Freshwater rinsing helps remove any residue from your skin.",
          img: require("@/assets/images/planning/Rinse Off After Swimming@2x.png")
        },
        {
          title: "Use Swim Goggles",
          sub_title:
            "Protect your eyes from small particles or irritants in the water.",
          img: require("@/assets/images/planning/Use Swim Goggles@2x.png")
        },
        {
          title: "Choose Eco-Friendly Sunscreen",
          sub_title:
            "Help protect the water and your skin by using biodegradable sunscreen.",
          img: require("@/assets/images/planning/Choose Eco-Friendly Sunscreen@2x.png")
        }
      ],
      mainContentData: [
        {
          title: "Hydrate & Pack Snacks:",
          sub_title: "Bring water and light snacks in reusable containers.",
          img: require("@/assets/images/planning/Hydrate@2x.png")
        },
        {
          title: "Protective Swim Gear:",
          sub_title: "Wear eco-friendly swimwear & water shoes for safety.",
          img: require("@/assets/images/planning/Protective Swim Gear@2x.png")
        },
        {
          title: "Eco-Friendly Sunscreen:",
          sub_title: "Use biodegradable sunscreen to protect the water.",
          img: require("@/assets/images/planning/Eco-Friendly Sunscreen@2x.png")
        },
        {
          title: "Dispose of waste properly:",
          sub_title: "Use bins or take trash home.",
          img: require("@/assets/images/planning/Dispose of waste properly@2x.png")
        },
        {
          title: "Stay within designated areas:",
          sub_title: "Avoid disrupting surrounding ecosystems.",
          img: require("@/assets/images/planning/Stay within designated areas@2x.png")
        }
        //  {
        //   title: "Stay within designated areas:",
        //   sub_title: "Bring water and light snacks in reusable containers.",
        //   img: require("@/assets/images/planning/Stay within designated areas@2x(1).png")
        // },
      ]
    };
  }
};
</script>

<style lang="less" scoped>
.title_box {
  font-weight: bold;
  font-size: 36px;
  color: #000000;
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
    height: 280px;
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
      color: #000000;
      margin-top: 12px;
    }
    .content_box {
      margin-top: 12px;

      font-weight: 400;
      font-size: 20px;
      color: #000000;
    }
  }
}
</style>
