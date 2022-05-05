<template>
  <div>
    <delivery
      :sections="
        data &&
        data.destinations_category.find(
          (item) => item.category == 'Advertising'
        ).destinations
      "
      :engagement-id="engagementId"
      :headers="columnDefs"
      section-type="destinations"
      deliveries-key="destination_audiences"
      class="mb-5"
      data-e2e="advertising-overview"
      @triggerSelectAudience="$emit('triggerSelectAudience', $event)"
      @refreshEntityDelivery="$emit('refreshEntityDelivery', $event)"
      @onOverviewDestinationAction="
        $emit('onOverviewDestinationAction', $event)
      "
      @triggerOverviewAction="$emit('triggerOverviewAction', $event)"
    >
      <template #title-left>
        <div class="d-flex align-center text-h3">
          <icon
            type="destinations"
            :size="24"
            color="black-darken4"
            class="mr-2"
          />
          Delivery Overview
        </div>
      </template>
      <template #title-right>
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
            Delivery History
          </v-btn>
        </div>
      </template>
    </delivery>
    <v-progress-linear
      :active="loadingMetrics"
      :indeterminate="loadingMetrics"
    />
    <campaign-summary
      :summary="displayAdsSummary"
      :campaign-data="audiencePerformanceAdsData"
      :engagement-id="engagementId"
      type="ads"
      data-e2e="ads-data"
      @onUpdateCampaignMappings="$emit('fetchMetrics', 'ads')"
    />
  </div>
</template>

<script>
import Delivery from "./Components/Delivery.vue"
import CampaignSummary from "@/components/CampaignSummary.vue"
import Icon from "@/components/common/Icon.vue"

export default {
  name: "DigitalAdvertising",
  components: { Delivery, CampaignSummary, Icon },
  props: {
    data: {
      type: Object,
      required: true,
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
    adData: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
  data() {
    return {
      columnDefs: [
        {
          text: "Audiences",
          value: "name",
          width: "30%",
        },
        {
          text: "Status",
          value: "status",
          width: "10%",
        },
        {
          text: "Target size",
          value: "size",
          width: "15%",
          hoverTooltip:
            "Average order value for all customers (known and anyonymous) for all time.",
          tooltipWidth: "201px",
        },
        {
          text: "Match Rate",
          value: "match_rate",
          width: "15%",
        },
        {
          text: "Last Delivery",
          value: "update_time",
          width: "15%",
        },
        {
          text: "Replace",
          value: "replace",
          width: "15%",
        },
      ],
    }
  },
  computed: {
    audiencePerformanceAdsData() {
      return this.adData ? this.adData.audience_performance : []
    },
    displayAdsSummary() {
      if (!this.adData || (this.adData && this.adData.length === 0)) return []
      return [
        {
          id: 1,
          title: "Spend",
          field: "spend",
          value: this.adData
            ? this.adData && this.fetchKey(this.adData["summary"], "spend")
            : "-",
        },
        {
          id: 2,
          field: "reach",
          title: "Reach",
          value: this.adData
            ? this.adData && this.fetchKey(this.adData["summary"], "reach")
            : "-",
        },
        {
          id: 3,
          title: "Impressions",
          field: "impressions",
          value: this.adData
            ? this.adData &&
              this.fetchKey(this.adData["summary"], "impressions")
            : "-",
        },
        {
          id: 4,
          title: "Conversions",
          field: "conversions",
          value: this.adData
            ? this.adData &&
              this.fetchKey(this.adData["summary"], "conversions")
            : "-",
        },
        {
          id: 5,
          title: "Clicks",
          field: "clicks",
          value: this.adData
            ? this.adData && this.fetchKey(this.adData["summary"], "clicks")
            : "-",
        },
        {
          id: 6,
          title: "Frequency",
          field: "frequency",
          value: this.adData
            ? this.adData && this.fetchKey(this.adData["summary"], "frequency")
            : "-",
        },
        {
          id: 7,
          title: "CPM",
          field: "cost_per_thousand_impressions",
          value: this.adData
            ? this.adData &&
              this.fetchKey(
                this.adData["summary"],
                "cost_per_thousand_impressions"
              )
            : "-",
        },
        {
          id: 8,
          title: "CTR",
          field: "click_through_rate",
          value: this.adData
            ? this.adData &&
              this.fetchKey(this.adData["summary"], "click_through_rate")
            : "-",
        },
        {
          id: 9,
          title: "CPA",
          field: "cost_per_action",
          value: this.adData
            ? this.adData &&
              this.fetchKey(this.adData["summary"], "cost_per_action")
            : "-",
        },
        {
          id: 10,
          title: "CPC",
          field: "cost_per_click",
          value:
            this.adData &&
            this.fetchKey(this.adData["summary"], "cost_per_click"),
        },
        {
          id: 11,
          title: "Engagement rate",
          field: "engagement_rate",
          value:
            this.adData &&
            this.fetchKey(this.adData["summary"], "engagement_rate"),
        },
      ]
    },
  },
  methods: {
    fetchKey(obj, key) {
      return obj && !isNaN(obj[key]) ? obj[key] : "-"
    },
  },
}
</script>

<style lang="scss" scoped></style>
