<template>
  <page max-width="100%" class="idr-wrapper">
    <template #header>
      <page-header class="page-header py-5" :header-height="110">
        <template #left>
          <div>
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
          </div>
          <div class="text-subtitle-1 font-weight-regular">
            Insights into the ingestion of all your customers’ data across your
            data sources that build a cohesive view of each individual customer.
          </div>
        </template>
        <template #right>
          <v-btn icon @click.native="isFilterToggled = !isFilterToggled">
            <icon
              type="filter"
              :size="27"
              :color="totalFiltersSelected > 0 ? 'primary' : 'black'"
              :variant="totalFiltersSelected > 0 ? 'lighten6' : 'darken4'"
            />
            <v-badge
              v-if="totalFiltersSelected > 0"
              :content="totalFiltersSelected"
              color="white"
              offset-x="6"
              offset-y="4"
              light
              bottom
              overlap
              bordered
            />
          </v-btn>
        </template>
      </page-header>

      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>

    <template>
      <div
        class="
          d-flex
          flex-nowrap
          align-stretch
          flex-grow-1 flex-shrink-0
          mw-100
        "
      >
        <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100 pa-6">
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
                        <icon
                          type="info"
                          :size="12"
                          color="primary"
                          variant="base"
                        />
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
              <v-card
                class="mt-2 rounded-lg box-shadow-5 overflow-hidden"
                min-height="400"
              >
                <v-progress-linear
                  v-if="loadingMatchingTrends"
                  :active="loadingMatchingTrends"
                  :indeterminate="loadingMatchingTrends"
                />

                <v-card-title class="chart-style pb-8 pl-5 pt-5">
                  <div class="mt-2">
                    <span class="black--text text--darken-4 text-h3">
                      ID Resolution matching trends
                    </span>
                    <span
                      v-if="
                        responseTimeFrame &&
                        responseTimeFrame.start_date &&
                        responseTimeFrame.end_date
                      "
                      class="black--text text--darken-4 text-body-1"
                    >
                      (
                      {{
                        this.$options.filters.Date(
                          responseTimeFrame["start_date"],
                          "MMMM YYYY"
                        )
                      }}
                      -
                      {{
                        this.$options.filters.Date(
                          responseTimeFrame["end_date"],
                          "MMMM YYYY"
                        )
                      }}
                      )
                    </span>
                  </div>
                </v-card-title>

                <template v-if="!loadingMatchingTrends">
                  <i-d-r-matching-trend
                    v-if="hasMatchingTrendsData"
                    :map-data="matchingTrends"
                  />
                  <div
                    v-if="!hasMatchingTrendsData"
                    class="overflow-hidden px-10"
                  >
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
            class="mt-3 mx-2"
            data-e2e="datafeedtable"
          />
        </div>

        <div class="ml-auto">
          <hux-filters-drawer
            :is-toggled="isFilterToggled"
            :count="totalFiltersSelected"
            @clear="resetFilters"
            @apply="refreshData"
          >
            <hux-filter-panels>
              <hux-filter-panel title="Time" :count="numFiltersSelected">
                <hux-select-date
                  v-model="filterStartDate"
                  label-month="Start month"
                  label-year="Start year"
                  :min="minDate"
                  :max="filterEndDate"
                />

                <div class="d-flex justify-center my-2">
                  <icon
                    class="rotate-icon-90"
                    type="arrow"
                    color="primary"
                    :size="19"
                  />
                </div>

                <hux-select-date
                  v-model="filterEndDate"
                  label-month="End month"
                  label-year="End year"
                  :min="filterStartDate"
                  :max="maxDate"
                />
              </hux-filter-panel>
            </hux-filter-panels>
          </hux-filters-drawer>
        </div>
      </div>
    </template>
  </page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import { endOfMonth } from "@/utils"

import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import HuxFiltersDrawer from "@/components/common/FiltersDrawer"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
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
    HuxFiltersDrawer,
    HuxFilterPanels,
    HuxFilterPanel,
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
      responseTimeFrame: "identity/responseTimeFrame",
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

    numFiltersSelected() {
      if (
        this.filterStartDate !== this.minDate ||
        this.filterEndDate !== this.maxDate
      ) {
        return 1
      }
      return 0
    },

    totalFiltersSelected() {
      return this.numFiltersSelected
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

    resetFilters() {
      this.filterStartDate = this.minDate
      this.filterEndDate = this.maxDate
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
$offset: 110px;
$headerOffsetX: 220px + 32px;
$headerOffsetY: 70px;

.idr-wrapper {
  padding-top: $offset;

  // TODO: update app layout to include page headers
  .page-header {
    position: fixed;
    top: $headerOffsetY;
    left: 0;
    right: 0;
    padding-left: $headerOffsetX !important;
    z-index: 3;
  }

  ::v-deep .container {
    padding: 0 !important;
  }

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
    margin: 4px !important;
  }
}
</style>
