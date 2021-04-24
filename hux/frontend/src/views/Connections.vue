<template>
  <div class="connections-wrap grey lighten-5 pt-10 pr-7 pb-7 pl-7">
    <v-row>
      <v-col cols="6" class="d-flex align-end">
        <v-icon> mdi-cloud-download-outline </v-icon>
        <span class="font-weight-light ml-2 mt-1">Data Sources</span>
        <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
      </v-col>

      <v-col cols="6" class="d-flex align-end">
        <v-icon> mdi-map-marker-circle </v-icon>
        <span class="font-weight-light ml-2 mt-1">Destinations</span>
        <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
        <v-spacer></v-spacer>
        <span class="add-icon font-weight-light ml-2 mt-1 float-right">
          View Destinations Details
          <v-icon class="mr-2" color="primary"> mdi-chevron-right </v-icon>
        </span>
      </v-col>

      <v-col cols="6 pt-0">
        <EmptyState>
          <template v-slot:icon> mdi-alert-circle-outline </template>
          <template v-slot:title> Oops! There’s nothing here yet </template>
          <template v-slot:subtitle>
            To create a connection, a data source must be imported!
            <br />
            Begin by selecting the plus button above.
          </template>
        </EmptyState>
      </v-col>

      <v-col cols="6 pt-0">
        <DestinationListCard v-for="item in destinations" :key="item.title">
          <template v-slot:logo>
            <v-img
              class="elevation-6"
              :alt="item.title"
              :src="getImgUrl(item)"
            ></v-img>
          </template>
          <template v-slot:title>
            {{ item.title }}
          </template>
        </DestinationListCard>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import DestinationListCard from "@/components/DestinationListCard"
import EmptyState from "@/components/EmptyState"

export default {
  name: "connections",
  components: { DestinationListCard, EmptyState },
  computed: {
    ...mapGetters({
      destinations: "AllDestinations",
    }),

    // This can be used, in-case, data required logic/filter
    // destinations () {
    //   return this.AllDestinations.map(destination => {
    //     return destination
    //   })
    // },

    hasDestinations() {
      return Boolean(this.destinations && this.destinations.length > 1)
    },
  },
  methods: {
    ...mapActions(["getAllDestinations"]),
    getImgUrl(item) {
      return item.logoUrl
    },
  },
  async mounted() {
    await this.getAllDestinations()
  },
}
</script>
<style lang="scss" scoped>
.connections-wrap {
  .add-icon {
    cursor: pointer;
  }
}
</style>
