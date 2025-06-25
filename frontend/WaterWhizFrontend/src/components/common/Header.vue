<template>
  <div class="main-header">
    <div class="header">
      <!-- Hamburger for Mobile -->
      <i class="fas fa-bars hamburger" @click="drawerVisible = true"></i>

      <!-- Centered Logo -->
      <div @click="handleSelect('home')" class="logo-wrapper">
        <img class="logoClass" src="../../../static/logostockmood.png" />
      </div>

      <!-- Desktop Menu -->
      <div class="right-menu">
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
        >
          <el-menu-item index="home">Home</el-menu-item>
          <el-menu-item index="insights">Dashboard</el-menu-item>
          <el-menu-item index="pricing">Pricing</el-menu-item>
          <el-menu-item v-if="!loggedInUser" index="login">Login</el-menu-item>
          <el-menu-item v-if="loggedInUser" index="profile">@{{ loggedInUser }}</el-menu-item>
        </el-menu>
      </div>
    </div>

    <!-- Mobile Sidebar Drawer -->
    <el-drawer
      :visible.sync="drawerVisible"
      direction="ltr"
      size="60%"
      :with-header="false"
    >
      <ul class="mobile-menu">
        <li @click="navigateAndClose('home')">Home</li>
        <li @click="navigateAndClose('insights')">Dashboard</li>
        <li @click="navigateAndClose('pricing')">Pricing</li>
        <li v-if="!loggedInUser" @click="navigateAndClose('login')">Login</li>
        <li v-if="loggedInUser" @click="navigateAndClose('profile')">@{{ loggedInUser }}</li>
      </ul>
    </el-drawer>
  </div>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      activeIndex: "1",
      loggedInUser: null,
      drawerVisible: false
    };
  },
  mounted() {
    const storedUser = localStorage.getItem("loggedInUser");
    if (!storedUser || storedUser === "null" || storedUser === "undefined") {
      this.loggedInUser = null;
      localStorage.removeItem("loggedInUser");
    } else {
      this.loggedInUser = storedUser;
    }

    this.handleOpen(this.$route);
    this.$root.$on('forceActiveUpdate', () => {
      this.handleOpen(this.$route);
    });
  },
  watch: {
    '$route.path'(newPath) {
      this.handleOpen({ path: newPath });
    }
  },
  methods: {
    handleOpen(to) {
      const pathMap = {
        '/home': 'home',
        '/insights': 'insights',
        '/pricing': 'pricing',
        '/login': 'login',
        '/profile': 'profile'
      };
      this.activeIndex = pathMap[to.path] || 'home';
    },
    handleSelect(key) {
      this.$router.push(`/${key}`);
    },
    navigateAndClose(key) {
      this.handleSelect(key);
      this.drawerVisible = false;
    }
  }
};
</script>

<style scoped lang="less">
@import "../../assets/style/variable";

.main-header {
  height: 80px;
  background: #fff;

  .header {
    height: 100%;
    width: 95%;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;

    .logo-wrapper {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
    }

    .logoClass {
      width: 200px;
      height: auto;
      cursor: pointer;
    }

    .right-menu {
      display: flex;
      align-items: center;

      .el-menu-item {
        font-size: 20px;
        margin: 0 10px;
      }

      .el-menu--horizontal > .el-menu-item.is-active {
        background: #a9c0e8;
        border-radius: 47px;
        color: #fff;
      }

      .el-menu--horizontal > .el-menu-item {
        border-bottom: none;
        border-radius: 47px;
        height: 48px;
        line-height: normal;
      }

      .el-menu--horizontal > .el-menu-item:not(.is-disabled):hover {
        background: #a9c0e8;
        border-radius: 47px;
        color: #fff;
      }

      @media (max-width: 768px) {
        display: none;
      }
    }

    .hamburger {
      position: absolute;
      left: 20px;
      font-size: 26px;
      cursor: pointer;
      display: none;

      @media (max-width: 768px) {
        display: block;
      }
    }
  }

  /deep/ .el-menu.el-menu--horizontal {
    border: none;
  }
}

.mobile-menu {
  list-style: none;
  padding: 20px;
  font-size: 18px;

  li {
    margin-bottom: 15px;
    cursor: pointer;
  }
}
</style>
