<template>
  <div id="app" class="initial">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style lang="less">
@import "assets/style/style";
* {
  box-sizing: content-box !important;
}
</style>
