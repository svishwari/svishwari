<template>
  <div>
    <div class="d-flex align-end mb-4">
      <Icon type="destinations" :size="20" color="neroBlack" />
      <h5 class="text-h4 ml-2 mt-1">Destinations</h5>
      <router-link
        :to="{ name: 'DestinationConfiguration' }"
        class="text-decoration-none"
      >
        <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
      </router-link>
    </div>
    <template v-if="hasAddedDestinations">
      <CardHorizontal
        v-for="destination in addedDestinations"
        :key="destination.id"
        :title="destination.name"
        :icon="destination.type"
        hideButton
        class="mb-3"
      />
    </template>
    <EmptyStateData v-else>
      <template #icon> mdi-alert-circle-outline </template>
      <template #title> Oops! There’s nothing here yet </template>
      <template #subtitle>
        To create a connection, you need to select a destination!
        <br />
        Begin by selecting the plus button above.
      </template>
    </EmptyStateData>
  </div>
</template>

<script>
import { mapGetters } from "vuex"

import CardHorizontal from "@/components/common/CardHorizontal"
import EmptyStateData from "@/components/common/EmptyStateData"
import Icon from "@/components/common/Icon"

export default {
  name: "destinations-list",

  components: {
    CardHorizontal,
    EmptyStateData,
    Icon,
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
}
</script>
