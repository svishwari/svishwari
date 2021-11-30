<template>
  <div class="customer-dashboard-wrap">
    <page-header class="py-5" :header-height="110">
      <template #left>
        <div>
          <breadcrumb :items="items" />
        </div>
        <div class="text-subtitle-1 font-weight-regular">
          Hux’s omni-view of your entire customer base to help you better
          understand how to create a personalized experience.
        </div>
      </template>
    </page-header>
    <v-progress-linear
      :active="loading"
      :indeterminate="loading"
      data-e2e="loader"
    />
    <div v-if="!loading">
      <div v-if="overviewListItems" class="px-15 mt-6 my-1">
        <v-card class="rounded pa-5 box-shadow-5">
          <div class="d-flex justify-space-between">
            <h5 class="text-h3 mb-1">Customer overview</h5>
            <v-btn
              text
              min-width="80"
              class="
                d-flex
                align-right
                primary--text
                text-decoration-none
                pl-0
                pr-0
                idr-link
                text-body-1
              "
              @click="toggleIDRInsightsDrawer()"
            >
              <icon
                type="identity-resolution"
                color="primary"
                :size="18"
                class="mr-1"
              />
              IDR Insights
            </v-btn>
          </div>
          <div class="row row-margin no-gutters">
            <metric-card
              v-for="item in overviewListItems"
              :key="item.title"
              class="card-margin"
              :grow="item.toolTipText ? 2 : 1"
              :title="item.title"
              :interactable="item.action ? true : false"
              data-e2e="customeroverview"
              @click="item.action ? onClick(item.action) : ''"
            >
              <template v-if="item.icon" #short-name>
                <icon :type="item.icon" :size="40" />
              </template>
              <template #subtitle-extended>
                <tooltip>
                  <template #label-content>
                    <span class="text-subtitle-1">
                      <span v-if="item.value == 'percentage'">
                        {{
                          item.subtitle
                            | Numeric(true, false, false, true)
                            | Empty("-")
                        }}
                      </span>
                      <span v-if="item.value == 'numeric'">
                        {{ item.subtitle | Numeric(true, true) | Empty("-") }}
                      </span>
                      <span v-if="item.value == 'none'">
                        {{ item.subtitle | Empty("-") }}
                      </span>
                      <span v-if="item.value == ''">
                        {{ item.subtitle | Numeric(true, true) | Empty("-") }}
                      </span>
                    </span>
                  </template>
                  <template #hover-content>
                    <div
                      v-if="
                        item.title == 'Customers' ||
                        item.title == 'Countries' ||
                        item.title == 'States' ||
                        item.title == 'Cities'
                      "
                    >
                      <div class="mb-1">{{ item.title }}</div>
                      {{
                        item.subtitle | Numeric(true, false, false) | Empty("-")
                      }}
                    </div>
                    <div v-if="item.title == 'Gender'">
                      <div class="mb-2">
                        <div class="mb-2">Men</div>
                        {{
                          item.menData
                            | Numeric(true, false, false)
                            | Empty("-")
                        }}
                      </div>
                      <div class="mb-2">
                        <div class="mb-2">Women</div>
                        {{
                          item.womenData
                            | Numeric(true, false, false)
                            | Empty("-")
                        }}
                      </div>
                      <div>
                        <div class="mb-2">Other</div>
                        {{
                          item.otherData
                            | Numeric(true, false, false)
                            | Empty("-")
                        }}
                      </div>
                    </div>
                    <span v-if="item.title == 'Age range'" class="mb-3">
                      {{ item.subtitle | Empty("-") }}
                    </span>
                  </template>
                </tooltip>
              </template>
              <template v-if="item.toolTipText" #extra-item>
                <tooltip position-top>
                  <template #label-content>
                    <icon
                      type="info"
                      :size="8"
                      color="primary"
                      variant="base"
                      class="mb-1"
                    />
                  </template>
                  <template #hover-content>
                    {{ item.toolTipText }}
                  </template>
                </tooltip>
              </template>
            </metric-card>
          </div>
        </v-card>

        <v-tabs v-model="tabOption" class="mt-8">
          <v-tabs-slider color="primary"></v-tabs-slider>
          <div class="d-flex">
            <v-tab
              key="overview"
              class="pa-2 mr-3 text-h3"
              color
              data-e2e="overview-tab"
              @click="loadCustomersList = false"
            >
              Overview
            </v-tab>
            <v-tab
              key="customerList"
              class="text-h3"
              data-e2e="customer-list-tab"
              @click="loadCustomersList = true"
            >
              Customer list
            </v-tab>
          </div>
        </v-tabs>
        <v-tabs-items v-model="tabOption" class="mt-2">
          <v-tab-item key="overview">
            <v-row>
              <v-col md="6">
                <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
                  <v-card-title class="pb-2 pl-6 pt-5">
                    <h3 class="text-h3">Total customers</h3>
                    <span class="text-body-1 time-frame">
                      &nbsp;({{ timeFrameLabel }})
                    </span>
                  </v-card-title>
                  <v-progress-linear
                    v-if="loadingCustomerChart"
                    :active="loadingCustomerChart"
                    :indeterminate="loadingCustomerChart"
                  />
                  <total-customer-chart
                    v-if="!loadingCustomerChart"
                    :customers-data="totalCustomers"
                    data-e2e="total-customer-chart"
                  />
                </v-card>
              </v-col>
              <v-col md="6">
                <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
                  <v-card-title class="pb-2 pl-6 pt-5">
                    <h3 class="text-h3">Total customer spend</h3>
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
                        Total order value for all customers (known and
                        anyonymous) over time.
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
                    data-e2e="customer-spend-chart"
                  />
                </v-card>
              </v-col>
            </v-row>
            <v-row class="mt-2 mb-4">
              <v-col md="12">
                <v-card class="mt-3 rounded-lg box-shadow-5" height="395">
                  <v-row>
                    <v-col md="7">
                      <v-progress-linear
                        v-if="loadingGeoOverview"
                        :active="loadingGeoOverview"
                        :indeterminate="loadingGeoOverview"
                      />
                      <v-card-title class="pb-2 pl-5 pt-2">
                        <div class="mt-2">
                          <span class="black--text text--darken-4 text-h3">
                            USA
                          </span>
                        </div>
                      </v-card-title>
                      <map-chart
                        v-if="!loadingGeoOverview"
                        :map-data="customersGeoOverview"
                        :configuration-data="configurationData"
                        data-e2e="map-chart"
                      />

                      <map-slider
                        v-if="!loadingGeoOverview"
                        :map-data="customersGeoOverview"
                        :configuration-data="configurationData"
                      />
                    </v-col>
                    <v-divider vertical class="combined-list" />
                    <v-col md="5 pt-0 pl-1">
                      <div class="combined-list">
                        <map-state-list
                          v-if="!loadingGeoOverview"
                          :map-data="customersGeoOverview"
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
          </v-tab-item>
          <v-tab-item key="customerList">
            <v-card class="mt-3 pa-6 rounded-lg box-shadow-5">
              <customer-list v-if="loadCustomersList" />
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </div>
      <geo-drawer
        geo-level="cities"
        :results="overview.total_cities"
        :toggle="geoDrawer.cities"
        @onToggle="(isToggled) => (geoDrawer.cities = isToggled)"
      />
      <geo-drawer
        geo-level="countries"
        :results="overview.total_countries"
        :toggle="geoDrawer.countries"
        @onToggle="(isToggled) => (geoDrawer.countries = isToggled)"
      />
      <geo-drawer
        geo-level="states"
        :results="overview.total_us_states"
        :toggle="geoDrawer.states"
        @onToggle="(isToggled) => (geoDrawer.states = isToggled)"
      />
      <i-d-r-insights-drawer v-model="idrInsightsDrawer" />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Tooltip from "@/components/common/Tooltip.vue"
