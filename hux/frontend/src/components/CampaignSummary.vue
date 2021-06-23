<template>
  <div class="pa-0 campaign-summary">
    <v-card flat class="card-style" style="position: sticky">
      <v-card-text>
        <div class="empty-state pa-5 text--gray" v-if="summary.length == 0">
          Be patient! Performance data is currently not available, check back
          tomorrow to see if the magic is ready.
        </div>
        <div v-if="summary.length > 0" class="d-flex summary-tab-wrap">
          <MetricCard
            class="list-item mr-3"
            v-for="(item, i) in summaryCards"
            :key="item.id"
            :maxWidth="item.width"
            :grow="i === 0 ? 2 : 1"
            :title="item.title"
          >
            <template #subtitle-extended>
              <span v-if="item.field.includes('|')">
                <tooltip>
                  <template #label-content>
                    <span class="font-weight-semi-bold">
                      <span
                        v-if="numericColumns.includes(item.field.split('|')[0])"
                      >
                        {{
                          item.value.split("|")[0] | Numeric(false, false, true)
                        }}
                      </span>
                    </span>
                  </template>
                  <template #hover-content>
                    {{ item.value.split("|")[0] }}
                  </template>
                </tooltip>
                &nbsp;&bull;&nbsp;
                <tooltip>
                  <template #label-content>
                    <span class="font-weight-semi-bold">
                      <span
                        v-if="
                          percentileColumns.includes(item.field.split('|')[1])
                        "
                      >
                        {{
                          item.value.split("|")[1]
                            | Numeric(true, false, false, "%")
                        }}
                      </span>
                      <span
                        v-else-if="
                          numericColumns.includes(item.field.split('|')[1])
                        "
                      >
                        {{
                          item.value.split("|")[1] | Numeric(false, false, true)
                        }}
                      </span>
                    </span>
                  </template>
                  <template #hover-content>
                    {{ item.value.split("|")[1] }}
                  </template>
                </tooltip>
              </span>
              <span else>
                <tooltip>
                  <template #label-content>
                    <span class="font-weight-semi-bold">
                      <span v-if="numericColumns.includes(item.field)">
                        {{ item.value | Numeric(false, false, true) }}
                      </span>
                      <span v-else-if="percentileColumns.includes(item.field)">
                        {{ item.value | Numeric(true, false, false, "%") }}
                      </span>
                      <span v-else-if="currencyColumns.includes(item.field)">
                        {{ item.value | Currency }}
                      </span>
                    </span>
                  </template>
                  <template #hover-content>
                    {{ item.value }}
                  </template>
                </tooltip>
              </span>
            </template>
          </MetricCard>
        </div>
      </v-card-text>
    </v-card>
    <v-card minHeight="145px" flat class="mt-6 card-style">
      <v-card-title class="d-flex justify-space-between pb-4 pl-7">
        <div class="d-flex align-center">
          <icon type="audiences" :size="24" color="neroBlack" class="mr-2" />
          <span class="text-h5 text--neroblack"> Audience performance </span>
        </div>
      </v-card-title>
      <v-card-text class="pl-6 pb-6 mt-0 pr-0">
        <!-- Campaign Nested Table -->
        <hux-data-table :headers="headers" :dataItems="data" nested>
          <template #item-row="{ item, expand, isExpanded }">
            <tr :class="{ 'v-data-table__expanded__row': isExpanded }">
              <td v-for="header in headers" :key="header.value">
                <div v-if="header.value == 'name'" class="w-100">
                  <v-icon
                    :class="{ 'rotate-icon-90': isExpanded }"
                    size="18"
                    @click="expand(!isExpanded)"
                  >
                    mdi-chevron-right
                  </v-icon>
                  <tooltip>
                    <template #label-content>
                      <!-- TODO Route Link to Audience Insight Page -->
                      <router-link
                        to="#"
                        class="text-decoration-none primary--text"
                        append
                      >
                        {{ item.name }}
                      </router-link>
                    </template>
                    <template #hover-content>
                      {{ item.name }}
                    </template>
                  </tooltip>
                </div>
                <div v-if="header.value != 'name'" class="w-100">
                  {{ item[header.value] }}
                </div>
              </td>
            </tr>
          </template>

          <template #expanded-row="{ headers, item }">
            <td :colspan="headers.length" class="pa-0 child">
              <hux-data-table
                :headers="headers"
                :dataItems="getCampaigns(item.campaigns)"
                :showHeader="false"
                v-if="item"
              >
                <template #row-item="{ item }">
                  <td
                    v-for="header in headers"
                    :key="header.value"
                    :style="{ width: header.width }"
                  >
                    <span v-if="header.value == 'name'">
                      <tooltip>
                        <template #label-content>
                          <logo
                            :type="logoType(item[header.value])"
                            :size="18"
                            class="mr-3"
                          />
                          <span class="text--neroblack ellipsis">
                            {{ item[header.value] }}
                          </span>
                        </template>
                        <template #hover-content>
                          {{ item[header.value] }}
                        </template>
                      </tooltip>
                    </span>
                    <span v-if="header.value != 'name'">
                      {{ item[header.value] }}
                    </span>
                  </td>
                </template>
              </hux-data-table>
            </td>
          </template>
        </hux-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import HuxDataTable from "./common/dataTable/HuxDataTable.vue"
