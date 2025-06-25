<template>
  <div class="register-wrapper">
    <div class="register-container">
      <h2>Create Your Account</h2>
      <form @submit.prevent="registerUser">
        <input v-model="firstName" placeholder="First Name" required />
        <input v-model="lastName" placeholder="Last Name" required />
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
        <button type="submit">Sign Up</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
      <p class="login-link">
        Already have an account?
        <router-link to="/login">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      firstName: '',
      lastName: '',
      username: '',
      password: '',
      confirmPassword: '',
      error: ''
    };
  },
  methods: {
    registerUser() {
      this.error = '';

      if (this.password !== this.confirmPassword) {
        this.error = 'Passwords do not match.';
        return;
      }

      axios.post('/api/register', {
        first_name: this.firstName,
        last_name: this.lastName,
        username: this.username,
        password: this.password
      })
      .then(res => {
        if (res.data.success) {
          localStorage.setItem('loggedInUser', this.username);
          this.$router.push('/home');
        }
      })
      .catch(err => {
        if (err.response && err.response.data && err.response.data.message) {
          this.error = err.response.data.message;
        } else {
          this.error = 'Registration failed.';
        }
      });
    }
  }
};
</script>

<style scoped>
.register-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 16px;
  min-height: 100vh;
  background-color: #eef1f5;
}

.register-container {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 30px 20px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  font-weight: 600;
  color: #333;
}

input {
  width: 100%;
  padding: 12px 14px;
  margin-bottom: 14px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #3f51b5;
}

button {
  width: 100%;
  padding: 12px;
  font-size: 17px;
  background-color: #3f51b5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #303f9f;
}

.error {
  color: red;
  margin-top: 12px;
  text-align: center;
  font-size: 14px;
}

.login-link {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
}

.login-link a {
  color: #3f51b5;
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}

/* Mobile tweaks */
@media (max-width: 480px) {
  .register-container {
    padding: 20px 15px;
    border-radius: 8px;
  }

  h2 {
    font-size: 20px;
  }

  input {
    padding: 10px;
  }

  button {
    padding: 10px;
    font-size: 16px;
  }
}
</style>
