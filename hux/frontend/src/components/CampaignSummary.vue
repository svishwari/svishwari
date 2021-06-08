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
        <hux-data-table :headers="AdsHeaders" :dataItems="campaignData" nested>
          <template v-slot:header="{ props: { headers } }">
            <thead class="v-data-table-header hello">
              <tr>
                <th
                  v-for="header in headers"
                  :key="header.value"
                  class="text-uppercase"
                  scope="col"
                >
                  {{ header.text }}
                </th>
              </tr>
            </thead>
          </template>
          <template v-slot:item="{ item }">
            {{ item }}
          </template>
          <template v-slot:expanded-row="{ headers, item }">
            <td :colspan="headers.length" class="pa-0">
              <hux-data-table
                :headers="headers"
                :dataItems="item.campaigns"
                :showHeader="false"
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
                      item[header.value] | FormatSize
                    }}</span>
                    <span v-if="header.value == 'reach'">{{
                      item[header.value] | FormatSize
                    }}</span>
                    <span v-if="header.value == 'impressions'">{{
                      item[header.value] | FormatSize
                    }}</span>
                    <span v-if="header.value == 'conversions'">{{
                      item[header.value] | FormatSize
                    }}</span>
                    <span v-if="header.value == 'clicks'">{{
                      item[header.value] | FormatSize
                    }}</span>
                    <span v-if="header.value == 'frequency'">{{
                      item[header.value] | FormatSize
                    }}</span>
                    <span
                      v-if="header.value == 'cost_per_thousand_impressions'"
                      >{{
                        item[header.value] | FormatSize | CurrentFormat
                      }}</span
                    >
                    <span v-if="header.value == 'click_through_rate'">{{
                      item[header.value] | FormatSize
                    }}</span>
                    <span v-if="header.value == 'cost_per_action'">{{
                      item[header.value] | FormatSize
                    }}</span>
                    <span v-if="header.value == 'cost_per_click'">{{
                      item[header.value] | FormatSize
                    }}</span>
                    <span v-if="header.value == 'engagement_rate'">{{
                      item[header.value] | FormatSize
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
      AdsHeaders: [
        { text: "Audiences", value: "name", width: "170px" },
        { text: "Spend", value: "spend", width: "90px" },
        { text: "Reach", value: "reach", width: "90px" },
        { text: "Impressions", value: "impressions", width: "90px" },
        { text: "Conversions", value: "conversions", width: "90px" },
        { text: "Clicks", value: "clicks", width: "90px" },
        { text: "Frequency", value: "frequency", width: "90px" },
        { text: "CPM", value: "cost_per_thousand_impressions", width: "90px" },
        { text: "CTR", value: "click_through_rate", width: "90px" },
        { text: "CPA", value: "cost_per_action", width: "90px" },
        { text: "CPC", value: "cost_per_click", width: "90px" },
        { text: "Engagement rate", value: "engagement_rate", width: "90px" },
      ],
    }
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
}
</script>

<style lang="scss" scoped>
::root {
}
</style>