import MetricCard from "@/components/common/MetricCard"
import Tooltip from "./common/Tooltip.vue"
import Icon from "./common/Icon.vue"
import Logo from "./common/Logo.vue"
export default {
  name: "CampaignSummary",
  components: {
    HuxDataTable,
    MetricCard,
    Tooltip,
    Icon,
    Logo,
  },
  data() {
    return {
      expand: [],
      AdsHeaders: [
        { text: "Audiences", value: "name", width: "278px" },
        {
          text: "Spend",
          value: "spend",
          width: "100px",
          tooltipValue:
            "CPM * Impressions / 1000 \n The amount paid to acquire the impressions served to individuals.",
        },
        {
          text: "Reach",
          value: "reach",
          width: "100px",
          tooltipValue:
            "Number of unique individuals that were served an impression",
        },
        {
          text: "Impressions",
          value: "impressions",
          width: "125px",
          tooltipValue: "Number of ads served",
        },
        {
          text: "Conversions",
          value: "conversions",
          width: "125px",
          tooltipValue:
            "Number of times the conversion pixel fired on a specific action (e.g. a sign up, \n purchase, etc.). ",
        },
        {
          text: "Clicks",
          value: "clicks",
          width: "100px",
          tooltipValue: "Number of times an ad was clicked",
        },
        { text: "Frequency", value: "frequency", width: "115px" },
        {
          text: "CPM",
          value: "cost_per_thousand_impressions",
          width: "90px",
          tooltipValue:
            "Cost per thousand impressions = spend / impressions * 1000",
        },
        {
          text: "CTR",
          value: "click_through_rate",
          width: "90px",
          tooltipValue: "Click through Rate = clicks / Impressions",
        },
        {
          text: "CPA",
          value: "cost_per_action",
          width: "90px",
          tooltipValue: "Cost per Action  = Spend / Conversions",
        },
        {
          text: "CPC",
          value: "cost_per_click",
          width: "90px",
          tooltipValue: "Clost per click = spend / clicks",
        },
        {
          text: "Engagement rate",
          value: "engagement_rate",
          width: "180px",
          tooltipValue: "Total Engagements / Total Followers * 100",
        },
      ],
      emailHeaders: [
        { text: "Audiences", value: "name", width: "278px" },
        {
          text: "Sent",
          value: "sent",
          width: "90px",
          tooltipValue: "Number of emails sent (including bounces etc)",
        },
        {
          text: "Hard bounces",
          value: "hard_bounces",
          width: "135px",
          tooltipValue:
            "Total number of permanent errors, such as a wrong email address",
        },
        {
          text: "Hard bounce rate",
          value: "hard_bounces_rate",
          width: "155px",
        },
        {
          text: "Delivered",
          value: "delivered",
          width: "110px",
          tooltipValue: "Number of messages successfully sent",
        },
        {
          text: "Delivered rate",
          value: "delivered_rate",
          width: "135px",
        },
        {
          text: "Open",
          value: "open",
          width: "90px",
          tooltipValue: "Number of messages that was opened",
        },
        {
          text: "Open rate",
          value: "open_rate",
          width: "110px",
        },
        {
          text: "CTR",
          value: "clicks",
          width: "90px",
          tooltipValue: "Number of email links or content clicked",
        },
        {
          text: "CTOR",
          value: "click_through_rate",
          width: "85px",
          tooltipValue: "Clicks / Opens * 100",
        },
        {
          text: "Unique clicks",
          value: "unique_clicks",
          width: "130px",
          tooltipValue: "Number of individuals who clicked on content or links",
        },
        {
          text: "Unique opens",
          value: "unique_opens",
          width: "135px",
          tooltipValue: "Number of individuals who opened the link",
        },
        {
          text: "Unsubscribe",
          value: "unsubscribe",
          width: "125px",
          tooltipValue:
            "Number of people who unsubscribed from ALL of the campaigns",
        },
        {
          text: "Unsubscribe rate",
          value: "unsubscribe_rate",
          width: "150px",
          tooltipValue: "Number of emails sent (including bounces etc)",
        },
      ],
      numericColumns: [
        // Summary Columns
        "sent",
        // Ads Columns
        "spend",
        "reach",
        "impressions",
        "conversions",
        "frequency",
        // Email Columns
        "sent",
        "hard_bounces",
        "delivered",
        "open",
        "clicks",
        "unique_clicks",
        "unique_opens",
        "click_through_rate",
        "unsubscribe",
      ],
      percentileColumns: [
        // Ads Columns
        "click_through_rate",

        "engagement_rate",
        // Email Columns
        "hard_bounces_rate",
        "delivered_rate",
        "open_rate",
        "click_to_open_rate",
        "unsubscribe_rate",
      ],
      currencyColumns: [
        // Ads Columns
        "cost_per_thousand_impressions",
        "cost_per_action",
        "cost_per_click",
        // Email Columns
      ],
      emptyCampaignData: [
        {
          campaigns: [],
          click_through_rate: "-",
          clicks: "-",
          conversions: "-",
          cost_per_action: "-",
          cost_per_click: "-",
          cost_per_thousand_impressions: "-",
          engagement_rate: "-",
          frequency: "-",
          impressions: "-",
          name: "Audience 1",
          reach: "-",
          spend: "-",
        },
        {
          campaigns: [],
          click_through_rate: "-",
          clicks: "-",
          conversions: "-",
          cost_per_action: "-",
          cost_per_click: "-",
          cost_per_thousand_impressions: "-",
          engagement_rate: "-",
          frequency: "-",
          impressions: "-",
          name: "Audience 2",
          reach: "-",
          spend: "-",
        },
        {
          campaigns: [],
          click_through_rate: "-",
          clicks: "-",
          conversions: "-",
          cost_per_action: "-",
          cost_per_click: "-",
          cost_per_thousand_impressions: "-",
          engagement_rate: "-",
          frequency: "-",
          impressions: "-",
          name: "Audience 3",
          reach: "-",
          spend: "-",
        },
      ],
      emptyCampaignEmailData: [
        {
          campaigns: [],
          sent: "-",
          hard_bounces: "-",
          hard_bounces_rate: "-",
          delivered: "-",
          delivered_rate: "-",
          open: "-",
          open_rate: "-",
          clicks: "-",
          click_through_rate: "-",
          click_to_open_rate: "-",
          unique_clicks: "-",
          unique_opens: "-",
          unsubscribe: "-",
          unsubscribe_rate: "-",
          name: "Audience 1",
        },
        {
          campaigns: [],
          sent: "-",
          hard_bounces: "-",
          hard_bounces_rate: "-",
          delivered: "-",
          delivered_rate: "-",
          open: "-",
          open_rate: "-",
          clicks: "-",
          click_through_rate: "-",
          click_to_open_rate: "-",
          unique_clicks: "-",
          unique_opens: "-",
          unsubscribe: "-",
          unsubscribe_rate: "-",
          name: "Audience 2",
        },
        {
          campaigns: [],
          sent: "-",
          hard_bounces: "-",
          hard_bounces_rate: "-",
          delivered: "-",
          delivered_rate: "-",
          open: "-",
          open_rate: "-",
          clicks: "-",
          click_through_rate: "-",
          click_to_open_rate: "-",
          unique_clicks: "-",
          unique_opens: "-",
          unsubscribe: "-",
          unsubscribe_rate: "-",
          name: "Audience 3",
        },
      ],
    }
  },
  computed: {
    data() {
      if (this.campaignData.length === 0) {
        return this.type === "ads"
          ? this.emptyCampaignData
          : this.emptyCampaignEmailData
      } else {
        return this.campaignData.map((item) => {
          return this.formatData(item)
        })
      }
    },
    headers() {
      return this.type === "ads" ? this.AdsHeaders : this.emailHeaders
    },
    summaryCards() {
      return this.summary.length === 0 ? [] : this.summary
    },
  },
  props: {
    summary: {
      type: Array,
      required: true,
      default: () => [],
    },
    campaignData: {
      type: Array,
      required: false,
      default: () => [],
    },
    type: {
      type: String,
      required: true,
      default: "ads",
    },
  },
  methods: {
    logoType(name) {
      return name.split(" ")[0].toLowerCase()
    },
    getCampaigns(campaigns) {
      return campaigns.map((camp) => this.formatData(camp))
    },
    formatData(item) {
      const obj = Object.assign({}, item)
      Object.keys(item).forEach((key) => {
        if (this.numericColumns.includes(key)) {
          obj[key] = this.$options.filters.Numeric(obj[key], true, false)
        } else if (this.percentileColumns.includes(key)) {
          obj[key] = this.$options.filters.Numeric(
            obj[key],
            true,
            false,
            false,
            "%"
          )
        } else if (this.currencyColumns.includes(key)) {
          obj[key] = this.$options.filters.Currency(obj[key])
        } else if (key === "name") {
          obj[key] = this.$options.filters.TitleCase(obj[key])
        }
      })
      return obj
    },
  },
}
</script>

