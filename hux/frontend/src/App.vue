<template>
  <v-app>
    <component :is="layout">
      <router-view />
    </component>
  </v-app>
</template>

<script>
export default {
  name: "App",
  computed: {
    layout() {
      return `${this.$route.meta.layout || "default"}-layout`
    },
  },
  mounted() {
    window.addEventListener("load", () => {
      document.getElementsByClassName("loader-overlay")[0].remove()
    })
  },
}
</script>

<style lang="scss">
body {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100vh;
  background: var(--v-black-lighten1) !important;
  font-family: "Open Sans";
  #nprogress .bar {
    height: 6px;
  }
}
/* All delay classes will take half the time to start */
:root {
  --animate-delay: 0.1s;
}
@import "../node_modules/ag-grid-community/dist/styles/ag-grid.css";
@import "../node_modules/ag-grid-community/dist/styles/ag-theme-alpine.css";
</style>
