<template>
  <page class="model-dashboard-wrap" max-width="100%">
    <template #header>
      <page-header>
        <template #left>
          <breadcrumb :items="breadcrumbItems" />
        </template>
        <template #right>
          <hux-button
            class="mr-4 pa-3"
            is-custom-icon
            is-tile
            icon="history"
            variant="white"
            @click="viewVersionHistory()"
          >
            Version history
          </hux-button>
          <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
            mdi-download
          </v-icon>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>
    <template v-if="!loading" #default>
      <v-row>
        <v-col col="6">
          <div class="model-dashboard__card px-6 py-5">
            {{ model.description }}
          </div>
        </v-col>
        <v-col col="6">
          <div class="d-flex">
            <div v-for="(metric, key) in model.performance_metric" :key="key">
              <div
                v-if="metric !== -1"
                class="model-dashboard__card px-6 py-3 mr-2"
              >
                <div class="text-overline neroBlack--text">
                  {{ metric }}
                </div>
                <div
                  v-if="key === 'current_version'"
                  class="text-caption gray--text pt-1"
                >
                  Current version
                </div>
                <div
                  v-else-if="key === 'rmse'"
                  class="text-caption gray--text pt-1"
                >
                  RMSE
                </div>
                <div
                  v-else-if="key === 'auc'"
                  class="text-caption gray--text pt-1"
                >
                  AUC
                </div>
                <div
                  v-else-if="key === 'recall'"
                  class="text-caption gray--text pt-1"
                >
                  Recall
                </div>
                <div
                  v-else-if="key === 'precision'"
                  class="text-caption gray--text pt-1"
                >
                  Precision
                </div>
              </div>
            </div>
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col md="6">
          <v-card class="mt-6 rounded-lg box-shadow-5" height="662">
            <v-progress-linear
              :active="featuresLoading"
              :indeterminate="featuresLoading"
            />
            <v-card-title class="chart-style pb-2 pl-5 pt-5">
              <div class="mt-2">
                <span v-if="modelFeatures" class="neroBlack--text text-h5">
                  Top
                  {{ modelFeatures.length }}
                  feature importance
                </span>
              </div>
            </v-card-title>
            <feature-chart
              v-if="!featuresLoading"
              :feature-data="modelFeatures"
            />
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="rounded-lg px-4 box-shadow-5 mt-6" height="662">
            <div class="pt-5 pl-2 pb-10 neroBlack--text text-h5">
              Drift
              <span
                v-if="
                  model.performance_metric &&
                  model.performance_metric['rmse'] !== -1
                "
                class="gray--text"
              >
                RMSE
              </span>
              <span v-else class="gray--text"> AUC </span>
            </div>
            <div ref="decisioning-drift">
              <drift-chart
                v-model="driftChartData"
                :chart-dimensions="chartDimensions"
                x-axis-format="%m/%d"
                :enable-grid="[false, true]"
              />
            </div>
            <div class="py-5 text-center neroBlack--text text-h6">Date</div>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col col="12">
          <v-card class="rounded-lg box-shadow-5 px-6 py-5">
            <div class="neroBlack--text text-h5 pb-4">Lift chart</div>
            <v-progress-linear
              v-if="loadingLift"
              :active="loadingLift"
              :indeterminate="loadingLift"
            />
            <lift-chart
              v-else
              :data="lift"
              :rmse="model.performance_metric['rmse']"
            />
          </v-card>
        </v-col>
      </v-row>
      <version-history v-model="versionHistoryDrawer" />
    </template>
  </page>
</template>
<script>
import Breadcrumb from "@/components/common/Breadcrumb"
import FeatureChart from "@/components/common/featureChart/FeatureChart"
import LiftChart from "@/components/common/LiftChart.vue"
import DriftChart from "@/components/common/Charts/DriftChart/DriftChart.vue"

import DriftChartData from "@/api/mock/factories/driftChartData.json"
import Page from "@/components/Page"
import PageHeader from "@/components/PageHeader"
import huxButton from "@/components/common/huxButton"
import VersionHistory from "./Drawers/VersionHistoryDrawer.vue"
import { mapGetters, mapActions } from "vuex"

export default {
  name: "ModelsDashboard",
  components: {
    Breadcrumb,
    FeatureChart,
    LiftChart,
    Page,
    PageHeader,
    huxButton,
    VersionHistory,
    DriftChart,
  },
  data() {
    return {
      loading: false,
      loadingLift: true,
      featuresLoading: false,
      versionHistoryDrawer: false,
      chartDimensions: {
        width: 0,
        height: 0,
      },
      chartData: DriftChartData.data,
    }
  },

  computed: {
    ...mapGetters({
      model: "models/overview",
      lift: "models/lift",
      features: "models/features",
    }),

    driftChartData() {
      let data = this.chartData.map((each) => {
        return {
          xAxisValue: new Date(each.run_date),
          yAxisValue: each.drift,
        }
      })

      return data
    },
    modelFeatures() {
      return this.features ? this.features.slice(0, 20) : []
    },

    breadcrumbItems() {
      const items = [
        {
          text: "Models",
          disabled: false,
          href: this.$router.resolve({ name: "Models" }).href,
          icon: "models",
        },
      ]
      if (this.model.model_name) {
        items.push({
          text: this.model.model_name,
          disabled: true,
          icon: `model-${this.model.model_type}`,
        })
      }
      return items
    },
  },

  async mounted() {
    this.loading = true
    this.chartDimensions.width = this.$refs["decisioning-drift"].clientWidth
    this.chartDimensions.height = 520
    await this.getOverview(this.$route.params.id)
    this.fetchLift()
    this.loading = false
    this.fetchFeatures()
  },

  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },

  updated() {
    if (this.$refs["decisioning-drift"]) {
      this.chartDimensions.width = this.$refs["decisioning-drift"].clientWidth
    }
  },

  methods: {
    ...mapActions({
      getOverview: "models/getOverview",
      getLift: "models/getLift",
      getFeatures: "models/getFeatures",
    }),
    async fetchLift() {
      this.loadingLift = true
      await this.getLift(this.$route.params.id)
      this.loadingLift = false
    },
    viewVersionHistory() {
      this.versionHistoryDrawer = !this.versionHistoryDrawer
    },
    async fetchFeatures() {
      this.featuresLoading = true
      await this.getFeatures(this.$route.params.id)
      this.featuresLoading = false
    },
    sizeHandler() {
      this.chartDimensions.width = this.$refs["decisioning-drift"].clientWidth
    },
  },
}
</script>
<style lang="scss" scoped>
.model-dashboard-wrap {
  .model-dashboard__card {
    height: 80px;
    border: 1px solid var(--v-zircon-base);
    border-radius: 12px;
  }
}
</style>
