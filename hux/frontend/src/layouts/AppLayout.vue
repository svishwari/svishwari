<template>
  <v-app>
    <nav-bar @toggleSidebarMenu="toggleSidebar"></nav-bar>
    <side-menu :toggle="toggleMini"></side-menu>
    <v-main>
      <v-container fluid ma-0 pa-0 class="views-container">
        <slot />
      </v-container>
    </v-main>
    <hux-alert />
    <confirm-modal
      v-model="infoModal"
      icon="access_denied"
      type="warning"
      title="Access Denied"
      body="You do not have the permission to perform this action. Please reach out to your Admin for access."
      :show-left-button="false"
      right-btn-text="Close"
      @onConfirm="infoModal = !infoModal"
    >
    </confirm-modal>
  </v-app>
</template>

<script>
import NavBar from "@/components/NavBar"
import SideMenu from "@/components/SideMenu"
import HuxAlert from "@/components/common/HuxAlert.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import { mapGetters } from "vuex"

export default {
  name: "AppLayout",
  components: { SideMenu, NavBar, HuxAlert, ConfirmModal },
  data: () => ({
    toggleMini: false,
    infoModal: false,
  }),
  computed: {
    ...mapGetters({
      alerts: "alerts/list",
    }),

    getAlerts() {
      return this.alerts.length > 0 ? this.alerts[0] : {}
    },
  },
  watch: {
    alerts: function () {
      if (this.alerts.length > 0 && this.alerts[0].code == 401) {
        this.infoModal = true
      } else {
        this.infoModal = false
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
</style>
