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
          <v-icon
            size="22"
            color="black lighten-3"
            class="icon-border pa-2 ma-1"
          >
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
                <div class="text-overline black--text text--darken-4">
                  {{ metric }}
                </div>
                <div
                  v-if="key === 'current_version'"
                  class="text-caption black--text text--darken-1 pt-1"
                >
                  Current version
                </div>
                <div
                  v-else-if="key === 'rmse'"
                  class="text-caption black--text text--darken-1 pt-1"
                >
                  RMSE
                </div>
                <div
                  v-else-if="key === 'auc'"
                  class="text-caption black--text text--darken-1 pt-1"
                >
                  AUC
                </div>
                <div
                  v-else-if="key === 'recall'"
                  class="text-caption black--text text--darken-1 pt-1"
                >
                  Recall
                </div>
                <div
                  v-else-if="key === 'precision'"
                  class="text-caption black--text text--darken-1 pt-1"
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
                <span
                  v-if="modelFeatures"
                  class="black--text text--darken-4 text-h5"
                >
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
            <v-progress-linear
              v-if="loadingDrift"
              :active="loadingDrift"
              :indeterminate="loadingDrift"
            />
            <div class="pt-5 pl-2 pb-10 black--text text--darken-4 text-h5">
              Drift
              <span
                v-if="
                  model.performance_metric &&
                  model.performance_metric['rmse'] !== -1
                "
                class="black--text text--darken-1"
              >
                RMSE
              </span>
              <span v-else class="black--text text--darken-1"> AUC </span>
            </div>
            <div ref="decisioning-drift">
              <drift-chart
                v-if="!loadingDrift"
                v-model="driftChartData"
                :chart-dimensions="chartDimensions"
                x-axis-format="%m/%d"
                :enable-grid="[true, true]"
              />
            </div>
            <div class="py-5 text-center black--text text--darken-4 text-h6">
              Date
            </div>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col col="12">
          <v-card class="rounded-lg box-shadow-5 px-6 py-5">
            <div class="black--text text--darken-4 text-h5 pb-4">
              Lift chart
            </div>
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
      <v-row v-if="dashboardFeatureSize">
        <v-col col="12">
          <v-card class="rounded-lg box-shadow-5 px-6 py-5">
            <div class="black--text text--darken-4 text-h5 pb-4">
              Features ({{ dashboardFeatureSize }})
            </div>
            <v-progress-linear
              v-if="loadingModelFeatures"
              :active="loadingModelFeatures"
              :indeterminate="loadingModelFeatures"
            />
            <features-table v-else :data="dashboardFeature" />
          </v-card>
        </v-col>
      </v-row>
      <version-history v-model="versionHistoryDrawer" />
    </template>
  </page>
</template>
<script>
import Breadcrumb from "@/components/common/Breadcrumb"
import DriftChart from "@/components/common/Charts/DriftChart/DriftChart.vue"
import FeaturesTable from "./FeaturesTable.vue"
import FeatureChart from "@/components/common/featureChart/FeatureChart"
import huxButton from "@/components/common/huxButton"
import LiftChart from "@/components/common/LiftChart.vue"
import Page from "@/components/Page"
import PageHeader from "@/components/PageHeader"
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
    FeaturesTable,
  },
  data() {
    return {
      loading: false,
      loadingLift: true,
      loadingModelFeatures: true,
      loadingDrift: true,
      featuresLoading: false,
      versionHistoryDrawer: false,
      chartDimensions: {
        width: 0,
        height: 0,
      },
    }
  },

  computed: {
    ...mapGetters({
      model: "models/overview",
      lift: "models/lift",
      features: "models/features",
      modelDashboardFeatures: "models/modelFeatures",
      drift: "models/drift",
    }),

    driftChartData() {
      let data = this.drift.map((each) => {
        let oldRunDate = new Date(each.run_date)
        let newRunDate = `${
          oldRunDate.getMonth() + 1
        }/${oldRunDate.getDate()}/${oldRunDate.getFullYear()}`
        return {
          xAxisValue: new Date(newRunDate),
          yAxisValue: each.drift,
        }
      })

      data.sort((a, b) => {
        let keyA = new Date(a.xAxisValue)
        let keyB = new Date(b.xAxisValue)

        if (keyA < keyB) return -1
        if (keyA > keyB) return 1
        return 0
      })

      return data
    },
    modelFeatures() {
      return this.features ? this.features.slice(0, 20) : []
    },
    // This will be used while integration of Model feature table.
    dashboardFeature() {
      return this.modelDashboardFeatures
    },
    dashboardFeatureSize() {
      return this.modelDashboardFeatures && this.modelDashboardFeatures.length
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
    this.fetchDrift()
    this.loading = false
    this.fetchFeatures()
    this.fetchModelFeatures() // Fetch data for Model feature table.
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
      getModelFeatures: "models/getModelFeatures", // used for Model feature table.
      getDrift: "models/getDrift",
    }),
    async fetchLift() {
      this.loadingLift = true
      await this.getLift(this.$route.params.id)
      this.loadingLift = false
    },
    async fetchDrift() {
      this.loadingDrift = true
      await this.getDrift(this.$route.params.id)
      this.loadingDrift = false
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
    async fetchModelFeatures() {
      this.loadingModelFeatures = true
      await this.getModelFeatures(this.$route.params.id)
      this.loadingModelFeatures = false
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
