<template>
  <div class="app-nav-bar">
    <v-app-bar app color="white" dark elevation="0" pa-0>
      <v-app-bar-nav-icon
        class="nav-back-burger"
        @click.stop="toggleSidebarMenu"
      >
        <icon
          :class="{ 'rotate-icon-180': toggleMini }"
          type="hamburger"
          :size="21"
          color="neroBlack"
        />
      </v-app-bar-nav-icon>
      <v-spacer></v-spacer>
      <nav-bar-menu></nav-bar-menu>
    </v-app-bar>
  </div>
</template>

<script>
import NavBarMenu from "@/components/NavBarMenu"
import Icon from "@/components/common/Icon"

export default {
  name: "NavBar",
  components: { NavBarMenu, Icon },
  data: () => ({
    toggleMini: false,
  }),
  methods: {
    toggleSidebarMenu() {
      this.toggleMini = !this.toggleMini
      this.$emit("toggleSidebarMenu")
    },
  },
}
</script>
<style lang="scss">
.v-toolbar__content {
  border-bottom: 1px solid rgb(208, 208, 206);
  padding: 0 !important;
}
</style>
<style lang="scss" scoped>
.app-nav-bar {
  button {
    &.v-app-bar__nav-icon {
      &.nav-back-burger {
        margin-left: 20px !important;
      }
    }
  }
  .v-icon {
    &.notranslate {
      &.mdi {
        &.mdi-backburger {
          &.theme--dark {
            &::before {
              color: var(--v-black-darken3);
            }
          }
        }
      }
    }
  }
}
</style>
