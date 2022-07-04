<template>
  <div class="match-rate-wrapper">
    <div v-if="numMatchRates !== 0" class="match-rate">
      <div class="text-h3 black--text text--base">Match rates</div>

      <v-row class="matchrate-header mt-3 body-2">
        <v-col cols="12" md="4" class="ml-0">
          <v-item> Destination </v-item>
        </v-col>
        <v-col cols="12" md="4" class="ml-n1">
          <v-item> Match rate </v-item>
        </v-col>
        <v-col cols="12" md="4" class="ml-n5"> Last delivery </v-col>
      </v-row>

      <v-row
        v-for="d in matchRate"
        :key="d.destination"
        class="matchrate-list body-1 mx-0 my-2"
      >
        <v-col cols="12" md="4" class="matchrate-col">
          <v-item>
            <logo :type="d.destination" :size="24"></logo>
          </v-item>
        </v-col>
        <v-col cols="12" md="4" class="matchrate-col">
          <v-item>
            <size :value="d.match_rate" />
          </v-item>
        </v-col>
        <v-col cols="12" md="4" class="matchrate-col">
          <time-stamp :value="d.last_delivery" date-class="body-1" />
        </v-col>
      </v-row>
    </div>
    <div v-else class="no-match-rate">
      <metric-card
        class=""
        title="Match rates"
        :height="76"
        :interactable="false"
        title-class="text-h3"
      >
        <template #subtitle-extended>
          <div class="black--text text--lighten-4 mt-4 text-body-2">
            Add an advertising destination and deliver this audience in order to
            view associated match rates.
          </div>
        </template>
      </metric-card>
    </div>
  </div>
</template>

<script>
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import Size from "@/components/common/huxTable/Size.vue"
import Logo from "@/components/common/Logo.vue"
import MetricCard from "@/components/common/MetricCard"

export default {
  name: "StandaloneDelivery",
  components: { TimeStamp, Size, Logo, MetricCard },
  props: {
    matchRate: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {}
  },
  computed: {
    numMatchRates() {
      return this.matchRate ? this.matchRate.length : 0
    },
  },
}
</script>

<style lang="scss" scoped>
.match-rate-wrapper {
  background-color: var(--v-primary-lighten1) !important;
  padding: 20px 24px !important;
  border: 1px solid var(--v-black-lighten2);
  box-sizing: border-box;
  border-radius: 5px;
  .match-rate {
    background-color: var(--v-primary-lighten1) !important;
    .matchrate-header {
      border: none !important;
    }
    .matchrate-list {
      background-color: var(--v-white-base) !important;
      border: 1px solid var(--v-black-lighten2);
      box-sizing: border-box;
      padding-left: 16px;
      padding-top: 11px;
      border-radius: 4px;
      display: flex;
      height: 45px;
      .matchrate-col {
        color: var(--v-black-base) !important;
        padding: 0px !important;
        margin: 0px !important;
      }
    }
  }
  .no-match-rate {
    background: var(--v-primary-lighten1);
    ::v-deep .metric-card-wrapper {
      padding: 16px 0px !important;
    }
  }
}
::v-deep .titleColor {
  color: var(--v-black-base) !important;
}
::v-deep .metric-card-wrapper {
  padding: 0px 0px !important;
  border: none;
}
</style>
