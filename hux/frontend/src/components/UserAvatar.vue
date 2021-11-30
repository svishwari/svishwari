<template>
  <v-menu v-model="menu" offset-y close-on-click min-width="192">
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
          <icon type="user_avatar" :size="35" />
        </v-avatar>
        <span class="text-subtitle-1 black--text">{{ initials }}</span>
        <span class="ml-4">
          <icon
            type="chevron-down"
            :size="14"
            class="arrow-icon d-block"
            :class="{ 'menu-active rotate-icon-180': menu }"
          ></icon>
        </span>
      </span>
    </template>
    <v-list min-width="192px">
      <v-list-item class="mb-4">
        <v-avatar class="mr-2" size="45">
          <icon type="user_avatar" :size="45" color="white" />
        </v-avatar>
        <v-list-item-title
          class="black--text font-weight-bold d-flex flex-column"
        >
          <span>{{ firstName }} {{ lastName }}</span>
        </v-list-item-title>
      </v-list-item>
      <v-list-item class="mb-1" data-e2e="change_password">
        <v-list-item-title class="text-body-1 black--text">
          <a
            class="text-decoration-none black--text"
            :href="changeDetailsLink"
            target="_blank"
            data-e2e="profile"
            height="32px"
          >
            My hux profile
          </a>
        </v-list-item-title>
      </v-list-item>
      <v-divider />
      <v-list-item data-e2e="logout" class="mt-2" @click="initiateLogout()">
        <v-list-item-title class="text-body-1 black--text">
          Logout
        </v-list-item-title>
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
    &:hover,
    &.menu-active {
      ::v-deep svg {
        path:first-child {
          fill: var(--v-success-base) !important;
        }
      }
    }
  }
  .arrow-icon {
    fill: var(--v-black-base);
    &:hover,
    &.menu-active {
      fill: var(--v-primary-lighten6);
    }
  }
}
.v-menu__content {
  .user-role {
    font-size: 10px;
    line-height: 13.62px;
    font-weight: normal;
  }
  .v-list-item {
    &:first-child {
      min-height: inherit;
    }
    min-height: 32px;
  }
}
</style>
