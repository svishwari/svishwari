<template>
  <v-navigation-drawer
    app
    floating
    :permanent="true"
    :mini-variant.sync="isMini"
    mini-variant-width="92"
    width="220"
    class="side-nav-bar"
  >
    <template #prepend>
      <logo
        type="logo"
        :size="56"
        :class="isMini ? 'd-flex ma-6 ml-5' : 'd-flex ma-6'"
        data-e2e="click-outside"
      />
      <v-menu v-model="menu" content-class="ml-n3" close-on-click offset-y>
        <template #activator="{ on }">
          <div
            :class="isMini ? 'pl-7 client py-2 mb-2' : 'px-4 client py-2 mb-2'"
            v-on="on"
          >
            <span class="d-flex align-center justify-space-between">
              <span class="d-flex align-center black--text text-h4">
                <div v-if="isDemoMode" :class="isMini ? 'dotMini' : 'dot mr-2'">
                  <logo :type="client.logo" :size="isMini ? 40 : 20" />
                </div>
                <logo
                  v-else
                  :type="client.logo"
                  :size="isMini ? 38 : 24"
                  :class="isMini ? '' : 'ml-1 mr-2'"
                />
                <span v-if="!isMini" class="ellipsis font-weight-regular">
                  {{ client.name }}
                </span>
              </span>
              <span v-if="!isMini" class="mr-0 pa-1">
                <icon
                  type="chevron-down"
                  :size="16"
                  class="arrow-icon d-block"
                  color="black"
                  :class="{ 'menu-active rotate-icon-180': menu }"
                  data-e2e="client_panel_dropdown"
                ></icon>
              </span>
            </span>
          </div>
        </template>
        <v-list-item class="white height-fix" data-e2e="client_panel">
          <v-list-item-title class="body-1">
            <a
              class="text-decoration-none black--text"
              href="/clients"
              height="32px"
              width="220px"
            >
              Switch client project
            </a>
          </v-list-item-title>
        </v-list-item>
      </v-menu>
    </template>

    <v-list
      v-for="item in displayedMenuItems"
      :key="item.name"
      color="var(-v--primary-base)"
    >
      <div
        v-if="item.children && item.children.length > 0"
        class="list-group black--text"
      >
        <span
          v-if="!isMini"
          class="
            text-h5
            black--text
            text--lighten-4
            pl-4
            menu-parent-item
            font-weight-bold
          "
        >
          {{ item.name }}
        </span>
      </div>

      <v-list-item
        v-if="!item.children"
        :class="{ 'pl-6 mr-2 mb-2': true, 'collapse-height pr-8': isMini }"
        :data-e2e="`nav-${item.icon}`"
        :to="item.link"
        @click="navigate(item)"
      >
        <v-list-item-icon
          v-if="item.icon"
          class="ma-0"
          :class="{ 'home-menu-icon ml-0': !isMini, ' mini-home-icon': isMini }"
        >
          <tooltip
            v-if="item.name"
            :key="item.name"
            position-top
            color="black-lighten4"
          >
            <template #label-content>
              <icon :type="item.icon" :size="iconSize" :class="iconClass" />
            </template>
            <template #hover-content>
              <span class="text-h6 error-base--text">
                {{ item.name }}
              </span>
            </template>
          </tooltip>
        </v-list-item-icon>
        <v-list-item-title class="black--text text-h6 pl-1">
          {{ item.name }}
        </v-list-item-title>

        <v-list-item-icon
          v-if="errorAlerts[item.name.toLowerCase().replace(' ', '')]"
          class="ma-0 alignment"
        >
          <status
            status="Critical"
            :show-label="false"
            class="d-flex my-3"
            :icon-size="12"
          />
        </v-list-item-icon>
      </v-list-item>

      <div v-if="item.children" class="mb-2">
        <v-list-item
          v-for="menu in item.children"
          :key="menu.name"
          :class="{ 'pl-6 mr-2 mb-1': true, 'collapse-height': isMini }"
          :data-e2e="`nav-${menu.icon}`"
          :to="menu.link"
          @click="navigate(menu)"
          @mouseover="onMouseOver(menu)"
          @mouseleave="onMouseLeave()"
        >
          <v-list-item-icon
            v-if="menu.icon"
            class="my-1 mr-0"
            :class="{ 'menu-icon': !isMini }"
          >
            <tooltip
              v-if="menu.icon"
              :key="menu.name"
              position-top
              color="black"
            >
              <template #label-content>
                <icon :type="menu.icon" :size="iconSize" :class="iconClass" />
              </template>
              <template #hover-content>
                <span class="black--text text-h6">
                  {{ menu.name }}
                </span>
              </template>
            </tooltip>
          </v-list-item-icon>
          <v-list-item-title class="black--text text-h6 pl-1">
            {{ menu.name }}
            <span v-if="menu.superscript" class="title-superscript">
              {{ menu.superscript }}
            </span>
          </v-list-item-title>
          <v-list-item-icon
            v-if="errorAlerts[menu.name.toLowerCase().replace(' ', '')]"
            class="ma-0 alignment"
          >
            <status
              status="Critical"
              :show-label="false"
              class="d-flex my-3"
              :icon-size="12"
            />
          </v-list-item-icon>
        </v-list-item>
      </div>
    </v-list>

    <template v-if="!isMini" #append>
      <div class="nav-footer text--darken-1 text-body-2 px-4 py-3">
        Hux by Deloitte Digital
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import Icon from "@/components/common/Icon"
import Tooltip from "@/components/common/Tooltip"
import Logo from "@/components/common/Logo"
import * as _ from "lodash"
import { mapGetters, mapActions } from "vuex"
import { formatText } from "@/utils"
import Status from "./common/Status.vue"
import { getAccess } from "../utils"

