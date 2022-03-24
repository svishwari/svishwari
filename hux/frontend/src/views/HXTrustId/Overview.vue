<template>
  <div class="white overview-card pa-6 pt-4">
    <div class="text-h3">HX TrustID scores for all customers</div>
    <div class="d-flex justify-start">
      <div class="mr-4">
        <tooltip max-width="256px">
          <template #label-content>
            <score-card
              title="HX TrustID"
              :value="overview && overview.trust_id_score"
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
        v-for="(scorecard, index) in overview && overview.attributes"
        :key="index"
        class="mr-4"
      >
        <tooltip max-width="288px">
          <template #label-content>
            <score-card
              :title="formatText(scorecard.attribute_name)"
              icon="hx-trustId-attribute"
              :value="scorecard.attribute_score"
              :width="150"
              :height="90"
              :stroke="colorCodes[scorecard.attribute_name].stroke"
              :variant="colorCodes[scorecard.attribute_name].variant"
            >
              <template #progress-bar>
                <progress-stack-bar
                  :width="81"
                  :height="6"
                  :show-percentage="false"
                  :value="
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
                {{ scorecard.attribute_description }}
              </div>
              <div class="d-flex flex-column">
                <span class="tooltip-subheading disagree-color my-2"
                  >Disagree</span
                >
                <span
                  >{{
                    scorecard.overall_customer_rating.rating.disagree.percentage
                      | Numeric(false, false, false, true)
                  }}
                  |
                  {{
                    numberWithCommas(
                      scorecard.overall_customer_rating.rating.disagree.count
                    )
                  }}</span
                >
                <span class="tooltip-subheading neutral-color my-2"
                  >Neutral</span
                >
                <span
                  >{{
                    scorecard.overall_customer_rating.rating.neutral.percentage
                      | Numeric(false, false, false, true)
                  }}
                  |
                  {{
                    numberWithCommas(
                      scorecard.overall_customer_rating.rating.neutral.count
                    )
                  }}</span
                >
                <span class="tooltip-subheading agree-color my-2"> Agree</span>
                <span
                  >{{
                    scorecard.overall_customer_rating.rating.agree.percentage
                      | Numeric(false, false, false, true)
                  }}
                  |
                  {{
                    numberWithCommas(
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
</template>

<script>
import { mapGetters } from "vuex"
import scoreCard from "@/components/common/scoreCard/scoreCard.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import ProgressStackBar from "@/components/common/ProgressStackBar/ProgressStackBar.vue"
import { formatText, numberWithCommas } from "@/utils"

export default {
  name: "HXTrustIDOverview",
  components: {
    scoreCard,
    Tooltip,
    ProgressStackBar,
  },
  computed: {
    ...mapGetters({
      overview: "trustId/getTrustOverview",
    }),
    colorCodes() {
      return {
        humanity: { stroke: "primary", variant: "darken6" },
        transparency: { stroke: "yellow", variant: "darken1" },
        capability: { stroke: "primary", variant: "darken5" },
        reliability: { stroke: "secondary", variant: "lighten2" },
      }
    },
  },
  methods: {
    formatText: formatText,
    numberWithCommas: numberWithCommas,
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
