<template>
  <Page class="model-dashboard-wrap" max-width="100%">
    <template #header>
      <PageHeader>
        <template #left>
          <Breadcrumb :items="items" />
        </template>
      </PageHeader>
    </template>
    <template #default>
      <v-row>
        <v-col col="6">
          <div class="model-dashboard__card px-6 py-5">
            {{ model.description }}
          </div>
          <div
            class="
              d-flex
              justify-center
              align-center
              mt-6
              rounded-lg
            "
          >
          <feature-chart :featureData="featureChartData" ></feature-chart>
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
                  Current Version
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
          <v-card
            class="
              d-flex
              justify-center
              align-center
              mt-6
              rounded-lg
              box-shadow-5
            "
            height="662"
          >
            <EmptyStateChart />
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col col="12">
          <v-card class="rounded-lg box-shadow-5 px-6 py-5">
            <div class="neroBlack--text text-h5 pb-4">Lift chart</div>
            <LiftChart />
          </v-card>
        </v-col>
      </v-row>
    </template>
  </Page>
</template>
<script>
import Breadcrumb from "@/components/common/Breadcrumb"
import EmptyStateChart from "@/components/common/EmptyStateChart"
import FeatureChart from "@/components/common/featureChart/FeatureChart"
import LiftChart from "@/components/common/LiftChart.vue"
import Page from "@/components/Page"
import PageHeader from "@/components/PageHeader"
import data from "@/components/common/featureChart/featureData.json"

export default {
  name: "ModelsDashboard",
  components: {
    Breadcrumb,
    EmptyStateChart,
    FeatureChart,
    LiftChart,
    Page,
    PageHeader,
  },
  data() {
    return {
      //TODO: API integration
      featureChartData: data,
      model: {
        model_name: "Propensity to Unsubscribe",
        description:
          "A propensity to unsubscribe model predicts how likely it is that a customer will unsubscribe from your email list at any given point in time",
        performance_metric: {
          rmse: -1,
          auc: 0.79,
          precision: 0.82,
          recall: 0.65,
          current_version: "3.1.2",
        },
        model_type: "ltv",
      },
      items: [
        {
          text: "Models",
          disabled: false,
          href: "/models",
          icon: "models",
        },
        {
          text: "Propensity to Unsubscribe",
          disabled: true,
          icon: "model-unsubscribe",
        },
      ],
    }
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
