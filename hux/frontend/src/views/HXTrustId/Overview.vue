<template>
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
                    formatCustomerCount(
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
                    formatCustomerCount(
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
</template>
