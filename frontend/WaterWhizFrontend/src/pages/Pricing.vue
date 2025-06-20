<template>
  <div class="pricing-page">
    <h1 class="title">Simple, transparent pricing</h1>
    <p class="subtitle">No hidden fees. No surprises.</p>

    <div class="plans">
      <div class="plan">
        <h2>Free</h2>
        <p class="price">$0<span>/month</span></p>
        <ul>
          <li>Basic Insights</li>
          <li>Access to Top 5 Cryptos</li>
          <li>Reddit Sentiment Only</li>
        </ul>
        <button>Start Free</button>
      </div>

      <div class="plan popular">
        <div class="badge">Most Popular</div>
        <h2>Pro</h2>
        <p class="price">$19<span>/month</span></p>
        <ul>
          <li>Unlimited Insights</li>
          <li>Reddit + Twitter Sentiment</li>
          <li>Download Reports</li>
        </ul>
        <button class="highlighted">Go Pro</button>
      </div>

      <div class="plan">
        <h2>Enterprise</h2>
        <p class="price">Custom</p>
        <ul>
          <li>Dedicated Support</li>
          <li>Custom Reports & API Access</li>
          <li>Bulk Queries</li>
        </ul>
        <button @click="$router.push('/contact')">Contact Us</button>
      </div>
    </div>

    <div class="compare-plans">
      <h2 class="compare-title">Compare All Features</h2>
      <table class="compare-table">
        <thead>
          <tr>
            <th>Features</th>
            <th>Free</th>
            <th>Pro</th>
            <th>Enterprise</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Insights Limit</td>
            <td>Basic Only</td>
            <td>Unlimited</td>
            <td>Unlimited + Custom</td>
          </tr>
          <tr>
            <td>Top Crypto Coverage</td>
            <td>Top 5 Only</td>
            <td>All Listed</td>
            <td>All + Custom Symbols</td>
          </tr>
          <tr>
            <td>Reddit Sentiment</td>
            <td>✔</td>
            <td>✔</td>
            <td>✔</td>
          </tr>
          <tr>
            <td>Twitter Sentiment</td>
            <td>✘</td>
            <td>✔</td>
            <td>✔</td>
          </tr>
          <tr>
            <td>Report Downloads</td>
            <td>✘</td>
            <td>✔</td>
            <td>✔</td>
          </tr>
          <tr>
            <td>API Access</td>
            <td>✘</td>
            <td>✘</td>
            <td>✔</td>
          </tr>
          <tr>
            <td>Support</td>
            <td>Email Only</td>
            <td>Email & Chat</td>
            <td>Dedicated Manager</td>
          </tr>
        </tbody>
      </table>
    </div>

    <el-backtop />
  </div>
</template>

<script>
export default {
  name: "Pricing"
};
</script>

<style scoped lang="less">
@import "../assets/style/variable";

.pricing-page {
  max-width: 1200px;
  margin: 50px auto;
  text-align: center;
  padding: 0 20px;
  font-family: 'Segoe UI', sans-serif;
}

.title {
  font-size: 40px;
  font-weight: bold;
}

.subtitle {
  font-size: 18px;
  margin-bottom: 40px;
  color: #666;
}

.plans {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
}

.plan {
  background: #f8f9fb;
  padding: 30px;
  border-radius: 16px;
  width: 300px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
  transition: 0.3s ease;
}

.plan:hover {
  transform: translateY(-5px);
}

.plan h2 {
  margin-bottom: 10px;
  font-size: 24px;
}

.plan .price {
  font-size: 32px;
  margin: 15px 0;
}

.plan .price span {
  font-size: 16px;
  color: #888;
}

.plan ul {
  list-style: none;
  padding: 0;
  margin: 20px 0;
  text-align: left;
}

.plan li {
  padding: 6px 0;
  border-bottom: 1px solid #e0e0e0;
}

.plan button {
  background: #a9c0e8;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
}

.plan.popular {
  border: 2px solid #a9c0e8;
  background: #eef3ff;
  position: relative;
}

.plan.popular .badge {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #a9c0e8;
  color: white;
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.plan .highlighted {
  background: #a9c0e8;
}

.compare-plans {
  margin-top: 60px;
  text-align: center;
}

.compare-title {
  font-size: 28px;
  margin-bottom: 20px;
  font-weight: 600;
}

.compare-table {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  border-collapse: collapse;
  text-align: center;
  font-size: 16px;
  background: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  overflow: hidden;
}

.compare-table th,
.compare-table td {
  padding: 15px;
  border-bottom: 1px solid #eaeaea;
}

.compare-table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.compare-table tr:last-child td {
  border-bottom: none;
}
</style>
