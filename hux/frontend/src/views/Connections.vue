<template>
  <div class="connections-wrap grey lighten-5 pt-10 pr-7 pb-7 pl-7">
    <v-row>
      <v-col cols="6" class="d-flex align-end">
          <v-icon> mdi-cloud-download-outline </v-icon>
          <span class="font-weight-light ml-2 mt-1">Data Sources</span>
          <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
      </v-col>
      <v-col cols="6" class="align-end">
          <v-icon> mdi-map-marker-circle </v-icon>
          <span class="font-weight-light ml-2 mt-1">Destinations</span>
          <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
          <span class="font-weight-light ml-2 mt-1 float-right">
            View Destinations Details
            <v-icon class="mr-2" color="primary"> mdi-plus-circle </v-icon>
          </span>
      </v-col>

      <v-col cols="6 pt-0">
        <v-card
          class="text-center pt-16 connection-sources"
          elevation="1"
          tile
          height="340px"
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
      </v-col>
      <v-col cols="6 pt-0">
        <v-card class="mx-auto mb-2" min-height="60" tile>
          <v-card-actions class="">
            <v-list-item class="grow">
              <v-list-item-avatar color="grey darken-3" width="26" height="26" min-width="26">
                <v-img
                  class="elevation-6"
                  alt=""
                  src="../assets/images/adobe-icon.png"
                ></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Adobe Experience</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "connections",
}
</script>

<style lang="scss" scoped>
.connections-wrap {
  .add-icon {
    cursor: pointer;
  }
}
</style>
