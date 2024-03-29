<template>
  <div class="model-dashboard-wrap">
    <page-header>
      <template #left>
        <breadcrumb
          :items="breadcrumbItems"
          :add-border="true"
          :reduce-icon="true"
        />
      </template>
      <template #right>
        <tooltip>
          <template #label-content>
            <span data-e2e="model-dashboard-options">
              <icon
                type="main_screen"
                :size="40"
                class="cursor-pointer mr-7"
                color="black-darken4"
                data-e2e="version-history-button"
                @click.native="viewVersionHistory()"
              />
            </span>
          </template>
          <template #hover-content>
            <div class="px-4 py-2 white caption cursor-pointer">
              Version history
            </div>
          </template>
        </tooltip>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <div
      v-if="!loading"
      class="flex-grow-1 flex-shrink-1 mw-100 content-section"
    >
      <v-tabs v-model="tabOption" class="tabs-group">
        <v-tabs-slider color="primary"></v-tabs-slider>
        <div class="d-flex">
          <v-tab key="model" class="pa-2 mr-3 text-h3" color>
            Model performance
          </v-tab>
          <v-tab key="pipeline" class="text-h3" data-e2e="pipeline-performance">
            Pipeline performance
          </v-tab>
        </div>
      </v-tabs>
      <v-tabs-items v-model="tabOption" class="tabs-item">
        <v-tab-item key="model" class="delivery-tab">
          <template v-if="!loading" #default>
            <v-row class="mt-2">
              <v-col col="6">
                <div class="model-dashboard__card pa-4">
                  <label class="text-body-2 black--text text--lighten-4 ma-0">
                    Description
                  </label>
                  <p class="text-body-1 ma-0">
                    {{ model.description | Empty }}
                  </p>
                </div>
              </v-col>
              <v-col col="6">
                <div class="d-flex">
                  <div
                    v-for="(metric, key) in model.performance_metric"
                    :key="key"
                    data-e2e="performancemetric"
                  >
                    <metric-card
                      v-if="key === 'created_on'"
                      class="model-dashboard__card px-6 py-3 mr-2"
                      :min-width="180"
                      :height="80"
                      :title="metric"
                      subtitle="Created On"
                      :high-level="true"
                      :interactable="false"
                      :title-above="true"
                    >
                      <template #title>
                        <tooltip>
                          <template #label-content>
                            {{ metric | Numeric }}
                          </template>
                          <template #hover-content>
                            {{ metric | Empty }}
                          </template>
                        </tooltip>
                      </template>
                    </metric-card>
                    <metric-card
                      v-if="key === 'rmse' && metric > 0"
                      class="model-dashboard__card px-6 py-3 mr-2"
                      :min-width="122"
                      :height="80"
                      :title="metric"
                      subtitle="RMSE"
                      :high-level="true"
                      :interactable="false"
                      :title-above="true"
                    >
                      <template #title>
                        <tooltip>
                          <template #label-content>
                            {{ metric | Numeric }}
                          </template>
                          <template #hover-content>
                            {{ metric | Empty }}
                          </template>
                        </tooltip>
                      </template>
                    </metric-card>
                    <metric-card
                      v-if="key === 'auc' && metric > 0"
                      class="model-dashboard__card px-6 py-3 mr-2"
                      :min-width="122"
                      :height="80"
                      :title="metric"
                      subtitle="AUC"
                      :high-level="true"
                      :interactable="false"
                      :title-above="true"
                    >
                      <template #title>
                        <tooltip>
                          <template #label-content>
                            {{ metric | Numeric }}
                          </template>
                          <template #hover-content>
                            {{ metric | Empty }}
                          </template>
                        </tooltip>
                      </template>
                    </metric-card>
                    <metric-card
                      v-if="key === 'precision' && metric > 0"
                      class="model-dashboard__card px-6 py-3 mr-2"
                      :min-width="122"
                      :height="80"
                      :title="metric"
                      subtitle="Precision"
                      :high-level="true"
                      :interactable="false"
                      :title-above="true"
                    >
                      <template #title>
                        <tooltip>
                          <template #label-content>
                            {{ metric | Numeric }}
                          </template>
                          <template #hover-content>
                            {{ metric | Empty }}
                          </template>
                        </tooltip>
                      </template>
                    </metric-card>
                    <metric-card
                      v-if="key === 'recall' && metric > 0"
                      class="model-dashboard__card px-6 py-3 mr-2"
                      :min-width="122"
                      :height="80"
                      :title="metric"
                      subtitle="Recall"
                      :high-level="true"
                      :interactable="false"
                      :title-above="true"
                    >
                      <template #title>
                        <tooltip>
                          <template #label-content>
                            {{ metric | Numeric }}
                          </template>
                          <template #tooltip>
                            {{ metric | Empty }}
                          </template>
                        </tooltip>
                      </template>
                    </metric-card>
                    <metric-card
                      v-if="key === 'current_version'"
                      class="model-dashboard__card px-6 py-3 mr-2"
                      :min-width="152"
                      :height="80"
                      :title="metric"
                      :subtitle="
                        showCurrentVersion ? 'Current version' : 'Past version'
                      "
                      :high-level="true"
                      :interactable="false"
                      :title-above="true"
                      :text-color="
                        showCurrentVersion ? '' : 'var(--v-error-base)'
                      "
                    >
                      <template #title>
                        <tooltip>
                          <template #label-content>
                            {{
                              showCurrentVersion ? metric : versionData | Empty
                            }}
                          </template>
                          <template #hover-content>
                            <div class="mb-3">
                              Trained date<br />
                              {{
                                modelMetricDetails.last_trained | Date | Empty
                              }}
                            </div>
                            <div class="mb-3">
                              Fulcrum date<br />
                              {{
                                modelMetricDetails.fulcrum_date | Date | Empty
                              }}
                            </div>
                            <div class="mb-3">
                              Lookback period (days)<br />
                              {{ modelMetricDetails.lookback_window }}
                            </div>
                            <div>
                              Prediction period (days)<br />
                              {{ modelMetricDetails.prediction_window }}
                            </div>
                          </template>
                        </tooltip>
                      </template>
                    </metric-card>
                  </div>
                </div>
              </v-col>
            </v-row>
            <v-row class="pt-0">
              <v-col md="6" class="pt-0">
                <v-card
                  class="mt-2 rounded-lg box-shadow-5"
                  :height="modelFeatures.length == 0 ? 280 : 662"
                >
                  <v-progress-linear
                    :active="featuresLoading"
                    :indeterminate="featuresLoading"
                  />
                  <v-card-title
                    v-if="modelFeatures.length != 0"
                    class="chart-style pb-6 px-6 pt-5"
                  >
                    <span class="black--text text--darken-4 text-h3">
                      Top
                      {{ modelFeatures.length }}
                      feature importance
                    </span>
                  </v-card-title>
                  <feature-chart
                    v-if="!featuresLoading && modelFeatures.length != 0"
                    :feature-data="modelFeatures"
                    data-e2e="feature-chart"
                  />
                  <v-row
                    v-else-if="!featuresLoading && modelFeatures.length == 0"
                    class="model-features-frame py-14"
                  >
                    <empty-page
                      v-if="
                        modelFeatures.length == 0 && !modelFeaturesErrorState
                      "
                      type="model-features-empty"
                      :size="50"
                    >
                      <template #title>
                        <div class="title-no-notification">No data to show</div>
                      </template>
                      <template #subtitle>
                        <div class="des-no-notification">
                          Top 20 features chart will appear here once
                          {{ modelMetricDetails.name }} finishes uploading.
                          <br />
                          Please check back later.
                        </div>
                      </template>
                    </empty-page>
                    <empty-page
                      v-else-if="modelFeaturesErrorState"
                      class="title-no-notification"
                      type="error-on-screens"
                      :size="50"
                    >
                      <template #title>
                        <div class="title-no-notification">
                          Top 20 features chart is currently unavailable
                        </div>
                      </template>
                      <template #subtitle>
                        <div class="des-no-notification">
                          Our team is working hard to fix it. Please be
                          patient.<br />Thank you!
                        </div>
                      </template>
                    </empty-page>
                  </v-row>
                  <div
                    v-if="modelFeatures.length != 0"
                    class="pt-2 pb-6 text-center black--text text-body-1"
                  >
                    Score
                  </div>
                </v-card>
              </v-col>
              <v-col
                md="6"
                :class="driftChartData.length == 0 ? 'pt-3' : 'pt-0'"
              >
                <v-card
                  class="rounded-lg px-4 box-shadow-5 mt-2"
                  :height="driftChartData.length == 0 ? 280 : 662"
                >
                  <v-progress-linear
                    v-if="loadingDrift"
                    :active="loadingDrift"
                    :indeterminate="loadingDrift"
                  />
                  <div
                    v-if="driftChartData.length != 0"
                    class="pt-5 pl-2 pb-10 black--text text--darken-4 text-h3"
                  >
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
                    <span v-else class="black--text text--lighten-4">
                      AUC
                    </span>
                  </div>
                  <div ref="decisioning-drift">
                    <!-- TODO: Refactor the yAxisZeroToOne prop in upcoming changes  -->
                    <drift-chart
                      v-if="!loadingDrift && driftChartData.length != 0"
                      v-model="driftChartData"
                      :chart-dimensions="chartDimensions"
                      x-axis-format="%m/%d"
                      :enable-grid="[true, true]"
                      data-e2e="drift-chart"
                      :y-axis-zero-to-one="model.type != 'ltv'"
                    />
                    <v-row
                      v-else-if="!loadingDrift && driftChartData.length == 0"
                      class="drift-chart-frame py-14"
                    >
                      <empty-page
                        v-if="!driftChartErrorState"
                        type="drift-chart-empty"
                        :size="50"
                      >
                        <template #title>
                          <div class="title-no-notification">
                            No data to show
                          </div>
                        </template>
                        <template #subtitle>
                          <div class="des-no-notification">
                            Drift chart will appear here once
                            {{ modelMetricDetails.name }} finishes uploading.
                            <br />
                            Please check back later.
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
                            Drift chart is currently unavailable
                          </div>
                        </template>
                        <template #subtitle>
                          <div class="des-no-notification">
                            Our team is working hard to fix it. Please be
                            patient.<br />Thank you!
                          </div>
                        </template>
                      </empty-page>
                    </v-row>
                  </div>
                  <div
                    v-if="driftChartData.length != 0"
                    class="pt-2 pb-6 text-center black--text text-body-1"
                  >
                    Date
                  </div>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col col="12">
                <v-card class="rounded-lg box-shadow-5 px-6 py-5">
                  <div
                    v-if="lift.length != 0"
                    class="black--text text--darken-4 text-h3 pb-4"
                  >
                    Lift chart
                  </div>
                  <v-progress-linear
                    v-if="loadingLift"
                    :active="loadingLift"
                    :indeterminate="loadingLift"
                  />
                  <lift-chart
                    v-else-if="!loadingLift && lift.length != 0"
                    :data="lift"
                    :rmse="model.performance_metric['rmse']"
                    data-e2e="table-lift"
                  />
                  <v-row
                    v-else-if="!loadingLift && lift.length == 0"
                    class="lift-chart-frame py-14"
                  >
                    <empty-page
                      v-if="!liftErrorState"
                      type="lift-table-empty"
                      :size="50"
                    >
                      <template #title>
                        <div class="title-no-notification">No data to show</div>
                      </template>
                      <template #subtitle>
                        <div class="des-no-notification">
                          Lift chart table will appear here once
                          {{ modelMetricDetails.name }} finishes uploading.
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
                          Lift table is currently unavailable
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
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col col="12">
                <v-card
                  class="rounded-lg box-shadow-5 px-6 py-5"
                  data-e2e="table-feature"
                >
                  <div
                    v-if="dashboardFeatureSize"
                    class="black--text text--darken-4 text-h3 pb-4"
                  >
                    Features ({{ dashboardFeatureSize }})
                  </div>
                  <v-progress-linear
                    v-if="loadingModelFeatures"
                    :active="loadingModelFeatures"
                    :indeterminate="loadingModelFeatures"
                  />
                  <features-table
                    v-else-if="
                      !loadingModelFeatures && dashboardFeatureSize != 0
                    "
                    :data="dashboardFeature"
                  />
                  <v-row
                    v-else-if="
                      !loadingModelFeatures && dashboardFeatureSize == 0
                    "
                    class="lift-chart-frame py-14"
                  >
                    <empty-page
                      v-if="!featuresErrorState"
                      type="lift-table-empty"
                      :size="50"
                    >
                      <template #title>
                        <div class="title-no-notification">No data to show</div>
                      </template>
                      <template #subtitle>
                        <div class="des-no-notification">
                          Features table will appear here once
                          {{ modelMetricDetails.name }} finishes uploading.
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
                          Features table is currently unavailable
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
                </v-card>
              </v-col>
            </v-row>
          </template>
        </v-tab-item>
        <v-tab-item key="pipeline" class="delivery-tab">
          <pipeline-perfrmance></pipeline-perfrmance>
        </v-tab-item>
        <version-history
          v-model="versionHistoryDrawer"
          data-e2e="version-history"
        />
      </v-tabs-items>
    </div>
  </div>
