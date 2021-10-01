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

        <hux-select-date
          v-model="filterStartDate"
          :min="minDate"
          :max="filterEndDate"
          @change="refreshData"
        />

        <icon class="mx-1" type="arrow" color="primary" :size="19" />

        <hux-select-date
          v-model="filterEndDate"
          :min="filterStartDate"
          :max="maxDate"
          @change="refreshData"
        />
      </hux-filters-bar>
    </template>
    <template>
      <div v-if="!loadingOverview">
        <v-slide-group ref="wrapper" class="idr-slide-group" show-arrows>
          <v-slide-item v-for="(metric, index) in overview" :key="index">
            <metric-card
              :title="metric.title"
              :min-width="170"
              class="idr-metric-card"
              data-e2e="overviewList"
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
      </div>
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
        :data="dataFeeds"
        :is-loading="loadingDataFeeds"
        class="mt-6 mx-2"
        data-e2e="datafeedtable"
      />
    </template>
  </page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import { endOfMonth } from "@/utils"

import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import HuxFiltersBar from "@/components/common/FiltersBar"
import HuxSelectDate from "@/components/common/SelectDate.vue"
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
    HuxSelectDate,
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
      isFilterToggled: false,
      filterStartDate: null,
      filterEndDate: null,
    }
  },

  computed: {
    ...mapGetters({
      overview: "identity/overview",
      timeFrame: "identity/timeFrame",
      dataFeeds: "identity/dataFeeds",
      matchingTrends: "identity/matchingTrends",
    }),

    minDate() {
      return this.$options.filters.Date(
        this.timeFrame["start_date"],
        "YYYY-MM-DD"
      )
    },

    maxDate() {
      return this.$options.filters.Date(
        this.timeFrame["end_date"],
        "YYYY-MM-DD"
      )
    },

    selectedDateRange() {
      return {
        startDate: this.filterStartDate,
        endDate: this.filterEndDate ? endOfMonth(this.filterEndDate) : null,
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
      this.loadingMatchingTrends = true
      this.loadingDataFeeds = true
      this.loadingOverview = true
      await this.loadOverview()
      this.loadDataFeeds()
      this.loadMatchingTrends()
    },

    setFilters({ startDate, endDate }) {
      if (startDate && endDate) {
        this.filterStartDate = this.$options.filters.Date(
          startDate,
          "YYYY-MM-DD"
        )
        this.filterEndDate = this.$options.filters.Date(endDate, "YYYY-MM-DD")
      }
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

  .idr-metric-card {
    margin: 6px !important;
  }
}
</style>
