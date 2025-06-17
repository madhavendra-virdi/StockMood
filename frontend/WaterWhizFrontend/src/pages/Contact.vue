<template>
  <el-container class="app-layout contact-page" :style="backgroundStyle">
    <el-main>
      <main class="main-layout">
        <div class="contact-form-wrapper">
          <h1>Contact Us</h1>
          <p>If you have any questions or want to reach out regarding the Enterprise plan, please fill out the form below.</p>

          <el-form :model="form" @submit.native.prevent="handleSubmit" label-position="top" class="contact-form">
            <el-form-item label="Full Name">
              <el-input v-model="form.name" :disabled="true"></el-input>
            </el-form-item>

            <el-form-item label="Email" :error="errors.email">
              <el-input v-model="form.email"></el-input>
            </el-form-item>

            <el-form-item label="Company (optional)">
              <el-input v-model="form.company"></el-input>
            </el-form-item>

            <el-form-item label="Message" :error="errors.message">
              <el-input type="textarea" v-model="form.message" required rows="5"></el-input>
            </el-form-item>

            <el-button type="primary" native-type="submit">Send Message</el-button>
          </el-form>

          <p v-if="successMessage" class="success-msg">{{ successMessage }}</p>

          <div class="direct-contact">
            <h2>Other Ways to Reach Us</h2>
            <p>Email: <a href="mailto:contactstockmood@gmail.com">contactstockmood@gmail.com</a></p>
            <p>Helpline: <a href="tel:+18001234567">+91 (800) 123-4567</a></p>
          </div>
        </div>
      </main>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Contact',
  data() {
    return {
      form: {
        name: '',
        email: '',
        company: '',
        message: ''
      },
      user: null,
      errors: {
        name: '',
        email: '',
        message: ''
      },
      successMessage: '',
      backgroundStyle: {
        backgroundImage: "url('/static/contact-bg.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '100vh'
      }
    };
  },
  mounted() {
    const username = localStorage.getItem("loggedInUser");
    if (!username) {
      this.$router.push('/login');
      return;
    }

    axios.get(`/api/user/${username}`)
      .then(res => {
        this.user = res.data;
        this.form.name = `${res.data.first_name} ${res.data.last_name}`;
      })
      .catch(() => {
        this.$router.push('/login');
      });
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.errors = { name: '', email: '', message: '' };

      if (!this.form.email.trim()) {
        this.errors.email = 'Email is required';
        isValid = false;
      } else if (!/^\S+@\S+\.\S+$/.test(this.form.email)) {
        this.errors.email = 'Invalid email format';
        isValid = false;
      }

      if (!this.form.message.trim()) {
        this.errors.message = 'Message is required';
        isValid = false;
      }

      return isValid;
    },
    handleSubmit() {
      if (!this.validateForm()) return;

      axios.post('/api/contact', this.form, {
        headers: {
            'Content-Type': 'application/json'
        }
    })

        .then(() => {
          this.successMessage = 'Thank you for reaching out! We will get back to you soon.';
          this.form.message = '';
          this.errors = { name: '', email: '', message: '' };
        })
        .catch(() => {
          this.successMessage = 'An error occurred. Please try again later.';
        });
    }
  }
};
</script>


<style scoped>
.contact-form-wrapper {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 2.5rem;
  border-radius: 20px;
  max-width: 700px;
  margin: 3rem auto;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.contact-form-wrapper h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-align: center;
  color: #2c3e50;
}

.contact-form-wrapper p {
  text-align: center;
  font-size: 1rem;
  color: #555;
  margin-bottom: 2rem;
}

.contact-form ::v-deep(.el-input__inner),
.contact-form ::v-deep(textarea.el-textarea__inner) {
  border-radius: 10px;
  border: 1px solid #ccc;
  padding: 0.75rem;
  font-size: 1rem;
}

.contact-form ::v-deep(.el-button--primary) {
  display: block;
  margin: 2rem auto 0;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  border-radius: 30px;
  background-color: #409EFF;
  border-color: #409EFF;
  transition: background-color 0.3s ease;
}

.contact-form ::v-deep(.el-button--primary:hover) {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

.success-msg {
  margin-top: 1.5rem;
  text-align: center;
  color: #28a745;
  font-size: 1.1rem;
  font-weight: 600;
}

.direct-contact {
  margin-top: 3rem;
  text-align: center;
  font-size: 1rem;
  color: #333;
}

.direct-contact h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.direct-contact a {
  color: #409EFF;
  text-decoration: none;
}

.direct-contact a:hover {
  text-decoration: underline;
}
</style>
