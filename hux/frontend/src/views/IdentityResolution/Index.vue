<template>
  <page max-width="100%">
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
        <template #right>
          <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
            mdi-download
          </v-icon>
        </template>
      </page-header>

      <page-header header-height="70">
        <template #left>
          <v-btn
            icon
            :color="isFilterToggled ? 'secondary' : 'black'"
            class="mr-6"
            @click.native="isFilterToggled = !isFilterToggled"
          >
            <v-icon medium>mdi-filter-variant</v-icon>
          </v-btn>
          <v-btn disabled icon color="black" class="mr-6">
            <v-icon medium>mdi-magnify</v-icon>
          </v-btn>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <hux-filters-bar :is-toggled="isFilterToggled">
        <label class="neroBlack--text mr-2"> Select timeframe: </label>

        <hux-select
          v-model="filters.startMonth"
          :items="options.months"
          label="Start month"
          class="mx-1"
          width="141"
          @change="refreshData"
        />

        <hux-select
          v-model="filters.startYear"
          :items="options.years"
          label="Start year"
          class="mx-1"
          width="126"
          @change="refreshData"
        />

        <icon class="mx-1" type="arrow" color="primary" :size="19" />

        <hux-select
          v-model="filters.endMonth"
          :items="options.months"
          label="End month"
          class="mx-1"
          width="141"
          @change="refreshData"
        />

        <hux-select
          v-model="filters.endYear"
          label="End year"
          :items="options.years"
          class="mx-1"
          width="126"
          @change="refreshData"
        />
      </hux-filters-bar>
    </template>
    <template>
      <v-row no-gutters>
        <metric-card
          v-for="(metric, index) in overview"
          :key="index"
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
                      metric.value | Numeric(true, false, false, true) | Empty
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
                    metric.value | Numeric(false, false, false, true) | Empty
                  }}
                </template>
              </template>
            </tooltip>
          </template>
        </metric-card>
      </v-row>
      <v-row class="px-2 mt-2">
        <v-col md="12">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="422">
            <v-progress-linear
              v-if="loadingMatchingTrends"
              :active="loadingMatchingTrends"
              :indeterminate="loadingMatchingTrends"
            />
            <v-card-title class="chart-style pb-12 pl-5 pt-5">
              <div class="mt-2">
                <span class="neroBlack--text text-h5">
                  ID Resolution matching trends
                </span>
              </div>
            </v-card-title>

            <i-d-r-matching-trend
              v-if="!loadingMatchingTrends"
              :map-data="identityMatchingTrend"
            />
          </v-card>
        </v-col>
      </v-row>

      <data-feeds
        v-if="!loadingDataFeeds"
        :data="dataFeeds"
        class="mt-6 mx-2"
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
  },

  data() {
    return {
      loadingOverview: false,
      loadingDataFeeds: false,
      loadingMatchingTrends: false,
      isFilterToggled: false,
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
      dateRange: "identity/dateRange",
      dataFeeds: "identity/dataFeeds",
      identityMatchingTrend: "identity/matchingTrend",
    }),

    startDate() {
      const startDate = `${this.filters.startMonth} ${this.filters.startYear}`
      return this.$options.filters.Date(startDate, "YYYY-MM-DD")
    },
    endDate() {
      const endDate = `${this.filters.endMonth} ${this.filters.endYear}`
      return this.$options.filters.Date(endDate, "YYYY-MM-DD")
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
      startDate: this.dateRange["start_date"],
      endDate: this.dateRange["end_date"],
    })
  },

  methods: {
    ...mapActions({
      getOverview: "identity/getOverview",
      getDataFeeds: "identity/getDataFeeds",
      getMatchingTrends: "identity/getMatchingTrend",
    }),

    async refreshData() {
      await this.loadOverview()
      this.loadDataFeeds()
      await this.loadMatchingTrends()
    },

    setFilters({ startDate, endDate }) {
      if (startDate && endDate) {
        const month = "MMMM"
        const year = "YYYY"
        this.filters.startMonth = this.$options.filters.Date(startDate, month)
        this.filters.startYear = this.$options.filters.Date(startDate, year)
        this.filters.endMonth = this.$options.filters.Date(endDate, month)
        this.filters.endYear = this.$options.filters.Date(endDate, year)
      }
    },

    async loadMatchingTrends() {
      this.loadingMatchingTrends = true
      await this.getMatchingTrends({
        startDate: this.startDate,
        endDate: this.endDate,
      })
      this.loadingMatchingTrends = false
    },

    async loadDataFeeds() {
      this.loadingDataFeeds = true
      await this.getDataFeeds({
        startDate: this.startDate,
        endDate: this.endDate,
      })
      this.loadingDataFeeds = false
    },

    async loadOverview() {
      this.loadingOverview = true
      await this.getOverview({
        startDate: this.startDate,
        endDate: this.endDate,
      })
      this.loadingOverview = false
    },
  },
}
</script>

<style lang="scss" scoped></style>
