<template>
  <v-card class="rounded-lg box-shadow-5" height="240" data-e2e="chord">
    <v-card-title class="card-heading chart-style py-5 pl-6 d-flex">
      <h3 class="text-h3">Individual Identity</h3>
      <tooltip position-top>
        <template #label-content>
          <icon
            type="info"
            :size="10"
            class="mb-1 ml-1"
            color="primary"
            variant="base"
          />
        </template>
        <template #hover-content>
          Most recent co-occurence between identifiers
        </template>
      </tooltip>
    </v-card-title>
    <identity-chart :chart-data="insights"></identity-chart>
  </v-card>
</template>

<script>
import Icon from "../../components/common/Icon.vue"
import IdentityChart from "../../components/common/identityChart/IdentityChart.vue"
import Tooltip from "../../components/common/Tooltip.vue"

export default {
  name: "InvidualIdentity",
  components: { IdentityChart, Tooltip, Icon },
  props: {
    insights: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
}
</script>
