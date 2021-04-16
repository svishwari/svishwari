<template>
  <v-menu offset-y close-on-click max-width="300" tile nudge-bottom="5">
    <template v-slot:activator="{ on }">
      <span v-on="on" class="d-flex avatar-menu">
        <v-btn tile class="main-button" color="#FFFFFF">
          Campaigns
          <v-icon right dark color="#005587"> mdi-chevron-down </v-icon>
        </v-btn>
      </span>
    </template>
    <v-card class="mx-auto">
      <v-list flat min-width="300" max-width="300" tile>
        <v-list-item>
          <v-list-item-title>1 - 10</v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>11 - 25</v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>26 - 50</v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>50+</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
</template>


<script>
export default {
  name: "dropdown-menu",

  props: {
    labelText: {
      type: String,
      required: false,
      default: "Add Account ID",
    },
  },
}
</script>
<style lang="scss" scoped>
</style>