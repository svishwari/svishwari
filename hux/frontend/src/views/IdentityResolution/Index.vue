<template>
  <page max-width="100%" class="idr-wrapper">
    <template #header>
      <page-header header-height="70">
        <template #left>
          <breadcrumb
            :items="[
              {
                text: 'Identity Resolution',
                disabled: true,
                href: '/identity-resolution',
                icon: 'identity-resolution',
              },
            ]"
          />
        </template>
      </page-header>

      <page-header header-height="71">
        <template #left>
          <v-btn
            icon
            :color="isFilterToggled ? 'secondary' : 'black'"
            class="ml-n2"
            @click.native="isFilterToggled = !isFilterToggled"
          >
            <v-icon medium>mdi-filter-variant</v-icon>
          </v-btn>
          <v-btn disabled icon color="black" class="pl-6">
            <v-icon medium>mdi-magnify</v-icon>
          </v-btn>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <hux-filters-bar :is-toggled="isFilterToggled">
        <label class="black--text text--darken-4 mr-2">
          Select timeframe:
        </label>

        <hux-select
          v-model="filters.startMonth"
          :items="options.months"
          :items-disabled="disabledOptions.startMonths"
          label="Start month"
          class="mx-1"
          width="141"
          @change="refreshData"
        />

        <hux-select
          v-model="filters.startYear"
          :items="options.years"
          :items-disabled="disabledOptions.startYears"
          label="Start year"
          class="mx-1"
          width="126"
          @change="refreshData"
        />

        <icon class="mx-1" type="arrow" color="primary" :size="19" />

        <hux-select
          v-model="filters.endMonth"
          :items="options.months"
          :items-disabled="disabledOptions.endMonths"
          label="End month"
          class="mx-1"
          width="141"
          @change="refreshData"
        />

        <hux-select
          v-model="filters.endYear"
          label="End year"
          :items="options.years"
          :items-disabled="disabledOptions.endYears"
          class="mx-1"
          width="126"
          @change="refreshData"
        />
      </hux-filters-bar>
    </template>
    <template>
      <v-row v-if="!loadingOverview" no-gutters>
        <v-slide-group ref="wrapper" class="idr-slide-group" show-arrows>
          <v-slide-item v-for="(metric, index) in overview" :key="index">
            <metric-card
              :title="metric.title"
              :min-width="170"
              class="mx-2 my-2 pt-3 pl-6"
            >
              <template #extra-item>
                <tooltip position-top>
                  <template #label-content>
                    <icon type="info" :size="12" />
                  </template>
                  <template #hover-content>
                    <v-sheet max-width="240px">
                      {{ metric.description }}
                    </v-sheet>
                  </template>
                </tooltip>
              </template>

              <template #subtitle-extended>
                <tooltip>
                  <template #label-content>
                    <span class="font-weight-semi-bold">
                      <template v-if="metric.format === 'numeric'">
                        {{ metric.value | Numeric(true, true) | Empty }}
                      </template>
                      <template v-if="metric.format === 'percentage'">
                        {{
                          metric.value
                            | Numeric(true, false, false, true)
                            | Empty
                        }}
                      </template>
                    </span>
                  </template>
                  <template #hover-content>
                    <template v-if="metric.format === 'numeric'">
                      {{ metric.value | Numeric(true, false) | Empty }}
                    </template>
                    <template v-if="metric.format === 'percentage'">
                      {{
                        metric.value
                          | Numeric(false, false, false, true)
                          | Empty
                      }}
                    </template>
                  </template>
                </tooltip>
              </template>
            </metric-card>
          </v-slide-item>
        </v-slide-group>
      </v-row>
      <v-row class="px-2 mt-0 mb-1">
        <v-col md="12">
          <v-card class="mt-3 rounded-lg box-shadow-5" min-height="400">
            <v-progress-linear
              v-if="loadingMatchingTrends"
              :active="loadingMatchingTrends"
              :indeterminate="loadingMatchingTrends"
            />

            <v-card-title class="chart-style pb-8 pl-5 pt-5">
              <div class="mt-2">
                <span class="black--text text--darken-4 text-h5">
                  ID Resolution matching trends
                </span>
              </div>
            </v-card-title>

            <template v-if="!loadingMatchingTrends">
              <i-d-r-matching-trend
                v-if="hasMatchingTrendsData"
                :map-data="matchingTrends"
              />
              <div v-if="!hasMatchingTrendsData" class="overflow-hidden px-10">
                <svg-as-component
                  src="assets/images/MultiLineChartEmpty"
                  class="d-flex"
                />
                <p class="text-caption d-flex align-center my-5">
                  <svg
                    width="12"
                    height="12"
                    viewBox="0 0 12 12"
                    fill="none"
                    class="mr-2"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <circle cx="6" cy="6" r="6" fill="#d0d0ce" />
                  </svg>
                  no data available
                </p>
              </div>
            </template>
          </v-card>
        </v-col>
      </v-row>

      <data-feeds
        v-if="!loadingDataFeeds"
        :data="dataFeeds"
        class="mt-6 mx-2"
        data-e2e="datafeedtable"
      />
    </template>
  </page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import { listOfMonths, listOfYears } from "@/utils"

