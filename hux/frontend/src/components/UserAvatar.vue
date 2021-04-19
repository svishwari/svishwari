<template>
  <v-menu offset-y close-on-click>
    <template v-slot:activator="{ on }">
      <span v-on="on" class="d-flex">
        <v-avatar color="primary" class="font-weight-bold">
          {{ firstName[0] }}{{ lastName[0] }}
        </v-avatar>
        <v-icon color="black"> mdi-chevron-down </v-icon>
      </span>
    </template>
    <v-list>
      <v-list-item class="font-weight-bold">
        <v-avatar color="primary" class="font-weight-bold white--text mr-2">
          {{ firstName[0] }}{{ lastName[0] }}
        </v-avatar>
        <v-list-item-title>{{ firstName }} {{ lastName }}</v-list-item-title>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>
          <a
            class="text-decoration-none text--primary"
            href="https://deloittedigital-ms.okta.com/enduser/settings"
            target="_blank"
            >My HUX Profile</a
          >
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

export default {
  name: "UserAvatar",
  methods: {
    initiateLogout() {
      auth.logout()
    },
  },
  computed: {
    firstName() {
      return this.$store.getters.getFirstname
    },
    lastName() {
      return this.$store.getters.getLastName
    },
  },
}
</script>
