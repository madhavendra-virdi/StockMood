<template>
  <div class="wrap">
    <div class="introduce">
      <h2>Welcome, {{ user.username }}</h2>
      <h3>{{ user.first_name }} {{ user.last_name }}</h3>
      <p>This is your profile page. You can still navigate using the header above.</p>

      <div v-if="favoriteStocks.length > 0" class="favorites">
        <h4>Your Favorite Stocks</h4>
        <ul>
          <li v-for="stock in favoriteStocks" :key="stock">
            <router-link :to="`/insights?stock=${encodeURIComponent(stock)}`">

              <i class="fas fa-star star-icon"></i> {{ stock }}
            </router-link>
          </li>
        </ul>

      </div>
      <p v-else>No favorite stocks yet.</p>

      <div class="plan-card">
        <h4>Your Current Plan: <span class="plan-name">{{ user.plan }}</span></h4>
        <button class="upgrade-btn" @click="goToPricing">Upgrade Plan</button>
      </div>

      <button class="logout-btn" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Profile',
  data() {
    return {
      user: {
        first_name: '',
        last_name: '',
        username: '',
        plan: 'Free'
      },
      favoriteStocks: []
    };
  },
  mounted() {
    const username = localStorage.getItem('loggedInUser');
    if (!username) {
      this.$router.push('/login');
      return;
    }

    axios.get(`/api/user/${username}`)
      .then(res => {
        this.user = res.data;
      })
      .catch(() => {
        this.$router.push('/login');
      });

    axios.get(`/api/user-favorites/${username}`)
      .then(res => {
        this.favoriteStocks = res.data;
      })
      .catch(() => {
        this.favoriteStocks = [];
      });
  },
  methods: {
    logout() {
      localStorage.removeItem('loggedInUser');
      this.$router.push('/login');
      location.reload();
    },
    goToPricing() {
      this.$router.push('/pricing').then(() => {
        this.$root.$emit('forceActiveUpdate');
      });

    },
    

  }
};
</script>

<style scoped>
.wrap {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 90vh;
  background-color: #f8f9fb;
  font-family: 'Segoe UI', sans-serif;
  padding: 60px 20px;
}

.introduce {
  background: #fff;
  padding: 40px 50px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  max-width: 600px;
  width: 100%;
  text-align: center;
}

.introduce h2 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
}

.introduce h3 {
  font-size: 18px;
  color: #666;
  margin-bottom: 20px;
}

.introduce p {
  font-size: 15px;
  color: #444;
  margin-bottom: 25px;
}

.favorites {
  margin: 30px 0;
  text-align: left;
}

.favorites h4 {
  font-size: 18px;
  margin-bottom: 10px;
}

.favorites li {
  margin: 8px 0;
  font-size: 16px;
}

.star-icon {
  color: #f4c542;
  margin-right: 8px;
}


.plan-card {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #dce5f3;
  background: #eef3ff;
  border-radius: 10px;
}

.plan-name {
  font-weight: bold;
  color: #4f80ff;
}

.upgrade-btn {
  margin-top: 15px;
  padding: 10px 18px;
  background-color: #4f80ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
}

.upgrade-btn:hover {
  background-color: #365edc;
}

.logout-btn {
  margin-top: 30px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
}

.logout-btn:hover {
  background-color: #c0392b;
}

</style>
