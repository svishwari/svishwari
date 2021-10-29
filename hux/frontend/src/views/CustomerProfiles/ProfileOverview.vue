<template>
  <v-row class="d-flex pb-2">
    <v-col class="mr-3 pr-0">
      <v-card
        class="rounded-lg card-info-wrapper box-shadow-5"
        min-width="200"
        color="white"
        height="75"
      >
        <v-card-text class="py-3 px-4 d-flex flex-column">
          <span class="d-flex align-baseline mb-1">
            <span class="text-body-2 black--text text--lighten-4 mr-2">
              First
            </span>
            <tooltip>
              <template #label-content>
                <span class="text-subtitle-1 text-elipsis black--text">
                  {{ profile["first_name"] }}
                </span>
              </template>
              <template #hover-content>
                {{ profile["first_name"] }}
              </template>
            </tooltip>
          </span>
          <span class="d-flex align-baseline">
            <span class="text-body-2 black--text text--lighten-4 mr-2"
              >Last</span
            >
            <tooltip>
              <template #label-content>
                <span
                  class="
                    text-subtitle-1 text-ellipsis
                    d-block
                    max-char
                    black--text
                  "
                >
                  {{ profile["last_name"] }}
                </span>
              </template>
              <template #hover-content>
                {{ profile["last_name"] }}
              </template>
            </tooltip>
          </span>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col v-for="data in overviewList" :key="data.id" class="mr-3 px-0">
      <v-card
        class="rounded-lg card-info-wrapper card-shadow no-background"
        :data-e2e="data.e2e"
        :min-width="data.width"
        height="75"
      >
        <v-card-text class="pl-3 pr-3 pb-3 pt-3 matrix-card">
          <div class="text-body-2 black--text text--lighten-4 pb-1">
            {{ data.title }}
            <tooltip v-if="data.hoverTooltip" position-top>
              <template #label-content>
                <icon
                  v-if="data.hoverTooltip"
                  type="info"
                  :size="12"
                  class="mb-1"
                  color="primary"
                  variant="base"
                />
              </template>
              <template #hover-content>
                {{ data.hoverTooltip }}
              </template>
            </tooltip>
          </div>
          <hux-slider
            v-if="data.format === 'slider'"
            :is-range-slider="false"
            :value="data.value"
          ></hux-slider>
          <span v-else class="black--text text-subtitle-1">
            <template v-if="data.format === 'date-relative'">
              {{ data.value | Date("relative", true) | Empty }}
            </template>
          </span>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import dayjs from "dayjs"

import HuxSlider from "../../components/common/HuxSlider.vue"
import Icon from "../../components/common/Icon.vue"
import Tooltip from "../../components/common/Tooltip.vue"
export default {
  name: "ProfileOverview",
  components: { Tooltip, Icon, HuxSlider },
  props: {
    profile: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
  computed: {
    overviewList() {
      return [
        {
          id: 1,
          title: "Customer length",
          value: this.profile["since"],
          format: "date-relative",
          e2e: "customer-length",
          width: "160",
        },
        {
          id: 2,
          title: "Match confidence",
          value: this.profile["match_confidence"],
          format: "slider",
          hoverTooltip:
            "A percentage that indicates the level of certainty that all incoming records were accurately matched to a given customer.",
          e2e: "match-confidence",
          width: "175",
        },
        {
          // this value from the API is a number of months (float).
          // we first convert it to a date (eg. months ago)
          // then display this date as relative time (x days, months, years, etc)
          id: 4,
          title: "Conversion time",
          value: dayjs().subtract(this.profile["conversion_time"], "month"),
          format: "date-relative",
          hoverTooltip:
            "The average time customer takes to convert to a purchase.",
          e2e: "conversion-time",
          width: "160",
        },
        {
          id: 5,
          title: "Last click",
          value: this.profile["last_click"],
          format: "date-relative",
          e2e: "last-click",
          width: "102",
        },
        {
          id: 6,
          title: "Last purchase date",
          value: this.profile["last_purchase"],
          format: "date-relative",
          e2e: "last-purchase-date",
          width: "160",
        },
        {
          id: 7,
          title: "Last open",
          value: this.profile["last_email_open"],
          format: "date-relative",
          e2e: "last-open",
          width: "130",
        },
      ]
    },
  },
}
</script>

<style lang="scss" scoped>
.profile-overview {
  .card-info-wrapper {
    margin-right: 12px;
  }
}
.max-char {
  width: 15ch;
}
</style>
