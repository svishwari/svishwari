<template>
  <div class="insight-tab">
    <v-row>
      <v-col md="6">
        <v-card class="mt-4 rounded-lg box-shadow-5" height="365">
          <v-progress-linear
            v-if="loadingAudienceChart"
            :active="loadingAudienceChart"
            :indeterminate="loadingAudienceChart"
          />
          <v-card-title class="pb-2 pl-6 pt-5">
            <span v-if="!loadingAudienceChart && totalCustomers.length != 0">
              <h3 class="text-h3">Audience Size</h3>
              <span class="text-body-1 time-frame">
                &nbsp;({{ timeFrameLabel }})
              </span>
            </span>
          </v-card-title>
          <total-customer-chart
            v-if="!loadingAudienceChart && totalCustomers.length != 0"
            :customers-data="totalCustomers"
            data-e2e="total-audience-chart"
          />
          <v-row
            v-else-if="!loadingAudienceChart && totalCustomers.length == 0"
            class="model-features-frame py-14 mt-4"
          >
            <empty-page
              v-if="totalCustomers.length == 0 && !totalAudienceError"
              type="model-features-empty"
              :size="50"
            >
              <template #title>
                <div class="title-no-notification">
                  No audience data to show
                </div>
              </template>
              <template #subtitle>
                <div class="des-no-notification mt-2">
                  Audience size chart will appear here once you create an
                  audience.
                </div>
              </template>
            </empty-page>
            <empty-page
              v-else-if="totalAudienceError"
              class="title-no-notification"
              type="error-on-screens"
              :size="50"
            >
              <template #title>
                <div class="title-no-notification">
                  Audience chart is currently unavailable
                </div>
              </template>
              <template #subtitle>
                <div class="des-no-notification mt-2">
                  Our team is working hard to fix it. Please be patient.
                  <br />Thank you!
                </div>
              </template>
            </empty-page>
          </v-row>
        </v-card>
      </v-col>
      <v-col md="6">
        <v-card class="mt-4 rounded-lg box-shadow-5" height="365">
          <v-progress-linear
            v-if="loadingSpendChart"
            :active="loadingSpendChart"
            :indeterminate="loadingSpendChart"
          />
          <v-card-title class="pb-2 pl-6 pt-5">
            <span v-if="!loadingAudienceChart && totalCustomers.length != 0">
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
                  Total order value for all customers (known and anyonymous)
                  over time.
                </template>
              </tooltip>
              <span class="text-body-1 time-frame">
                &nbsp;({{ timeFrameLabel }})
              </span>
            </span>
          </v-card-title>
          <total-customer-spend-chart
            v-if="!loadingSpendChart && totalCustomerSpend.length != 0"
            :customer-spend-data="totalCustomerSpend"
            data-e2e="audience-spend-chart"
          />
          <v-row
            v-else-if="!loadingSpendChart && totalCustomerSpend.length == 0"
            class="drift-chart-frame py-14 mt-4"
          >
            <empty-page
              v-if="totalCustomerSpend.length == 0 && !audienceSpendError"
              type="drift-chart-empty"
              :size="50"
            >
              <template #title>
                <div class="title-no-notification">
                  No audience data to show
                </div>
              </template>
              <template #subtitle>
                <div class="des-no-notification mt-2">
                  Audience spend chart will appear here once you create an
                  audience.
                </div>
              </template>
            </empty-page>
            <empty-page
              v-else-if="audienceSpendError"
              class="title-no-notification"
              type="error-on-screens"
              :size="50"
            >
              <template #title>
                <div class="title-no-notification">
                  Revenue chart is currently unavailable
                </div>
              </template>
              <template #subtitle>
                <div class="des-no-notification mt-2">
                  Our team is working hard to fix it. Please be patient.
                  <br />Thank you!
                </div>
              </template>
            </empty-page>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="mt-2 mb-4">
      <v-col md="12">
        <v-card class="mt-4 rounded-lg box-shadow-5" height="395">
          <v-row>
            <v-progress-linear
              v-if="loadingDemographics"
              :active="loadingDemographics"
              :indeterminate="loadingDemographics"
            />
            <!-- <span > -->
            <v-col
              v-if="!loadingDemographics && mapChartData.length != 0"
              md="7"
            >
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
            <v-col
              v-if="!loadingDemographics && mapChartData.length != 0"
              md="5 pt-0 pl-0"
            >
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
            <!-- </span> -->

            <v-col
              v-else-if="!loadingDemographics && mapChartData.length == 0"
              md="12"
              class="py-14 mt-14"
            >
              <empty-page
                v-if="mapChartData.length == 0 && !geoOverviewError"
                type="drift-chart-empty"
                :size="50"
              >
                <template #title>
                  <div class="title-no-notification">
                    No audience data to show
                  </div>
                </template>
                <template #subtitle>
                  <div class="des-no-notification mt-2">
                    Map feature chart will appear here once you create an
                    audience.
                  </div>
                </template>
              </empty-page>
              <empty-page
                v-else-if="geoOverviewError"
                class="title-no-notification"
                type="error-on-screens"
                :size="50"
              >
                <template #title>
                  <div class="title-no-notification">
                    Map feature is currently unavailable
                  </div>
                </template>
                <template #subtitle>
                  <div class="des-no-notification mt-2">
                    Our team is working hard to fix it. Please be patient and
                    try again soon!
                  </div>
                </template>
              </empty-page>
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
import EmptyPage from "@/components/common/EmptyPage"

export default {
  name: "InsightTab",
  components: {
    Tooltip,
    Icon,
    MapChart,
    mapSlider,
    MapStateList,
    EmptyPage,
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
      totalAudienceError: false,
      audienceSpendError: false,
      geoOverviewError: false,
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
      } catch (error) {
        this.geoOverviewError = true
      }
      this.loadingDemographics = false
    },

    async fetchTotalCustomers() {
      this.loadingAudienceChart = true
      try {
        await this.getTotalCustomers()
      } catch (error) {
        this.totalAudienceError = true
      }
      this.loadingAudienceChart = false
    },

    async fetchCustomerSpend() {
      this.loadingSpendChart = true
      try {
        await this.getCustomerSpend()
      } catch (error) {
        this.audienceSpendError = true
      }
      this.loadingSpendChart = false
    },
    async fetchGeoOverview() {
      this.loadingGeoOverview = true
      try {
        await this.getGeoOverview()
      } catch (error) {
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
::v-deep .hux-data-table .table-overflow {
  border-top-right-radius: 12px !important;
}
.model-features-frame {
  background-image: url("../../../assets/images/no-barchart-frame.png");
  background-position: center;
}
.drift-chart-frame {
  background-image: url("../../../assets/images/no-drift-chart-frame.png");
  background-position: center;
}
.title-no-notification {
  font-size: 24px !important;
  line-height: 34px !important;
  font-weight: 300 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}
.des-no-notification {
  font-size: 14px !important;
  line-height: 16px !important;
  font-weight: 400 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}
.pre-formatted {
  white-space: pre;
}
</style>
