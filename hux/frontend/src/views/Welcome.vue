<template>
  <div v-if="!authenticated" class="welcome-wrap">
    <div class="content">
      <logo />
      <h1>Unleash the power of Hux</h1>
      <span>
        We’ve built a new framework for connecting capabilities end-to-end and
        elevating experiences. Hux, paired with our team of Experience
        Management experts, helps our clients regain ownership of their data,
        decisioning, and omnichannel orchestration capabilities to manage
        experiences at scale.
      </span>
      <v-btn
        :to="{ name: 'Home' }"
        data-e2e="signin"
        elevation="2"
        small
        tile
        class="btn-signin mt-8"
        color="primary"
      >
        Sign In
      </v-btn>
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
  data() {
    return {
      authenticated: false,
    }
  },
  beforeMount() {
    this.setup()
  },
  methods: {
    async setup() {
      this.isAuthenticated()
      this.claims = await this.$auth.getUser()
      if (this.claims) {
        this.$store.dispatch("users/setUserProfile", {
          userProfile: this.claims,
        })
        const authStorage = JSON.parse(
          localStorage.getItem("okta-token-storage")
        )
        this.$store.dispatch("users/setUserToken", {
          accessToken: authStorage.accessToken,
          idToken: authStorage.idToken,
        })
        const redirect = sessionStorage.getItem("appRedirect")
        sessionStorage.removeItem("appRedirect")
        this.$store.dispatch("users/getUserProfile")
        this.$router.replace(
          redirect || {
            name: "Home",
          }
        )
      } else {
        this.$store.dispatch("users/setUserProfile", {})
        this.$store.dispatch("users/setUserToken", {})
      }
    },
    async isAuthenticated() {
      this.authenticated = await this.$auth.isAuthenticated()
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
    max-width: 72.291666666666667%;
    background: var(--v-white-base);
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
      font-family: Open Sans Light;
      font-style: normal;
      font-weight: normal;
      font-style: normal;
      font-weight: 400;
      font-size: 28px;
      line-height: 40px;
      margin-top: 48px;
    }
    span {
      font-family: Open Sans;
      font-style: normal;
      font-weight: normal;
      font-size: 16px;
      line-height: 22px;
      text-align: center;
      color: var(--v-black-lighten4);
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
      color: var(--v-greenLight-base);
      margin-top: 8px;
    }
    .btn-signin {
      min-height: 40px;
      min-width: 95px;
      font-size: 14px;
    }
  }
}
</style>
