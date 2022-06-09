<template>
  <v-navigation-drawer
    v-model="localDrawer"
    right
    :style="transition"
    :width="drawerWidth"
    app
    floating
    hide-overlay
    temporary
  >
    <v-toolbar
      width="100%"
      class="drawer-header no-shadow border-bottom pl-2 pr-2"
      :height="headerHeight"
    >
      <v-toolbar-title class="title-wrap">
        <icon v-if="iconType" :type="iconType" size="38" color="primary" />
        <span class="text-h2">{{ title }}</span>
        <v-spacer></v-spacer>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <slot name="header-right"></slot>
    </v-toolbar>

    <slot name="loading">
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </slot>

    <div
      class="drawer-content"
    >
      <slot></slot>
    </div>

    <v-footer
      class="drawer-footer d-flex justify-space-between align-center px-6 py-4"
      absolute
      color="white"
      elevation="5"
    >
      <div>
        <hux-button
          size="large"
          tile
          variant="secondary"
          class="btn-border box-shadow-none"
          @click="localDrawer = !localDrawer"
        >
          {{ secondaryButtonText }}
        </hux-button>
        <span v-if="footerTextField && primaryButtonText" class="ml-2">{{ footerTextField }}</span>
      </div>
      <div>
        <span v-if="footerTextField && !primaryButtonText">{{ footerTextField }}</span>
        <hux-button
          v-if="primaryButtonText"
          tile
          color="primary"
        >
          {{ primaryButtonText }}
        </hux-button>
      </div>
    </v-footer>
  </v-navigation-drawer>
</template>

<script>
import icon from "../icons/Icon2.vue"
import huxButton from "../huxButton/huxButton2.vue"

export default {
  name: "Drawer",
  components: { icon, huxButton },
  props: {
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
    headerHeight: {
      type: String,
      required: false,
      default: "72",
    },
    title: {
      type: String,
      required: true,
    },
    iconType: {
      type: String,
      required: false,
    },
    secondaryButtonText: {
      type: String,
      required: false,
      default: "Close",
    },
    primaryButtonText: {
      type: String,
      required: false,
    },
    footerTextField: {
      type: String, 
      required: false,
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
$drawer-header-height: 72px;
$drawer-footer-height: 72px;
$drawer-data-table-padding: 9px 25px;

::v-deep .v-navigation-drawer__content {
  overflow-y: hidden;
}
.drawer-header {
  ::v-deep > .v-toolbar__content {
    height: $drawer-header-height !important;
    border-bottom: 1px solid var(--v-black-lighten3);
  }
}
.drawer-footer {
  height: $drawer-footer-height;
  box-shadow: none !important;
  border-top: 1px solid var(--v-black-lighten3) !important;
}
.drawer-content {
  height: calc(100% - #{$drawer-header-height + $drawer-footer-height});
  overflow-y: auto;
  border-bottom: 1px solid var(--v-black-lighten3) !important;
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
              background: var(--v-primary-lighten2) !important;
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
.title-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
