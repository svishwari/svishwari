<template>
  <div v-if="!authenticated" class="welcome-wrap">
    <div class="content">
      <logo />
      <div class="font-weight-light text-h1 welcome-header">
        Unleash the power of Hux
      </div>
      <span class="text-body-1 welcome-body">
        We’ve built a new framework for connecting capabilities end-to-end and
        elevating experiences. Hux, paired with our team of Experience
        Management experts, helps our clients regain ownership of their data,
        decisioning, and omnichannel orchestration capabilities to manage
        experiences at scale.
      </span>
      <v-btn
        :to="getDefaultRoute(role)"
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
import { mapGetters } from "vuex"
import { getDefaultRoute } from "../utils"

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
  computed: {
    ...mapGetters({
      role: "users/getCurrentUserRole",
    }),
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
        this.$store.dispatch("users/getAccessMetrics")
        this.$router.replace(redirect || getDefaultRoute(this.role))
      } else {
        this.$store.dispatch("users/setUserProfile", {})
        this.$store.dispatch("users/setUserToken", {})
      }
    },
    async isAuthenticated() {
      this.authenticated = await this.$auth.isAuthenticated()
    },
    getDefaultRoute: getDefaultRoute,
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
    .welcome-header {
      font-weight: 400;
      margin-top: 48px;
    }
    .welcome-body {
      text-align: center;
      color: var(--v-black-lighten4);
      margin-top: 8px;
      max-width: 80%;
    }
    .btn-signin {
      min-height: 40px;
      min-width: 95px;
      font-size: 14px;
    }
  }
}
</style>
