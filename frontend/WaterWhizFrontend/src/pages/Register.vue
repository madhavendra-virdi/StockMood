<template>
    <div class="register-container">
      <h2>Register</h2>
      <form @submit.prevent="registerUser">
        <input v-model="firstName" placeholder="First Name" required />
        <input v-model="lastName" placeholder="Last Name" required />
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
        <button type="submit">Sign Up</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
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
  .register-container {
    width: 400px;
    margin: 40px auto;
    padding: 20px;
    background: #f5f5f5;
    border-radius: 8px;
  }
  
  input {
    display: block;
    width: 100%;
    margin-bottom: 12px;
    padding: 10px;
    font-size: 16px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    font-size: 18px;
    background-color: #3f51b5;
    color: white;
    border: none;
    border-radius: 4px;
  }
  
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  