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
                <div class="attribute-name">
                  <rhombus-number
                    class="rhombus-icon"
                    :color="getRhombusColour(item).stroke"
                    :variant="getRhombusColour(item).variant"
                  />
                  {{ item[col.value] }}
                </div>
              </template>
              <template v-else-if="col.value === 'attribute_score'">
                <rhombus-number
                  class="ml-10"
                  :value="item[col.value]"
                  :color="getRhombusColour(item).stroke"
                  :variant="getRhombusColour(item).variant"
                />
              </template>
              <template v-else-if="col.value === 'attribute_description'">
                <tooltip min-width="300px" max-width="300px">
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
                <tooltip max-width="183px">
                  <template #label-content>
                    <progress-stack-bar
                      :width="180"
                      :height="6"
                      :show-percentage="true"
                      :data="getRating(item[col.value].rating)"
                      :bar-id="index + 'table'"
                    />
                  </template>
                  <template #hover-content>
                    <div class="body-2">
                      <div class="d-flex flex-column">
                        <span class="tooltip-subheading disagree-color my-2">
                          Disagree
                        </span>
                        <span>
                          {{
                            item[col.value].rating.agree.percentage
                              | Numeric(false, false, false, true)
                          }}
                          |
                          {{
                            numberWithCommas(item[col.value].rating.agree.count)
                          }}
                        </span>
                        <span class="tooltip-subheading neutral-color my-2">
                          Neutral
                        </span>
                        <span>
                          {{
                            item[col.value].rating.neutral.percentage
                              | Numeric(false, false, false, true)
                          }}
                          |
                          {{
                            numberWithCommas(
                              item[col.value].rating.neutral.count
                            )
                          }}
                        </span>
                        <span class="tooltip-subheading agree-color my-2">
                          Agree
                        </span>
                        <span>
                          {{
                            item[col.value].rating.disagree.percentage
                              | Numeric(false, false, false, true)
                          }}
                          |
                          {{
                            numberWithCommas(
                              item[col.value].rating.disagree.count
                            )
                          }}
                        </span>
                      </div>
                    </div>
                  </template>
                </tooltip>
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
import { numberWithCommas } from "@/utils"

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
        humanity: { stroke: "primary", variant: "darken6" },
        transparency: { stroke: "yellow", variant: "darken1" },
        capability: { stroke: "primary", variant: "darken5" },
        reliability: { stroke: "secondary", variant: "lighten2" },
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
    numberWithCommas: numberWithCommas,
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
        .attribute-name {
          line-height: 8px;
          .rhombus-icon {
            width: 11px;
            height: 11px;
            float: left;
            margin-right: 8px;
          }
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

.v-application {
  .disagree-color {
    color: var(--v-error-base);
  }
  .neutral-color {
    color: var(--v-yellow-base);
  }
  .agree-color {
    color: var(--v-success-lighten3);
  }
}
</style>
