<template>
  <div>
    <delivery :section="data" class="mb-5" />
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

export default {
  name: "DigitalAdvertising",
  components: { Delivery, CampaignSummary },
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
      return obj && obj[key] ? obj[key] : "-"
    },
  },
}
</script>

<style lang="scss" scoped></style>
