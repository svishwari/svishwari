<template>
  <page max-width="100%">
    <template #header>
      <page-header>
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
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>
    <template>
      <v-row no-gutters>
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
      <v-row class="px-2 mt-2">
        <v-col md="12">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="522">
            <v-card-title class="chart-style pb-12 pl-5 pt-5">
              <div class="mt-2">
                <span class="neroBlack--text text-h5">
                 ID Resolution matching trends
                </span>
              </div>
            </v-card-title>
           <IDR-Matching-Trend
           :map-data="identityMatchingTrend"
           />
          </v-card>
        </v-col>
      </v-row>

      <data-feeds
        v-if="!loadingDataFeeds"
        :data="dataFeeds"
        class="mt-6 mx-2"
      ></data-feeds>
    </template>
  </page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

import Page from "@/components/Page.vue"
import Breadcrumb from "@/components/common/Breadcrumb"
import Icon from "@/components/common/Icon"
import MetricCard from "@/components/common/MetricCard"
import PageHeader from "@/components/PageHeader"
import Tooltip from "@/components/common/Tooltip.vue"
import DataFeeds from "./DataFeeds.vue"
import IDRMatchingTrend from "@/components/common/IDRMatchingTrend/IDRMatchingTrend"

export default {
  name: "IdentityResolution",

  components: {
    Page,
    Breadcrumb,
    Icon,
    MetricCard,
    PageHeader,
    Tooltip,
    DataFeeds,
    IDRMatchingTrend
  },

  data() {
    return {
      loadingOverview: false,
      loadingDataFeeds: false,
      loadingMatchingTrend: false,
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
