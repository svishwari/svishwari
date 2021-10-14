<template>
  <div class="pa-0 campaign-summary">
    <v-card flat class="card-style" style="position: sticky">
      <v-card-text>
        <div
          v-if="!hasData(summaryCards, 'summary')"
          class="empty-state pa-5 black--text text--darken-1"
        >
          Be patient! Performance data is currently not available, check back
          tomorrow to see if the magic is ready.
        </div>
        <div
          v-if="hasData(summaryCards, 'summary')"
          class="d-flex summary-tab-wrap"
        >
          <metric-card
            v-for="(item, i) in summaryCards"
            :key="item.id"
            class="list-item mr-3"
            :max-width="item.width"
            :grow="i === 0 ? 2 : 1"
            :title="item.title"
            :height="70"
          >
            <template #subtitle-extended>
              <span v-if="item.field.includes('|')">
                <tooltip>
                  <template #label-content>
                    <span class="text--subtitle-1 font-weight-semi-bold">
                      <span
                        v-if="numericColumns.includes(item.field.split('|')[0])"
                      >
                        {{
                          Number(item.value.split("|")[0])
                            | Numeric(true)
                            | Empty
                        }}
                      </span>
                    </span>
                  </template>
                  <template #hover-content>
                    {{
                      Number(item.value.split("|")[0]) | Numeric(true) | Empty
                    }}
                  </template>
                </tooltip>
                &nbsp;&bull;&nbsp;
                <tooltip>
                  <template #label-content>
                    <span class="text--subtitle-1 font-weight-semi-bold">
                      <span
                        v-if="
                          percentileColumns.includes(item.field.split('|')[1])
                        "
                      >
                        {{
                          parseFloat(item.value.split("|")[1])
                            | Numeric(false, false, false, (percentage = true))
                        }}
                      </span>
                      <span
                        v-else-if="
                          numericColumns.includes(item.field.split('|')[1])
                        "
                      >
                        {{
                          Number(item.value.split("|")[1])
                            | Numeric(true, false, true)
                        }}
                      </span>
                    </span>
                  </template>
                  <template #hover-content>
                    <span
                      v-if="
                        percentileColumns.includes(item.field.split('|')[1])
                      "
                    >
                      {{
                        parseFloat(item.value.split("|")[1])
                          | Numeric(false, false, false, (percentage = true))
                      }}
                    </span>
                    <span
                      v-else-if="
                        numericColumns.includes(item.field.split('|')[1])
                      "
                    >
                      {{
                        Number(item.value.split("|")[1]) | Numeric(true, false)
                      }}
                    </span>
                  </template>
                </tooltip>
              </span>
              <span else>
                <tooltip>
                  <template #label-content>
                    <span class="text--subtitle-1">
                      <span v-if="numericColumns.includes(item.field)">
                        {{ item.value | Numeric(true, false) }}
                      </span>
                      <span v-else-if="percentileColumns.includes(item.field)">
                        {{ item.value | Percentage }}
                      </span>
                      <span v-else-if="currencyColumns.includes(item.field)">
                        {{ item.value | Currency }}
                      </span>
                    </span>
                  </template>
                  <template #hover-content>
                    <span v-if="percentileColumns.includes(item.field)">
                      {{
                        item.value
                          | Numeric(false, false, false, (percentage = true))
                      }}
                    </span>
                    <span v-else> {{ item.value | Numeric(true, false) }}</span>
                  </template>
                </tooltip>
              </span>
            </template>
          </metric-card>
        </div>
      </v-card-text>
    </v-card>
    <v-card min-height="145px" flat class="mt-6 card-style">
      <v-card-title class="d-flex justify-space-between pb-4 pl-7">
        <div class="d-flex align-center">
          <icon
            type="audiences"
            :size="24"
            color="black-darken4"
            class="mr-2"
          />
          <span class="text-h5 black--text text--darken-4">
            Audience performance
          </span>
        </div>
      </v-card-title>
      <v-card-text class="pl-6 pb-6 mt-0 pr-0">
        <div
          v-if="!hasData(data, 'performance')"
          class="empty-state pa-5 text--gray"
        >
          Nothing to show here yet. Add an audience, assign and deliver that
          audience to a destination.
        </div>
        <!-- Campaign Nested Table -->
        <hux-data-table
          v-if="hasData(data, 'performance')"
          :columns="headers"
          :data-items="data"
          nested
        >
          <template #item-row="{ item, expandFunc, isExpanded }">
            <tr :class="{ 'v-data-table__expanded__row': isExpanded }">
              <td v-for="header in headers" :key="header.value">
                <div
                  v-if="header.value == 'name'"
                  class="w-100 d-flex align-center"
                >
                  <v-icon
                    :class="{ 'rotate-icon-90': isExpanded }"
                    size="18"
                    @click="expandFunc(!isExpanded)"
                  >
                    mdi-chevron-right
                  </v-icon>

                  <span class="d-flex align-center">
                    <router-link
                      :to="{ name: 'AudienceInsight', params: { id: item.id } }"
                      class="text-decoration-none"
                      append
                    >
                      <span class="audience-name d-flex align-center">
                        <tooltip>
                          <template #label-content>
                            <div class="primary--text ellipsis max-26">
                              {{ item.name }}
                            </div>
                          </template>
                          <template #hover-content>
                            {{ item.name }}
                          </template>
                        </tooltip>
                        <tooltip>
                          <template #label-content>
                            <icon
                              v-if="needsCampaignMapping(item)"
                              type="information"
                              :size="16"
                              class="ml-2"
                            />
                          </template>
                          <template #hover-content>
                            Mapping required to show related metrics.
                          </template>
                        </tooltip>
                      </span>
                    </router-link>
                  </span>
                </div>
                <div v-if="header.value != 'name'" class="w-100">
                  {{ item[header.value] }}
                </div>
              </td>
            </tr>
          </template>

          <template #expanded-row="{ expandedHeaders, parentItem }">
            <td :colspan="expandedHeaders.length" class="pa-0 child">
              <hux-data-table
                v-if="parentItem"
                :columns="expandedHeaders"
                :data-items="
                  getFormattedItems(parentItem.destinations || item.campaigns)
                "
                :show-header="false"
                nested
              >
                <template #item-row="{ item, expandFunc, isExpanded }">
                  <tr :class="{ 'v-data-table__expanded__row': isExpanded }">
                    <td :style="{ width: expandedHeaders[0].width }">
                      <div
                        class="w-100 d-flex align-center destination-col"
                        :class="{
                          'pl-11': !item.is_mapped && type === 'ads',
                          'pl-3': item.campaigns && item.campaigns.length > 0,
                        }"
                      >
                        <span
                          v-if="item.campaigns && item.campaigns.length > 0"
                          class="d-flex align-center"
                        >
                          <v-icon
                            :class="{
                              'rotate-icon-90': isExpanded,
                              'mr-2': true,
                            }"
                            size="18"
                            @click="expandFunc(!isExpanded)"
                          >
                            mdi-chevron-right
                          </v-icon>

                          <span class="d-flex align-center">
                            <logo
                              :type="logoType(item[expandedHeaders[0].value])"
                              :size="18"
                              class="mr-3"
                            />
                            <span class="text--neroblack ellipsis">
                              {{ item[expandedHeaders[0].value] | Empty("-") }}
                            </span>
                            <v-btn
                              v-if="item.is_mapped && type === 'ads'"
                              icon
                              small
                              class="ml-3"
                              @click="triggerCampaignMap(parentItem, item)"
                            >
                              <icon type="mapping" :size="28" />
                            </v-btn>
                          </span>
                        </span>
                        <span v-else class="d-flex align-center">
                          <div class="audience-insight">
                            <logo
                              :type="logoType(item[expandedHeaders[0].value])"
                              :size="18"
                              class="mr-3"
                            />
                            <span
                              class="text--neroblack ellipsis icon-audiences"
                            >
                              {{ item[expandedHeaders[0].value] | Empty("-") }}
                            </span>
                          </div>
                        </span>
                      </div>
                    </td>
                    <td
                      v-if="!item.is_mapped && type === 'ads'"
                      :colspan="getDestinationHeaders(expandedHeaders).length"
                      :style="{
                        width: totalWidth(
                          getDestinationHeaders(expandedHeaders)
                        ),
                      }"
                    >
                      <div class="d-flex align-center">
                        <div class="error--text mr-2 d-flex align-center">
                          <icon
                            type="information"
                            :size="16"
                            class="icon-info mr-2"
                          />
                          To view KPIs you need to map to a Facebook campaign.
                        </div>
                        <v-btn
                          tile
                          class="error--text px-2 pl-2 pr-4"
                          color="white"
                          height="29"
                          width="99"
                          @click="triggerCampaignMap(parentItem, item)"
                        >
                          <icon type="map_now_icon" :size="20" class="mr-1" />
                          Map now
                        </v-btn>
                      </div>
                    </td>
                    <td
                      v-for="header in getDestinationHeaders(expandedHeaders)"
                      v-else
                      :key="header.value"
                      :style="{ width: header.width }"
                    >
                      {{ item[header.value] }}
                    </td>
                  </tr>
                </template>
                <!-- eslint-disable vue/no-template-shadow -->
                <template #expanded-row="{ expandedHeaders, parentItem }">
                  <td :colspan="expandedHeaders.length" class="pa-0 child">
                    <hux-data-table
                      v-if="parentItem"
                      :columns="expandedHeaders"
                      :data-items="getFormattedItems(parentItem.campaigns)"
                      :show-header="false"
                    >
                      <template #row-item="{ item }">
                        <td
                          v-for="header in expandedHeaders"
                          :key="header.value"
                          :style="{ width: header.width }"
                        >
                          <span v-if="header.value == 'name'">
                            <tooltip>
                              <template #label-content>
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
                <!-- eslint-enable -->
              </hux-data-table>
            </td>
          </template>
        </hux-data-table>
      </v-card-text>
    </v-card>
    <campaign-map-drawer
      ref="campaignMapDrawer"
      :toggle="showCampaignMapDrawer"
      @onToggle="(toggle) => (showCampaignMapDrawer = toggle)"
      @onCampaignMappings="updateCampaignMappings($event)"
    />
  </div>
