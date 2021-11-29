<template>
  <v-navigation-drawer
    app
    floating
    :permanent="true"
    :mini-variant.sync="isMini"
    mini-variant-width="90"
    width="220"
    class="side-nav-bar"
  >
    <template #prepend>
      <logo
        type="logo"
        :size="isMini ? 40 : 56"
        class="d-flex ma-6"
        data-e2e="click-outside"
      />
      <v-menu v-if="!isMini" open-on-hover offset-y>
        <template #activator="{ on }">
          <div class="pl-6 client py-4 mb-2" v-on="on">
            <span class="d-flex align-center black--text">
              <logo :type="client.logo" :size="16" class="mr-2" />
              {{ client.name }}
            </span>
          </div>
        </template>
      </v-menu>
    </template>

    <v-list
      v-for="item in displayedMenuItems"
      :key="item.title"
      color="var(-v--primary-base)"
    >
      <div v-if="item.label" class="list-group black--text mt-2">
        <span v-if="!isMini" class="text-h5 black--text text--lighten-4 pl-6">
          {{ item.label }}
        </span>
      </div>

      <v-list-item
        v-if="!item.menu"
        class="pl-6 mr-2"
        :to="item.link"
        :data-e2e="`nav-${item.icon}`"
      >
        <v-list-item-icon
          v-if="item.icon"
          class="ma-2"
          :class="{ 'home-menu-icon': !isMini }"
        >
          <tooltip
            v-if="item.title"
            :key="item.title"
            position-top
            color="black-lighten4"
          >
            <template #label-content>
              <icon :type="item.icon" :size="iconSize" class="mr-0" />
            </template>
            <template #hover-content>
              <span class="text-h6 error-base--text">
                {{ item.title }}
              </span>
            </template>
          </tooltip>
        </v-list-item-icon>
        <v-list-item-title class="black--text text-h6">
          {{ item.title }}
        </v-list-item-title>
      </v-list-item>

      <div v-if="item.menu">
        <v-list-item
          v-for="menu in item.menu"
          :key="menu.title"
          :to="menu.link"
          class="pl-6 mr-2"
          :data-e2e="`nav-${menu.icon}`"
        >
          <v-list-item-icon
            v-if="menu.icon"
            class="my-3 mr-0"
            :class="{ 'menu-icon': !isMini }"
          >
            <tooltip
              v-if="menu.icon"
              :key="menu.title"
              position-top
              color="black"
            >
              <template #label-content>
                <icon :type="menu.icon" :size="iconSize" class="mr-0" />
              </template>
              <template #hover-content>
                <span class="black--text text-h6">
                  {{ menu.title }}
                </span>
              </template>
            </tooltip>
          </v-list-item-icon>
          <v-list-item-title class="black--text text-h6">
            {{ menu.title }}
          </v-list-item-title>
        </v-list-item>
      </div>
    </v-list>

    <template v-if="!isMini" #append>
      <div
        class="
          nav-footer
          primary--text
          text--darken-1 text-body-2
          pl-4
          pr-3
          pb-2
        "
      >
        Hux by Deloitte Digital
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import menuConfig from "@/menuConfig.json"
import Icon from "@/components/common/Icon"
import Tooltip from "@/components/common/Tooltip"
import Logo from "@/components/common/Logo"

export default {
  name: "SideMenu",

  components: { Icon, Tooltip, Logo },

  props: {
    toggle: Boolean,
  },

  data: () => ({
    // TODO: integrate with API endpoint for configuring this in the UI
    client: {
      name: "Client",
      logo: "client",
    },
    items: menuConfig.menu,
  }),

  computed: {
    isMini() {
      return this.$vuetify.breakpoint.smAndDown || this.toggle
    },

    iconSize() {
      return this.isMini ? 21 : 14
    },

    displayedMenuItems() {
      return this.items.filter((x) => {
        if (x.menu && x.display) {
          x.menu = x.menu.filter((y) => y.display)
          return true
        } else {
          return x.display
        }
      })
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

  .client {
    background-color: rgba(160, 220, 255, 0.25);
    color: var(--v-black-lighten4);
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
        fill: var(--v-primary-lighten6) !important;
      }
      .v-list-item__title {
        color: var(--v-primary-lighten6) !important;
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
    border-left: solid 4px var(--v-primary-lighten6);
    border-top-right-radius: 40px;
    border-bottom-right-radius: 40px;
    padding-left: 20px !important;

    svg {
      fill: var(--v-primary-lighten6) !important;
    }
    .v-list-item__title {
      color: var(--v-primary-lighten6) !important;
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
.nav-footer {
  opacity: 0.8;
}
.v-menu__content {
  @extend .box-shadow-25;
}
</style>
