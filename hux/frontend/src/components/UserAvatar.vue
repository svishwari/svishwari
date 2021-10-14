<template>
  <v-menu v-model="menu" offset-y close-on-click>
    <template #activator="{ on }">
      <span
        class="d-flex cursor-pointer mr-6 d-flex align-center user-avatar"
        data-e2e="profile-dropdown"
        v-on="on"
      >
        <v-avatar
          class="mr-2"
          size="35"
          color="white"
          :class="{ 'menu-active': menu }"
        >
        </v-avatar>
        <span class="text--subtitle-1 black--text">{{ initials }}</span>
        <span class="ml-4">
          <icon
            type="chevron-down"
            :size="14"
            class="arrow-icon d-block"
            :class="{ 'menu-active': menu }"
          ></icon>
        </span>
      </span>
    </template>
    <v-list>
      <v-list-item class="font-weight-bold">
        <v-btn color="primary" class="font-weight-bold mr-2" small outlined fab>
          {{ initials }}
        </v-btn>
        <v-list-item-title
          class="text-h6 black--text text--darken-4 font-weight-bold"
          >{{ firstName }} {{ lastName }}</v-list-item-title
        >
      </v-list-item>
      <v-list-item>
        <v-list-item-title>
          <a
            class="text-decoration-none text-h6 black--text text--darken-4"
            :href="changeDetailsLink"
            target="_blank"
            data-e2e="profile"
            >My Hux Profile</a
          >
        </v-list-item-title>
      </v-list-item>
      <v-divider />
      <v-list-item data-e2e="logout" @click="initiateLogout()">
        <v-list-item-title class="text-h6 black--text text--darken-4"
          >Logout</v-list-item-title
        >
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import config from "@/config"
import { mapGetters } from "vuex"
import Icon from "./common/Icon.vue"

export default {
  name: "UserAvatar",
  components: { Icon },
  data() {
    return {
      changeDetailsLink: config.userDetails,
      menu: false,
    }
  },

  computed: {
    ...mapGetters({
      firstName: "users/getFirstname",
      lastName: "users/getLastName",
    }),
    initials() {
      return this.firstName[0] + this.lastName[0]
    },
  },
  methods: {
    initiateLogout() {
      this.$auth.logout()
    },
  },
}
</script>
<style lang="scss" scoped>
.user-avatar {
  .v-avatar {
    border: solid 1px var(--v-primary-base) !important;
    &:hover,
    &.menu-active {
      border: solid 2px var(--v-success-base) !important;
    }
  }
  .arrow-icon {
    fill: var(--v-black-lighten4);
    &:hover,
    &.menu-active {
      fill: var(--v-primary-base);
    }
  }
}
</style>
