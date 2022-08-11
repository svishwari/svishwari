<template>
  <v-app>
    <component :is="layout">
      <router-view :key="$route.path" />
      <p v-if="isIdle"></p>
      <session-modal
        v-model="showConfirmModal"
        icon="time"
        @logout="logout()"
        @sessioncontinue="showConfirmModal = false"
      >
      </session-modal>
    </component>
  </v-app>
</template>

<script>
import SessionModal from "@/components/common/SessionModal"
export default {
  name: "App",
  components: {
    SessionModal,
  },
  data() {
    return {
      initialLoad: true,
      showConfirmModal: false,
    }
  },
  computed: {
    layout() {
      return `${this.$route.meta.layout || "default"}-layout`
    },
    isIdle() {
      this.showAlertModel(this.$store.state.idleVue.isIdle)
      return this.$store.state.idleVue.isIdle
    },
  },
  mounted() {
    window.addEventListener("load", () => {
      document.getElementsByClassName("loader-overlay")[0].remove()
    })
  },
  methods: {
    showAlertModel(idleState) {
      if (idleState && !this.initialLoad && this.layout !== "default-layout") {
        this.showConfirmModal = true
      } else if (this.initialLoad && this.layout !== "default-layout") {
        this.initialLoad = false
      }
    },
    async logout() {
      await this.$store.dispatch("users/getUserProfile")
      this.$auth.logout()
    },
  },
}
</script>

<style lang="scss">
body {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100vh;
  #nprogress .bar {
    height: 6px;
  }
}
/* All delay classes will take half the time to start */
:root {
  --animate-delay: 0.1s;
}
</style>
