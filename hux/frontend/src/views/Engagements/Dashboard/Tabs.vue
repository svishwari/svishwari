<template>
  <div class="tabs-wrapper">
    <v-tabs v-model="tabOption" class="mt-8">
      <v-tabs-slider color="primary" class="sliderCss"></v-tabs-slider>
      <div class="d-flex" data-e2e="engagement-tabs">
        <v-tab
          key="overview"
          class="pa-2 mr-3 text-h3 black--text text--lighten-4"
        >
          Overview
        </v-tab>
        <v-tab
          v-if="
            data &&
            data.destinations_category.find(
              (item) => item.category == 'Advertising'
            )
          "
          key="digital"
          class="pa-2 mr-3 text-h3 black--text text--lighten-4"
          @click="$emit('fetchMetrics', 'ads')"
        >
          Digital Advertising
        </v-tab>
        <v-tab
          v-if="
            data &&
            data.destinations_category.find(
              (item) => item.category == 'Marketing'
            )
          "
          key="email"
          class="text-h3 black--text text--lighten-4"
          @click="$emit('fetchMetrics', 'email')"
        >
          Email Marketing
        </v-tab>
      </div>
    </v-tabs>
    <v-tabs-items v-model="tabOption" class="mt-2">
      <v-tab-item key="overview">
        <overview
          :data="data"
          :loading-audiences="loadingAudiences"
          @openDeliveryHistoryDrawer="
            $emit('openDeliveryHistoryDrawer', $event)
          "
          @triggerSelectAudience="$emit('triggerSelectAudience', $event)"
          @triggerOverviewAction="$emit('onOverviewSectionAction', $event)"
          @deliverEngagement="$emit('deliverEngagement', $event)"
        />
      </v-tab-item>
      <v-tab-item
        v-if="
          data &&
          data.destinations_category.find(
            (item) => item.category == 'Advertising'
          )
        "
        key="digital"
      >
        <digital-advertising
          :data="data"
          :engagement-id="engagementId"
          :ad-data="adData"
          :loading-metrics="loadingMetrics"
          @fetchMetrics="$emit('fetchMetrics', $event)"
          @openDeliveryHistoryDrawer="
            $emit('openDeliveryHistoryDrawer', $event)
          "
          @triggerSelectAudience="$emit('triggerSelectAudience', $event)"
          @triggerSelectDestination="$emit('triggerSelectDestination', $event)"
          @onOverviewDestinationAction="
            $emit('onOverviewDestinationAction', $event)
          "
          @triggerOverviewAction="$emit('onOverviewSectionAction', $event)"
          @refreshEntityDelivery="$emit('refreshEntityDelivery', $event)"
        />
      </v-tab-item>
      <v-tab-item
        v-if="
          data &&
          data.destinations_category.find(
            (item) => item.category == 'Marketing'
          )
        "
        key="email"
      >
        <email-marketing
          :data="data"
          :engagement-id="engagementId"
          :email-data="emailData"
          :loading-metrics="loadingMetrics"
          @openDeliveryHistoryDrawer="
            $emit('openDeliveryHistoryDrawer', $event)
          "
          @triggerSelectAudience="$emit('triggerSelectAudience', $event)"
          @triggerSelectDestination="$emit('triggerSelectDestination', $event)"
          @onOverviewDestinationAction="
            $emit('onOverviewDestinationAction', $event)
          "
          @triggerOverviewAction="$emit('onOverviewSectionAction', $event)"
          @refreshEntityDelivery="$emit('refreshEntityDelivery', $event)"
        />
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import DigitalAdvertising from "./DigitalAdvertising.vue"
import EmailMarketing from "./EmailMarketing.vue"
import Overview from "./Overview.vue"

export default {
  name: "EngagementDashboardTabs",
  components: { DigitalAdvertising, EmailMarketing, Overview },
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
    adData: {
      type: Object,
      required: true,
      default: () => {},
    },
    emailData: {
      type: Object,
      required: true,
      default: () => {},
    },
    engagementId: {
      type: String,
      required: true,
      default: () => "",
    },
    loadingMetrics: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      tabOption: 0,
    }
  },
}
</script>

<style lang="scss" scoped>
.sliderCss {
  position: absolute;
  top: 2px;
}
::v-deep .v-tabs .v-tabs-bar .v-tabs-bar__content .v-tab {
  color: var(--v-black-lighten4) !important;
}
</style>
