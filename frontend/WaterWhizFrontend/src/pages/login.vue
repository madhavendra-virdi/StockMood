<template>
  <div class="wrap">
    <div class="content">
      <!-- Left: Intro Section (Hidden on mobile) -->
      <div class="introduce">
        <h2>Welcome to</h2>
        <h3>StockMood</h3>
        <p>ANALYSIS REDEFINED.</p>
      </div>

      <!-- Right: Login Section -->
      <div class="login">
        <h1>Login</h1>
        <div class="info-input">
          <el-input placeholder="Username" v-model="username"></el-input>
          <el-input
            placeholder="Password"
            v-model="password"
            @keypress.enter.native="login"
            type="password"
            show-password
          ></el-input>
        </div>
        <el-button :loading="loading" @click="login">LOGIN</el-button>

        <p class="register-text">
          Not a member?
          <router-link to="/register">Register now</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapMutations } from "vuex";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      loading: false
    };
  },
  methods: {
    ...mapMutations(["setUserInfo"]),

    login() {
      if (this.loading) return;
      if (!this.__check()) return;

      this.loading = true;

      axios.post('/api/login', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        if (response.data.success) {
          localStorage.setItem('loggedInUser', this.username);

          this.setUserInfo({
            avatar: "/static/avatar/woman.png",
            realname: this.username
          });

          this.$router.push('/home');
        } else {
          this.$message.error("Invalid credentials.");
        }
      })
      .catch(error => {
        this.$message.error(
          (error.response && error.response.data && error.response.data.message) ||
          "Login failed. Please try again."
        );
      })
      .finally(() => {
        this.loading = false;
      });
    },

    __check() {
      if (this.username.trim() === "") {
        this.$message.error("Please enter your username.");
        return false;
      }
      if (this.password.trim() === "") {
        this.$message.error("Please enter your password.");
        return false;
      }
      return true;
    }
  }
};
</script>

<style scoped lang="less">
@import "../assets/style/variable";

.wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(to right, #dbe9ff, #e7f0fa);
  padding: 20px;

  .content {
    display: flex;
    width: 100%;
    max-width: 1080px;
    background: #fff;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    flex-direction: row;

    @media (max-width: 768px) {
      flex-direction: column;
    }

    .introduce {
      background: linear-gradient(135deg, #5b7fff, #2d5fff);
      color: white;
      width: 50%;
      padding: 60px 40px;
      display: flex;
      flex-direction: column;
      justify-content: center;

      h2 {
        font-size: 30px;
        font-weight: 400;
      }

      h3 {
        font-size: 42px;
        font-weight: 700;
        margin: 10px 0;
      }

      p {
        font-size: 16px;
        opacity: 0.9;
      }

      @media (max-width: 768px) {
        display: none;
      }
    }

    .login {
      flex: 1;
      padding: 60px 40px;
      display: flex;
      flex-direction: column;
      justify-content: center;

      h1 {
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 32px;
        color: #333;
        text-align: center;
      }

      .info-input {
        margin-bottom: 24px;

        /deep/ .el-input {
          margin-bottom: 20px;

          .el-input__inner {
            height: 44px;
            background: #f5f7fa;
            border-radius: 8px;
            border: 1px solid #dcdfe6;
            transition: border 0.2s;

            &:focus {
              border-color: @primary-color;
              box-shadow: 0 0 0 2px fade(@primary-color, 20%);
            }
          }
        }
      }

      .el-button {
        height: 48px;
        width: 100%;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        background: linear-gradient(to right, @primary-color + 20, @primary-color - 20);
        color: white;
      }

      .register-text {
        margin-top: 24px;
        font-size: 14px;
        color: #666;
        text-align: center;

        a {
          color: @primary-color;
          font-weight: 500;
        }
      }
    }
  }
}
</style>
