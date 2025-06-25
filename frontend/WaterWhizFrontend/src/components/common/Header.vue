<template>
  <div class="main-header">
    <div class="header">
      <!-- Hamburger icon comes first on mobile -->
      <div class="mobile-header-left">
        <div class="hamburger-menu-mobile" @click="sidebarVisible = true">
          <i class="el-icon-menu"></i>
        </div>
        <div @click="handleSelect('home')">
          <img class="logoClass" src="../../../static/logostockmood.png" />
        </div>
      </div>
      <div class="right-menu">
        <el-menu
          :active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
        >

          <el-menu-item index="home">Home</el-menu-item>
          <el-menu-item index="insights">Dashboard</el-menu-item>
          <el-menu-item index="pricing">Pricing</el-menu-item>

          <el-menu-item v-if="!loggedInUser" index="login">Login</el-menu-item>
          <el-menu-item v-if="loggedInUser" :index="'profile'">
            @{{ loggedInUser }}
          </el-menu-item>





          <!-- <el-menu-item index="4">Visulisation</el-menu-item>
          <el-menu-item index="5">All Model</el-menu-item>
          <el-menu-item index="6">About us</el-menu-item> -->
        </el-menu>
      </div>
    </div>
    <el-drawer
      title="Menu"
      :visible.sync="sidebarVisible"
      direction="ltr"
      class="mobile-drawer"
    >
      <el-menu
        :default-active="activeIndex"
        class="el-menu-vertical"
        @select="handleSidebarSelect"
      >
        <el-menu-item index="home">Home</el-menu-item>
        <el-menu-item index="insights">Dashboard</el-menu-item>
        <el-menu-item index="pricing">Pricing</el-menu-item>
        <el-menu-item v-if="!loggedInUser" index="login">Login</el-menu-item>
        <el-menu-item v-if="loggedInUser" :index="'profile'">@{{ loggedInUser }}</el-menu-item>
      </el-menu>
    </el-drawer>
  </div>
</template>

<script>
export default {
  name: "Header",

  data() {
    return {
    activeIndex: "1",
    loggedInUser: null, // set it in mounted instead
    sidebarVisible: false,
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
    console.log(this.$route.path);
    // if (this.$route.path === "/home") {
    //   this.activeIndex = "home";
    // } else if (this.$route.path === "/calculator") {
    //   this.activeIndex = "calculator";
    // } else if (this.$route.path === "/insights") {
    //   this.activeIndex = "insights";
    // } else if (this.$route.path === "/catchments") {
    //   this.activeIndex = "catchments";
    // }
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
    handleOpen(to, keyPath) {
      if (to.path === "/home") {
        this.activeIndex = "home";
      } else if (to.path === "/insights") {
        this.activeIndex = "insights";

      } else if (to.path === "/pricing") {
        this.activeIndex = "pricing";
      }else if (to.path === "/login") {
        this.activeIndex = "login";
      }else if (to.path === "/profile") {
        this.activeIndex = "profile";
      }
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
      if (key === "home") {
        this.$router.push("/home");
      } else if (key === "insights") {
        this.$router.push("/insights");
      }else if (key === "login") {
        this.$router.push("/login");
      }else if (key === "pricing") {
        this.$router.push("/pricing");
      } else if (key === "profile") {
        this.$router.push("/profile");
      }
    },
    handleSidebarSelect(key) {
    this.handleSelect(key);
    this.sidebarVisible = false;
  }
  }

};
</script>

<style scoped lang="less">
@import "../../assets/style/variable";
.main-header {
  overflow: hidden;
  height: 80px;
  background: #fff;

  .header {
    height: 100%;
    width: 95%; /* Ensures the header spans the full width */
    padding: 0 20px; /* Adds some spacing to the edges */
    display: flex;
    align-items: center;
    justify-content: space-between; /* Pushes items to the edges */

    .logoClass {
      margin-top: 0%;
      width: 350px; /* Adjusted width for better fit */
      height: auto; /* Ensures aspect ratio is maintained */
      cursor: pointer;
    }

    .right-menu {
      display: flex;
      align-items: center;

      .el-menu-item {
        font-size: 20px;
        margin: 0 10px;
        display: flex;
        align-items: center;
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
    }
  }

  /deep/ .el-menu.el-menu--horizontal {
    border: none;
  }
}

.mobile-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Mobile-specific styles */
.hamburger-menu-mobile {
  display: none;
  font-size: 28px;
  cursor: pointer;
  z-index: 3001;
  background: #fff;
  padding: 5px;
  border-radius: 6px;
}

.mobile-drawer {
  z-index: 3000 !important;
}

@media (max-width: 768px) {
  .hamburger-menu-mobile {
    display: block;
  }

  .right-menu {
    display: none !important;
  }
}



</style>