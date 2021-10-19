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
            <h5 class="text-h5 mb-1">Customer overview</h5>
            <v-btn
              text
              small
              class="
                d-flex
                align-right
                primary--text
                text-decoration-none
                pl-0
                pr-0
                idr-link
              "
              @click="toggleIDRInsightsDrawer()"
            >
              <icon
                type="identity-resolution"
                color="primary"
                :size="16"
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
                    <span class="font-weight-semi-bold">
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
                    <span v-if="item.title == 'Customers'">
                      Customers<br />
                      {{
                        item.subtitle | Numeric(true, false, false) | Empty("-")
                      }}
                    </span>
                    <span v-if="item.title == 'Countries'">
                      Countries<br />
                      {{ item.subtitle | Empty("-") }}
                    </span>
                    <span v-if="item.title == 'Cities'">
                      Cities<br />
                      {{
                        item.subtitle | Numeric(true, false, false) | Empty("-")
                      }}
                    </span>
                    <div v-if="item.title == 'Gender'">
                      <div class="mb-3">
                        Men<br />
                        {{
                          item.menData
                            | Numeric(true, false, false)
                            | Empty("-")
                        }}
                      </div>
                      <div class="mb-3">
                        Women<br />
                        {{
                          item.womenData
                            | Numeric(true, false, false)
                            | Empty("-")
                        }}
                      </div>
                      <div class="mb-3">
                        Other<br />
                        {{
                          item.otherData
                            | Numeric(true, false, false)
                            | Empty("-")
                        }}
                      </div>
                    </div>
                    <span
                      v-if="item.title == 'Age range' || item.title == 'States'"
                      class="mb-3"
                    >
                      {{ item.subtitle | Empty("-") }}
                    </span>
                  </template>
                </tooltip>
              </template>
              <template v-if="item.toolTipText" #extra-item>
                <tooltip position-top>
                  <template #label-content>
                    <icon type="info" :size="12" />
                  </template>
                  <template #hover-content>
                    {{ item.toolTipText }}
                  </template>
                </tooltip>
              </template>
            </metric-card>
          </div>
        </v-card>
      </div>
      <v-row class="px-15 mt-2">
        <v-col md="12">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="350">
            <v-card-title class="pb-2 pl-5 pt-5">
              <div class="mt-2">
                <span class="black--text text--darken-4 text-h5">
                  Total customers
                  <span class="text-body-2 time-frame">
                    ({{ timeFrameLabel }})
                  </span>
                </span>
              </div>
            </v-card-title>
            <v-progress-linear
              v-if="loadingCustomerChart"
              :active="loadingCustomerChart"
              :indeterminate="loadingCustomerChart"
            />
            <total-customer-chart
              v-if="!loadingCustomerChart"
              :customers-data="totalCustomers"
              data-e2e="overview-chart"
            />
          </v-card>
        </v-col>
      </v-row>
      <v-row class="px-15 mt-2">
        <v-col md="7">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="386">
            <v-card-title class="pb-2 pl-5 pt-5">
              <div class="mt-2">
                <span class="black--text text--darken-4 text-h5">
                  Demographic Overview
                </span>
              </div>
            </v-card-title>
            <v-progress-linear
              v-if="loadingGeoOverview"
              :active="loadingGeoOverview"
              :indeterminate="loadingGeoOverview"
            />
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
          </v-card>
        </v-col>
        <v-col md="5">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="386">
            <v-card-title class="pb-2 pl-5 pt-5">
              <div class="mt-2">
                <span class="black--text text--darken-4 text-h5">
                  United States
                </span>
              </div>
            </v-card-title>
            <v-divider class="ml-5 mr-8 mt-0 mb-1" />
            <v-progress-linear
              v-if="loadingGeoOverview"
              :active="loadingGeoOverview"
              :indeterminate="loadingGeoOverview"
            />
            <map-state-list
              v-if="!loadingGeoOverview"
              :map-data="customersGeoOverview"
              :configuration-data="configurationData"
            />
          </v-card>
        </v-col>
      </v-row>
      <v-row class="px-15 mt-2">
        <v-col md="3">
          <v-card class="mt-3 rounded-lg box-shadow-5 pl-2 pr-2" height="290">
            <v-progress-linear
              v-if="loadingDemographics"
              :active="loadingDemographics"
              :indeterminate="loadingDemographics"
            />
            <v-card-title v-if="!loadingDemographics" class="pb-0 pl-5 pt-5">
              <div class="mt-2">
                <span class="black--text text--darken-4 text-h5">
                  Top location &amp; Income
                </span>
              </div>
            </v-card-title>
            <income-chart
              v-if="!loadingDemographics"
              :data="demographicsData.income"
              data-e2e="income-chart"
            />
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="mt-3 genderSpend rounded-lg box-shadow-5" height="290">
            <v-progress-linear
              v-if="loadingDemographics"
              :active="loadingDemographics"
              :indeterminate="loadingDemographics"
            />
            <v-card-title v-if="!loadingDemographics" class="pb-0 pl-2 pt-5">
              <div class="mt-1 pl-5">
                <span class="black--text text--darken-4 text-h5">
                  Gender &sol; monthly spending
                </span>
                <span class="text-body-2 time-frame">(last 6 months)</span>
              </div>
            </v-card-title>
            <gender-spend-chart
              v-if="!loadingDemographics"
              :data="demographicsData.spend"
              data-e2e="gender-spend-chart"
            />
          </v-card>
        </v-col>
        <v-col md="3">
          <v-card class="mt-3 rounded-lg box-shadow-5 pl-2 pr-2" height="290">
            <v-progress-linear
              v-if="loadingDemographics"
              :active="loadingDemographics"
              :indeterminate="loadingDemographics"
            />
            <v-card-title v-if="!loadingDemographics" class="pb-0 pl-5 pt-5">
              <div class="mt-2">
                <span class="black--text text--darken-4 text-h5"> Gender </span>
              </div>
            </v-card-title>
            <div v-if="!loadingDemographics" ref="genderChart">
              <doughnut-chart
                :chart-dimensions="genderChartDimensions"
                :data="genderChartData"
                label="Gender"
                data-e2e="gender-chart"
              />
            </div>
          </v-card>
        </v-col>
      </v-row>
      <customer-details v-model="customerProfilesDrawer" />
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
import CustomerDetails from "./Drawers/CustomerDetailsDrawer.vue"
import GeoDrawer from "@/views/Shared/Drawers/GeoDrawer.vue"
import IncomeChart from "@/components/common/incomeChart/IncomeChart"
import GenderSpendChart from "@/components/common/GenderSpendChart/GenderSpendChart"
import MapChart from "@/components/common/MapChart/MapChart"
import MapStateList from "@/components/common/MapChart/MapStateList"
import mapSlider from "@/components/common/MapChart/mapSlider"
import DoughnutChart from "@/components/common/DoughnutChart/DoughnutChart"
import TotalCustomerChart from "@/components/common/TotalCustomerChart/TotalCustomerChart"
import configurationData from "@/components/common/MapChart/MapConfiguration.json"
import IDRInsightsDrawer from "./Drawers/IDRInsightsDrawer"
import dayjs from "dayjs"