export default {
  name: "SideMenu",

  components: { Icon, Tooltip, Logo, Status },

  props: {
    toggle: Boolean,
  },

  data: () => ({
    // TODO: integrate with API endpoint for configuring this in the UI
    client: {
      name: "Retail Co",
      logo: "client",
    },
    menu: false,
    prevItem: null,
    isBrodcasterOn: true,
    navigationItems: [],
  }),

  computed: {
    ...mapGetters({
      sideBarItems: "configuration/sideBarConfigs",
      demoConfiguration: "users/getDemoConfiguration",
      seenNotification: "notifications/seenNotifications",
      errorAlerts: "notifications/error_alerts",
      clientAppData: "clients/clientAppData",
    }),

    isMini() {
      return this.$vuetify.breakpoint.smAndDown || this.toggle
    },

    isDemoMode() {
      return this.demoConfiguration?.demo_mode
    },

    iconSize() {
      return this.isMini ? 40 : 24
    },

    iconClass() {
      return this.isMini ? "pt-1 icon-padding pa-1 mr-0" : "pa-1 mr-0"
    },

    displayedMenuItems() {
      return this.navigationItems.filter((x) => {
        if (x.children && x.enabled) {
          x.children = x.children.filter((y) => y.enabled)
          return true
        } else {
          return x.enabled
        }
      })
    },
  },

  async mounted() {
    this.updateClientInfo()
    await this.getSideBarConfig()
    this.trustidRoute(this.$route.name)
    this.navigationItems = this.sideBarItems
  },

  updated() {
    this.getCurrentConfiguration()
  },

  methods: {
    ...mapActions({
      getSideBarConfig: "configuration/getSideBarConfig",
      getClientsAppData: "clients/getClientAppData",
    }),

    navigate(item) {
      this.trustidRoute(item.name)
      if (
        this.prevItem &&
        this.prevItem.defaultState &&
        this.prevItem.link.name != item.link.name
      ) {
        setTimeout(
          this.$store.replaceState({
            ...this.$store.state,
            [this.prevItem.link.name.charAt(0).toLowerCase() +
            this.prevItem.link.name.slice(1)]: _.cloneDeep(
              this.prevItem.defaultState
            ),
          }),
          2000
        )
      }
      this.prevItem = item
    },

    checkColored(title) {
      if (
        this.navigationItems?.length > 0 &&
        ["HX TrustID", "HXTrustID"].includes(title)
      ) {
        this.navigationItems
          .find((elem) => elem.name == "Insights")
          .children.find((item) => item.name == "HX TrustID").icon =
          "hx-trustid-colored"
        return true
      }
      return false
    },

    trustidRoute(title) {
      if (this.navigationItems?.length > 0 && !this.checkColored(title)) {
        this.navigationItems
          .find((elem) => elem.name == "Insights")
          .children.find((item) => item.name == "HX TrustID").icon =
          "hx-trustid"
      }
    },

    onMouseOver(item) {
      if (item) {
        this.checkColored(item.name)
      }
    },
    onMouseLeave() {
      this.trustidRoute(this.$route.name)
    },
    updateClientInfo() {
      if (this.isDemoMode) {
        this.client = {
          name: `${this.demoConfiguration.industry} Co`,
          logo: this.demoConfiguration?.industry.toLowerCase(),
        }
      } else {
        this.client = {
          name: "Retail Co",
          logo: "client",
        }
      }
    },
    async setDemoConfiguration() {
      await this.getSideBarConfig()
      this.navigationItems = []
      this.navigationItems = this.sideBarItems
    },
    async getCurrentConfiguration() {
      if (getAccess("client_config", "client_settings")) {
        if (this.isBrodcasterOn) {
          this.$root.$on("update-config-settings", () => {
            this.setDemoConfiguration()
            this.updateClientInfo()
            this.isBrodcasterOn = false
          })
        }
      } else {
        await this.getClientsAppData()
        this.client = this.clientAppData
      }
    },

    formatText: formatText,
  },
}
</script>

