<template>
  <page max-width="100%" class="hx-trust-id-wrapper">
    <template #header>
      <page-header
        class="page-header py-5"
        header-min-height="110"
        header-max-height="120"
      >
        <template #left>
          <div>
            <breadcrumb
              :items="[
                {
                  text: 'HX TrustID',
                  disabled: true,
                  href: '/hx-trustid',
                  icon: 'hx-trustid-colored',
                  iconSize: 36,
                  iconColor: 'black',
                  iconColorVariant: 'base',
                },
              ]"
            />
          </div>
          <div class="text-subtitle-1 font-weight-regular pt-0 pl-0">
            Measure the signals of trust, predict how trust sentiment will
            impact customer &nbsp; employee behaviors, and identify actions to
            (re)build trust.
          </div>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>
    <div class="ma-1">
      <score-card :width="150" :height="90" title="Transparency" :value="73" />
    </div>
    <div class="ma-1">
      <score-card :width="150" :height="90" title="Humanity" :value="71">
        <template #progress-bar>
          <progress-stack-bar
            :width="81"
            :height="6"
            :show-percentage="false"
          />
        </template>
      </score-card>
    </div>
    <div>
      <score-card :width="150" :height="90" />
      <v-tabs v-model="tabOption" class="mt-8">
        <v-tabs-slider color="primary" class="sliderCss"></v-tabs-slider>
        <div class="d-flex">
          <v-tab
            key="comparison"
            class="pa-2 mr-3 text-h3"
            color
            data-e2e="comparison-tab"
          >
            Comparison
          </v-tab>
          <v-tab key="attributes" class="text-h3" data-e2e="attributes-tab">
            Attributes
          </v-tab>
        </div>
      </v-tabs>
      <v-tabs-items v-model="tabOption" class="mt-2 tabs-item">
        <v-tab-item key="comparison" class="tab-item">
          <v-row>
            <v-col md="12">
              <v-card
                class="mt-3 rounded-lg box-shadow-5 tab-card-1"
                height="365"
              >
                <v-progress-linear
                  v-if="loading"
                  :active="loading"
                  :indeterminate="loading"
                />
                <v-card-title class="pb-2 pl-6 pt-5">
                  <span class="d-flex">
                    <h3 class="text-h3">HX TrustID scores across segments</h3>
                  </span>
                </v-card-title>
                <trust-comparison-chart
                    :segment-scores="segmentScores"
                    data-e2e="trust-comparison-chart"
                  />
              </v-card>
            </v-col>
          </v-row>
        </v-tab-item>
        <v-tab-item key="attributes" class="tab-item"> </v-tab-item>
      </v-tabs-items>
      <progress-stack-bar :width="180" :height="6" :show-percentage="true" />
    </div>
  </page>
</template>

<script>
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import scoreCard from "@/components/common/scoreCard/scoreCard.vue"
import TrustComparisonChart from "@/components/common/TrustIDComparisonChart/TrustComparisonChart"
import segmentScores from "@/api/mock/fixtures/segmentScores.js"
import ProgressStackBar from "@/components/common/ProgressStackBar/ProgressStackBar.vue"

export default {
  name: "HXTrustID",
  components: {
    Page,
    PageHeader,
    Breadcrumb,
    scoreCard,
    TrustComparisonChart,
    ProgressStackBar,
  },
  data() {
    return {
      loading: false,
      tabOption: 0,
      segmentScores: segmentScores.scores
    }
  },
}
</script>

<style lang="scss" scoped>
.hx-trust-id-wrapper {
  ::v-deep .v-breadcrumbs {
    li {
      font-family: Open Sans Light;
      font-size: 28px;
      font-style: normal;
      font-weight: 400 !important;
      line-height: 40px;
      letter-spacing: 0px;
      text-align: left;
    }
  }

  .overview-card {
    border-radius: 12px !important;
  }
}
</style>
