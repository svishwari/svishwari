<template>
  <page max-width="100%">
    <div slot="header">
      <page-header header-height="110" class="mt-n2">
        <template slot="left">
          <div>
            <breadcrumb :items="breadcrumbs" />
          </div>
          <div class="text-subtitle-1 font-weight-regular mt-1">
            Decide where your valuable data should go for optimum results.
          </div>
        </template>
      </page-header>
      <page-header header-height="71">
        <template #left>
          <v-btn disabled icon>
            <icon type="search" size="20" color="black" variant="lighten3" />
          </v-btn>
        </template>

        <template #right>
          <router-link
            :to="{ name: 'DestinationConfiguration' }"
            class="text-decoration-none"
            data-e2e="addDestination"
          >
            <huxButton
              button-text="Add a destination"
              variant="primary"
              size="large"
              is-tile
              height="40"
              class="ma-2 font-weight-regular no-shadow mr-0 caption"
            >
              Add a destination
            </huxButton>
          </router-link>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </div>
    <div v-if="!loading">
      <v-row v-if="isConnectionStarted">
        <v-col>
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
      </div>
    </div>
    <data-source-configuration v-model="drawer" />
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import DestinationsList from "./DestinationsList"
import Page from "@/components/Page"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import DataSourceConfiguration from "@/views/DataSources/Configuration"
import Icon from "../../components/common/Icon.vue"

export default {
  name: "Destinations",

  components: {
    DestinationsList,
    Page,
    PageHeader,
    Breadcrumb,
    huxButton,
    DataSourceConfiguration,
    Icon,
  },

  data() {
    return {
      breadcrumbs: [
        {
          text: "Destinations",
          icon: "destinations",
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
