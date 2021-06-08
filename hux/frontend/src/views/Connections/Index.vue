<template>
  <page maxWidth="100%">
    <div slot="header">
      <page-header>
        <template slot="left">
          <Breadcrumb :items="breadcrumbs" />
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </div>
    <div v-if="!loading">
      <v-row v-if="isConnectionStarted">
        <v-col cols="6">
          <data-sources-list></data-sources-list>
        </v-col>
        <v-col cols="6">
          <destinations-list></destinations-list>
        </v-col>
      </v-row>
      <div class="empty-state-wrap text-center" v-else>
        <v-icon color="secondary" x-large> mdi-alert-circle-outline </v-icon>
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
            iconPosition="left"
            variant="primary"
            size="small"
            iconSize="small"
            :isTile="true"
            class="ma-2 text-h6 font-weight-regular"
          >
            <template #text>
              <span>Destination</span>
            </template>
          </huxButton>
        </router-link>
        <router-link
          :to="{ name: 'DataSourceConfiguration', query: { select: true } }"
          class="text-decoration-none"
        >
          <huxButton
            ButtonText="Data source"
            icon="mdi-plus"
            iconPosition="left"
            variant="primary"
            size="small"
            :isTile="true"
            class="ma-2 text-h6 font-weight-regular"
          >
            <template #text>
              <span>Data source</span>
            </template>
          </huxButton>
        </router-link>
      </div>
    </div>
    <DataSourceConfiguration v-model="drawer" />
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
  name: "connections",

  components: {
    DataSourcesList,
    DestinationsList,
    Page,
    PageHeader,
    Breadcrumb,
    huxButton,
    DataSourceConfiguration,
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

  watch: {
    $route() {
      if (this.$route.query.select) {
        this.drawer = true
      } else {
        this.drawer = false
      }
    },

    drawer() {
      if (!this.drawer) {
        this.$router.push({ name: "Connections" })
      }
    },
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

  async mounted() {
    this.loading = true
    await this.getDataSources()
    await this.getDestinations()
    this.loading = false

    if (this.$route.query.select) {
      this.drawer = true
    }
  },
}
</script>

<style lang="scss" scoped>
.empty-state-wrap {
  padding-top: 160px;
}
</style>
