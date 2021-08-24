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
        />

        <hux-select
          v-model="filters.startYear"
          :items="options.years"
          label="Start year"
          class="mx-1"
          width="126"
        />

        <icon class="mx-1" type="arrow" color="primary" :size="19" />

        <hux-select
          v-model="filters.endMonth"
          :items="options.months"
          label="End month"
          class="mx-1"
          width="141"
        />

        <hux-select
          v-model="filters.endYear"
          label="End year"
          :items="options.years"
          class="mx-1"
          width="126"
        />
      </hux-filters-bar>
    </template>
    <template>
      <v-row v-if="!loadingOverview" no-gutters>
        <metric-card
          v-for="(metric, index) in overview"
          :key="index"
          :title="metric.title"
          :min-width="170"
          class="mx-2 my-2"
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
                    {{ metric.value | Numeric(true, true) }}
                  </template>
                  <template v-if="metric.format === 'percentage'">
                    {{ metric.value | Numeric(true, false, false, true) }}
                  </template>
                </span>
              </template>
              <template #hover-content>
                <template v-if="metric.format === 'numeric'">
                  {{ metric.value | Numeric(true, false) }}
                </template>
                <template v-if="metric.format === 'percentage'">
                  {{ metric.value | Numeric(false, false, false, true) }}
                </template>
              </template>
            </tooltip>
          </template>
        </metric-card>
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

import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import HuxFiltersBar from "@/components/common/FiltersBar"
import HuxSelect from "@/components/common/Select.vue"
import Icon from "@/components/common/Icon"
import MetricCard from "@/components/common/MetricCard"
import Tooltip from "@/components/common/Tooltip.vue"
import DataFeeds from "./DataFeeds.vue"

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
  },

  data() {
    return {
      loadingOverview: false,
      loadingDataFeeds: false,
      loadingMatchingTrend: false,
      isFilterToggled: false,
      options: {
        months: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ],
        years: ["2021", "2020", "2019", "2018", "2017", "2016", "2015"],
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
      dataFeeds: "identity/dataFeeds",
      identityMatchingTrend: "identity/matchingTrend",
    }),

    loading() {
      return this.loadingOverview || this.loadingDataFeeds
    },
  },

  async mounted() {
    this.loadOverview()
    this.loadDataFeeds()
    this.fetchMatchingTrend()
  },

  methods: {
    ...mapActions({
      getOverview: "identity/getOverview",
      getDataFeeds: "identity/getDataFeeds",
      getMatchingTrend: "identity/getMatchingTrend",
    }),

    async fetchMatchingTrend() {
      this.loadingMatchingTrend = true
      await this.getMatchingTrend()
      this.loadingMatchingTrend = false
    },

    async loadOverview() {
      this.loadingOverview = true
      await this.getOverview()
      this.loadingOverview = false
    },

    async loadDataFeeds() {
      this.loadingDataFeeds = true
      await this.getDataFeeds()
      this.loadingDataFeeds = false
    },
  },
}
</script>

<style lang="scss" scoped></style>
