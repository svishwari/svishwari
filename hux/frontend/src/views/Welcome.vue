<template>
  <div
    :style="{
      'background-image':
        'url(' + require('../assets/images/welcome_background.png') + ')',
    }"
    class="welcome-wrap"
  >
    <div class="content">
      <Logo />
      <h1>Welcome to Hux!</h1>
      <pre>
      An all-purpose tool to transform raw data into powerful market insights and deliberate campaigns:
      Aggregated Customer Data • Customized CDP • Deep Dive Insights • Personalized Campaigns 
      Targeted Segmentation • Addressable Audiences • Measure & Optimize
      </pre>
      <h2>All Together, Entirely</h2>
      <v-btn
        elevation="2"
        outlined
        small
        class="mt-8"
        color="primary"
        @click="login()"
        >Sign In</v-btn
      >
    </div>
  </div>
</template>

<script>
import Logo from "../assets/images/logo.svg"
// import auth from "./auth/auth";

export default {
  name: "Welcome",
  data() {
    return {
      PATH_TO_PROTECTED_ROUTE: "/home",
    }
  },
  components: {
    Logo,
  },
  methods: {
    login() {
      this.$router.push("home")
    },
  },
}
</script>

<style lang="scss" scoped>
.welcome-wrap {
  height: 100vh;
  background-repeat: space;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  .content {
    width: 72.291666666666667%;
    height: 77.777777777777778%;
    background: #ffffff;
    box-shadow: 0px 0px 20px 5px rgba(0, 0, 0, 0.15);
    border-radius: 5px;
    display: flex;
    padding: 120px;
    flex-direction: column;
    align-items: center;
    svg {
      width: 150px;
      height: 150px;
    }
    h1 {
      font-style: normal;
      font-weight: 600;
      font-size: 24px;
      line-height: 40px;
      margin-top: 48px;
    }
    pre {
      font-family: Open Sans;
      font-style: normal;
      font-weight: normal;
      font-size: 14px;
      line-height: 22px;
      text-align: center;
      color: #757b7b;
      margin-top: 8px;
    }
    h2 {
      font-style: normal;
      font-weight: 600;
      font-size: 21px;
      line-height: 40px;
      text-align: center;
      letter-spacing: 0.1px;
      color: #86bc25;
      margin-top: 8px;
    }
  }
}
</style>
