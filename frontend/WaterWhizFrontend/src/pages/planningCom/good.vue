<template>
  <div>
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
</style>
