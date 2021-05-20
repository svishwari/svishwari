<template>
  <div>
    <div class="d-flex align-end mb-4">
      <v-icon> mdi-cloud-download-outline </v-icon>
      <h5 class="text-h4 ml-2 mt-1">Data Sources</h5>
      <router-link
        :to="{
          name: 'DataSourceConfiguration',
          query: { select: true },
        }"
        class="text-decoration-none"
      >
        <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
      </router-link>
    </div>

    <template v-if="hasAddedDatasources">
      <CardHorizontal
        v-for="dataSource in addedDataSources"
        :key="dataSource.id"
        :title="dataSource.name"
        :icon="dataSource.type"
        hideButton
        class="mb-3"
      >
        <Status :status="dataSource.status" />
      </CardHorizontal>
    </template>

    <EmptyStateData v-else>
      <template v-slot:icon> mdi-alert-circle-outline </template>
      <template v-slot:title> Oops! There’s nothing here yet </template>
      <template v-slot:subtitle>
        To create a connection, a data source must be imported!
        <br />
        Begin by selecting the plus button above.
      </template>
    </EmptyStateData>
  </div>
</template>

<script>
import { mapGetters } from "vuex"

import CardHorizontal from "@/components/common/CardHorizontal"
import Status from "@/components/common/Status"
import EmptyStateData from "@/components/common/EmptyStateData"

export default {
  name: "data-sources-list",

  components: { EmptyStateData, CardHorizontal, Status },

  computed: {
    ...mapGetters({
      dataSources: "dataSources/list",
    }),

    addedDataSources() {
      return this.dataSources.filter((dataSource) => dataSource.is_added)
    },

    hasAddedDatasources() {
      return Boolean(this.addedDataSources && this.addedDataSources.length)
    },
  },
}
</script>
