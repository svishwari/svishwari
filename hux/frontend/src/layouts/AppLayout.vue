<template>
  <v-app>
    <nav-bar @toggleSidebarMenu="toggleSidebar"></nav-bar>
    <side-menu :toggle="toggleMini"></side-menu>
    <div
      class="toggle-menu"
      :style="{ 'margin-left': marginLeft }"
      @click="toggleSidebar()"
    >
      <icon
        type="side-arrow"
        class="toggle-icon"
        :class="{ 'rotate-icon-180': !toggleMini }"
        :size="24"
        color="primary"
        variant="base"
      />
    </div>
    <v-main>
      <v-container fluid ma-0 pa-0 class="views-container">
        <slot />
      </v-container>
    </v-main>
    <hux-alert />
  </v-app>
</template>

<script>
import NavBar from "@/components/NavBar"
import SideMenu from "@/components/SideMenu"
import HuxAlert from "@/components/common/HuxAlert.vue"
import Icon from "@/components/common/Icon"

export default {
  name: "AppLayout",
  components: { SideMenu, NavBar, HuxAlert, Icon },
  data: () => ({
    toggleMini: false,
  }),
  computed: {
    marginLeft() {
      return this.toggleMini ? "77px" : "207px"
    },
  },
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
.toggle-icon {
  background: var(--v-white-base);
  box-shadow: 1.5px 1.5px 5px rgb(57 98 134 / 15%);
  border-radius: 50%;
  padding: 4px;
  transition-duration: 0.2s;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-property: transform, visibility, width;
}
.toggle-menu {
  bottom: 0;
  position: fixed;
  z-index: 9;
}
</style>
