<template>
  <div class="container-fluid">
    <v-app>
      <NavBar @toggleSidebarMenu="toggleSidebar"></NavBar>
      <SideMenu v-bind:toggle="toggleMini"></SideMenu>
      <v-main>
        <v-container>
          <slot />
        </v-container>
      </v-main>
    </v-app>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar";
import SideMenu from "@/components/SideMenu";

export default {
  name: "app-layout",
  components: { SideMenu, NavBar },
   data: () => ({ 
     toggleMini: false
   }),
  methods: {
    toggleSidebar() {
      this.toggleMini = !this.toggleMini;
    }
  }
};
</script>
