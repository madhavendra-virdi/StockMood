<template>
  <div class="wrap">
    <div class="introduce">
      <h2></h2>
      <h3></h3>
      <p></p>
    </div>
    <div class="login">
      <h1>LOG IN</h1>
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
      <p style="margin-top: 20px; font-size: 14px;">
        Not a member?
        <router-link to="/register" style="color: #409EFF;">Register now</router-link>
      </p>
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
  width: 100%;
  height: 100vh;
  background-image: url("../../static/dizzy.png");
  background-repeat: no-repeat;
  background-size: auto 100%;
  background-clip: content-box;
  background-position: center;
  
  .introduce {
    padding-left: 10%;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    color: #fff;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    flex-direction: column;
    justify-content: center;
    h2 {
      font-size: 34px;
      font-style: italic;
      font-weight: 900;
      margin-top: 50px;
    }
    h3 {
      font-size: 49px;
      font-weight: 300;
      margin: 25px 0;
    }
  }

  .login {
    height: 100%;
    width: 45%;
    max-width: 640px;
    flex-shrink: 0;
    text-align: center;
    background: #fff;
    padding: 0 8%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
    h1 {
      font-size: 28px;
      font-weight: 500;
    }
    .info-input {
      margin-top: 32px;
      margin-bottom: 62px;
      /deep/ .el-input {
        margin-top: 38px;
        .el-input__inner {
          height: 50px;
          background: #f9f9f9;
          border: 1px solid transparent;
          &:focus {
            border: 1px solid @primary-color;
          }
        }
      }
    }
    .el-button {
      height: 50px;
      width: 100%;
      color: #fff;
      font-size: 16px;
      background: linear-gradient(
        130deg,
        @primary-color + 20 0%,
        @primary-color - 20 100%
      );
    }
  }
}
</style>
