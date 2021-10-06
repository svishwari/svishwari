<template>
  <v-menu v-model="menu" offset-y close-on-click>
    <template #activator="{ on }">
      <span
        class="d-flex cursor-pointer mr-6"
        data-e2e="profile-dropdown"
        v-on="on"
      >
        <v-btn color="primary" class="font-weight-bold" small outlined fab>
          {{ initials }}
        </v-btn>
        <v-icon color="primary" :class="{ 'rotate-icon-180': menu }">
          mdi-chevron-down
        </v-icon>
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

export default {
  name: "UserAvatar",
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
