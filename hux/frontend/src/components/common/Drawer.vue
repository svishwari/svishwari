<template>
  <v-navigation-drawer
    v-model="localDrawer"
    :right="toRight"
    :style="transition"
    :width="drawerWidth"
    app
    floating
    hide-overlay
    temporary
  >
    <v-toolbar width="100%" class="box-shadow-25">
      <v-toolbar-title class="px-6">
        <slot name="header-left"></slot>
        <slot name="header-right"></slot>
      </v-toolbar-title>
      <template v-if="expandable">
        <v-icon
          color="primary"
          @click="onExpandIconClick"
          class="cursor-pointer px-6 ml-auto"
        >
          {{ expanded ? "mdi-arrow-collapse" : "mdi-arrow-expand" }}
        </v-icon>
      </template>
    </v-toolbar>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <div class="drawer-content pa-2">
      <slot></slot>
    </div>

    <v-footer
      class="d-flex justify-space-between align-center px-6 py-5"
      absolute
      padless
      height="80"
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
      expanded: false,
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
      type: Number,
      required: false,
      default: 600,
    },

    expandedWidth: {
      type: Number,
      required: false,
      default: 900,
    },

    expandable: {
      type: Boolean,
      required: false,
      default: false,
    },

    disableTransition: {
      type: Boolean,
      required: false,
      default: false,
    },

    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  computed: {
    transition() {
      return {
        transitionDuration: this.disableTransition ? "0s" : "0.5s",
      }
    },
    drawerWidth() {
      return this.expanded ? this.expandedWidth : this.width
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
        this.reset()
      }
    },
  },

  methods: {
    onExpandIconClick: function () {
      this.expanded = !this.expanded
      this.$emit("iconToggle", this.expanded)
    },

    reset() {
      this.expanded = false
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
  overflow-y: auto;
}
::v-deep .v-icon.v-icon::after {
  content: none;
}
</style>
