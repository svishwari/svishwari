<template>
  <v-row class="menu-cell-wrapper">
    <v-col class="d-flex pr-0">
      <slot name="expand-icon"></slot>
      <router-link
        :to="routePath"
        class="text-decoration-none menu-link"
        append
      >
        <tooltip>
          <template slot="label-content">
            <span class="primary--text ellipsis" :class="labelClass">
              {{ value }}
            </span>
          </template>
          <template slot="hover-content">
            {{ value }}
          </template>
        </tooltip>
      </router-link>
      <v-spacer></v-spacer>
      <div class="d-flex align-center">
        <v-btn
          v-if="hasFavorite"
          icon
          height="22"
          width="22"
          plain
          class="align-center"
          :class="{ 'action-icon': !isFavorite, 'mr-3 fixed-icon': isFavorite }"
          @click="$emit('actionFavorite')"
        >
          <icon v-if="isFavorite" type="fav_filled" :size="18" color="" />
          <icon v-else type="fav_blank" :size="18" color="" />
        </v-btn>
        <span class="action-icon font-weight-light float-right">
          <v-menu v-model="openMenu" class="menu-wrapper" bottom offset-y>
            <template #activator="{ on, attrs }">
              <v-icon
                v-bind="attrs"
                class="mr-2 more-action"
                color="primary"
                v-on="on"
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
                  <v-list-item-title
                    v-if="!item.menu"
                    @click="item.onClick && item.onClick(data)"
                  >
                    {{ item.title }}
                  </v-list-item-title>

                  <v-menu
                    v-else
                    v-model="isSubMenuOpen"
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
                        @click="item.menu.onClick(data)"
                      >
                        <logo
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
      </div>
    </v-col>
  </v-row>
</template>
<script>
import Vue from "vue"
import Tooltip from "../Tooltip.vue"
import Logo from "@/components/common/Logo.vue"
import Icon from "../Icon.vue"

export default Vue.extend({
  name: "MenuCell",
  components: {
    Logo,
    Tooltip,
    Icon,
  },

  props: {
    navigateTo: {
      type: Object,
      required: false,
    },
    value: {
      type: String,
      required: true,
      default: () => "",
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
    data: {
      type: Object,
      required: false,
    },
    labelClass: {
      type: [String, Object],
      required: false,
      default: "",
    },
    isFavorite: {
      type: Boolean,
      required: false,
      default: false,
    },
    hasFavorite: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      openMenu: null,
      isSubMenuOpen: null,
    }
  },
  computed: {
    routePath() {
      return {
        name: this.routeName,
        params: { id: this.routeParam },
      }
    },
  },

  watch: {
    isSubMenuOpen(newValue) {
      this.openMenu = newValue
    },
  },
  methods: {
    takeActions(evnt) {
      evnt.preventDefault()
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
    max-width: 28ch;
    display: inline-block;
    width: 28ch;
    white-space: nowrap;
  }
  :hover {
    .action-icon {
      display: block;
    }
    .fixed-icon {
      margin-right: 0px !important;
    }
  }
  .menu-link {
    position: absolute;
    margin-left: 24px;
    margin-top: 1px;
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
