<template>
  <v-app>
    <component :is="layout">
      <router-view :key="$route.path" />
      <p v-if="isIdle"></p>
    </component>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      initialLoad: true,
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
        alert("you have left this browser idle for 28 minutes!")
      } else if (this.initialLoad && this.layout !== "default-layout") {
        this.initialLoad = false
      }
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