</template>

<script>
import HuxDataTable from "./common/dataTable/HuxDataTable.vue"
import MetricCard from "@/components/common/MetricCard"
import Tooltip from "./common/Tooltip.vue"
import Icon from "./common/Icon.vue"
import Logo from "./common/Logo.vue"
import CampaignMapDrawer from "@/views/Engagements/Configuration/Drawers/CampaignMapDrawer.vue"
import { mapActions } from "vuex"
export default {
  name: "CampaignSummary",
  components: {
    HuxDataTable,
    MetricCard,
    Tooltip,
    Icon,
    Logo,
    CampaignMapDrawer,
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
    engagementId: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      showCampaffoignMapDrawer: false,
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
      audienceId: null,
      destinationId: null,
      showCampaignMapDrawer: false,
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
  methods: {
    ...mapActions({
      saveCampaignMappings: "engagements/saveCampaignMappings",
    }),
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
            if (uniqueValues === "0,$0,0%" || uniqueValues === "0,0%")
              return false
          }
          return true
        }
      }
      return false
    },
    logoType(name) {
      return name.split(" ")[0].toLowerCase()
    },
    async updateCampaignMappings(optedMappings) {
      const campaignsPayload = {
        campaigns: Object.values(optedMappings.mappings).map((mapping) => ({
          name: mapping.campaign.name,
          id: mapping.campaign.id,
          delivery_job_id: mapping.delivery_job.id,
        })),
      }
      const payload = { ...optedMappings.attrs, data: campaignsPayload }
      await this.saveCampaignMappings(payload)
      this.$emit("onUpdateCampaignMappings")
    },
    getFormattedItems(destinationRollups) {
      return destinationRollups.map((destinationRollup) => {
        return this.formatData(destinationRollup)
      })
    },
    needsCampaignMapping(item) {
      return (
        (item.destinations &&
          item.destinations.some(
            (dest) =>
              !dest.is_mapped && this.type === "ads" && dest.name === "Facebook"
          )) ||
        false
      )
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
            true
          )
        } else if (this.currencyColumns.includes(key)) {
          obj[key] = this.$options.filters.Currency(obj[key])
        }
      })
      return obj
    },
    getDestinationHeaders(headers) {
      return headers.filter((_, i) => i > 0)
    },
    totalWidth(headers) {
      return (
        headers.reduce(
          (n, header) => n + parseFloat(header.width.replace("px", "")),
          0
        ) +
        1 +
        "px"
      )
    },
    triggerCampaignMap(audience, destination) {
      this.showCampaignMapDrawer = true
      this.$refs.campaignMapDrawer.loadCampaignMappings({
        id: this.engagementId,
        audienceId: audience.id,
        destinationId: destination.id,
      })
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
    color: var(--v-black-darken1);
    border: 1px solid rgba(208, 208, 206, 0.3);
    box-sizing: border-box;
    border-radius: 5px;
  }
  .summary-tab-wrap {
    flex-wrap: wrap;
    ::v-deep .metric-card-wrapper {
      border: 1px solid var(--v-black-lighten2);
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
          background: var(--v-primary-lighten2);
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
          background: var(--v-primary-lighten2) !important;
        }
        height: 64px;
        td {
          font-size: 14px !important;
          line-height: 22px;
          color: var(--v-black-darken4);
          .audience-name {
            span {
              display: flex;
            }
          }
        }
        td:nth-child(1) {
          background: var(--v-white-base);
          border-right: thin solid rgba(0, 0, 0, 0.12);
          &:hover {
            background: var(--v-primary-lighten2) !important;
          }
        }
      }
      .ellipsis {
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 21ch;
        display: inline-block;
        white-space: nowrap;
      }
      .max-26 {
        max-width: 26ch;
        width: 26ch;
      }
      .v-data-table__expanded__row {
        background: var(--v-primary-lighten2);
        td:nth-child(1) {
          background: var(--v-primary-lighten2);
        }
      }
    }
    .child {
      ::v-deep .theme--light {
        background: var(--v-primary-lighten1);
        .v-data-table__wrapper {
          box-shadow: inset 0px 10px 10px -4px var(--v-black-lighten3);
          border-bottom: thin solid rgba(0, 0, 0, 0.12);
        }
      }
      ::v-deep table {
        background: inherit;
        tbody {
          td {
            &:first-child {
              background: inherit;
            }
          }
        }
        .v-data-table__expanded__row {
          background: inherit !important;
        }
      }
      ::v-deep .child {
        .v-data-table__wrapper {
          box-shadow: none;
        }
        tbody {
          td {
            &:first-child {
              padding-left: 80px;
            }
          }
        }
      }
    }
  }
  .icon-audiences {
    position: absolute;
    margin-top: -1px;
  }
  .audience-insight {
    cursor: default;
    color: var(--v-naroBlack-base) !important;
  }
  .destination-col {
    margin-top: 5px;
  }
}
</style>
