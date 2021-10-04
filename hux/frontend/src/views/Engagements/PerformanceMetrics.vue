<template>
  <div>
    <v-tabs v-model="tabOption" class="mt-8">
      <v-tabs-slider color="primary"></v-tabs-slider>
      <div class="d-flex">
        <v-tab
          key="displayAds"
          class="pa-2 mr-3"
          color
          @click="$emit('fetchMetrics', 'ads')"
        >
          Digital Advertising
        </v-tab>
        <v-tab
          key="email"
          class="text-h5"
          @click="$emit('fetchMetrics', 'email')"
        >
          Email Marketing
        </v-tab>
      </div>
      <div>
        <tooltip>
          <template #label-content>
            <v-icon
              size="22"
              :color="myIconColor"
              class="icon-border pa-2 ma-1 mr-0"
              :disabled="
                !hasData(emailDataData, 'performance') &&
                !hasData(audiencePerformanceAdsData, 'performance')
              "
            >
              @mousedown="changeColorOnSelect()" @mouseup="
              changeColorOnDeselect() initiateMetricsDownload() " > mdi-download
            </v-icon>
          </template>
          <template #hover-content>
            <div class="tooltipdownloadmetrics">
              {{ tooltipValue }}
            </div>
          </template>
        </tooltip>
      </div>
    </v-tabs>
    <v-tabs-items v-model="tabOption" class="mt-2">
      <v-tab-item key="displayAds">
        <v-progress-linear
          :active="loadingMetrics"
          :indeterminate="loadingMetrics"
        />
        <campaign-summary
          :summary="displayAdsSummary"
          :campaign-data="audiencePerformanceAdsData"
          :engagement-id="engagementId"
          type="ads"
          @onUpdateCampaignMappings="$emit('fetchMetrics', 'ads')"
        />
      </v-tab-item>
      <v-tab-item key="email">
        <v-progress-linear
          :active="loadingMetrics"
          :indeterminate="loadingMetrics"
        />
        <campaign-summary
          :summary="emailSummary"
          :campaign-data="emailDataData"
          type="email"
        />
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import { saveFile } from "@/utils"
import { mapActions } from "vuex"
import CampaignSummary from "../../components/CampaignSummary.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "EngagementPerformanceMetrics",
  components: {
    CampaignSummary,
    Tooltip,
  },
  props: {
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
      myIconColor: "primary",
      tooltipValue:
        "Download Email Marketing and Digital Advertising performance metrics as CSVs.",
    }
  },
  computed: {
    audiencePerformanceAdsData() {
      return this.adData ? this.adData.audience_performance : []
    },
    emailDataData() {
      return this.emailData ? this.emailData.audience_performance : []
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
    ...mapActions({
      downloadAudienceMetrics: "engagements/fetchAudienceMetrics",
      setAlert: "alerts/setAlert",
    }),
    async initiateMetricsDownload() {
      this.setAlert({
        type: "pending",
        message:
          "The download has started. Please be patient while it finishes.",
      })
      const fileBlob = await this.downloadAudienceMetrics({
        id: this.engagementId,
      })
      saveFile(fileBlob)
    },
    fetchKey(obj, key) {
      return obj && obj[key] ? obj[key] : "-"
    },
    changeColorOnSelect() {
      this.myIconColor = "secondary"
    },
    changeColorOnDeselect() {
      this.myIconColor = "primary"
    },
    hasData(data, type) {
      if (data && Array.isArray(data)) {
        if (type === "summary") {
          return !data
            .map((o) => o.value)
            .every((o) => o === "-" || o === "-|-")
        } else {
          if (data.length === 0) return false
          if (
            data.length === 1 &&
            data[0] &&
            data[0]["destinations"] &&
            data[0]["destinations"].length === 0
          ) {
            const _temp = JSON.parse(JSON.stringify(data[0]))
            delete _temp.destinations
            delete _temp.id
            delete _temp.name
            delete _temp.is_mapped
            const uniqueValues = [...new Set(Object.values(_temp))].join()
            if (uniqueValues === "0") return false
          }
          return true
        }
      }
      return false
    },
  },
}
</script>

<style lang="scss" scoped>
.v-tabs {
  ::v-deep .v-tabs-bar {
    background: transparent !important;
    .v-tabs-bar__content {
      border-bottom: 2px solid var(--v-zircon-base);
      display: flex;
      justify-content: space-between;
      .v-tabs-slider-wrapper {
        width: 128px;
        .v-tabs-slider {
          background-color: var(--v-primary-lighten8) !important;
          border-color: var(--v-primary-lighten8) !important;
        }
      }
      .v-tab {
        text-transform: inherit;
        padding: 8px;
        color: var(--v-primary-base) !important;
        font-size: 15px !important;
        line-height: 20px;
        letter-spacing: inherit;
        svg {
          fill: transparent !important;
          path {
            stroke: var(--v-primary-base);
          }
        }
        &.v-tab--active {
          color: var(--v-primary-lighten8) !important;
          svg {
            path {
              stroke: var(--v-primary-lighten8);
            }
          }
        }
      }
      .v-icon {
        bottom: 4px;
      }
    }
  }
}
.v-tabs-items {
  overflow: inherit;
  background-color: transparent !important;
  .v-window-item--active {
    background: transparent;
  }
}
.tooltipdownloadmetrics {
  width: 252px;
  height: 38px;
}
</style>
