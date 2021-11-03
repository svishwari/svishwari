<template>
  <page max-width="100%">
    <div slot="header">
      <page-header header-height="110" class="mt-n2">
        <template slot="left">
          <div>
            <breadcrumb :items="breadcrumbs" />
          </div>
          <div class="text-subtitle-1 font-weight-regular mt-1">
            Insights into the consumer data that is collected from both online,
            offline, and 3rd party channels.
          </div>
        </template>
      </page-header>

      <page-header v-if="isConnectionStarted" header-height="71">
        <template #left>
          <v-btn disabled icon color="black">
            <v-icon medium>mdi-magnify</v-icon>
          </v-btn>
        </template>

        <template #right>
          <huxButton
            button-text="Request a data source"
            variant="primary"
            size="large"
            is-tile
            height="40"
            class="ma-2 font-weight-regular no-shadow mr-0 caption"
            data-e2e="addDataSource"
            @click="toggleDrawer()"
          >
            Request a data source
          </huxButton>
        </template>
      </page-header>

      <v-progress-linear :active="loading" :indeterminate="loading" />
    </div>
    <div v-if="!loading">
      <v-row v-if="isConnectionStarted">
        <v-col>
          <data-sources-list
            @onAddDatasource="toggleDrawer()"
          ></data-sources-list>
        </v-col>
      </v-row>
      <hux-empty
        v-else
        icon-type="destinations-null"
        :icon-size="50"
        title="No data sources to show"
        subtitle="The list of data sources will appear here once they have been added."
      >
        <template #button>
          <hux-button
            variant="primary"
            is-tile
            width="224"
            height="40"
            class="text-button my-4"
            @click="toggleDrawer()"
          >
            Request a data sources
          </hux-button>
        </template>
      </hux-empty>
    </div>
    <data-source-configuration v-model="drawer" />
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import DataSourcesList from "./DataSourcesList"
import Page from "@/components/Page"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxEmpty from "@/components/common/screens/Empty"
import DataSourceConfiguration from "@/views/DataSources/Configuration"

export default {
  name: "DataSources",

  components: {
    DataSourcesList,
    Page,
    PageHeader,
    Breadcrumb,
    huxButton,
    DataSourceConfiguration,
    HuxEmpty,
  },

  data() {
    return {
      breadcrumbs: [
        {
          text: "Data Sources",
          icon: "data-source",
        },
      ],
      drawer: false,
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      dataSources: "dataSources/list",
      destinations: "destinations/list",
    }),

    isConnectionStarted() {
      const availableDataSources = this.dataSources.filter(
        (each) => each.is_added
      )
      const availableDestinations = this.destinations.filter(
        (each) => each.is_added
      )
      return availableDataSources.length > 0 || availableDestinations.length > 0
    },
  },

  watch: {
    $route() {
      if (this.$route.params.select) {
        this.drawer = true
      } else {
        this.drawer = false
      }
    },
  },

  async mounted() {
    this.loading = true
    await this.getDataSources()
    await this.getDestinations()
    this.loading = false

    if (this.$route.params.select) {
      this.drawer = true
    }

    this.$root.$on("same-route-DataSources", () => {
      this.toggleDrawer()
    })
  },

  methods: {
    ...mapActions({
      getDataSources: "dataSources/getAll",
      getDestinations: "destinations/getAll",
    }),
    toggleDrawer() {
      this.drawer = !this.drawer
    },
  },
}
</script>
<style lang="scss" scoped></style>
