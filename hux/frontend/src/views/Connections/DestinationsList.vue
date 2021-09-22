<template>
  <div class="list-wrapper">
    <div class="d-flex align-end mb-4">
      <icon type="destinations" :size="20" color="black-darken4" />
      <h5 class="text-h4 ml-2 mt-1">Destinations</h5>
      <router-link
        :to="{ name: 'DestinationConfiguration' }"
        class="text-decoration-none"
      >
        <icon class="add-icon cursor-pointer" type="add" :size="27" />
      </router-link>
    </div>
    <template v-if="hasAddedDestinations">
      <card-horizontal
        v-for="destination in addedDestinations"
        :key="destination.id"
        :title="destination.name"
        :icon="destination.type"
        hide-button
        data-e2e="destinationsList"
        class="mb-3 list"
      />
    </template>
    <empty-state-data v-else>
      <template #icon> mdi-alert-circle-outline </template>
      <template #title> Oops! There’s nothing here yet </template>
      <template #subtitle>
        To create a connection, you need to select a destination!
        <br />
        Begin by selecting the plus button above.
      </template>
    </empty-state-data>
  </div>
</template>

<script>
import { mapGetters } from "vuex"

import CardHorizontal from "@/components/common/CardHorizontal"
import EmptyStateData from "@/components/common/EmptyStateData"
import Icon from "@/components/common/Icon"

export default {
  name: "DestinationsList",

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
<style lang="scss" scoped>
.list-wrapper {
  .add-icon {
    display: block;
    margin-left: 7px;
    position: relative;
    top: 3px;
  }
  .list {
    &:hover {
      cursor: auto;
    }
  }
}
</style>
