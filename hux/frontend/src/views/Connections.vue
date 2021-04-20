<template>
  <div class="grey lighten-5 ml-8 mr-8">
    <v-row>
      <v-col cols="6 pb-0">
        <div>
          <div class="float-left">
            <v-icon> mdi-cloud-download-outline </v-icon>
          </div>
          <p class="font-weight-light float-left ml-2 mt-1">Data Sources</p>
          <v-icon class="ml-2" color="primary"> mdi-plus-circle </v-icon>
        </div>
      </v-col>
      <v-col cols="6">
        <div>
          <div class="float-left">
            <v-icon> mdi-map-marker-circle </v-icon>
          </div>
          <p class="font-weight-light float-left ml-2 mt-1">Destinations</p>
          <v-icon class="ml-2" color="primary"> mdi-plus-circle </v-icon>
          <div class="float-right">
            <p class="font-weight-light float-left ml-2 mt-1">
              View Destinations Details
            </p>
          </div>
        </div>
      </v-col>

      <v-col cols="6 pt-0">
        <v-card
          class="text-center pt-16"
          elevation="1"
          min-width="551px"
          tile
          height="340px"
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
        <v-card class="mx-auto" min-width="550" min-height="60" tile>
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

<style lang="scss" scoped></style>
