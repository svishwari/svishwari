<template>
  <div class="app-nav-bar">
    <v-app-bar app color="white" dark elevation="0" pa-0 height="70">
      <v-spacer></v-spacer>
      <nav-bar-menu></nav-bar-menu>
    </v-app-bar>
  </div>
</template>

<script>
import NavBarMenu from "@/components/NavBarMenu"

export default {
  name: "NavBar",
  components: { NavBarMenu },
  data: () => ({
    toggleMini: false,
  }),
}
</script>
<style lang="scss" scoped>
.app-nav-bar {
  ::v-deep .v-toolbar__content {
    border-bottom: 1px solid rgb(208, 208, 206);
    padding: 0 !important;
  }
}
</style>
