<template>
  <v-app>
    <v-btn icon class="icon-btn">
      <v-avatar>
        <img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="John" />
      </v-avatar>
    </v-btn>
    <div class="vertical-center">
      <p class="font-weight-bold short-name">SH</p>
    </div>
    <v-menu bottom :offset-y="offset" :close-on-content-click="closeOnContentClick">
      <template v-slot:activator="{ on, attrs }">
        <v-icon v-bind="attrs" v-on="on" class="chevron-icon">mdi-chevron-down</v-icon>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title> Profile </v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title> Settings </v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title> Log-out </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app>
</template>

<script>
export default {
  name: "UserAvatar",
  data: () => ({
    offset: true,
    closeOnContentClick: true,
  })
};
</script>
<style lang="scss">
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
</style>