export default {
  name: "CustomerProfiles",
  components: {
    MetricCard,
    PageHeader,
    Breadcrumb,
    Tooltip,
    Icon,
    CustomerDetails,
    GeoDrawer,
    IncomeChart,
    GenderSpendChart,
    MapChart,
    MapStateList,
    mapSlider,
    DoughnutChart,
    TotalCustomerChart,
    IDRInsightsDrawer,
  },

  data() {
    return {
      customerProfilesDrawer: false,
      idrInsightsDrawer: false,
      loadingCustomerChart: false,
      configurationData: configurationData,
      geoDrawer: {
        cities: false,
        countries: false,
        states: false,
      },
      loadingGeoOverview: false,
      loadingDemographics: true,
      timeFrameLabel: "last 9 months",
      overviewListItems: [
        {
          title: "Customers",
          subtitle: "",
          icon: "customer-no",
          toolTipText:
            "Total no. of unique hux ids generated to represent a customer.",
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
          text: "All Customers",
          disabled: true,
          href: "/customers",
          icon: "customer-profiles",
        },
        {
          text: "",
          disabled: true,
          href: this.$route.path,
        },
      ],
      loading: true,
      updatedTime: [],
      genderChartDimensions: {
        width: 269,
        height: 200,
      },
    }
  },
  computed: {
    ...mapGetters({
      overview: "customers/overview",
      customersInsights: "customers/insights",
      totalCustomers: "customers/totalCustomers",
      customersGeoOverview: "customers/geoOverview",
      demographicsData: "customers/demographics",
    }),
    updatedTimeStamp() {
      if (this.updatedTime.length !== 0) {
        return (
          this.updatedTime[0] + "<span> &bull; </span>" + this.updatedTime[1]
        )
      } else {
        return "-"
      }
    },

    genderChartData() {
      if (
        this.demographicsData.gender &&
        (this.demographicsData.gender.gender_men ||
          this.demographicsData.gender.gender_women ||
          this.demographicsData.gender.gender_other)
      ) {
        return [
          {
            label: "Men",
            population_percentage:
              this.demographicsData.gender.gender_men.population_percentage,
            size: this.demographicsData.gender.gender_men.size,
          },
          {
            label: "Women",
            population_percentage:
              this.demographicsData.gender.gender_women.population_percentage,
            size: this.demographicsData.gender.gender_women.size,
          },
          {
            label: "Other",
            population_percentage:
              this.demographicsData.gender.gender_other.population_percentage,
            size: this.demographicsData.gender.gender_other.size,
          },
        ]
      }
      return []
    },
  },
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },

  async mounted() {
    this.loading = true
    this.sizeHandler()
    await this.getOverview()
    this.mapOverviewData()
    this.fetchTotalCustomers()
    this.fetchGeoOverview()
    this.fetchDemographics()
    this.loading = false
  },

  methods: {
    ...mapActions({
      getOverview: "customers/getOverview",
      getTotalCustomers: "customers/getTotalCustomers",
      getGeoOverview: "customers/getGeoOverview",
      getDemographics: "customers/getDemographics",
    }),

    async fetchGeoOverview() {
      this.loadingGeoOverview = true
      await this.getGeoOverview()
      this.loadingGeoOverview = false
    },

    async fetchDemographics() {
      this.loadingDemographics = true
      await this.getDemographics({
        start_date: dayjs().subtract(6, "months").format("YYYY-MM-DD"),
        end_date: dayjs().format("YYYY-MM-DD"),
      })
      this.loadingDemographics = false
    },

    async fetchTotalCustomers() {
      this.loadingCustomerChart = true
      await this.getTotalCustomers()
      this.loadingCustomerChart = false
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
    toggleProfilesDrawer() {
      this.customerProfilesDrawer = !this.customerProfilesDrawer
    },
    toggleGeoDrawer(geoLevel = "states") {
      this.geoDrawer[geoLevel] = !this.geoDrawer[geoLevel]
    },
    onClick(action) {
      switch (action) {
        case "toggleProfilesDrawer":
          this.toggleProfilesDrawer()
          break
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
    sizeHandler() {
      if (this.$refs.genderChart) {
        this.genderChartDimensions.width = this.$refs.genderChart.clientWidth
        this.genderChartDimensions.height = 200
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
  color: var(--v-gray-base) !important;
}

.customer-dashboard-wrap {
  ::v-deep .mdi-chevron-right::before {
    content: none;
  }
  ::v-deep .metric-card-wrapper .v-icon::before {
    font-size: 30px;
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
}

.icon-border {
  cursor: default !important;
}
::v-deep .genderSpend .container {
  margin-top: 8px !important;
}
.color-last-month {
  color: var(--v-grey-base) !important;
}
</style>
