<template>
  <v-menu v-model="menu" offset-y close-on-click>
    <template v-slot:activator="{ on }">
      <span v-on="on" class="d-flex cursor-pointer mr-6">
        <v-btn color="primary" class="font-weight-bold" small outlined fab>
          {{ initials }}
        </v-btn>
        <v-icon color="primary" :class="{ 'rotate-icon': menu }">
          mdi-chevron-down
        </v-icon>
      </span>
    </template>
    <v-list>
      <v-list-item class="font-weight-bold">
        <v-btn color="primary" class="font-weight-bold mr-2" small outlined fab>
          {{ initials }}
        </v-btn>
        <v-list-item-title class="text-h6 neroBlack--text font-weight-bold"
          >{{ firstName }} {{ lastName }}</v-list-item-title
        >
      </v-list-item>
      <v-list-item>
        <v-list-item-title>
          <a
            class="text-decoration-none text-h6 neroBlack--text"
            :href="changeDetailsLink"
            target="_blank"
            >My Hux Profile</a
          >
        </v-list-item-title>
      </v-list-item>
      <v-divider />
      <v-list-item @click="initiateLogout()">
        <v-list-item-title class="text-h6 neroBlack--text"
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
  methods: {
    initiateLogout() {
      this.$auth.logout()
    },
  },
  computed: {
    ...mapGetters({
      firstName: "getFirstname",
      lastName: "getLastName",
    }),
    initials() {
      return this.firstName[0] + this.lastName[0]
    },
  },
}
</script>

<style lang="scss" scoped>
.rotate-icon {
  transition: 0.7s;
  -webkit-transition: 0.7s;
  -moz-transition: 0.7s;
  -ms-transition: 0.7s;
  -o-transition: 0.7s;
  -webkit-transform: rotate(180deg);
  -moz-transform: rotate(180deg);
  -o-transform: rotate(180deg);
  -ms-transform: rotate(180deg);
  transform: rotate(180deg);
}
</style>
