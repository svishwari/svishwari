<template>
  <v-menu v-model="menu" offset-y close-on-click>
    <template #activator="{ on }">
      <span v-on="on" class="d-flex cursor-pointer mr-6">
    <v-btn
      class="mx-2"
      fab
      small
      color="white"
    >
      <v-icon color="secondary">
        mdi-plus
      </v-icon>
    </v-btn>
      </span>
    </template>
    <v-list class="dropdown">
      <v-list-item>
        <v-list-item-title class="add"> 
          Add
        </v-list-item-title>
      </v-list-item>
      <v-list-item v-for="link in dropdownLinks" :key="link" @click="initiateLogout()">
        <v-list-item-title class="text-h6 neroBlack--text"
          >{{link}}</v-list-item-title
        >
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import config from "@/config"
import { mapGetters } from "vuex"

export default {
  name: "HeaderNavigation",
  data() {
    return {
      changeDetailsLink: config.userDetails,
      menu: false,
      dropdownLinks: ['Data Source', 'Destination', 'Audience', 'Engagement']
    }
  },
  methods: {
    initiateLogout() {
      this.$auth.logout()
    },
  },
}
</script>

<style lang="scss">
.v-list-item {
  align-items: center;
    display: flex;
    flex: 1 1 100%;
    letter-spacing: normal;
    min-height: 32px;
    outline: none;
    padding: 0 16px;
    position: relative;
    text-decoration: none;
    width: 170px;
}
.dropdown {
 // background-color: red;
    top: 64px;
    left: 1312px;
}

.v-menu {
 // v-list {
    background-color: red;
 // }
}



::v-deep .v-menu__content .theme--light .v-menu__content--fixed .menuable__content__active {
// background-color: red;
    top: 64px;
    left: 1312px;
}

::v-deep .theme--light.v-sheet {
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25);
}

  ::v-deep .v-menu__content {
.v-list {
//background-color: red;
    top: 64px;
    left: 1312px;
}
  }

   .v-list {
    background-color: red;
  }

  .add {
    font-family: Open Sans;
font-style: normal;
font-weight: 600;
font-size: 14px;
line-height: 19px;
margin-bottom: 10px;
  }
</style>
