<template>
  <div class="verification-code-container">
    <h2>Please enter the verification code</h2>
    <form @submit.prevent="verifyCode">
      <div class="input-group">
        <input v-model="code" type="text" placeholder="input code" required />
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      code: ""
    };
  },
  methods: {
    verifyCode() {
      if (this.code == "virdi") {
        window.localStorage.setItem("isVerified", true);
        this.$router.push("/home");
      } else {
        alert("Verification code error, please re-enter");
      }
      this.code = "";
    }
  }
};
</script>

<style scoped>
.verification-code-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

.input-group {
  width: 300px;
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}
</style>
