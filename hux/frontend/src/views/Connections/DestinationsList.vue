<template>
  <div>
    <div class="d-flex align-end mb-4">
      <v-icon> mdi-map-marker-circle </v-icon>
      <h5 class="font-weight-light text-h5 ml-2 mt-1">Destinations</h5>
      <router-link
        :to="{ name: 'add-destination' }"
        class="text-decoration-none"
      >
        <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
      </router-link>
    </div>
    <template v-if="hasAddedDestinations">
      <DestinationListCard
        v-for="destination in addedDestinations"
        :key="destination.id"
      >
        <template v-slot:logo>
          <Logo :type="destination.type" />
        </template>
        <template v-slot:title>
          {{ destination.name }}
        </template>
      </DestinationListCard>
    </template>
    <EmptyStateData v-else>
      <template v-slot:icon> mdi-alert-circle-outline </template>
      <template v-slot:title> Oops! There’s nothing here yet </template>
      <template v-slot:subtitle>
        To create a connection, you need to select a destination!
        <br />
        Begin by selecting the plus button above.
      </template>
    </EmptyStateData>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import DestinationListCard from "@/components/DestinationListCard"
import Logo from "@/components/common/Logo"
import EmptyStateData from "@/components/common/EmptyStateData"

export default {
  name: "destinations-list",

  components: {
    DestinationListCard,
    EmptyStateData,
    Logo,
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
    }),

    addedDestinations() {
      return this.destinations.filter((destination) => destination.is_added)
    },

    hasAddedDestinations() {
      return Boolean(this.addedDestinations && this.addedDestinations.length)
    },
  },

  methods: {
    ...mapActions({
      getDestinations: "destinations/getAll",
    }),
  },

  async mounted() {
    await this.getDestinations()
  },
}
</script>
