<template>
  <div>
    <page-header>
      <template slot="left">
        <breadcrumb :items="breadcrumbs" />
      </template>
    </page-header>
    <v-row class="pa-10" v-if="isSomethingAdded">
      <v-col cols="6">
        <data-sources-list></data-sources-list>
      </v-col>
      <v-col cols="6">
        <destinations-list></destinations-list>
      </v-col>
    </v-row>
    <div class="empty-state-wrap text-center" v-else>
      <v-icon color="secondary" x-large> mdi-alert-circle-outline </v-icon>
      <div class="fs-21 font-weight-light">Oops! There’s nothing here yet</div>
      <div class="font-weight-regular text-h6 my-2">
        To create a connection, you need to add a destination or a data source!
        <br />
        Begin by selecting a button below.
      </div>
      <router-link
        :to="{ name: 'add-destination' }"
        class="text-decoration-none"
      >
        <huxButton
          ButtonText="Destination"
          icon="mdi-plus"
          iconPosition="left"
          variant="primary"
          size="small"
          iconSize="small"
          v-bind:isTile="true"
          class="ma-2 text-h6 font-weight-regular"
        />
      </router-link>
      <huxButton
        ButtonText="Data source"
        icon="mdi-plus"
        iconPosition="left"
        variant="primary"
        size="small"
        v-bind:isTile="true"
        class="ma-2 text-h6 font-weight-regular"
        @click="toggleDrawer"
      />
    </div>
    <AddDataSource v-model="drawer" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import DataSourcesList from "./DataSourcesList"
import DestinationsList from "./DestinationsList"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import AddDataSource from "@/views/DataSources/Configuration"

export default {
  name: "connections",

  components: {
    DataSourcesList,
    DestinationsList,
    PageHeader,
    Breadcrumb,
    huxButton,
    AddDataSource,
  },

  computed: {
    ...mapGetters({
      dataSources: "dataSources/list",
      destinations: "destinations/list",
    }),

    isSomethingAdded() {
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
          icon: "mdi-connection",
        },
      ],
      drawer: false,
    }
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
    await this.getDataSources()
    await this.getDestinations()
  },
}
</script>

<style lang="scss" scoped>
.empty-state-wrap {
  padding-top: 160px;
}
</style>