import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import HuxFiltersBar from "@/components/common/FiltersBar"
import HuxSelect from "@/components/common/Select.vue"
import Icon from "@/components/common/Icon"
import MetricCard from "@/components/common/MetricCard"
import Tooltip from "@/components/common/Tooltip.vue"
import DataFeeds from "./DataFeeds.vue"
import IDRMatchingTrend from "@/components/common/IDRMatchingTrend/IDRMatchingTrend"
import svgAsComponent from "@/components/common/SVG.vue"

export default {
  name: "IdentityResolution",

  components: {
    Page,
    Breadcrumb,
    Icon,
    HuxFiltersBar,
    HuxSelect,
    MetricCard,
    PageHeader,
    Tooltip,
    DataFeeds,
    IDRMatchingTrend,
    svgAsComponent,
  },

  data() {
    return {
      loadingOverview: true,
      loadingDataFeeds: true,
      loadingMatchingTrends: true,
      isFilterToggled: true,
      options: {
        months: listOfMonths(),
        years: listOfYears(),
      },
      filters: {
        startMonth: null,
        startYear: null,
        endMonth: null,
        endYear: null,
      },
    }
  },

  computed: {
    ...mapGetters({
      overview: "identity/overview",
      timeFrame: "identity/timeFrame",
      dataFeeds: "identity/dataFeeds",
      matchingTrends: "identity/matchingTrends",
    }),

    startDate() {
      return this.formatDate(
        `${this.filters.startMonth} ${this.filters.startYear}`
      )
    },

    endDate() {
      return this.formatDate(`${this.filters.endMonth} ${this.filters.endYear}`)
    },

    selectedDateRange() {
      return {
        startDate: this.startDate,
        endDate: this.endDate,
      }
    },

    timeFrameBounds() {
      const timeFrameStart = this.timeFrame["start_date"]
      const timeFrameEnd = this.timeFrame["end_date"]
      return {
        minMonth: this.formatDate(timeFrameStart, "month"),
        minYear: this.formatDate(timeFrameStart, "year"),
        maxMonth: this.formatDate(timeFrameEnd, "month"),
        maxYear: this.formatDate(timeFrameEnd, "year"),
      }
    },

    enabledOptions() {
      let startMonth = "January"
      let endMonth = "December"
      const sameYearSelected = this.filters.startYear === this.filters.endYear

      if (sameYearSelected) {
        const yearSelected = this.filters.startYear
        const startYearSelected = yearSelected === this.timeFrameBounds.minYear
        const endYearSelected = yearSelected === this.timeFrameBounds.maxYear

        if (startYearSelected) {
          startMonth = this.timeFrameBounds.minMonth
        } else if (endYearSelected) {
          endMonth = this.timeFrameBounds.maxMonth
        }
      }

      return {
        startMonths: listOfMonths({
          startMonth: this.timeFrameBounds.minMonth,
          endMonth: endMonth,
        }),
        startYears: listOfYears({
          startYear: this.timeFrameBounds.minYear,
          endYear: this.filters.endYear,
        }),
        endMonths: listOfMonths({
          startMonth: startMonth,
          endMonth: this.timeFrameBounds.maxMonth,
        }),
        endYears: listOfYears({
          startYear: this.filters.startYear,
          endYear: this.timeFrameBounds.maxYear,
        }),
      }
    },

    disabledOptions() {
      let startMonths = []
      let endMonths = []

      const disabledStartMonths = this.options.months.filter(
        (month) => !this.enabledOptions.startMonths.includes(month)
      )

      const disabledEndMonths = this.options.months.filter(
        (month) => !this.enabledOptions.endMonths.includes(month)
      )

      if (this.filters.startYear === this.timeFrameBounds.maxYear) {
        startMonths = disabledEndMonths
      }

      if (this.filters.startYear === this.timeFrameBounds.minYear) {
        startMonths = disabledStartMonths
      }

      if (this.filters.endYear === this.timeFrameBounds.minYear) {
        endMonths = disabledStartMonths
      }

      if (this.filters.endYear === this.timeFrameBounds.maxYear) {
        endMonths = disabledEndMonths
      }

      if (this.filters.startYear === this.filters.endYear) {
        if (this.filters.startYear === this.timeFrameBounds.minYear) {
          startMonths = endMonths = disabledStartMonths
        }
        if (this.filters.endYear === this.timeFrameBounds.maxYear) {
          startMonths = endMonths = disabledEndMonths
        }
      }

      const startYears = this.options.years.filter(
        (year) => !this.enabledOptions.startYears.includes(year)
      )

      const endYears = this.options.years.filter(
        (year) => !this.enabledOptions.endYears.includes(year)
      )

      return {
        startMonths: startMonths,
        endMonths: endMonths,
        startYears: startYears,
        endYears: endYears,
      }
    },

    hasMatchingTrendsData() {
      return this.matchingTrends && this.matchingTrends.length
    },

    loading() {
      return (
        this.loadingOverview ||
        this.loadingDataFeeds ||
        this.loadingMatchingTrends
      )
    },
  },

  async mounted() {
    await this.refreshData()
    this.setFilters({
      startDate: this.timeFrame["start_date"],
      endDate: this.timeFrame["end_date"],
    })
  },

  methods: {
    ...mapActions({
      getOverview: "identity/getOverview",
      getDataFeeds: "identity/getDataFeeds",
      getMatchingTrends: "identity/getMatchingTrends",
    }),

    async refreshData() {
      await this.loadOverview()
      await this.loadDataFeeds()
      await this.loadMatchingTrends()
    },

    setFilters({ startDate, endDate }) {
      if (startDate && endDate) {
        const updatedFilters = {
          startMonth: this.formatDate(startDate, "month"),
          startYear: this.formatDate(startDate, "year"),
          endMonth: this.formatDate(endDate, "month"),
          endYear: this.formatDate(endDate, "year"),
        }

        this.filters = updatedFilters

        this.options.years = listOfYears({
          startYear: updatedFilters.startYear,
          endYear: updatedFilters.endYear,
        })
      }
    },

    formatDate(date, format) {
      let dateFormat = "YYYY-MM-DD"
      if (format === "month") dateFormat = "MMMM"
      if (format === "year") dateFormat = "YYYY"
      return this.$options.filters.Date(date, dateFormat)
    },

    async loadMatchingTrends() {
      this.loadingMatchingTrends = true
      await this.getMatchingTrends(this.selectedDateRange)
      this.loadingMatchingTrends = false
    },

    async loadDataFeeds() {
      this.loadingDataFeeds = true
      await this.getDataFeeds(this.selectedDateRange)
      this.loadingDataFeeds = false
    },

    async loadOverview() {
      this.loadingOverview = true
      await this.getOverview(this.selectedDateRange)
      this.loadingOverview = false
    },
  },
}
</script>
<style lang="scss" scoped>
.idr-wrapper {
  .idr-slide-group {
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
}
</style>
