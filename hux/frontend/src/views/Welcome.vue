<template>
  <div class="welcome-wrap">
    <div class="content">
      <Logo />
      <h1>Welcome to Hux!</h1>
      <span>
        An all-purpose tool to transform raw data into powerful market insights
        and deliberate engagements: Aggregated Customer Data • Customized CDP •
        Deep Dive Insights • Personalized Engagements Targeted Segmentation •
        Addressable Audiences • Measure &amp; Optimize
      </span>
      <h2>All Together, Entirely</h2>
      <v-btn
        elevation="2"
        small
        tile
        class="mt-8"
        color="primary"
        @click="login()"
        >Sign In</v-btn
      >
    </div>
  </div>
</template>

<script>
import Logo from "@/assets/images/logo.svg"

export default {
  name: "Welcome",

  components: {
    Logo,
  },

  methods: {
    login() {
      this.$router.push("overview")
    },
  },
}
</script>

<style lang="scss" scoped>
.welcome-wrap {
  height: 100vh;
  background-repeat: space;
  background-size: cover;
  background-image: url("../assets/images/welcome_background.png");
  display: flex;
  justify-content: center;
  align-items: center;
  .content {
    min-width: 72.291666666666667%;
    min-height: 77.777777777777778%;
    max-width: 72.291666666666667%;
    max-height: 77.777777777777778%;
    background: #ffffff;
    box-shadow: 0px 0px 20px 5px rgba(0, 0, 0, 0.15);
    border-radius: 5px;
    display: flex;
    padding: 120px;
    flex-direction: column;
    align-items: center;
    svg {
      min-width: 150px;
      min-height: 150px;
      width: 150px;
      height: 150px;
    }
    h1 {
      font-family: Open Sans;
      font-style: normal;
      font-weight: normal;
      font-style: normal;
      font-weight: 500;
      font-size: 24px;
      line-height: 40px;
      margin-top: 48px;
    }
    span {
      font-family: Open Sans;
      font-style: normal;
      font-weight: normal;
      font-size: 14px;
      line-height: 22px;
      text-align: center;
      color: #4f4f4f;
      margin-top: 8px;
      max-width: 80%;
    }
    h2 {
      font-style: normal;
      font-weight: 500;
      font-size: 21px;
      line-height: 40px;
      text-align: center;
      letter-spacing: 0.1px;
      color: #86bc25;
      margin-top: 8px;
    }
    button {
      min-height: 40px;
      min-width: 95px;
      font-size: 14px;
    }
  }
}
</style>
