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
            Monitor the ingestion and integration of all relevant data sources
            as we create a single, persistent identifier of each customer.
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
          minh-100
        "
      >
        <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100 pa-6">
          <div v-if="!loadingOverview">
            <v-slide-group ref="wrapper" class="idr-slide-group" show-arrows>
              <v-slide-item v-for="(metric, index) in overview" :key="index">
                <metric-card
                  :title="metric.title"
                  :min-width="175"
                  class="idr-metric-card"
                  data-e2e="overviewList"
                >
                  <template #extra-item>
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
                        <v-sheet max-width="240px">
                          {{ metric.description }}
                        </v-sheet>
                      </template>
                    </tooltip>
                  </template>

                  <template #subtitle-extended>
                    <tooltip>
                      <template #label-content>
                        <span class="text-subtitle-1">
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
                :class="
                  !hasMatchingTrendsData && !loadingMatchingTrends
                    ? 'middle'
                    : ''
                "
                min-height="400"
              >
                <v-progress-linear
                  v-if="loadingMatchingTrends"
                  :active="loadingMatchingTrends"
                  :indeterminate="loadingMatchingTrends"
                />

                <template v-if="!loadingMatchingTrends">
                  <span v-if="hasMatchingTrendsData">
                    <v-card-title class="chart-style pb-8 pl-6 pt-5">
                      <div class="mt-2">
                        <span class="black--text text-h3">
                          ID Resolution matching trends
                        </span>
                        <span
                          v-if="
                            responseTimeFrame &&
                            responseTimeFrame.start_date &&
                            responseTimeFrame.end_date
                          "
                          class="black--text text--lighten-4 text-body-1"
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

                    <i-d-r-matching-trend :map-data="matchingTrends" />
                  </span>

                  <v-row v-else class="matching-trend-chart-frame py-14">
                    <empty-page
                      v-if="!matchingTrendsErrorState"
                      type="model-features-empty"
                      :size="50"
                    >
                      <template #title>
                        <div class="title-no-notification">No data to show</div>
                      </template>
                      <template #subtitle>
                        <div class="des-no-notification">
                          IDR matching trend chart will appear here once data
                          feeds are ingested.
                        </div>
                      </template>
                    </empty-page>
                    <empty-page
                      v-else
                      class="title-no-notification"
                      type="error-on-screens"
                      :size="50"
                    >
                      <template #title>
                        <div class="title-no-notification">
                          IDR matching trends is currently unavailable
                        </div>
                      </template>
                      <template #subtitle>
                        <div class="des-no-notification">
                          Our team is working hard to fix it. Please be patient
                          and try again soon!
                        </div>
                      </template>
                    </empty-page>
                  </v-row>
                </template>
              </v-card>
            </v-col>
          </v-row>

          <data-feeds
            :data="dataFeeds"
            :is-loading="loadingDataFeeds"
            :is-error-state="dataFeedsErrorState"
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
            @close="isFilterToggled = !isFilterToggled"
          >
            <hux-filter-panels :expanded="[0]">
              <hux-filter-panel
                title="Time"
                :count="numFiltersSelected"
                :disabled="true"
                :hide-actions="true"
              >
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
import EmptyPage from "@/components/common/EmptyPage"

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
    EmptyPage,
  },

  data() {
    return {
      loadingOverview: true,
      loadingDataFeeds: true,
      loadingMatchingTrends: true,
      isFilterToggled: false,
      filterStartDate: null,
      filterEndDate: null,
      matchingTrendsErrorState: false,
      dataFeedsErrorState: false,
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
    try {
      await this.refreshData()
    } finally {
      this.setFilters({
        startDate: this.timeFrame["start_date"],
        endDate: this.timeFrame["end_date"],
      })
    }
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
      try {
        await this.loadOverview()
      } finally {
        this.loadDataFeeds()
        this.loadMatchingTrends()
      }
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
      try {
        await this.getMatchingTrends(this.selectedDateRange)
      } catch (error) {
        this.matchingTrendsErrorState = true
      } finally {
        this.loadingMatchingTrends = false
      }
    },

    async loadDataFeeds() {
      this.loadingDataFeeds = true
      try {
        await this.getDataFeeds(this.selectedDateRange)
      } catch (error) {
        this.dataFeedsErrorState = true
      } finally {
        this.loadingDataFeeds = false
      }
    },

    async loadOverview() {
      this.loadingOverview = true
      try {
        await this.getOverview(this.selectedDateRange)
      } finally {
        this.loadingOverview = false
      }
    },
  },
}
</script>
<style lang="scss" scoped>
$offset: 110px;
$headerOffsetX: 220px + 32px;
$headerOffsetY: 70px;

.idr-wrapper {
  ::v-deep .container {
    padding: 0 !important;
  }

  .idr-slide-group {
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

  .matching-trend-chart-frame {
    background-image: url("../../assets/images/no-matching-trend-chart-frame.png");
    background-position: center;
  }
}
</style>
