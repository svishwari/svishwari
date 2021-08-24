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
    <v-toolbar width="100%" class="drawer-header box-shadow-25">
      <v-toolbar-title :class="contentHeaderPadding">
        <slot name="header-left"></slot>
        <slot name="header-right"></slot>
      </v-toolbar-title>
      <template v-if="expandable">
        <v-icon
          color="primary"
          class="cursor-pointer px-6 ml-auto"
          @click="onExpandIconClick"
        >
          {{ expanded ? "mdi-arrow-collapse" : "mdi-arrow-expand" }}
        </v-icon>
      </template>
    </v-toolbar>

    <slot name="loading">
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </slot>

    <div
      class="drawer-content"
      :class="{
        contentPadding,
        'drawer-content-without-footer': !hasFooterSlots,
      }"
    >
      <slot></slot>
    </div>

    <v-footer
      v-if="hasFooterSlots"
      class="drawer-footer d-flex justify-space-between align-center px-6 py-5"
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

    contentPadding: {
      type: String,
      required: false,
      default: "pa-2",
    },

    contentHeaderPadding: {
      type: String,
      required: false,
      default: "px-6",
    },
  },

  data() {
    return {
      localDrawer: this.value,
      expanded: false,
    }
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

    hasFooterSlots() {
      return !!(this.$slots["footer-left"] || this.$slots["footer-right"])
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
$drawer-header-height: 64px;
$drawer-footer-height: 80px;
$drawer-data-table-padding: 9px 25px;

::v-deep .v-navigation-drawer__content {
  overflow-y: hidden;
}
.drawer-header {
  ::v-deep > .v-toolbar__content {
    height: $drawer-header-height !important;
  }
}
.drawer-footer {
  height: $drawer-footer-height;
}
.drawer-content {
  height: calc(100% - #{$drawer-header-height + $drawer-footer-height});
  overflow-y: auto;
}
.drawer-content-without-footer {
  height: calc(100% - #{$drawer-header-height});
}
::v-deep .v-icon.v-icon::after {
  content: none;
}

::v-deep .hux-data-table {
  .v-data-table {
    > .v-data-table__wrapper {
      > table {
        > thead {
          > tr {
            > th {
              background: var(--v-aliceBlue-base) !important;
            }
          }
        }

        > thead > tr > th,
        > tbody > tr > td {
          padding: $drawer-data-table-padding;
        }
      }
    }
  }
}
</style>
