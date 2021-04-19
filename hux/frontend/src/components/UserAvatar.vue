<template>
  <v-menu offset-y close-on-click>
    <template v-slot:activator="{ on }">
      <span v-on="on" class="d-flex">
        <v-avatar color="primary" class="font-weight-bold">
          {{ initials }}
        </v-avatar>
        <v-icon color="black"> mdi-chevron-down </v-icon>
      </span>
    </template>
    <v-list>
      <v-list-item class="font-weight-bold">
        <v-avatar color="primary" class="font-weight-bold white--text mr-2">
          {{ initials }}
        </v-avatar>
        <v-list-item-title>{{ firstName }} {{ lastName }}</v-list-item-title>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>
          <a
            class="text-decoration-none text--primary"
            :href="changeDetailsLink"
            target="_blank"
            >My Hux Profile</a>
        </v-list-item-title>
      </v-list-item>
      <v-divider />
      <v-list-item @click="initiateLogout()">
        <v-list-item-title>Logout</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import auth from "@/auth"
import config from "@/config"

export default {
  name: "UserAvatar",
  data() {
    return {
      firstName: this.$store.getters.getFirstname,
      lastName: this.$store.getters.getLastName,
      changeDetailsLink: config.userDetails,
    }
  },
  methods: {
    initiateLogout() {
      auth.logout()
    },
  },
  computed: {
    initials() {
      return this.firstName[0] + this.lastName[0]
    },
  },
}
</script>
