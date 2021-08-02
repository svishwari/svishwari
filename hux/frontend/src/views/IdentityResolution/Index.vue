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
  },

  data() {
    return {
      loadingOverview: false,
      loadingDataFeeds: false,
    }
  },

  computed: {
    ...mapGetters({
      overview: "identity/overview",
      dataFeeds: "identity/dataFeeds",
    }),

    loading() {
      return this.loadingOverview || this.loadingDataFeeds
    },
  },

  async mounted() {
    this.loadOverview()
    this.loadDataFeeds()
  },

  methods: {
    ...mapActions({
      getOverview: "identity/getOverview",
      getDataFeeds: "identity/getDataFeeds",
    }),

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
