<template>
  <div class="white overview-card pa-6 pt-4">
    <div v-if="data">
      <div class="text-h3">HX TrustID scores for all customers</div>
      <div class="d-flex justify-start">
        <div class="mr-4">
          <tooltip max-width="256px">
            <template #label-content>
              <score-card
                title="HX TrustID"
                icon="hx-trustid-colored"
                :value="data && data.trust_id_score"
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
          v-for="(scorecard, index) in data && data.factors"
          :key="index"
          class="mr-4"
        >
          <tooltip max-width="288px">
            <template #label-content>
              <score-card
                :title="formatText(scorecard.factor_name)"
                icon="hx-trustId-attribute"
                :value="scorecard.factor_score"
                :width="150"
                :height="90"
                :stroke="cardColors(scorecard.factor_name).stroke"
                :variant="cardColors(scorecard.factor_name).variant"
              >
                <template #progress-bar>
                  <progress-stack-bar
                    :width="81"
                    :height="6"
                    :show-percentage="false"
                    :data="
                      progressBarData(scorecard.overall_customer_rating.rating)
                    "
                    :bar-id="index"
                  />
                </template>
              </score-card>
            </template>
            <template #hover-content>
              <div class="body-2">
                <div class="mb-1">
                  {{ scorecard.factor_description }}
                </div>
                <div class="d-flex flex-column">
                  <span class="tooltip-subheading disagree-color my-2">
                    Disagree
                  </span>
                  <span>
                    {{
                      scorecard.overall_customer_rating.rating.disagree
                        .percentage | Numeric(false, false, false, true)
                    }}
                    |
                    {{
                      numberWithCommas(
                        scorecard.overall_customer_rating.rating.disagree.count
                      )
                    }}
                  </span>
                  <span class="tooltip-subheading neutral-color my-2">
                    Neutral
                  </span>
                  <span>
                    {{
                      scorecard.overall_customer_rating.rating.neutral
                        .percentage | Numeric(false, false, false, true)
                    }}
                    |
                    {{
                      numberWithCommas(
                        scorecard.overall_customer_rating.rating.neutral.count
                      )
                    }}
                  </span>
                  <span class="tooltip-subheading agree-color my-2">
                    Agree
                  </span>
                  <span>
                    {{
                      scorecard.overall_customer_rating.rating.agree.percentage
                        | Numeric(false, false, false, true)
                    }}
                    |
                    {{
                      numberWithCommas(
                        scorecard.overall_customer_rating.rating.agree.count
                      )
                    }}
                  </span>
                </div>
              </div>
            </template>
          </tooltip>
        </div>
      </div>
    </div>
    <empty-page v-else type="error-on-screens" class="pt-5" :size="50">
      <template #title>
        <div>Trust ID overview is currently unavailable</div>
      </template>
      <template #subtitle>
        <div>
          Our team is working hard to fix it. Please be patient and try again
          soon!
        </div>
      </template>
    </empty-page>
  </div>
</template>

<script>
import scoreCard from "@/components/common/scoreCard/scoreCard.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import ProgressStackBar from "@/components/common/ProgressStackBar/ProgressStackBar.vue"
import { formatText, numberWithCommas } from "@/utils"
import EmptyPage from "../../components/common/EmptyPage.vue"

export default {
  name: "HXTrustIDOverview",
  components: {
    scoreCard,
    Tooltip,
    ProgressStackBar,
    EmptyPage,
  },
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatText: formatText,
    numberWithCommas: numberWithCommas,
    cardColors(factorName) {
      switch (factorName) {
        case "humanity":
          return { stroke: "primary", variant: "darken6" }

        case "transparency":
          return { stroke: "yellow", variant: "darken1" }

        case "capability":
          return { stroke: "primary", variant: "darken5" }

        case "reliability":
          return { stroke: "secondary", variant: "lighten2" }

        default:
          return { stroke: "primary", variant: "base" }
      }
    },
    progressBarData(data) {
      if (Object.keys(data).length == 0) return []
      let dataFormatted = []
      for (const [key, value] of Object.entries(data)) {
        switch (key) {
          case "disagree":
            dataFormatted[0] = this.progressKeyValue(key, value.percentage)
            break

          case "neutral":
            dataFormatted[1] = this.progressKeyValue(key, value.percentage)
            break

          default:
            dataFormatted[2] = this.progressKeyValue(key, value.percentage)
        }
      }
      return dataFormatted
    },
    progressKeyValue(key, value) {
      return {
        label: key,
        value: parseInt(
          this.$options.filters.Numeric(value, true, false, false, true)
        ),
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.v-application {
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
