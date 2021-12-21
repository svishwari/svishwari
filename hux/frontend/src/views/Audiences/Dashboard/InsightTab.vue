<template>
  <div class="insight-tab">
    <v-row>
      <v-col md="6">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
          <v-card-title class="pb-2 pl-6 pt-5">
            <h3 class="text-h3">Audience Size</h3>
            <span class="text-body-1 time-frame">
              &nbsp;({{ timeFrameLabel }})
            </span>
          </v-card-title>
          <v-progress-linear
            v-if="loadingAudienceChart"
            :active="loadingAudienceChart"
            :indeterminate="loadingAudienceChart"
          />
          <total-customer-chart
            v-if="!loadingAudienceChart"
            :customers-data="totalCustomers"
            data-e2e="total-audience-chart"
          />
        </v-card>
      </v-col>
      <v-col md="6">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
          <v-card-title class="pb-2 pl-6 pt-5">
            <h3 class="text-h3">Total audience spend</h3>
            <tooltip position-top>
              <template #label-content>
                <icon
                  type="info"
                  :size="8"
                  class="mb-1 ml-1"
                  color="primary"
                  variant="base"
                />
              </template>
              <template #hover-content>
                Total order value for all customers (known and anyonymous) over
                time.
              </template>
            </tooltip>
            <span class="text-body-1 time-frame">
              &nbsp;({{ timeFrameLabel }})
            </span>
          </v-card-title>
          <v-progress-linear
            v-if="loadingSpendChart"
            :active="loadingSpendChart"
            :indeterminate="loadingSpendChart"
          />
          <total-customer-spend-chart
            v-if="!loadingSpendChart"
            :customer-spend-data="totalCustomerSpend"
            data-e2e="audience-spend-chart"
          />
        </v-card>
      </v-col>
    </v-row>
    <v-row class="mt-2 mb-4">
      <v-col md="12">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="395">
          <v-row>
            <v-progress-linear
              v-if="loadingDemographics"
              :active="loadingDemographics"
              :indeterminate="loadingDemographics"
            />
            <v-col md="7">
              <v-card-title class="pb-2 pl-5 pt-2">
                <div class="mt-2">
                  <span class="black--text text--darken-4 text-h3"> USA </span>
                </div>
              </v-card-title>
              <map-chart
                v-if="!loadingDemographics"
                :map-data="mapChartData"
                :configuration-data="configurationData"
                data-e2e="map-chart"
              />

              <map-slider
                v-if="!loadingDemographics"
                :map-data="mapChartData"
                :configuration-data="configurationData"
              />
            </v-col>
            <v-col md="5 pt-0 pl-0">
              <div class="list-tab">
                <map-state-list
                  v-if="!loadingDemographics"
                  :map-data="mapChartData"
                  :configuration-data="configurationData"
                  :header-config="mapStateHeaderList"
                  :height="395"
                />
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { mapGetters, mapActions } from "vuex"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon"
import MapChart from "@/components/common/MapChart/MapChart"
import mapSlider from "@/components/common/MapChart/mapSlider"
import TotalCustomerChart from "@/components/common/TotalCustomerChart/TotalCustomerChart"
import TotalCustomerSpendChart from "@/components/common/TotalCustomerSpend/TotalCustomerSpendChart"
import MapStateList from "@/components/common/MapChart/MapStateList"
import configurationData from "@/components/common/MapChart/MapConfiguration.json"

export default {
  name: "InsightTab",
  components: {
    Tooltip,
    Icon,
    MapChart,
    mapSlider,
    MapStateList,

    TotalCustomerChart,
    TotalCustomerSpendChart,
  },
  data() {
    return {
      configurationData: configurationData,
      loadingDemographics: true,
      mapStateHeaderList: ["name", "avg_spend", "population_percentage"],

      timeFrameLabel: "last 6 months",
      loadingSpendChart: false,
      loadingAudienceChart: false,
      loadingGeoOverview: false,
    }
  },
  computed: {
    ...mapGetters({
      demographicsData: "audiences/demographics",
      totalCustomers: "customers/totalCustomers",
      totalCustomerSpend: "customers/totalCustomerSpend",
      customersGeoOverview: "customers/geoOverview",
    }),
    mapChartData() {
      return this.demographicsData.demo
    },
  },
  async mounted() {
    this.fetchDemographics()
    this.fetchTotalCustomers()
    this.fetchCustomerSpend()
    this.fetchGeoOverview()
  },
  methods: {
    ...mapActions({
      getDemographics: "audiences/getDemographics",
      getTotalCustomers: "customers/getTotalCustomers",
      getCustomerSpend: "customers/getCustomerSpend",
      getGeoOverview: "customers/getGeoOverview",
    }),
    async fetchDemographics() {
      this.loadingDemographics = true
      try {
        await this.getDemographics(this.$route.params.id)
      } finally {
        this.loadingDemographics = false
      }
    },

    async fetchTotalCustomers() {
      this.loadingAudienceChart = true
      try {
        await this.getTotalCustomers()
      } finally {
        this.loadingAudienceChart = false
      }
    },

    async fetchCustomerSpend() {
      this.loadingSpendChart = true
      try {
        await this.getCustomerSpend()
      } finally {
        this.loadingSpendChart = false
      }
    },
    async fetchGeoOverview() {
      this.loadingGeoOverview = true
      try {
        await this.getGeoOverview()
      } finally {
        this.loadingGeoOverview = false
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.insight-tab {
  .list-tab {
    border-left: 1px solid var(--v-black-lighten3) !important;
    height: 386px !important;
  }
}
</style>
