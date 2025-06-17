<template>
  <div class="header-wrapper">
    <div class="main-header">
      <div class="header-container">
        <div class="logo" @click="handleLogoClick">
          <img src="../../../static/logostockmood.png" class="logo-image" />
        </div>

        <el-menu
          :default-active="activeIndex"
          mode="horizontal"
          class="nav-menu"
          @select="handleSelect"
          background-color="transparent"
          text-color="#ccc"
          active-text-color="#ffffff"
        >
          <el-menu-item index="insights">Dashboard</el-menu-item>
          <el-menu-item index="pricing">Pricing</el-menu-item>
          <el-menu-item v-if="!loggedInUser" index="login">Login</el-menu-item>
          <el-menu-item v-if="loggedInUser" :index="'profile'">@{{ loggedInUser }}</el-menu-item>
        </el-menu>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      activeIndex: "",
      loggedInUser: null
    };
  },
  mounted() {
    const storedUser = localStorage.getItem("loggedInUser");
    this.loggedInUser = storedUser && storedUser !== "null" && storedUser !== "undefined" ? storedUser : null;
    this.handleOpen(this.$route);
    this.$root.$on("forceActiveUpdate", () => {
      this.handleOpen(this.$route);
    });
  },
  watch: {
    "$route.path"(newPath) {
      this.handleOpen({ path: newPath });
    }
  },
  methods: {
    handleLogoClick() {
      this.$router.push("/home");
    },
    handleOpen(to) {
      const map = {
        "/insights": "insights",
        "/pricing": "pricing",
        "/login": "login",
        "/profile": "profile"
      };
      this.activeIndex = map[to.path] || "";
    },
    handleSelect(key) {
      const map = {
        insights: "/insights",
        pricing: "/pricing",
        login: "/login",
        profile: "/profile"
      };
      this.$router.push(map[key]);
    }
  }
};
</script>

<style scoped lang="less">
.header-wrapper {
  display: flex;
  justify-content: center;
  padding: 24px 0 40px;
  background: transparent; // Remove black background
}

.main-header {
  width: 92%;
  max-width: 1080px;
  background: #ffffff; // Light background to match the page
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  padding: 12px 0;
  border: 1px solid rgba(0, 0, 0, 0.05);
  z-index: 10;
  position: relative;

  .header-container {
    max-width: 100%;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;

    .logo-image {
      height: 38px;
      transform: scale(5); // Scale the logo up visually
      transform-origin: left center; // Anchor scaling from the left
      cursor: pointer;
    }

    .nav-menu {
      background: transparent;
      border: none;
      display: flex;
      gap: 8px;

      .el-menu-item {
        font-family: 'Poppins', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        color: #3b82f6 !important; // Your desired color
        border-radius: 16px !important;
        transition: all 0.3s ease;

        &:hover {
          color: #1f1e1e !important;
          background: rgb(51, 51, 51) !important;
        }

        &.is-active {
          color: #fff !important;
          background: #3b82f6 !important;
        }
      }
    }
  }
}

</style>
