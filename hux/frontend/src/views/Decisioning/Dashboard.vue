<template>
  <page class="model-dashboard-wrap" max-width="100%">
    <template #header>
      <page-header>
        <template #left>
          <breadcrumb :items="breadcrumbItems" />
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
            <v-card-title class="chart-style pb-2 pl-5 pt-5">
              <div class="mt-2">
                <span
                  v-if="model.feature_importance"
                  class="neroBlack--text text-h5"
                >
                  Top {{ model.feature_importance.length }} feature importance
                </span>
              </div>
            </v-card-title>
            <feature-chart :feature-data="model.feature_importance || []" />
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="rounded-lg px-4 box-shadow-5 mt-6" height="662">
            <div class="pt-5 pl-2 pb-10 neroBlack--text text-h5">Drift AUC</div>
            <div ref="drift">
              <drift-chart
                v-model="lineChartData"
                :chart-dimensions="chartDimensions"
                :x-axis-formating-func="xAxisFormatingFunc"
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
            <lift-chart
              v-if="model.performance_metric"
              :data="model.lift_data || []"
              :rmse="model.performance_metric['rmse']"
            />
          </v-card>
        </v-col>
      </v-row>
    </template>
  </page>
</template>
<script>
import Breadcrumb from "@/components/common/Breadcrumb"
import FeatureChart from "@/components/common/featureChart/FeatureChart"
import LiftChart from "@/components/common/LiftChart.vue"
import DriftChart from "@/components/common/Charts/DriftChart/DriftChart.vue"

import LineChartData from "@/api/mock/factories/lineChartData.json"
import Page from "@/components/Page"
import PageHeader from "@/components/PageHeader"
import { mapGetters, mapActions } from "vuex"

export default {
  name: "ModelsDashboard",
  components: {
    Breadcrumb,
    FeatureChart,
    LiftChart,
    Page,
    PageHeader,
    DriftChart,
  },
  data() {
    return {
      loading: false,
      chartDimensions: {
        width: 0,
        height: 0,
      },
      lineChart: LineChartData.data,
    }
  },

  computed: {
    ...mapGetters({
      model: "models/overview",
    }),

    lineChartData() {
      let data = this.lineChart.map((each) => {
        return {
          xAxisValue: new Date(each.run_date),
          yAxisValue: each.drift,
        }
      })

      return data
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
    this.chartDimensions.width = this.$refs.drift.clientWidth - 110
    this.chartDimensions.height = 520
    await this.getOverview(this.$route.params.id)
    this.loading = false
  },

  methods: {
    ...mapActions({
      getOverview: "models/getOverview",
    }),
    xAxisFormatingFunc(date) {
      return `${date.getMonth() + 1}/${date.getDate()}`
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
