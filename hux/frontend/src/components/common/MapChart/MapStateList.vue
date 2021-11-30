<template>
  <div class="list-container">
    <hux-data-table
      :columns="columnDefs"
      :height="height"
      :sort-column="customMetric"
      :sort-desc="true"
      :data-items="stateListData"
    >
      <template #row-item="{ item }">
        <td
          v-for="header in columnDefs"
          :key="header.value"
          class="text-body-2"
          :style="{ width: header.width }"
          data-e2e="map-state-list"
        >
          <div v-if="header.value == defaultMetric" class="text-body-1">
            <span v-if="item[defaultMetric]">{{ item[defaultMetric] }} </span>
          </div>
          <div v-if="header.value == customMetric" class="text-body-1">
            <tooltip>
              <template #label-content>
                {{
                  item[customMetric]
                    | Numeric(true, true)
                    | Currency
                    | Empty("-")
                }}
              </template>
              <template #hover-content>
                <div class="mb-1">Avg. spend</div>
                {{
                  item[customMetric]
                    | Numeric(true, false, false)
                    | Currency
                    | Empty("-")
                }}
              </template>
            </tooltip>
          </div>
          <div v-if="header.value == primaryMetric" class="text-body-1">
            <tooltip>
              <template #label-content>
                {{
                  item[primaryMetric]
                    | Numeric(true, false, false, true)
                    | Empty("-")
                }}
              </template>
              <template #hover-content>
                <div class="mb-1">Population</div>
                {{ item.size | Numeric(true, false, false) | Empty("-") }}
              </template>
            </tooltip>
          </div>
        </td>
      </template>
    </hux-data-table>
  </div>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "MapStateList",
  components: {
    HuxDataTable,
    Tooltip,
  },
  props: {
    mapData: {
      type: Array,
      required: true,
    },
    configurationData: {
      type: Object,
      required: true,
    },
    height: {
      type: Number,
      required: false,
    },
    headerConfig: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      mapChartData: [],
      stateListData: [],
      columnDefs: [
        {
          text: "State",
          value: "name",
          width: "40%",
        },
        {
          text: "Avg. spend",
          value: "avg_spend",
          width: "30%",
          hoverTooltip:
            "Average order value for all customers (known and anyonymous) for all time.",
        },
        {
          text: "Population %",
          value: "population_percentage",
          width: "30%",
        },
      ],
    }
  },
  computed: {
    primaryMetric() {
      return this.configurationData.primary_metric.key
    },
    defaultMetric() {
      return this.configurationData.default_metric.key
    },
    customMetric() {
      return this.configurationData.custom_metric.key
    },
  },
  mounted() {
    this.processStateListData()
  },
  methods: {
    processStateListData() {
      this.stateListData = JSON.parse(JSON.stringify(this.mapData))

      this.columnDefs = this.columnDefs.filter((column) =>
        this.headerConfig.includes(column.value)
      )
    },
    applyFilter(value, filter) {
      switch (filter) {
        case "numeric":
          return this.$options.filters.Numeric(value, true, false, false)
        case "percentage":
          return this.$options.filters.Numeric(value, true, false, false, true)
        case "currency":
          return this.$options.filters.Currency(value)
        default:
          return this.$options.filters.Empty
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.global-text-line {
  display: inline-block;
  font-style: normal;
  font-size: $font-size-root;
  line-height: 19px;
}
.list-container {
  max-height: 550px;
  min-height: 20px;

  ::v-deep .hux-data-table {
    table {
      .v-data-table-header {
        th:nth-child(1) {
          position: sticky;
          left: 0;
          z-index: 9;
          overflow-y: visible;
          overflow-x: visible;
        }
      }
      tbody {
        height: calc(100% - 40px);
        overflow: auto;
        width: 100%;
        position: absolute;
        display: inline-block;
        tr {
          display: table;
          width: 100%;
          td {
            &:last-child {
              padding-left: 19px;
            }
          }
        }
      }
    }
    .v-data-table {
      .v-data-table-header {
        tr {
          height: 40px !important;
        }
        th {
          background: var(--v-primary-lighten1);
          &:last-child {
            border-top-right-radius: 12px;
          }
        }
      }
    }
  }
  .content-style {
    padding-top: 0px !important;
    min-height: 100px;
    max-height: 318px;
    overflow-y: scroll;
    .sub-props {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      .subprop-name {
        @extend .global-text-line;
        flex: 1 0 30%;
        text-align: right;
        margin-right: 30px;
      }
      .value {
        @extend .global-text-line;
        color: var(--v-black-darken4);
        flex: 1;
        text-align: left;
      }
    }
  }
}
</style>
