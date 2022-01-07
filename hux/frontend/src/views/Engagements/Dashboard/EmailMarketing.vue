<template>
  <div>
    <delivery :section="data" class="mb-5" />

    <v-progress-linear
      :active="loadingMetrics"
      :indeterminate="loadingMetrics"
    />
    <campaign-summary
      :summary="emailSummary"
      :campaign-data="emailDataData"
      type="email"
      data-e2e="email-data"
    />
  </div>
</template>

<script>
import CampaignSummary from "@/components/CampaignSummary.vue"
import Delivery from "./Components/Delivery.vue"

export default {
  name: "EmailMarketing",
  components: { CampaignSummary, Delivery },
  props: {
    data: {
      type: Object,
      required: true,
    },
    emailData: {
      type: Object,
      required: true,
      default: () => {},
    },
    loadingMetrics: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    emailDataData() {
      return this.emailData ? this.emailData.audience_performance : []
    },
    emailSummary() {
      if (!this.emailData || (this.emailData && this.emailData.length === 0))
        return []
      return [
        {
          id: 1,
          title: "Sent",
          field: "sent",
          value:
            this.emailData && this.emailData["summary"]
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "sent")
              : "-",
        },
        {
          id: 2,
          title: "Hard bounces / Rate",
          field: "hard_bounces|hard_bounces_rate",
          value: `${`${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "hard_bounces")
              : "-"
          }|${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "hard_bounces_rate")
              : "-"
          }`}`,
        },
        {
          id: 3,
          title: "Delivered / Rate",
          field: "delivered|delivered_rate",
          value: `${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "delivered")
              : "-"
          }|${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "delivered_rate")
              : "-"
          }`,
        },
        {
          id: 4,
          title: "Open / Rate",
          field: "open|open_rate",
          value: `${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "open")
              : "-"
          }|${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "open_rate")
              : "-"
          }`,
        },
        {
          id: 5,
          title: "Click / CTR",
          field: "clicks|click_through_rate",
          value: `${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "clicks")
              : "-"
          }|${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "click_through_rate")
              : "-"
          }`,
        },
        {
          id: 6,
          title: "Click to open rate  ",
          field: "click_to_open_rate",
          value: this.emailData
            ? this.emailData &&
              this.fetchKey(this.emailData["summary"], "click_to_open_rate")
            : "-",
        },
        {
          id: 7,
          title: "Unique clicks / Unique opens",
          field: "unique_clicks|unique_opens",
          value: `${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "unique_clicks")
              : "-"
          }|${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "unique_opens")
              : "-"
          }`,
        },
        {
          id: 8,
          title: "Unsubscribe / Rate",
          field: "unsubscribe|unsubscribe_rate",
          value: `${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "unsubscribe")
              : "-"
          }|${
            this.emailData
              ? this.emailData &&
                this.fetchKey(this.emailData["summary"], "unsubscribe_rate")
              : "-"
          }`,
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