<style lang="scss" scoped>
.side-nav-bar {
  border-right: solid 1px var(--v-black-lighten3);
  @media (min-height: 900px) {
    background-position: bottom 30px center;
  }

  ::v-deep.v-navigation-drawer__content {
    &::-webkit-scrollbar {
      display: none;
    }
    .v-list {
      .list-group {
        .menu-parent-item {
          color: var(--v-black-lighten6) !important;
          text-transform: none !important;
        }
      }
    }
  }

  .client {
    background-color: rgba(160, 220, 255, 0.25);
    color: var(--v-black-lighten4);
    font-family: Open Sans Light;
  }

  .v-icon {
    transition: none;
  }

  .icon-padding {
    padding: 6px !important;
  }

  .v-list {
    padding: 0;
    .list-group {
      border-top: 1px solid rgba(226, 234, 236, 0.5);
    }
  }

  .v-list-item__icon {
    margin-right: 0.5rem;
  }
  .v-list-item {
    border-top-right-radius: 40px;
    border-bottom-right-radius: 40px;
    min-height: 40px;
    max-height: 40px;
    svg {
      fill: var(--v-black-lighten4);
    }
    &:hover {
      svg {
        fill: var(--v-primary-base) !important;
      }
      .v-list-item__title {
        color: var(--v-primary-base) !important;
      }
      &::before {
        opacity: 0;
      }
    }
    &:focus {
      &::before {
        opacity: 0;
      }
    }
  }

  .v-list-item--active {
    background-color: var(--v-primary-lighten1);
    border-left: solid 4px var(--v-primary-base);
    border-top-right-radius: 40px;
    border-bottom-right-radius: 40px;
    padding-left: 20px !important;

    svg {
      fill: var(--v-primary-base) !important;
    }
    .v-list-item__title {
      color: var(--v-primary-base) !important;
    }
    &::before {
      opacity: 0;
    }
  }

  .list-group {
    span {
      text-transform: uppercase;
      min-height: 40px;
      display: flex;
      align-items: center;
    }
  }

  // Apply this css only if icon size is 14 otherwise icon size should be 18
  .home-menu-icon {
    svg {
      top: 20%;
      position: absolute;
    }
  }
  .menu-icon {
    svg {
      top: 20%;
      position: absolute;
    }
  }
}
.mini-home-icon {
  svg {
    top: 5px;
    position: absolute;
  }
}
.nav-footer {
  opacity: 0.8;
  height: 40px;
  padding-top: 10px;
  border-top: 1px solid var(--v-black-lighten1);
  color: var(--v-success-darken1) !important;
}
.v-menu__content {
  @extend .box-shadow-25;
}
.height-fix {
  min-height: 32px;
}
.collapse-height {
  min-height: 52px !important;
  max-height: 52px !important;
}
.title-superscript {
  @extend .superscript;
  font-size: 6px;
  left: -4px;
  top: -8px;
}
.dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--black-lighten2);
  @extend .box-shadow-1;
  background: var(--v-white-base);
  text-align: -webkit-center;
  padding-top: 2px !important;
}
.dotMini {
  @extend .dot;
  width: 40px;
  height: 40px;
}
.ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 12ch;
  display: inline-block;
  width: 28ch;
  white-space: nowrap;
}

.alignment {
  align-self: center;
  position: absolute;
  right: 3px;
}
</style>
