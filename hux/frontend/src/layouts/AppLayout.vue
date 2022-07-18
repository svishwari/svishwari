<template>
  <v-app>
    <nav-bar @toggleSidebarMenu="toggleSidebar"></nav-bar>
    <side-menu v-if="!clientPanel" :toggle="toggleMini"></side-menu>
    <div
      v-if="!clientPanel"
      class="toggle-menu"
      :style="{ 'margin-left': marginLeft }"
      @click="toggleSidebar()"
    >
      <icon
        type="side-arrow"
        class="toggle-icon"
        :class="{ 'rotate-icon-180': !toggleMini }"
        :size="24"
        color="black"
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
import { mapGetters } from "vuex"

export default {
  name: "AppLayout",
  components: { SideMenu, NavBar, HuxAlert, Icon },
  data: () => ({
    toggleMini: false,
  }),
  computed: {
    ...mapGetters({
      alerts: "alerts/list",
      getUserRole: "users/getCurrentUserRole",
    }),

    marginLeft() {
      return this.toggleMini ? "80px" : "207px"
    },

    clientPanel() {
      return this.$route.name == "ClientPanel"
    },
  },
  watch: {
    alerts: function () {
      if (this.alerts.length > 0 && this.alerts[0].code == 401) {
        this.$route.push({
          name: "NoAccess",
        })
      }
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
  box-shadow: -1.5px 1.5px 5px rgb(57 98 134 / 15%);
  border-radius: 50%;
  padding: 4px;
  transition-duration: 0.2s;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-property: transform, visibility, width;
}
.toggle-menu {
  bottom: 3px;
  position: fixed;
  z-index: 9;
}
</style>
