<template>
  <div class="workbench">
    <div class="wrap"></div>
  </div>
</template>

<script>
export default {
  name: "Workbench",
  data() {
    return {};
  },
};
</script>

<style scoped lang="less">
@import "../assets/style/variable";
.workbench {
  height: 100%;
  text-align: center;
  color: #777;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  .wrap {
    margin-top: -100px;
  }
  h2 {
    font-size: 32px;
    color: #555;
    margin-bottom: 20px;
  }
  p {
    line-height: 30px;
  }
  em,
  a {
    font-style: normal;
    font-weight: bold;
    margin: 0 3px;
    color: @primary-color;
  }
}
</style>
