<template>
  <div class="screen">
    <div class="image-container">
      <!-- Add multiple images -->
      <img class="background-image" src="@/assets/images/home/yu.png" alt="Background" />
      <img class="background-image" src="@/assets/images/home/AI@2x.png" alt="Background" />
      <img class="background-image" src="@/assets/images/home/AI@2x.png" alt="Background" />
      <img class="background-image" src="@/assets/images/home/AI@2x.png" alt="Background" />
      <img class="background-image" src="@/assets/images/home/AI@2x.png" alt="Background" />
    </div>
    <!-- <div class="container">
      <h1>404</h1>
      <p style="margin-bottom: 50px;">
        Oops! The page you're looking for doesn't exist.
      </p>
      <a style="margin-top: 20px" href="/">Go Back to Home</a>
    </div> -->
  </div>
</template>

<script>

</script>

<style lang="less" scoped>
.screen {
  margin: 0;
  padding: 0;
  font-family: "Arial", sans-serif;
  background-color: #f2f6fa;
  color: #333;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  overflow: hidden;
}

.image-container {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  width: 100%;
  height: 300px;
  overflow: hidden;
  pointer-events: none;
}

.background-image {
  position: absolute;
  width: 100px; /* Adjust the image size */
  height: 100px;
  object-fit: cover;
  animation: moveHorizontal 5s infinite linear;
  opacity: 0.8;
}

/* Position images evenly across the width of the screen */
.background-image:nth-child(1) {
  left: -150px; /* Start off-screen */
  top: 40%;
  animation-delay: 0s;
}

.background-image:nth-child(2) {
  left: -150px;
  top: 40%;
  animation-delay: 1s;
}

.background-image:nth-child(3) {
  left: -150px;
  top: 40%;
  animation-delay: 2s;
}

.background-image:nth-child(4) {
  left: -150px;
  top: 40%;
  animation-delay: 3s;
}

.background-image:nth-child(5) {
  left: -150px;
  top: 40%;
  animation-delay: 4s;
}

/* Horizontal motion animation */
@keyframes moveHorizontal {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(110vw); /* Move completely off-screen to the right */
  }
}

.container {
  text-align: center;
  animation: fadeIn 2s ease-in-out;
}

h1 {
  font-size: 72px;
  color: #58a4db;
  margin: 0;
  animation: float 3s ease-in-out infinite;
}

p {
  font-size: 20px;
  color: #666;
  margin: 10px 0 20px 0;
  animation: fadeIn 3s ease-in-out;
}

a {
  color: #58a4db;
  text-decoration: none;
  padding: 10px 20px;
  border: 2px solid #58a4db;
  border-radius: 25px;
  font-size: 18px;
  transition: background-color 0.3s ease, color 0.3s ease;
  animation: slideIn 1.5s ease-in-out;
}

a:hover {
  background-color: #58a4db;
  color: white;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes slideIn {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
