<template>
  <v-app>
    <nav-bar @toggleSidebarMenu="toggleSidebar"></nav-bar>
    <side-menu :toggle="toggleMini"></side-menu>
    <v-main>
      <v-container fluid ma-0 pa-0 class="views-container">
        <slot />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "@/components/NavBar"
import SideMenu from "@/components/SideMenu"

export default {
  name: "AppLayout",
  components: { SideMenu, NavBar },
  data: () => ({
    toggleMini: false,
  }),
  methods: {
    toggleSidebar() {
      this.toggleMini = !this.toggleMini
    },
  },
}
</script>

<style lang="scss">
.views-container,
.views-container > div {
  height: 100%;
}
</style>
