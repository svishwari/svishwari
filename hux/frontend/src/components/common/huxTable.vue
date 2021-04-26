<template>
  <div :style="`width:${width}; height:${height}; transition:all 0.5s;`">
    <ag-grid-vue
      class="ag-theme-alpine hux-table"
      style="width: 100%; height: 100%"
      :columnDefs="appliedColumns"
      :rowData="filterRows"
      :gridOptions="gridOptions"
      :overlayLoadingTemplate="overlayLoadingTemplate"
      :overlayNoRowsTemplate="overlayNoRowsTemplate"
      :frameworkComponents="frameworkComponents"
      :rowHeight="rowHeight"
    >
    </ag-grid-vue>
  </div>
</template>

<script>
import "ag-grid-community/dist/styles/ag-grid.css"
import "ag-grid-community/dist/styles/ag-theme-balham.css"
import { AgGridVue } from "ag-grid-vue"

export default {
  name: "huxTable",

  components: {
    AgGridVue,
  },

  props: {
    columnDef: {
      type: Array,
      default: () => [
        { field: "make" },
        { field: "model" },
        { field: "price" },
      ],
      required: true,
    },

    tableData: {
      type: Array,
      default: () => [],
      required: true,
    },

    width: {
      type: String,
      default: "100%",
    },

    height: {
      type: String,
      default: "100px",
    },

    hasCheckBox: {
      type: Boolean,
      default: false,
    },

    frameworkComponents: {
      type: Object,
      default: null,
    },

    rowHeight: {
      type: Number,
      default: 60,
    },
  },
  data() {
    return {
      gridOptions: {
        animateRows: true,
        rowDragManaged: true,
        suppressRowClickSelection: true,
      },
    }
  },
  computed: {
    appliedColumns() {
      let columnDefinitiions = [...this.columnDef]
      if (!this.hasCheckBox) return columnDefinitiions

      columnDefinitiions[0]["headerCheckboxSelection"] = true
      columnDefinitiions[0]["headerCheckboxSelectionFilteredOnly"] = true
      columnDefinitiions[0]["checkboxSelection"] = true

      columnDefinitiions.forEach((col) => (col["suppressMovable"] = true))
      return columnDefinitiions
    },
    filterRows() {
      return this.tableData
    },
  },
  methods: {
    refresh: async function () {
      let vo = this
      try {
        vo.gridOptions.api.redrawRows()
      } catch (err) {
        console.error(err)
      }
    },
  },
  beforeMount() {
    this.gridOptions = {
      rowSelection: "multiple",
      headerHeight: 32,
    }
    this.overlayLoadingTemplate =
      "<span class='ag-overlay-loading-center'>Please wait while your rows are loading</span>"
    this.overlayNoRowsTemplate =
      "<span style=\"padding: 10px; border: 2px solid #444; background: lightgoldenrodyellow;\">This is a custom 'no rows' overlay</span>"
  },
  mounted() {},
}
</script>

<style lang="scss" scoped>
.hux-table {
  &.ag-theme-alpine {
    font-family: Open Sans;
    font-style: normal;
    font-weight: 400;
    line-height: 16px;
  }
  background: red;
  font-family: inherit;
  font-size: 12px;
  ::v-deep .ag-root-wrapper {
    border: none;
    border-top: solid 1px;
    border-color: #babfc7;
    .menu-cells {
      .ag-cell-value {
        width: 100%;
      }
    }
    .ag-root-wrapper-body {
      .ag-header {
        height: 32px !important;
        font-size: 12px;
        font-family: inherit;
        font-style: normal;
        font-weight: 600;
        line-height: 16px;
        background: transparent;
      }
      .ag-row-hover {
        background: rgba(0, 118, 168, 0.05);
        .ag-checkbox {
          .ag-input-wrapper {
            display: block;
          }
        }
      }
      .ag-row-selected {
        background: rgba(0, 118, 168, 0.05);
        .ag-checkbox {
          .ag-input-wrapper {
            display: block;
          }
        }
      }
      .ag-header-row {
        .ag-checkbox {
          .ag-input-wrapper {
            display: block;
          }
        }
      }

      .ag-checkbox {
        .ag-input-wrapper {
          display: none;
        }
      }
      .ag-center-cols-container {
        min-width: inherit !important;
      }
    }
  }
}
</style>
