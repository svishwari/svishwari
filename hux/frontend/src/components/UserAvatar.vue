<template>
  <v-menu offset-y close-on-click>
    <template v-slot:activator="{ on }">
      <span v-on="on" class="d-flex avatar-menu">
        <v-btn icon class="icon-btn">
          <v-avatar>
            <img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="John" />
          </v-avatar>
        </v-btn>
        <div class="vertical-center">
          <p class="font-weight-bold short-name">
           {{ firstName }} {{ lastName }}
          </p>
        </div>
        <v-icon color="black"> mdi-chevron-down </v-icon>
      </span>
    </template>
    <v-list>
      <v-list-item>
        <v-list-item-title>My HUX Profile</v-list-item-title>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>Change Password</v-list-item-title>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>Change Username</v-list-item-title>
      </v-list-item>
      <v-list-item @click="initiateLogout()">
        <v-list-item-title>Logout</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import auth from "@/auth";

export default {
  name: "UserAvatar",
  methods: {
    initiateLogout() {
      auth.logout();
    },
  },
  computed: {
    firstName() {
      return this.$store.getters.getFirstname;
    },
    lastName() {
      return this.$store.getters.getLastName;
    }
  }
};
</script>
<style lang="scss" scoped>
.avatar-menu{
  .vertical-center {
    transform: translateY(20%);
    font-family: Open Sans;
    font-size: 16px;
    font-style: normal;
    font-weight: 600;
    line-height: 22px;
    letter-spacing: 0px;
    text-align: left;
    margin-right: 18px;
  }
  .short-name {
    color: #232323;
    margin-top: 5px;
  }
}
</style>
