<template>
  <page max-width="100%">
    <div slot="header">
      <page-header>
        <template slot="left">
          <breadcrumb :items="breadcrumbs" />
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </div>
    <div v-if="!loading">
      <v-row v-if="isConnectionStarted">
        <v-col cols="6">
          <data-sources-list
            @onAddDatasource="toggleDrawer()"
          ></data-sources-list>
        </v-col>
        <v-col cols="6">
          <destinations-list></destinations-list>
        </v-col>
      </v-row>
      <div v-else class="empty-state-wrap text-center">
        <v-icon color="primary lighten-8" x-large>
          mdi-alert-circle-outline
        </v-icon>
        <div class="text-h3">Oops! There’s nothing here yet</div>
        <div class="font-weight-regular text-h6 my-2">
          To create a connection, you need to add a destination or a data
          source!
          <br />
          Begin by selecting a button below.
        </div>
        <router-link
          :to="{ name: 'DestinationConfiguration' }"
          class="text-decoration-none"
        >
          <huxButton
            icon="mdi-plus"
            icon-position="left"
            variant="primary"
            size="small"
            icon-size="small"
            :is-tile="true"
            class="ma-2 text-h6 font-weight-regular"
          >
            Destination
          </huxButton>
        </router-link>
        <router-link
          :to="{ name: 'Connections', params: { select: true } }"
          class="text-decoration-none"
        >
          <huxButton
            button-text="Data source"
            icon="mdi-plus"
            icon-position="left"
            variant="primary"
            size="small"
            :is-tile="true"
            class="ma-2 text-h6 font-weight-regular"
          >
            Data source
          </huxButton>
        </router-link>
      </div>
    </div>
    <data-source-configuration v-model="drawer" />
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import DataSourcesList from "./DataSourcesList"
import DestinationsList from "./DestinationsList"
import Page from "@/components/Page"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import DataSourceConfiguration from "@/views/DataSources/Configuration"

export default {
  name: "Connections",

  components: {
    DataSourcesList,
    DestinationsList,
    Page,
    PageHeader,
    Breadcrumb,
    huxButton,
    DataSourceConfiguration,
  },

  data() {
    return {
      breadcrumbs: [
        {
          text: "Connections",
          icon: "connections",
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

    this.$root.$on("same-route-Connections", () => {
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

<style lang="scss" scoped>
.empty-state-wrap {
  padding-top: 160px;
}
</style>
