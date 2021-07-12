<template>
  <v-row class="menu-cell-wrapper">
    <v-col class="d-flex pr-0">
      <slot name="expand-icon"></slot>
      <router-link :to="routePath" class="text-decoration-none" append>
        <tooltip>
          <template slot="label-content">
            <span class="primary--text ellipsis"> {{ value }} </span>
          </template>
          <template slot="hover-content">
            {{ value }}
          </template>
        </tooltip>
      </router-link>
      <v-spacer></v-spacer>
      <span class="action-icon font-weight-light float-right">
        <v-menu v-model="openMenu" class="menu-wrapper" bottom offset-y>
          <template #activator="{ on, attrs }">
            <v-icon
              v-bind="attrs"
              v-on="on"
              class="mr-2 more-action"
              color="primary"
              @click="takeActions($event)"
            >
              mdi-dots-vertical
            </v-icon>
          </template>
          <v-list class="list-wrapper">
            <v-list-item-group>
              <v-list-item
                v-for="(item, index) in menuOptions"
                :key="index"
                :disabled="item.isDisabled"
              >
                <v-list-item-title v-if="!item.menu">
                  {{ item.title }}
                </v-list-item-title>

                <v-menu
                  v-model="isSubMenuOpen"
                  v-else
                  offset-x
                  nudge-right="16"
                  nudge-top="4"
                >
                  <template #activator="{ on, attrs }">
                    <v-list-item-title v-bind="attrs" v-on="on">
                      {{ item.title }}
                      <v-icon> mdi-chevron-right </v-icon>
                    </v-list-item-title>
                  </template>
                  <template #default>
                    <div
                      class="sub-menu-class white"
                      @click="item.menu.onClick()"
                    >
                      <Logo
                        v-if="item.menu.icon"
                        :size="18"
                        :type="item.menu.icon"
                      />
                      <span class="ml-1">{{ item.menu.title }}</span>
                    </div>
                  </template>
                </v-menu>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>
      </span>
    </v-col>
  </v-row>
</template>
<script>
import Vue from "vue"
import Tooltip from "../Tooltip.vue"
import Logo from "@/components/common/Logo.vue"

export default Vue.extend({
  name: "MenuCell",
  components: {
    Logo,
    Tooltip,
  },

  data() {
    return {
      openMenu: null,
      isSubMenuOpen: null,
    }
  },
  props: {
    navigateTo: {
      type: Object,
      required: false,
    },
    value: {
      type: String,
      required: true,
    },
    menuOptions: {
      type: Array,
      required: false,
      default: () => [],
    },
    routeName: {
      type: String,
      required: true,
    },
    routeParam: {
      type: String,
      required: true,
    },
  },
  computed: {
    routePath() {
      return {
        name: this.routeName,
        params: { id: this.routeParam },
      }
    },
  },
  methods: {
    takeActions(evnt) {
      evnt.preventDefault()
    },
  },

  watch: {
    isSubMenuOpen(newValue) {
      this.openMenu = newValue
    },
  },
})
</script>
<style lang="scss" scoped>
::v-deep.v-menu__content {
  .v-list-item {
    &.theme--light {
      min-height: 32px !important;
    }
  }
}
.menu-cell-wrapper {
  .ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 31ch;
    display: inline-block;
    width: 31ch;
    white-space: nowrap;
  }
  :hover {
    .action-icon {
      display: block;
    }
  }
}
.sub-menu-class {
  display: flex;
  align-items: center;
  padding: 5px 8px;
  min-height: 32px;
  @extend .cursor-pointer;
}
</style>
