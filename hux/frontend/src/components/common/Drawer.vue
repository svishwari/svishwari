<template>
  <v-navigation-drawer
    v-model="localDrawer"
    :right="toRight"
    :width="width"
    temporary
    floating
    app
  >
    <v-card
      tile
      elevation="5"
      height="70"
      class="d-flex justify-space-between align-center px-6 py-5"
    >
      <slot name="header-left"></slot>
      <slot name="header-right"></slot>
    </v-card>
    <slot></slot>
    <v-footer absolute padless color="white" elevation="5">
      <v-card
        tile
        height="70"
        class="d-flex justify-space-between align-center px-6 py-5"
        min-width="100%"
      >
        <slot name="footer-left"></slot>
        <slot name="footer-right"></slot>
      </v-card>
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
