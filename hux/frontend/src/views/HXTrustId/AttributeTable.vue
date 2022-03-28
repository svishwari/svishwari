<template>
  <v-card flat class="attribute-table-wrapper">
    <v-progress-linear :active="isLoading" :indeterminate="isLoading" />
    <template v-if="!isLoading">
      <v-card-title v-if="data.length > 0" class="py-5 px-6">
        <span class="text-h3 black--text">HX TrustID attributes</span>
      </v-card-title>
      <v-card-text v-if="data.length > 0" class="px-6">
        <hux-data-table
          v-if="!isLoading"
          class="attribute-table"
          :columns="columns"
          :data-items="data"
          :sort-column="sortColumn"
          :sort-desc="sortDesc"
          empty="Be patient! The data feeds are currently not available, check back tomorrow to see if the magic is ready."
        >
          <template #row-item="{ item, index }">
            <td
              v-for="col in columns"
              :key="col.value"
              class="black--text text--darken-4 text-body-1"
            >
              <template v-if="col.value === 'attribute_name'">
                {{ item[col.value] }}
              </template>
              <template v-else-if="col.value === 'attribute_score'">
                <rhombus-number
                  class="ml-10"
                  :value="item[col.value]"
                  :color="getRhombusColour(item)"
                />
              </template>
              <template v-else-if="col.value === 'attribute_description'">
                <tooltip>
                  <template slot="label-content">
                    <span class="text-ellipsis text-width">
                      {{ item[col.value] }}
                    </span>
                  </template>
                  <template slot="hover-content">
                    {{ item[col.value] }}
                  </template>
                </tooltip>
              </template>
              <template v-else-if="col.value === 'overall_customer_rating'">
                <progress-stack-bar
                  :width="180"
                  :height="6"
                  :show-percentage="true"
                  :data="getRating(item[col.value].rating)"
                  :bar-id="index + 'table'"
                />
              </template>
            </td>
          </template>
        </hux-data-table>
      </v-card-text>
    </template>
  </v-card>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import ProgressStackBar from "@/components/common/ProgressStackBar/ProgressStackBar.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import RhombusNumber from "../../components/common/RhombusNumber.vue"

export default {
  name: "TrustIdAttributes",
  components: {
    HuxDataTable,
    ProgressStackBar,
    Tooltip,
    RhombusNumber,
  },
  props: {
    data: {
      type: Array,
      required: false,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
    isErrorState: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      sortColumn: "attribute_name",
      sortDesc: true,
      trustColor: {
        humanity: "#037E8E",
        transparency: "#D0C539",
        capability: "#3C89B7",
        reliability: "#92C7CD",
      },
      columns: [
        {
          text: "Name of signal",
          value: "attribute_name",
          width: "170px",
          tooltipWidth: "300px",
          hoverTooltip:
            "The trustwortiness of a brand is measured with key elements such as Capability, Humanity, Reliability and Transparency.  ",
        },
        {
          text: "Attribute score",
          value: "attribute_score",
          width: "134px",
          tooltipWidth: "300px",
          hoverTooltip:
            "Attribute scores are additional data points that can be used to diagnose what is driving a particular signal score.",
        },
        {
          text: "Attributes",
          value: "attribute_description",
          width: "605px",
          tooltipWidth: "300px",
          hoverTooltip:
            "Attributes are the trust-building actions that have the greatest impact on your 4 HX TrustID signal scores.",
        },
        {
          text: "Customer rating",
          value: "overall_customer_rating",
          width: "196px",
          tooltipWidth: "300px",
          hoverTooltip:
            "Percentage of customers who disagree with the attributes (red), are neutral (yellow), or agree (green).",
        },
      ],
    }
  },
  computed: {},
  methods: {
    getRating(rating) {
      let results = []
      Object.entries(rating).map((item) => {
        let obj = {
          label: item[0],
          value: parseFloat((item[1].percentage * 100).toFixed(2)),
        }
        results.push(obj)
      })
      return results
    },
    getRhombusColour(val) {
      return this.trustColor[val.attribute_name]
    },
  },
}
</script>
<style lang="scss" scoped>
.attribute-table-wrapper {
  .attribute-table {
    ::v-deep .v-data-table .v-data-table-header th:first-child {
      border-top-left-radius: 12px !important;
    }
    ::v-deep .v-data-table .v-data-table-header th:last-child {
      border-top-right-radius: 12px !important;
    }
    ::v-deep .theme--light.v-data-table.v-data-table--fixed-header thead th {
      box-shadow: none !important;
    }
    ::v-deep .v-data-table__wrapper {
      tbody {
        .text-width {
          width: 580px;
          text-align: left;
        }
      }
    }
  }
  .hux-data-table {
    ::v-deep table {
      .v-data-table-header {
        tr {
          th {
            background: var(--v-primary-lighten2);
            height: 40px !important;
          }
        }
      }
    }
  }
}
</style>
