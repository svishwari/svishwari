<template>
  <div>
    <div class="d-flex align-end mb-4">
      <v-icon> mdi-cloud-download-outline </v-icon>
      <h5 class="font-weight-light text-h5 ml-2 mt-1">Data Sources</h5>
      <v-icon @click="toggleDrawer" class="ml-2 add-icon" color="primary">
        mdi-plus-circle
      </v-icon>
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

    <EmptyState v-else>
      <template v-slot:icon> mdi-alert-circle-outline </template>
      <template v-slot:title> Oops! There’s nothing here yet </template>
      <template v-slot:subtitle>
        To create a connection, a data source must be imported!
        <br />
        Begin by selecting the plus button above.
      </template>
    </EmptyState>
    <AddDatasource v-model="drawer" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import EmptyState from "@/components/EmptyState"
import AddDatasource from "@/views/DataSources/Configuration"
import CardHorizontal from "@/components/common/CardHorizontal"
import Status from "@/components/common/Status"

export default {
  name: "data-sources-list",

  components: { EmptyState, AddDatasource, CardHorizontal, Status },

  data() {
    return {
      drawer: false,
    }
  },

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

  methods: {
    toggleDrawer() {
      this.drawer = !this.drawer
    },
    ...mapActions({
      getDataSources: "dataSources/getAll",
    }),
  },

  async mounted() {
    await this.getDataSources()
  },
}
</script>
