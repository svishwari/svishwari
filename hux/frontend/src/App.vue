<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script>
export default {
  name: "App",
  computed: {
    layout() {
      // none-layout will be used if the meta.layout tag is not set
      // computed may not be best place in vue lifecycle for this but it works ok
      return `${this.$route.meta.layout || "none"}-layout`;
    },
  },
  mounted() {
    window.addEventListener("load", () => {
      document.getElementsByClassName("loader-overlay")[0].remove();
    });
  },
};
</script>

<style lang="scss">
body {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100vh;
  background: #f8f9fa !important;
  #nprogress .bar {
    height: 6px;
  }
}
/* All delay classes will take half the time to start */
:root {
  --animate-delay: 0.1s;
}
</style>
