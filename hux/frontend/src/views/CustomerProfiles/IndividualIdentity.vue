<template>
  <div>
    <v-card
      v-if="insights && !profileError"
      class="rounded-lg box-shadow-5"
      height="240"
      data-e2e="chord"
    >
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
    <v-card
      v-else
      class="no-data-chart-frame pt-4 rounded-lg box-shadow-5"
      height="280px"
    >
      <empty-page
        class="title-no-notification pa-8"
        :type="profileError ? 'error-on-screens' : 'no-customer-data'"
        :size="50"
      >
        <template #title>
          <div class="title-no-notification">{{profileError ? "Individual ID unavailable" : "No customer data"}}</div>
        </template>
        <template #subtitle>
          <div class="des-no-notification">
            {{profileError ? "Our team is working hard to fix it. Please be patient and try again soon!" : "Individual ID will appear here once customer data is available."}}
          </div>
        </template>
      </empty-page>
    </v-card>
  </div>
</template>

<script>
import Icon from "../../components/common/Icon.vue"
import IdentityChart from "../../components/common/identityChart/IdentityChart.vue"
import Tooltip from "../../components/common/Tooltip.vue"
import EmptyPage from "@/components/common/EmptyPage.vue"

export default {
  name: "IndividualIdentity",
  components: { IdentityChart, Tooltip, Icon, EmptyPage },
  props: {
    insights: {
      type: Object,
      required: true,
      default: () => {},
    },
    profileError: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
<style lang="scss" scoped>
.no-data-chart-frame {
  @include no-data-frame-bg("empty-1-chart.png");
}
</style>
