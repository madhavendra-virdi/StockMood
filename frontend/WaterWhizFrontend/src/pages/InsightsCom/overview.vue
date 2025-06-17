<template>
    <div class="overview-com">
      <h2>Overview</h2>
  
      <!-- ForumScout Fetch Button -->
      <button @click="fetchForumPosts" class="forum-button">
        Fetch Forum Posts
      </button>
      <button @click="fetchCryptoTweets">Fetch Twitter Posts (Top 100 Cryptos)</button>
      <button @click="fetchCryptoTweetsFromForumScout">
  Fetch Crypto Tweets (via ForumScout)
</button>
      <!-- Loading and Success Message -->
      <p v-if="loading">Fetching posts...</p>
      <p v-if="successMessage">{{ successMessage }}</p>
    </div>
</template>
  
<script>
  export default {
    name: "overviewCom",
    data() {
      return {
        selectedStock: JSON.parse(sessionStorage.getItem("selectedStock")) || null,
        loading: false,
        successMessage: ""
      };
    },
    methods: {
      async fetchForumPosts() {
    this.loading = true;
    this.successMessage = "";

    try {
      const res = await fetch("/api/reddit/fetch-crypto", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sort: "top",
          limit: 100,
          time: "year"
        })
      });

      const data = await res.json();
      if (data.message) {
        this.successMessage = data.message;
      } else {
        this.successMessage = "❌ Failed to fetch posts.";
      }
    } catch (err) {
      console.error("❌ Error fetching crypto posts:", err);
      this.successMessage = "❌ An error occurred.";
    }

    this.loading = false;
  },
  async fetchCryptoTweets() {
    this.loading = true;
    this.successMessage = "";

    try {
      const res = await fetch("/api/twitter/fetch-crypto", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          limit: 100,
        }),
      });

      const data = await res.json();
      if (data.message) {
        this.successMessage = data.message;
      } else {
        this.successMessage = "❌ Failed to fetch tweets.";
      }
    } catch (err) {
      console.error("❌ Error fetching tweets:", err);
      this.successMessage = "❌ An error occurred.";
    }

    this.loading = false;
  },
  async fetchCryptoTweetsFromForumScout() {
    this.loading = true;
    this.successMessage = "";

    try {
      const res = await fetch("/api/forumscout/fetch-crypto", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });

      const data = await res.json();
      if (data.message) {
        this.successMessage = data.message;
      } else {
        this.successMessage = "❌ Failed to fetch tweets from ForumScout.";
      }
    } catch (err) {
      console.error("❌ Error fetching ForumScout tweets:", err);
      this.successMessage = "❌ An error occurred.";
    }

    this.loading = false;
  }



    }
  };
</script>


  
<style scoped>
  .overview-com {
    padding: 20px;
  }
  
  .forum-button {
    background-color: #a9c0e8;
    color: white;
    border: none;
    padding: 10px 16px;
    font-size: 16px;
    border-radius: 8px;
    cursor: pointer;
    margin: 10px 0;
  }
  
  .forum-button:hover {
    background-color: #8aaed8;
  }
</style>
  