<template>
  <div class="pa-0">
    <v-card flat class="card-style">
      <v-card-text class="d-flex summary-tab-wrap" v-if="summary.length > 0">
        <metric-card
          class="list-item mr-1 rounded-lg"
          :min-width="item.width"
          :height="70"
          v-for="item in summary"
          :key="item.id"
          :title="item.title"
          :subtitle="item.value"
          :interactable="false"
        ></metric-card>
      </v-card-text>
    </v-card>
    <v-card minHeight="145px" flat class="mt-6 card-style">
      <v-card-title class="d-flex justify-space-between pb-6">
        <div class="d-flex align-center">
          <icon
            type="audiences"
            :size="24"
            color="neroBlack"
            class="mr-2"
          /><span class="text-h5">Audience performance</span>
        </div>
      </v-card-title>
      <v-card-text class="pl-6 pr-6 pb-6 mt-6">
        <div
          class="blank-section rounded-sm pa-5"
          v-if="campaignData.length == 0"
        >
          Nothing to show here yet. Add an audience and then assign a
          destination.
        </div>
        <!-- Campaign Nested Table -->
        <hux-data-table
          :headers="AdsHeaders"
          :dataItems="data"
          nested
          class="parent-table"
        >
          <template #expanded-row="{ headers, item }">
            <td :colspan="headers.length" class="pa-0 child">
              <hux-data-table
                :headers="headers"
                :dataItems="item.campaigns"
                :showHeader="false"
                v-if="item"
                class="child-table"
              >
                <template v-slot:row-item="{ item }">
                  <td
                    v-for="header in headers"
                    v-bind:key="header.value"
                    :style="{ width: header.width }"
                  >
                    <span v-if="header.value == 'name'">
                      <tooltip>
                        <template slot="label-content">
                          {{ item[header.value] }}
                        </template>
                        <template slot="hover-content">
                          {{ item[header.value] }}
                        </template>
                      </tooltip>
                    </span>
                    <span v-if="header.value == 'spend'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span v-if="header.value == 'reach'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span v-if="header.value == 'impressions'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span v-if="header.value == 'conversions'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span v-if="header.value == 'clicks'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span v-if="header.value == 'frequency'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span
                      v-if="header.value == 'cost_per_thousand_impressions'"
                      >{{ item[header.value] | Currency }}</span
                    >
                    <span v-if="header.value == 'click_through_rate'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span v-if="header.value == 'cost_per_action'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span v-if="header.value == 'cost_per_click'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
                    <span v-if="header.value == 'engagement_rate'">{{
                      item[header.value] | Numeric(true, false)
                    }}</span>
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
export default {
  name: "CampaignSummary",
  components: {
    HuxDataTable,
    MetricCard,
    Tooltip,
    Icon,
  },
  data() {
    return {
      expand: [],
      AdsHeaders: [
        { text: "Audiences", value: "name", width: "170px" },
        {
          text: "Spend",
          value: "spend",
          width: "90px",
          tooltipValue:
            "CPM * Impressions / 1000 \n The amount paid to acquire the impressions served to individuals.",
        },
        {
          text: "Reach",
          value: "reach",
          width: "90px",
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
          width: "90px",
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
          width: "150px",
          tooltipValue: "Total Engagements / Total Followers * 100",
        },
      ],
    }
  },
  computed: {
    data() {
      return this.campaignData.map((item) => this.formatData(item))
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
  },
  methods: {
    formatData(item) {
      const obj = Object.assign({}, item)
      obj["name"] = this.$options.filters.TitleCase(obj["name"])
      obj["spend"] = this.$options.filters.Numeric(obj["spend"], true, false)
      obj["reach"] = this.$options.filters.Numeric(obj["reach"], true, false)
      obj["impressions"] = this.$options.filters.Numeric(
        obj["impressions"],
        true,
        false
      )
      obj["conversions"] = this.$options.filters.Numeric(
        obj["conversions"],
        true,
        false
      )
      obj["frequency"] = this.$options.filters.Numeric(
        obj["frequency"],
        true,
        false
      )
      obj["cost_per_thousand_impressions"] = this.$options.filters.Currency(
        obj["cost_per_thousand_impressions"]
      )
      obj["click_through_rate"] = this.$options.filters.Numeric(
        obj["click_through_rate"],
        true,
        false
      )
      obj["cost_per_action"] = this.$options.filters.Numeric(
        obj["cost_per_action"],
        true,
        false
      )
      obj["cost_per_click"] = this.$options.filters.Numeric(
        obj["cost_per_click"],
        true,
        false
      )
      obj["engagement_rate"] = this.$options.filters.Numeric(
        obj["engagement_rate"],
        true,
        false
      )

      return obj
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-data-table {
  margin-left: -20px;
  ::v-deep table {
    table-layout: fixed !important;
    thead {
      th:first-child {
        visibility: hidden;
      }
    }
    .v-data-table__expand-icon {
      left: 15px;
      transform: rotate(-90deg);
      &.v-data-table__expand-icon--active {
        transform: rotate(0deg);
      }
    }
    .child-table {
      margin-left: 20px;
    }
  }
}
</style>
