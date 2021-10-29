<template>
  <drawer v-model="localDrawer" content-padding="pa-0">
    <template #header-left>
      <div class="d-flex align-center">
        <icon type="idr-insights" :size="32" class="mr-2" />
        <h3 class="text-h2">IDR Insights</h3>
      </div>
    </template>

    <template #default>
      <div class="header-break"></div>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <hux-data-table
        :columns="columns"
        :data-items="idrItems"
        :show-header="false"
      >
        <template #row-item="{ item }">
          <td
            v-for="(col, index) in columns"
            :key="index"
            :style="{ width: col.width }"
            class="text body-1"
          >
            <template v-if="col.value === 'result'">
              <tooltip v-if="item.toolTipText">
                <template #label-content>
                  <span v-if="item.metricType == 'percentage'">
                    {{
                      item[col.value]
                        | Numeric(true, false, false, true)
                        | Empty("-")
                    }}
                  </span>
                  <span v-if="item.metricType == 'numeric'">
                    {{ item[col.value] | Numeric(true, true) | Empty("-") }}
                  </span>
                </template>
                <template #hover-content>
                  <span v-if="item.metricType == 'percentage'">
                    {{
                      item[col.value]
                        | Numeric(true, false, false, true)
                        | Empty("-")
                    }}
                  </span>
                  <span v-if="item.metricType == 'numeric'">
                    {{
                      item[col.value] | Numeric(true, false, false) | Empty("-")
                    }}
                  </span>
                </template>
              </tooltip>
              <span v-else>
                {{ item[col.value] | Date("MM/DD/YYYY h:mm A") | Empty("-") }}
              </span>
            </template>
            <template v-else>
              {{ item[col.value] }}
              <tooltip v-if="item.toolTipText" position-top>
                <template #label-content>
                  <icon type="info" :size="12" color="primary" variant="base" />
                </template>
                <template #hover-content>
                  {{ item.toolTipText }}
                </template>
              </tooltip>
            </template>
          </td>
        </template>
      </hux-data-table>
    </template>
  </drawer>
</template>

<script>
import { mapGetters } from "vuex"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Drawer from "@/components/common/Drawer.vue"
import Icon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "IDRInsightsDrawer",

  components: {
    HuxDataTable,
    Drawer,
    Icon,
    Tooltip,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
  },

  data() {
    return {
      localDrawer: this.value,
      loading: false,
      items: [],
      columns: [
        {
          value: "metric",
          text: "Metrics",
          width: "50%",
        },
        {
          value: "result",
          text: "Results",
          width: "50%",
        },
      ],
      idrItems: [
        {
          metric: "Updated",
          metricType: "",
          result: "",
        },
        {
          metric: "Total no. of records",
          metricType: "",
          result: "",
          toolTipText: "Total number of input records across all data feeds.",
        },
        {
          metric: "Match rate",
          metricType: "",
          result: "",
          toolTipText:
            "Percentage of input records that are consolidated into Hux IDs.",
        },
        {
          metric: "Anonymous IDs",
          metricType: "",
          result: "",
          toolTipText:
            "IDs related to online visitors that have not logged in, typically identified by a browser cookie or device ID.",
        },
        {
          metric: "Known IDs",
          metricType: "",
          result: "",
          toolTipText:
            "IDs related to profiles that contain PII from online or offline engagement: name, postal address, email address, and phone number.",
        },
        {
          metric: "Individual IDs",
          metricType: "",
          result: "",
          toolTipText:
            "Represents a First Name, Last Name and Address combination, used to identify a customer that lives at an address.",
        },
        {
          metric: "Household IDs",
          metricType: "",
          result: "",
          toolTipText:
            "Represents a Last Name and Address combination, used to identify family members that live at the same address.",
        },
      ],
    }
  },

  computed: {
    ...mapGetters({
      overview: "customers/overview",
    }),
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },

  mounted() {
    this.mapIDRItems()
  },

  methods: {
    mapIDRItems() {
      this.idrItems[0].result = this.overview.updated
      this.idrItems[0].metricType = "date"
      this.idrItems[1].result = this.overview.total_records
      this.idrItems[1].metricType = "numeric"
      this.idrItems[2].result = this.overview.match_rate
      this.idrItems[2].metricType = "percentage"
      this.idrItems[3].result = this.overview.total_unknown_ids
      this.idrItems[3].metricType = "numeric"
      this.idrItems[4].result = this.overview.total_known_ids
      this.idrItems[4].metricType = "numeric"
      this.idrItems[5].result = this.overview.total_individual_ids
      this.idrItems[5].metricType = "numeric"
      this.idrItems[6].result = this.overview.total_household_ids
      this.idrItems[6].metricType = "numeric"
    },
  },
}
</script>
<style lang="scss" scoped>
.hux-data-table {
  ::v-deep .v-data-table__wrapper {
    .v-data-table-header {
      th {
        &:first-child {
          padding: 9px 10px 9px 25px !important;
        }
        padding: 9px 10px !important;
        &:last-child {
          padding: 9px 20px 9px 10px !important;
        }
      }
    }
    tbody {
      tr {
        td {
          &:first-child {
            padding: 9px 10px 9px 25px !important;
          }
          padding: 9px 10px !important;
          &:last-child {
            padding: 9px 20px 9px 10px !important;
          }
        }
      }
    }
  }
}
.header-break {
  border-bottom: 1px solid var(--v-black-lighten2) !important;
}
</style>
