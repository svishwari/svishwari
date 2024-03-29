<template>
  <v-row class="menu-cell-wrapper">
    <v-col
      :class="{ 'pl-9': !showStar }"
      class="d-flex pr-0 align-center"
      style="height: 100%"
    >
      <slot name="expand-icon"></slot>
      <tooltip v-if="!showStar">
        <template #label-content>
          <icon type="lookalike" :size="20" />
        </template>
        <template #hover-content>Lookalike audience</template>
      </tooltip>
      <router-link
        v-if="routePath"
        :to="routePath"
        class="text-decoration-none menu-link"
        append
      >
        <tooltip :nudge-top="nudgeTop">
          <template slot="label-content">
            <span class="primary--text ellipsis menu-value" :class="labelClass">
              {{ value }}
            </span>
          </template>
          <template slot="hover-content">
            {{ value }}
          </template>
        </tooltip>
      </router-link>
      <tooltip v-else>
        <template slot="label-content">
          <span class="ellipsis menu-value" :class="labelClass">
            {{ value }}
          </span>
        </template>
        <template slot="hover-content">
          {{ value }}
        </template>
      </tooltip>
      <v-spacer></v-spacer>
      <div class="d-flex">
        <span class="action-icon font-weight-light menu-activator">
          <v-btn
            v-if="hasFavorite"
            icon
            height="22"
            width="22"
            plain
            class="align-center fav-action"
            :class="{
              'action mr-8': !isFavorite,
              'd-block mr-8': isFavorite,
            }"
            @click="$emit('actionFavorite')"
          >
            <icon v-if="isFavorite" type="fav_filled" :size="18" color="" />
            <icon v-else type="fav_blank" :size="18" color="" />
          </v-btn>
          <v-menu
            v-if="getMenuOptions.length > 0"
            v-model="openMenu"
            class="menu-wrapper"
            bottom
            offset-y
          >
            <template #activator="{ on, attrs }">
              <v-icon
                v-bind="attrs"
                class="mr-2 more-action"
                color="primary"
                :class="{ 'd-inline-block': openMenu }"
                v-on="on"
                @click="takeActions($event)"
              >
                mdi-dots-vertical
              </v-icon>
            </template>
            <v-list class="list-wrapper">
              <v-list-item-group>
                <v-list-item
                  v-for="(item, index) in getMenuOptions"
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
                      <v-list-item
                        v-if="typeof item.menu === Object"
                        :disabled="item.menu.isDisabled"
                        class="white"
                      >
                        <v-list-item-title
                          class="sub-menu-class"
                          @click="item.menu.onClick(data)"
                        >
                          <logo
                            v-if="item.menu.icon"
                            :size="18"
                            :type="item.menu.icon"
                          />
                          <span class="ml-1">{{ item.menu.title }}</span>
                        </v-list-item-title>
                      </v-list-item>
                      <v-list-item
                        v-for="(dataMenu, ind) in item.menu"
                        v-else
                        :key="ind"
                        :disabled="dataMenu.isDisabled"
                        class="white"
                      >
                        <v-list-item-title
                          class="sub-menu-class"
                          @click="dataMenu.onClick(data)"
                        >
                          <logo
                            v-if="dataMenu.icon"
                            :size="18"
                            :type="dataMenu.icon"
                          />
                          <span class="ml-1">{{ dataMenu.title }}</span>
                        </v-list-item-title>
                      </v-list-item>
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
      required: false,
    },
    routeParam: {
      type: String,
      required: false,
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
    showStar: {
      type: Boolean,
      required: false,
      default: true,
    },
    nudgeTop: {
      type: [String, Number],
      required: false,
      default: 0,
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
      return this.routeName && this.routeParam
        ? {
            name: this.routeName,
            params: { id: this.routeParam },
          }
        : null
    },
    getMenuOptions() {
      return this.menuOptions.filter((x) => !x.isHidden)
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
    max-width: 22ch;
    display: inline-block;
    width: 28ch;
    white-space: nowrap;
  }
  .menu-activator {
    .more-action {
      position: absolute;
      top: 0;
      right: 0;
      height: 100%;

      &[aria-expanded="true"] {
        &::after {
          transition: opacity 0.2s cubic-bezier(0.4, 0, 0.6, 1);
          opacity: 0.12;
          border-radius: inherit;
          height: 80%;
          width: 24px;
          margin-top: 6px;
        }
      }
      &:focus {
        &::after {
          border-radius: inherit;
          height: 80%;
          width: 24px;
          margin-top: 6px;
        }
      }
    }
  }
  :hover {
    .action-icon {
      display: block;
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
