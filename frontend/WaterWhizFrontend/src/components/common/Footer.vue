<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="brand-section">
        <div class="logo">
          <img src="../../../static/logostockmood.png" alt="StockMood Logo" class="logo-image" />
        </div>
        <div class="cta-buttons">
          <div
            class="cta-box"
            @click="$router.push(isLoggedIn ? '/pricing' : '/login')"
          >
            {{ isLoggedIn ? 'Upgrade Plan' : 'Get Started For Free' }}
          </div>
          <div class="cta-box" @click="$router.push('/contact')">Contact Sales</div>
        </div>
      </div>

      <div class="link-sections">
        <div class="link-column">
          <h4>Products</h4>
          <ul>
            <li @click="$router.push('/aboutCom')">Sentiment Analyzer</li>
            <li>Crypto Insights</li>
            <li>Relative evaluation</li>
            <li>Modelling</li>
          </ul>
        </div>

        <div class="link-column">
          <h4>Resources</h4>
          <ul>
            <li @click="$router.push('/contact')">Help Center</li>
            <li>Blog</li>
            <li>API Docs</li>
          </ul>
        </div>

        <div class="link-column">
          <h4>Social</h4>
          <ul>
            <li>X / Twitter</li>
            <li>LinkedIn</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>© 2025 StockMood Inc. All rights reserved.</p>
      <div class="policy-links">
        <span>Privacy Policy</span>
        <span>Terms of Service</span>
      </div>
    </div>
  </footer>
</template>

<script>
import router from '../../router';

export default {
  name: "Footer",
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("loggedInUser");
    }
  }
};
</script>

<style scoped>
.footer {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 24px 24px 0 0;
  padding: 60px 40px 30px;
  color: #fff;
  font-family: 'Segoe UI', sans-serif;
  background-color: #1b1b1f;
  margin-top: 100px;
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
}

.brand-section {
  flex: 1 1 300px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.logo {
  margin-bottom: 6px;
}

.logo-image {
  width: 240px;
  height: auto;
  object-fit: contain;
}

.cta-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%;
}

.cta-box {
  background: rgba(255, 255, 255, 0.07);
  padding: 14px 18px;
  border-radius: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
  text-align: center;
}

.cta-box:hover {
  background: rgba(255, 255, 255, 0.15);
}

.link-sections {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  flex: 2 1 500px;
  justify-content: space-between;
}

.link-column {
  flex: 1 1 120px;
}

.link-column h4 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #ddd;
}

.link-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.link-column li {
  margin-bottom: 8px;
  color: #bbb;
  cursor: pointer;
  transition: color 0.3s;
}

.link-column li:hover {
  color: #fff;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 60px;
  flex-wrap: wrap;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
  font-size: 14px;
  color: #999;
}

.policy-links {
  display: flex;
  gap: 15px;
}

.policy-links span {
  cursor: pointer;
  transition: color 0.3s;
}

.policy-links span:hover {
  color: #fff;
}
</style>
