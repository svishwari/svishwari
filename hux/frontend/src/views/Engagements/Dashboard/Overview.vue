<template>
  <div class="pt-2">
    <v-card class="overview-card px-6 py-5 card-style">
      <v-card-title class="d-flex justify-space-between pa-0">
        <h3 class="text-h3 mb-2">Engagement overview</h3>
        <div class="d-flex align-center">
          <v-btn
            text
            color="primary"
            class="text-body-1 ml-n3 mt-n2"
            data-e2e="delivery-history"
            @click="$emit('openDeliveryHistoryDrawer', $event)"
          >
            <icon
              class="mr-1"
              type="history"
              :size="24"
              :color="'primary'"
              :variant="'base'"
            />
            Delivery history
          </v-btn>
        </div>
      </v-card-title>

      <overview-metric-cards :data="data" />
    </v-card>
    <v-card class="pa-6 card-style mt-6">
      <v-card-title class="d-flex justify-space-between pa-0">
        <h3 class="text-h3 mb-2">
          <icon
            type="audiences"
            :size="24"
            color="black-darken4"
            class="mr-2"
          />
          <span class="p-absolute"
            >Audiences ({{ data.audiences.length }})</span
          >
        </h3>
        <div class="d-flex align-center">
          <v-btn
            text
            color="primary"
            class="text-body-1 ml-n3 mt-n2"
            data-e2e="deliver-all"
            @click="openDeliveryHistoryDrawer()"
          >
            <icon
              class="mr-1"
              type="deliver_2"
              :size="24"
              :color="'primary'"
              :variant="'base'"
            />
            Deliver All
          </v-btn>
        </div>
      </v-card-title>

      <delivery-table
        :section="data"
        @triggerSelectAudience="$emit('triggerSelectAudience', $event)"
      />
    </v-card>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon.vue"
import OverviewMetricCards from "./Components/OverviewMetricCards.vue"
import DeliveryTable from "./Components/DeliveryTable.vue"

export default {
  name: "Overview",
  components: { OverviewMetricCards, Icon, DeliveryTable },
  props: {
    data: {
      type: Object,
      required: true,
    },
    loadingAudiences: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.p-absolute {
  position: absolute !important;
}
.overview-card {
  height: 150px;
}
</style>