</template>
<script>
import Breadcrumb from "@/components/common/Breadcrumb"
import Tooltip from "@/components/common/Tooltip"
import DriftChart from "@/components/common/Charts/DriftChart/DriftChart.vue"
import FeaturesTable from "./FeaturesTable.vue"
import FeatureChart from "@/components/common/featureChart/FeatureChart"
import Icon from "@/components/common/Icon"
import LiftChart from "@/components/common/LiftChart.vue"
import PageHeader from "@/components/PageHeader"
import VersionHistory from "./Drawers/VersionHistoryDrawer.vue"
import MetricCard from "@/components/common/MetricCard"
import EmptyPage from "@/components/common/EmptyPage"
import { mapGetters, mapActions } from "vuex"
import PipelinePerfrmance from "./PipelinePerfrmance"
export default {
  name: "ModelsDashboard",
  components: {
    Breadcrumb,
    Tooltip,
    FeatureChart,
    LiftChart,
    PageHeader,
    Icon,
    VersionHistory,
    DriftChart,
    FeaturesTable,
    MetricCard,
    EmptyPage,
    PipelinePerfrmance,
  },
  data() {
    return {
      loading: false,
      loadingLift: true,
      modalOptions: false,
      loadingModelFeatures: true,
      loadingDrift: true,
      featuresLoading: false,
      versionHistoryDrawer: false,
      tabOption: 0,
      chartDimensions: {
        width: 0,
        height: 0,
      },
      modelFeaturesErrorState: false,
      driftChartErrorState: false,
      liftErrorState: false,
      featuresErrorState: false,
      modelTypes: [
        "purchase",
        "prediction",
        "ltv",
        "churn",
        "propensity",
        "unsubscribe",
        "regression",
        "classification",
      ],
      versionData: null,
      showCurrentVersion: true,
    }
  },
  computed: {
    ...mapGetters({
      model: "models/overview",
      modelDetails: "models/single",
      lift: "models/lift",
      modelDashboardFeatures: "models/modelFeatures",
      drift: "models/drift",
    }),
    modelMetricDetails() {
      return this.modelDetails(this.$route.params.id) || {}
    },
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
      return this.modelDashboardFeatures
        ? this.modelDashboardFeatures.slice(0, 20)
        : []
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
      if (this.$route.params.name) {
        items.push({
          text: this.$route.params.name,
          disabled: true,
          logo: `model-${
            this.modelTypes.includes(
              this.$route.params.type
                ? this.$route.params.type.toLowerCase()
                : ""
            )
              ? this.$route.params.type.toLowerCase()
              : "unknown"
          }`,
        })
      } else if (this.model.model_name) {
        items.push({
          text: this.model.model_name,
          disabled: true,
          logo: `model-${this.model.model_type.toLowerCase()}`,
        })
      }
      return items
    },
  },
  async mounted() {
    this.loading = true
    this.chartDimensions.width = this.$refs["decisioning-drift"].clientWidth
    this.chartDimensions.height = 520
    let params = this.$route.params
    try {
      if (!this.modelDetails(params.id)) {
        await this.getModels()
      }
      await this.getOverview(params)
    } finally {
      this.fetchLift(params)
      this.fetchDrift(params)
      this.loading = false
      this.fetchModelFeatures(params) // Fetch data for Model feature table.
      this.getVersionLabel(params)
    }
  },
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    this.$store.dispatch("models/clearModelValues")
    window.removeEventListener("resize", this.sizeHandler)
  },
  methods: {
    ...mapActions({
      getOverview: "models/getOverview",
      getModels: "models/getAll",
      getLift: "models/getLift",
      getModelFeatures: "models/getModelFeatures", // used for Model feature table.
      getDrift: "models/getDrift",
    }),
    getVersionLabel(params) {
      if (params.version) {
        this.showCurrentVersion = false
        this.versionData = params.version
      } else this.showCurrentVersion = true
    },
    async fetchLift(params) {
      this.loadingLift = true
      try {
        await this.getLift(params)
      } catch (error) {
        this.liftErrorState = true
      }
      this.loadingLift = false
    },
    async fetchDrift(params) {
      this.loadingDrift = true
      try {
        await this.getDrift(params)
      } catch (error) {
        this.driftChartErrorState = true
      }
      this.loadingDrift = false
    },
    viewVersionHistory() {
      this.versionHistoryDrawer = !this.versionHistoryDrawer
    },
    async fetchFeatures(params) {
      this.featuresLoading = true
      try {
        await this.getFeatures(params)
      } catch (error) {
        this.modelFeaturesErrorState = true
      }
      this.featuresLoading = false
    },
    sizeHandler() {
      if (this.$refs["decisioning-drift"]) {
        this.chartDimensions.width = this.$refs["decisioning-drift"].clientWidth
      }
    },
    async fetchModelFeatures(params) {
      this.loadingModelFeatures = true
      try {
        await this.getModelFeatures(params)
      } catch (error) {
        this.featuresErrorState = true
      }
      this.loadingModelFeatures = false
    },
  },
}
</script>
<style lang="scss" scoped>
.model-dashboard-wrap {
  .tabs-item {
    overflow: hidden !important;
  }
  .model-dashboard__card {
    height: 80px;
    border: 1px solid var(--v-black-lighten2);
    border-radius: 12px;
  }
}
.model-features-frame {
  background-image: url("../../assets/images/no-barchart-frame.png");
  background-position: center;
}
.drift-chart-frame {
  background-image: url("../../assets/images/no-drift-chart-frame.png");
  background-position: center;
}
.lift-chart-frame {
  background-image: url("../../assets/images/no-lift-chart-frame.png");
  background-position: center;
}
//to overwrite the classes
.title-no-notification {
  font-size: 24px !important;
  line-height: 34px !important;
  font-weight: 300 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}
.des-no-notification {
  font-size: 14px !important;
  line-height: 16px !important;
  font-weight: 400 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}
.pre-formatted {
  white-space: pre;
}
::v-deep .theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active) {
  color: var(--v-black-lighten4) !important;
}
::v-deep
  .v-tabs
  .v-tabs-bar
  .v-tabs-bar__content
  .v-tabs-slider-wrapper
  .v-tabs-slider {
  margin-top: 2px !important;
}
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--v-white-base);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--v-black-lighten3);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--v-black-lighten3);
}
.content-section {
  height: calc(100vh - 180px);
  overflow-y: auto !important;
  overflow-x: hidden !important;
  padding: 30px;
}
</style>