import MetricCard from "@/components/common/MetricCard"
import Icon from "@/components/common/Icon"
import GeoDrawer from "@/views/Shared/Drawers/GeoDrawer.vue"
import MapChart from "@/components/common/MapChart/MapChart"
import MapStateList from "@/components/common/MapChart/MapStateList"
import mapSlider from "@/components/common/MapChart/mapSlider"
import TotalCustomerChart from "@/components/common/TotalCustomerChart/TotalCustomerChart"
import TotalCustomerSpendChart from "@/components/common/TotalCustomerSpend/TotalCustomerSpendChart"
import configurationData from "@/components/common/MapChart/MapConfiguration.json"
import IDRInsightsDrawer from "./Drawers/IDRInsightsDrawer"
import CustomerList from "./CustomerList"

export default {
  name: "CustomerProfiles",
  components: {
    MetricCard,
    PageHeader,
    Breadcrumb,
    Tooltip,
    Icon,
    GeoDrawer,
    MapChart,
    MapStateList,
    mapSlider,
    TotalCustomerChart,
    TotalCustomerSpendChart,
    IDRInsightsDrawer,
    CustomerList,
  },

  data() {
    return {
      idrInsightsDrawer: false,
      loadingCustomerChart: false,
      loadingSpendChart: false,
      configurationData: configurationData,
      geoDrawer: {
        cities: false,
        countries: false,
        states: false,
      },
      loadingGeoOverview: false,
      loadingDemographics: true,
      timeFrameLabel: "last 6 months",
      overviewListItems: [
        {
          title: "Customers",
          subtitle: "",
          icon: "customer-no",
          toolTipText:
            "Total number of unique Hux IDs generated to represent a customer.",
          value: "",
        },
        {
          title: "Countries",
          subtitle: "",
          icon: "countries",
          value: "",
          action: "toggleCountriesDrawer",
        },
        {
          title: "States",
          subtitle: "",
          icon: "states",
          toolTipText:
            "US states or regions equivalent to US state-level , eg. counties, districts, departments, divisions, parishes, provinces etc.",
          value: "",
          action: "toggleStatesDrawer",
        },
        {
          title: "Cities",
          subtitle: "",
          icon: "cities",
          value: "",
          action: "toggleCitiesDrawer",
        },
        { title: "Age range", subtitle: "", icon: "birth", value: "" },
        {
          title: "Gender",
          subtitle: "",
          value: "",
          menData: "",
          womenData: "",
          otherData: "",
        },
      ],
      items: [
        {
          text: "Customer Profiles",
          disabled: true,
          href: "/customers",
          icon: "customer-profiles",
        },
      ],
      loading: true,
      updatedTime: [],
      genderChartDimensions: {
        width: 269,
        height: 200,
      },
      tabOption: 0,
      showOverviewTab: true,
      enableLazyLoad: false,
      loadCustomersList: false,
      localDrawer: this.value,
      batchCount: 1,
      columnDefs: [
        {
          text: "Hux ID",
          value: "hux_id",
          width: "auto",
        },
        {
          text: "Last name",
          value: "last_name",
          width: "auto",
        },
        {
          text: "First name",
          value: "first_name",
          width: "auto",
        },
        {
          text: "Match confidence",
          value: "match_confidence",
          width: "250px",
        },
      ],
      lastBatch: 0,
      batchDetails: {
        batchSize: 100,
        batchNumber: 1,
        isLazyLoad: false,
      },
      mapStateHeaderList: ["name", "avg_spend", "population_percentage"],
    }
  },
  computed: {
    ...mapGetters({
      overview: "customers/overview",
      customersInsights: "customers/insights",
      totalCustomers: "customers/totalCustomers",
      totalCustomerSpend: "customers/totalCustomerSpend",
      customersGeoOverview: "customers/geoOverview",
      demographicsData: "customers/demographics",
    }),
  },

  async mounted() {
    this.loading = true
    try {
      await this.getOverview()
      this.mapOverviewData()
      this.fetchTotalCustomers()
      this.fetchCustomerSpend()
      this.fetchGeoOverview()
    } finally {
      this.loading = false
    }
  },

  methods: {
    ...mapActions({
      getOverview: "customers/getOverview",
      getTotalCustomers: "customers/getTotalCustomers",
      getGeoOverview: "customers/getGeoOverview",
      getCustomerSpend: "customers/getCustomerSpend",
      getDemographics: "customers/getDemographics",
    }),

    async fetchGeoOverview() {
      this.loadingGeoOverview = true
      try {
        await this.getGeoOverview()
      } finally {
        this.loadingGeoOverview = false
      }
    },

    async fetchTotalCustomers() {
      this.loadingCustomerChart = true
      try {
        await this.getTotalCustomers()
      } finally {
        this.loadingCustomerChart = false
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

    // TODO: refactor this and move this logic to a getter in the store
    mapOverviewData() {
      if (this.overview) {
        this.overviewListItems[0].subtitle = this.overview.total_customers
        this.overviewListItems[0].value = "numeric"
        this.overviewListItems[1].subtitle = this.overview.total_countries
        this.overviewListItems[2].subtitle = this.overview.total_us_states
        this.overviewListItems[3].subtitle = this.overview.total_cities
        this.overviewListItems[3].value = "numeric"
        let min_age = this.overview.min_age
        let max_age = this.overview.max_age
        if (min_age && max_age && min_age === max_age) {
          this.overviewListItems[4].subtitle = min_age
        } else if (min_age && max_age) {
          this.overviewListItems[4].subtitle = `${min_age}-${max_age}`
        } else {
          this.overviewListItems[4].subtitle = "-"
        }
        this.overviewListItems[4].value = "none"
        this.overviewListItems[5].subtitle = this.mapGenderData()
      }
    },

    toggleGeoDrawer(geoLevel = "states") {
      this.geoDrawer[geoLevel] = !this.geoDrawer[geoLevel]
    },

    onClick(action) {
      switch (action) {
        case "toggleCitiesDrawer":
          this.toggleGeoDrawer("cities")
          break
        case "toggleCountriesDrawer":
          this.toggleGeoDrawer("countries")
          break
        case "toggleStatesDrawer":
          this.toggleGeoDrawer("states")
          break
      }
    },
    mapGenderData() {
      this.overviewListItems[5].menData = this.overview.gender_men_count
      this.overviewListItems[5].womenData = this.overview.gender_women_count
      this.overviewListItems[5].otherData = this.overview.gender_other_count

      let menData = this.setValueOrEmpty(this.overview.gender_men)
      let womenData = this.setValueOrEmpty(this.overview.gender_women)
      let otherData = this.setValueOrEmpty(this.overview.gender_other)
      return `M: ${menData}  W: ${womenData}  O: ${otherData}`
    },

    setValueOrEmpty(value) {
      return value != null
        ? this.$options.filters.Numeric(value, true, false, false, true)
        : this.$options.filters.Empty("-")
    },

    toggleIDRInsightsDrawer() {
      this.idrInsightsDrawer = !this.idrInsightsDrawer
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-btn {
  &:not(.v-btn--round).v-size--default {
    height: 28px;
    min-width: 178px;
  }
  .v-btn__content {
    color: var(--v-cerulean-base) !important;
  }
}
.row-margin {
  margin-left: -6px;
  margin-right: -6px;
}

.card-margin {
  margin: 6px !important;
}

.time-frame {
  color: var(--v-black-lighten4) !important;
}

.customer-dashboard-wrap {
  ::v-deep .mdi-chevron-right::before {
    content: none;
  }
  ::v-deep .metric-card-wrapper .v-icon::before {
    font-size: 30px;
  }
  .combined-list {
    max-height: 395px;
  }

  .customer-slide-group {
    ::v-deep .v-slide-group__wrapper {
      overflow: auto !important;
    }
    ::v-deep .theme--light.v-icon {
      color: var(--v-primary-base) !important;
    }
    ::v-deep .v-icon--disabled.theme--light.v-icon {
      color: var(--v-black-lighten3) !important;
    }
  }

  .idr-link {
    min-width: 0px;
    margin-top: -5px;
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
}

.icon-border {
  cursor: default !important;
}
.color-last-month {
  color: var(--v-grey-base) !important;
}

::v-deep .theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active) {
  color: var(--v-black-lighten4) !important;
}
</style>
