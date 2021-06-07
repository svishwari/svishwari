<template>
  <v-navigation-drawer
    app
    floating
    :permanent="true"
    :mini-variant.sync="isMini"
    mini-variant-width="90"
    width="220"
    class="side-nav-bar primary"
  >
    <template v-slot:prepend>
      <img
        src="@/assets/images/logo.png"
        alt="Hux"
        width="55"
        height="55"
        class="d-flex ma-4"
      />
      <v-menu open-on-hover offset-y>
        <template v-slot:activator="{ on }">
          <div v-on="on" class="client">
            <span>
              {{ clientName }}
            </span>
            <v-icon v-if="!isMini" color="rgba(255, 255, 255, 0.5)">
              mdi-chevron-down
            </v-icon>
          </div>
        </template>
        <template v-slot:default>
          <div class="px-6 py-5 white">
            <v-icon color="primary"> mdi-information </v-icon>
            <span class="pl-4 text-caption neroBlack--text">
              This is where your future client accounts will be held.
            </span>
          </div>
        </template>
      </v-menu>
    </template>

    <v-list
      v-for="item in items"
      :key="item.title"
      color="rgba(0, 85, 135, 0.9)"
    >
      <div class="list-group" v-if="item.label">
        <span v-if="!isMini">
          {{ item.label }}
        </span>
      </div>

      <v-list-item class="my-2" v-if="!item.menu" :to="item.link">
        <v-list-item-icon class="my-3" v-if="item.icon">
          <Icon :type="item.icon" :size="iconSize" color="white" />
        </v-list-item-icon>
        <v-list-item-title class="white--text">
          {{ item.title }}
        </v-list-item-title>
      </v-list-item>

      <div v-if="item.menu" class="pb-2">
        <v-list-item
          v-for="menu in item.menu"
          :key="menu.title"
          :to="menu.link"
        >
          <v-list-item-icon class="my-3" v-if="menu.icon">
            <Icon :type="menu.icon" :size="iconSize" color="white" />
          </v-list-item-icon>
          <v-list-item-title class="white--text">
            {{ menu.title }}
          </v-list-item-title>
        </v-list-item>
      </div>
    </v-list>

    <template v-slot:append v-if="!isMini">
      <div class="nav-footer">Hux by Deloitte Digital</div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import menuConfig from "@/menuConfig.json"
import Icon from "@/components/common/Icon"

export default {
  name: "SideMenu",

  components: { Icon },

  props: {
    toggle: Boolean,
  },

  computed: {
    isMini() {
      return this.$vuetify.breakpoint.smAndDown || this.toggle
    },

    iconSize() {
      return this.isMini ? 24 : 21
    },
  },

  data: () => ({
    clientName: "Pendleton",
    items: menuConfig.menu,
  }),
}
</script>

<style lang="scss" scoped>
.side-nav-bar {
  @media (min-height: 900px) {
    // background-image: url("../assets/images/nav-bg.png");
    background-position: bottom 30px center;
  }

  .client {
    align-items: center;
    background-color: rgba(0, 0, 0, 0.25);
    color: var(--v-white-base);
    cursor: default;
    display: flex;
    font-size: 0.93rem;
    line-height: 1.75rem;
    font-weight: normal;
    justify-content: space-between;
    padding: 0.8rem 1.78rem;
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

  .v-list-item__title {
    font-size: 0.93rem;
    font-weight: normal;
  }

  .v-list-item--active {
    &::before {
      background-color: var(--v-white-base);
      opacity: 0.1;
    }
  }

  .list-group {
    border-top: 1px solid rgba(255, 255, 255, 0.25);

    span {
      color: var(--v-white-base);
      display: flex;
      font-size: 0.93rem;
      font-weight: normal;
      opacity: 0.5;
      padding: 0.75rem 1rem;
      text-transform: uppercase;
    }
  }

  .nav-footer {
    color: var(--v-white-base);
    font-size: 12px;
    font-weight: normal;
    opacity: 0.5;
    padding: 1rem;
  }
}
.v-menu__content {
  @extend .box-shadow-25;
}
</style>
