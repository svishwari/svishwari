<template>
  <div class="match-rate-wrapper">
    <div v-if="false" class="match-rate mx-6">
      <div class="text-h3 black-base pt-5">Match rates</div>

      <v-row class="matchrate-header mt-4">
        <v-col cols="12" md="4">
          <v-item> Destination </v-item>
        </v-col>
        <v-col cols="12" md="4">
          <v-item> Match rate </v-item>
        </v-col>
        <v-col cols="12" md="4"> Last delivery </v-col>
      </v-row>

      <v-row v-for="d in deliveries" :key="d.type" class="matchrate-list">
        <v-col cols="12" md="4">
          <v-item>
            <logo :type="d.type" :size="22"></logo>
          </v-item>
        </v-col>
        <v-col cols="12" md="4">
          <v-item>
            <size :value="d.size" />
          </v-item>
        </v-col>
        <v-col cols="12" md="4">
          <time-stamp :value="d.next_delivery" />
        </v-col>
      </v-row>
    </div>
    <div v-if="true" class="no-match-rate">
      <metric-card
        class=""
        title="Match rates"
        :height="115"
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
  props: {},
  data() {
    return {
      selection: null,
      deliveries: [
        {
          name: "Facebook",
          type: "facebook",
          status: "Active",
          size: 878326,
          next_delivery: "2021-11-30T00:21:21.857Z",
        },
        {
          name: "Qualtrics",
          type: "qualtrics",
          status: "Active",
          size: 838326,
          next_delivery: "2021-11-30T01:31:31.957Z",
        },
      ],
    }
  },
  computed: {},
}
</script>

<style lang="scss" scoped>
.match-rate-wrapper {
  .match-rate {
    background-color: var(--v-primary-lighten1) !important;
    .matchrate-header {
      background-color: var(--v-primary-lighten1) !important;
      border: none !important;
    }
    .matchrate-list {
      background-color: var(--v-white-base) !important;
      border: 1px solid var(--v-black-lighten2);
      box-sizing: border-box;
      border-radius: 4px;
      display: flex;
      margin: 4px;
      height: 45px;
    }
  }
  .no-match-rate {
    background: var(--v-primary-lighten1);
  }
}
::v-deep .titleColor {
  color: var(--v-black-base) !important;
}
::v-deep .metric-card-wrapper {
  padding: 20px 24px !important;
}
</style>
