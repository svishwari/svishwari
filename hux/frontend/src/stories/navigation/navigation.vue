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
            :class="isMini ? 'pl-7 client py-2 mb-2' : 'pl-4 client py-2 mb-2'"
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
                <span v-if="!isMini" class="ellipsis">{{ client.name }}</span>
              </span>
              <span v-if="!isMini" class="mr-3">
                <icon
                  type="chevron-down"
                  :size="14"
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
        class="list-group black--text mt-2"
      >
        <span v-if="!isMini" class="text-h5 black--text text--lighten-4 pl-4">
          {{ item.name }}
        </span>
      </div>

      <v-list-item
        v-if="!item.children"
        :class="{ 'pl-6 mr-2 mb-1': true, 'collapse-height': isMini }"
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
              <icon
                :type="item.icon"
                :size="iconSize"
                :class="{ 'pl-1 mr-0': true, 'pt-1': isMini }"
              />
            </template>
            <template #hover-content>
              <span class="text-h6 error-base--text">
                {{ item.name }}
              </span>
            </template>
          </tooltip>
        </v-list-item-icon>
        <v-list-item-title class="black--text text-h6">
          {{ item.name }}
        </v-list-item-title>
      </v-list-item>

      <div v-if="item.children">
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
            class="my-3 mr-0"
            :class="{ 'menu-icon': !isMini }"
          >
            <tooltip
              v-if="menu.icon"
              :key="menu.name"
              position-top
              color="black"
            >
              <template #label-content>
                <icon
                  :type="menu.icon"
                  :size="iconSize"
                  :class="{ 'pl-1 mr-0': true, 'pt-1': isMini }"
                />
              </template>
              <template #hover-content>
                <span class="black--text text-h6">
                  {{ menu.name }}
                </span>
              </template>
            </tooltip>
          </v-list-item-icon>
          <v-list-item-title class="black--text text-h6">
            {{ menu.name }}
            <span v-if="menu.superscript" class="title-superscript">
              {{ menu.superscript }}
            </span>
          </v-list-item-title>
        </v-list-item>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import Icon from "@/components/common/Icon"
import Tooltip from "@/components/common/Tooltip"
import Logo from "@/components/common/Logo"

export default {
  name: "SideMenu",

  components: { Icon, Tooltip, Logo },

  props: {
    toggle: Boolean,
    sideBarItems: Array,
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
  }),

  computed: {
    demoConfiguration() {
      return {
        demo_mode: true,
        industry: "Healthcare",
        description: "Pharmaceutical",
        target: "Physicians",
        track: "Sales",
      }
    },

    isMini() {
      return this.$vuetify.breakpoint.smAndDown || this.toggle
    },

    isDemoMode() {
      return this.demoConfiguration?.demo_mode
    },

    iconSize() {
      return this.isMini ? 24 : 16
    },

    displayedMenuItems() {
      return this.sideBarItems
    },
  },
}
</script>

<style lang="scss" scoped>
.side-nav-bar {
  border-right: solid 1px var(--v-black-lighten3);
  @media (min-height: 900px) {
    background-position: bottom 30px center;
  }

  ::v-deep.v-navigation-drawer__content::-webkit-scrollbar {
    display: none;
  }

  .client {
    background-color: rgba(160, 220, 255, 0.25);
    color: var(--v-black-lighten4);
    font-family: Open Sans Light;
  }

  .v-icon {
    transition: none;
  }

  .v-list {
    padding: 0;
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
    border-top: 1px solid rgba(226, 234, 236, 0.5);

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
      top: 30%;
      position: absolute;
    }
  }
  .menu-icon {
    svg {
      top: 32.89%;
    }
  }
}
.mini-home-icon {
  svg {
    top: 8px;
    position: absolute;
  }
}
.nav-footer {
  opacity: 0.8;
  height: 27px;
  margin-top: -35px;
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
</style>
