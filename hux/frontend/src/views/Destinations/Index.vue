<template>
  <page max-width="100%">
    <div slot="header">
      <page-header header-height="110">
        <template slot="left">
          <div>
            <breadcrumb :items="breadcrumbs" />
          </div>
          <div class="text-subtitle-1 font-weight-regular mt-1">
            Decide where to route your consumer data to for advertising,
            marketing, reporting, and more.
          </div>
        </template>
      </page-header>
      <page-header v-if="areDestinationsAvailable" header-height="71">
        <template #left>
          <v-btn disabled icon>
            <icon type="search" :size="20" color="black" variant="lighten3" />
          </v-btn>
        </template>

        <template #right>
          <router-link
            v-if="!showError && getAccess('destinations', 'create_one')"
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
      <destinations-list :show-error="showError" />
    </div>
    <data-source-configuration v-model="drawer" />
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import DestinationsList from "./DestinationsList.vue"
import Page from "@/components/Page"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import DataSourceConfiguration from "@/views/DataSources/Configuration"
import Icon from "../../components/common/Icon.vue"
import { getAccess } from "../../utils"

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
      showError: false,
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
      getRole: "users/getCurrentUserRole",
    }),

    areDestinationsAvailable() {
      return this.destinations.some((each) => each.is_added)
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
    try {
      await this.getDestinations()
    } catch (error) {
      this.showError = true
    }
    this.loading = false

    if (this.$route.params.select) {
      this.drawer = true
    }
    //not using
    // this.$root.$on("same-route-Connections", () => {
    //   this.toggleDrawer()
    // })
  },

  methods: {
    ...mapActions({
      getDestinations: "destinations/getAll",
    }),
    // not uisng
    // toggleDrawer() {
    //   this.drawer = !this.drawer
    // },
    getAccess: getAccess,
  },
}
</script>

<style lang="scss" scoped>
.empty-state-wrap {
  padding-top: 160px;
}
</style>