<style lang="scss" scoped>
.campaign-summary {
  .empty-state {
    background: rgba(236, 244, 249, 0.3);
    width: 100%;
    font-size: 14px;
    line-height: 22px;
    color: var(--v-gray-base);
    border: 1px solid rgba(208, 208, 206, 0.3);
    box-sizing: border-box;
    border-radius: 5px;
  }
  .summary-tab-wrap {
    flex-wrap: wrap;
    ::v-deep .metric-card-wrapper {
      border: 1px solid var(--v-zircon-base);
      box-sizing: border-box;
      height: 75px;
      padding: 10px;
      margin-right: 5px !important;
      .text-caption {
        font-size: 12px;
        line-height: 16px;
        margin: 0 !important;
      }
      .font-weight-semi-bold {
        font-size: 14px;
        line-height: 19px;
      }
    }
  }
  .hux-data-table {
    ::v-deep table {
      table-layout: fixed !important;
      .mdi-chevron-right {
        transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
      }
      .v-data-table-header {
        th {
          background: var(--v-aliceBlue-base);
          &:first-child {
            border-radius: 12px 0px 0px 0px;
          }
          &:last-child {
            border-radius: 0px 12px 0px 0px;
          }
        }
        th:nth-child(1) {
          border-right: thin solid rgba(0, 0, 0, 0.12);
        }
        border-radius: 12px 12px 0px 0px;
      }
      tr {
        &:hover {
          background: var(--v-aliceBlue-base) !important;
        }
        height: 64px;
        td {
          font-size: 14px !important;
          line-height: 22px;
          color: var(--v-neroBlack-base);
        }
        td:nth-child(1) {
          background: var(--v-white-base);
          border-right: thin solid rgba(0, 0, 0, 0.12);
          &:hover {
            background: var(--v-aliceBlue-base) !important;
          }
        }
      }
      .ellipsis {
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 21ch;
        display: inline-block;
        width: 21ch;
        white-space: nowrap;
      }
      .v-data-table__expanded__row {
        background: var(--v-aliceBlue-base);

        td:nth-child(1) {
          background: var(--v-aliceBlue-base);
        }
      }
    }
    .child {
      ::v-deep .theme--light {
        background: var(--v-background-base);
        .v-data-table__wrapper {
          box-shadow: inset 0px 10px 10px -4px var(--v-lightGrey-base);
          border-bottom: thin solid rgba(0, 0, 0, 0.12);
        }
      }

      ::v-deep table {
        background: inherit;
        tbody {
          td {
            &:first-child {
              padding-left: 45px;
              background: inherit;
            }
          }
        }
      }
    }
  }
}
</style>
