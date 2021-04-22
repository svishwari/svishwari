<template>
  <v-card
    class="text-center pt-16 connection-sources"
    elevation="1"
    tile
    height="340"
    color="#ecf4f9"
  >
    <v-icon color="primary" x-large> mdi-alert-circle-outline </v-icon>
    <v-card-title class="justify-center font-weight-light">
      Oops! There’s nothing here yet
    </v-card-title>
    <v-card-subtitle>
      To create a connection, a data source must be imported!
      <br />
      Begin by selecting the plus button above.
    </v-card-subtitle>
  </v-card>
</template>
<script>
export default {
  name: "EmptyDataSource",
}
</script>
<style lang="scss" scoped></style>
