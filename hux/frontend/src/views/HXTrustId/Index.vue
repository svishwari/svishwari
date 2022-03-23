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
    <template>
      <div>
        <div class="white overview-card pa-6 pt-4">
          <div class="text-h3">HX TrustID scores for all customers</div>
          <div class="d-flex justify-start">
            <div class="mr-4">
              <tooltip max-width="256px">
                <template #label-content>
                  <score-card
                    title="HX TrustID"
                    :value="overview.trust_id_score"
                    :width="150"
                    :height="90"
                  />
                </template>
                <template #hover-content>
                  <span class="body-2">
                    HX TrustID is scored on a scale between -100 to 100
                  </span>
                </template>
              </tooltip>
            </div>
            <div
              v-for="(scorecard, index) in overview.attributes"
              :key="index"
              class="mr-4"
            >
              <tooltip max-width="288px">
                <template #label-content>
                  <score-card
                    :title="capitalizeAttributeName(scorecard.attribute_name)"
                    icon="hx-trustid-attribute"
                    :value="scorecard.attribute_score"
                    :width="150"
                    :height="90"
                    stroke="trustId"
                    :variant="mapColorByAttribute(scorecard.attribute_name)"
                  >
                    <template #progress-bar>
                      <progress-stack-bar
                        :width="81"
                        :height="6"
                        :show-percentage="false"
                        :value="
                          progressBarData(
                            scorecard.overall_customer_rating.rating
                          )
                        "
                        :bar-id="index"
                      />
                    </template>
                  </score-card>
                </template>
                <template #hover-content>
                  <div class="body-2">
                    <div class="mb-1">
                      {{ scorecard.attribute_description }}
                    </div>
                    <div class="d-flex flex-column">
                      <span class="trust-tooltip-rating disagree-color my-2"
                        >Disagree</span
                      >
                      <span
                        >{{
                          scorecard.overall_customer_rating.rating.disagree
                            .percentage | Numeric(false, false, false, true)
                        }}
                        |
                        {{
                          formatCustomerCount(
                            scorecard.overall_customer_rating.rating.disagree
                              .count
                          )
                        }}</span
                      >
                      <span class="trust-tooltip-rating neutral-color my-2"
                        >Neutral</span
                      >
                      <span
                        >{{
                          scorecard.overall_customer_rating.rating.neutral
                            .percentage | Numeric(false, false, false, true)
                        }}
                        |
                        {{
                          formatCustomerCount(
                            scorecard.overall_customer_rating.rating.neutral
                              .count
                          )
                        }}</span
                      >
                      <span class="trust-tooltip-rating agree-color my-2">
                        Agree</span
                      >
                      <span
                        >{{
                          scorecard.overall_customer_rating.rating.agree
                            .percentage | Numeric(false, false, false, true)
                        }}
                        |
                        {{
                          formatCustomerCount(
                            scorecard.overall_customer_rating.rating.agree.count
                          )
                        }}</span
                      >
                    </div>
                  </div>
                </template>
              </tooltip>
            </div>
          </div>
        </div>
      </div>
      <div>
        <v-tabs v-model="tabOption" class="mt-6">
          <v-tabs-slider color="primary" class="tab-slider"></v-tabs-slider>
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
    </div>
    <div>
      <link-dropdown
        :data-list="getSegment"
        :width="245"
        @onselect="getSelectedData"
      ></link-dropdown>
    </div>
    </template>
  </page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import LinkDropdown from "@/components/common/LinkDropdown.vue"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import scoreCard from "@/components/common/scoreCard/scoreCard.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import ProgressStackBar from "@/components/common/ProgressStackBar/ProgressStackBar.vue"
import TrustComparisonChart from "@/components/common/TrustIDComparisonChart/TrustComparisonChart"
import segmentScores from "@/api/mock/fixtures/segmentComparisonScores.js"
import { formatText, numberWithCommas } from "@/utils"

export default {
  name: "HXTrustID",
  components: {
    Breadcrumb,
    LinkDropdown,
    Page,
    PageHeader,
    scoreCard,
    Tooltip,
    ProgressStackBar,
    TrustComparisonChart,
  },
  data() {
    return {
      loading: false,
      tabOption: 0,
      segmentScores: segmentScores,
      selectedSegment: null,
    }
  },
  computed: {
    ...mapGetters({
      overview: "users/getTrustOverview",
    }),
    getSegment() {
      return this.segmentScores.map((item) => {
        return item.segment_filter
      })
    },
  },
  async mounted() {
    await this.getOverview()
  },
  methods: {
    ...mapActions({
      getOverview: "users/getTrustIdOverview",
    }),
    capitalizeAttributeName(name) {
      return formatText(name)
    },
    formatCustomerCount(value) {
      return numberWithCommas(value)
    },
    getSelectedData(value) {
      this.selectedSegment = value
    },
    mapColorByAttribute(name) {
      switch (name) {
        case "humanity":
          return "base"
        case "transparency":
          return "lighten1"
        case "capability":
          return "lighten2"
        case "reliability":
          return "lighten3"
        default:
          return "base"
      }
    },
    progressBarData(data) {
      let dataFormatted = []
      for (const [key, value] of Object.entries(data)) {
        switch (key) {
          case "disagree":
            dataFormatted[0] = { label: key, value: value.percentage * 100 }
            break

          case "neutral":
            dataFormatted[1] = { label: key, value: value.percentage * 100 }
            break

          default:
            dataFormatted[2] = { label: key, value: value.percentage * 100 }
        }
      }
      return dataFormatted
    },
  },
}
</script>

<style lang="scss" scoped>
.v-application {
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
      width: 100%;
      border-radius: 12px !important;
      ::v-deep {
        .text-h3 {
          margin-top: 2px !important ;
          margin-bottom: 18px !important;
        }
      }
    }
    ::v-deep .theme--light.v-tabs {
      .v-tabs-bar .v-tab:not(.v-tab--active) {
        color: var(--v-black-lighten4) !important;
      }
    }
    .tab-slider {
      position: absolute;
      top: 2px;
    }
  }
  .disagree-color {
    color: var(--v-error-base);
  }
  .neutral-color {
    color: var(--v-yellow-base);
  }
  .agree-color {
    color: var(--v-success-lighten3);
  }
}
</style>
