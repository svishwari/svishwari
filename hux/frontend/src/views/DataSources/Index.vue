<template>
  <page max-width="100%">
    <div slot="header">
      <span class="header-section">
        <page-header header-height="110" is-sticky>
          <template slot="left">
            <div>
              <breadcrumb :items="breadcrumbs" />
            </div>
            <div class="text-subtitle-1 font-weight-regular mt-1">
              Gain visibility into the customer data that is collected from
              online, offline, and 3rd party channels.
            </div>
          </template>
        </page-header>

        <page-header v-if="isConnectionStarted" header-height="71" is-sticky>
          <template #left>
            <v-btn disabled icon color="black">
              <icon type="search" :size="20" color="black" variant="lighten3" />
            </v-btn>
          </template>

          <template #right>
            <huxButton
              button-text="Request a data source"
              variant="primary"
              size="large"
              is-tile
              height="40"
              class="ma-2 font-weight-regular no-shadow mr-10 caption"
              data-e2e="addDataSource"
              @click="toggleDrawer()"
            >
              Request a data source
            </huxButton>
          </template>
        </page-header>

        <v-progress-linear :active="loading" :indeterminate="loading" />
      </span>
    </div>
    <div v-if="!loading" class="datasource-loaded content-section">
      <v-row v-if="isConnectionStarted" class="ma-0">
        <v-col>
          <data-sources-list
            @onAddDatasource="toggleDrawer()"
          ></data-sources-list>
        </v-col>
      </v-row>
      <hux-empty
        v-if="!isConnectionStarted && !errorState"
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
      <v-row
        v-if="!isConnectionStarted && errorState"
        class="ma-0 white error-row"
      >
        <empty-page type="error-on-screens" :size="50">
          <template #title>
            <div>Data sources are currently unavailable</div>
          </template>
          <template #subtitle>
            <div>
              Our team is working hard to fix it. Please be patient and try
              again soon!
            </div>
          </template>
        </empty-page>
      </v-row>
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
import Icon from "@/components/common/Icon"
import EmptyPage from "@/components/common/EmptyPage"

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
    Icon,
    EmptyPage,
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
      errorState: false,
    }
  },

  computed: {
    ...mapGetters({
      dataSources: "dataSources/list",
    }),

    isConnectionStarted() {
      return this.dataSources.some((each) => each.is_added)
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
      await this.getDataSources()
    } catch (error) {
      this.errorState = true
    } finally {
      this.loading = false
    }

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
    }),
    toggleDrawer() {
      this.drawer = !this.drawer
    },
  },
}
</script>
<style lang="scss" scoped>
.datasource-loaded {
  ::v-deep {
    .error-row {
      margin-top: -70px !important;
      padding-top: 75px !important;
      padding-bottom: 75px !important;
      position: relative;
    }
  }
}
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--v-white-base);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--v-black-lighten3);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--v-black-lighten3);
}
.header-section {
  position: fixed;
  width: 89%;
  z-index: 6 !important;
}
.content-section {
  margin-top: 180px;
}
</style>
