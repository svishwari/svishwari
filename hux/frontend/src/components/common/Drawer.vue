<template>
  <v-navigation-drawer
    v-model="localDrawer"
    :right="toRight"
    :width="width"
    temporary
    floating
    app
  >
    <v-toolbar
      style="width: 100%"
      class="d-flex justify-space-between align-center px-6 py-5"
      height="70"
      tile
      absolute
      padless
      color="white"
      elevation="5"
    >
      <slot name="header-left"></slot>
      <slot name="header-right"></slot>
    </v-toolbar>

    <div class="drawer-content"><slot></slot></div>
    <v-footer
      class="d-flex justify-space-between align-center px-6 py-5"
      absolute
      padless
      color="white"
      elevation="5"
    >
      <slot name="footer-left"></slot>
      <slot name="footer-right"></slot>
    </v-footer>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "Drawer",

  data() {
    return {
      localDrawer: this.value,
    }
  },

  props: {
    toRight: {
      type: Boolean,
      required: false,
      default: true,
    },

    value: {
      type: Boolean,
      required: true,
      default: false,
    },

    width: {
      type: String,
      required: false,
      default: "600",
    },
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
      if (!this.localDrawer) {
        this.$emit("onClose")
      }
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-navigation-drawer__content {
  overflow-y: hidden;
}
.drawer-content {
  height: calc(100% - 130px);
  margin-top: 70px;
  overflow-y: auto;
}
</style>
