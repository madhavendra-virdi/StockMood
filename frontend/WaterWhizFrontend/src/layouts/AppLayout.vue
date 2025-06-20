<template>
  <el-container class="app-layout">
    <el-main>
      <header>
        <AppHeader />
      </header>
      <main class="main-layout">
        <transition name="el-fade-in-linear">
          <router-view></router-view>
        </transition>
        <footer>
          <Footer />
        </footer>
        <el-backtop target=".main-layout">
          <div style="height: 100%; text-align: center; color: #fff;">
            <div>
              <i class="el-icon-caret-top"></i>
            </div>
            TOP
          </div>
        </el-backtop>
      </main>
    </el-main>
  </el-container>
</template>

<script>
import { mapState } from "vuex";
import Header from "../components/common/Header";
import Footer from "../components/common/Footer";
import Menu from "../components/common/Menu";

export default {
  name: "DefaultLayout",
  components: { AppHeader: Header, Menu, Footer },
  computed: {
    ...mapState(["menuData"])
  },
  mounted() {
    console.log(window.localStorage.getItem("isVerified"))
    if (!window.localStorage.getItem("isVerified")) {
      this.$router.push("/verify");
    }
  }
};
</script>

<style scoped lang="less">
@import "../assets/style/variable";

.el-container {
  background: #ffffff;
  height: 100%;
  margin: 0 auto;
  display: flex;
  overflow: hidden;

  .el-aside {
    width: @menu-width !important;
    flex-shrink: 0;
    height: 100%;
    overflow-y: auto;
    background: @primary-color;
    color: #fff;
    transition: width ease 0.3s;

    &.collapse {
      width: 64px !important;
    }
  }

  .el-main {
    width: 100%;
    height: 100%;
    padding: 0;
    position: relative;
    display: flex;
    flex-direction: column;
    overflow: hidden;

    & > header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 1000;
      height: @header-height;
      background: #ffffff;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
      width: 100vw;
      padding: 0;
      margin: 0;
    }

    & > main.main-layout {
      height: 100%;
      overflow-y: auto;
      padding-top: @header-height;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s;
  opacity: 1;
  position: absolute;
  width: 100%;
}

.fade-enter,
.fade-leave-to {
  transform: translateY(900px);
  opacity: 0;
  transition: all 0.5s;
  position: absolute;
}

.el-backtop {
  width: 60px;
  height: 60px;
  font-size: 20px;
  border-radius: 30px;
  background: #a9c0e8;
  color: #fff !important;
}
</style>
