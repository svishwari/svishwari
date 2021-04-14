<template>
  <v-app>
      <v-app-bar app color="primary" dark elevation="0">
          <v-app-bar-nav-icon @click.stop="toggleSidebarMenu" class="nav-back-burger">
            <v-icon :class="{'rotate-icon': toggleMini}">mdi-backburger</v-icon>
          </v-app-bar-nav-icon>
          <v-spacer></v-spacer>
          <NavBarMenu></NavBarMenu>
      </v-app-bar>
  </v-app>
</template>

<script>
import NavBarMenu from "@/components/NavBarMenu";

export default {
  name: "NavBar",
  components: { NavBarMenu },
  data: () => ({ 
    toggleMini: false,
  }),
  methods: {
    toggleSidebarMenu() { 
        this.toggleMini = !this.toggleMini;
        this.$emit("toggleSidebarMenu");  
    }
  }
};
</script>

<style lang="scss">
.v-application--wrap {
  .v-toolbar__content {
    background-color: white ;
    border-bottom: 1px solid rgb(208, 208, 206) ;
    color: #FFFFFF ;
  }
}
button.v-app-bar__nav-icon.nav-back-burger {
  margin-left: 30px !important;
}
.v-icon.notranslate.mdi.mdi-backburger.theme--dark {
  &::before {
    color: #232323;
  } 
}
.rotate-icon {
  transition: 0.70s;
  -webkit-transition: 0.70s;
  -moz-transition: 0.70s;
  -ms-transition: 0.70s;
  -o-transition: 0.70s;
  -webkit-transform: rotate(180deg);
  -moz-transform: rotate(180deg);
  -o-transform: rotate(180deg);
  -ms-transform: rotate(180deg);
  transform: rotate(180deg);
}
</style>
