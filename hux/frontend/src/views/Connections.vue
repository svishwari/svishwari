<template>
  <div class="connections-wrap grey lighten-5">
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
    </PageHeader>
    <v-row class="pt-10 pr-7 pb-7 pl-7">
      <v-col cols="6" class="d-flex align-end">
        <v-icon> mdi-cloud-download-outline </v-icon>
        <h5 class="font-weight-light text-h5 ml-2 mt-1">Data Sources</h5>
        <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
      </v-col>

      <v-col cols="6" class="d-flex align-end">
        <v-icon> mdi-map-marker-circle </v-icon>
        <h5 class="font-weight-light text-h5 ml-2 mt-1">Destinations</h5>
        <router-link
          :to="{ name: 'add-destination' }"
          class="text-decoration-none"
        >
          <v-icon class="ml-2 add-icon" color="primary">
            mdi-plus-circle
          </v-icon>
        </router-link>
        <v-spacer></v-spacer>
        <router-link
          :to="{ name: 'destinations' }"
          class="text-decoration-none"
        >
          <span
            class="add-icon font-weight-light ml-2 mt-1 float-right primary--text"
          >
            View Destinations Details
            <v-icon class="mr-2" color="primary"> mdi-chevron-right </v-icon>
          </span>
        </router-link>
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
        <EmptyState v-else>
          <template v-slot:icon> mdi-alert-circle-outline </template>
          <template v-slot:title> Oops! There’s nothing here yet </template>
          <template v-slot:subtitle>
            To create a connection, you need to select a destination!
            <br />
            Begin by selecting the plus button above.
          </template>
        </EmptyState>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import DestinationListCard from "@/components/DestinationListCard"
import Logo from "@/components/common/Logo"
import EmptyState from "@/components/EmptyState"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"

export default {
  name: "connections",

  components: { DestinationListCard, EmptyState, PageHeader, Breadcrumb, Logo },

  data() {
    return {
      items: [
        {
          text: "Connections",
          disabled: false,
          href: this.$route.path,
          icon: "mdi-connection",
        },
      ],
    }
  },

  computed: {
    ...mapGetters(["destinations"]),

    addedDestinations() {
      return this.destinations
      // return this.destinations.filter((destination) => destination.is_added)
    },

    hasAddedDestinations() {
      return Boolean(this.addedDestinations && this.addedDestinations.length)
    },
  },

  methods: {
    ...mapActions(["getAllDestinations"]),
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
