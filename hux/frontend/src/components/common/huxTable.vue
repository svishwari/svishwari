<template>
  <div :style="`width:${width}; height:${height}; transition:all 0.5s;`">
    <ag-grid-vue
      class="ag-theme-alpine hux-table"
      style="width: 100%; height: 100%"
      :column-defs="appliedColumns"
      :row-data="filterRows"
      :grid-options="gridOptions"
      :overlay-loading-template="overlayLoadingTemplate"
      :overlay-no-rows-template="overlayNoRowsTemplate"
      :framework-components="frameworkComponents"
      :row-height="rowHeight"
    ></ag-grid-vue>
  </div>
</template>

<script>
import "ag-grid-community/dist/styles/ag-grid.css"
import "ag-grid-community/dist/styles/ag-theme-balham.css"
import { AgGridVue } from "ag-grid-vue"

export default {
  name: "HuxTable",

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
        suppressCellSelection: true,
        headerHeight: "32",
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
  beforeMount() {
    this.gridOptions = {
      rowSelection: "multiple",
      headerHeight: "32",
    }
    this.overlayLoadingTemplate =
      "<span class='ag-overlay-loading-center'>Please wait while your rows are loading</span>"
    this.overlayNoRowsTemplate =
      "<span style=\"padding: 10px; border: 2px solid #444; background: lightgoldenrodyellow;\">This is a custom 'no rows' overlay</span>"
  },
  mounted() {},
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
  ::v-deep .ag-root-wrapper {
    border: none;
    border-top: solid 1px;
    border-color: var(--v-black-lighten3) !important;
    .menu-cells {
      .ag-cell-value {
        width: 100%;
      }
    }
    .ag-root-wrapper-body {
      .ag-header {
        height: 32px !important;
        max-height: 32px !important;
        min-height: 32px !important;
        background: transparent;
        border-color: var(--v-black-lighten3) !important;
        .ag-header-row {
          height: 32px !important;
        }
      }
      .ag-row {
        border-color: var(--v-black-lighten3) !important;
        .ag-cell {
          display: flex;
          align-items: center;
          cursor: default !important;
        }
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
        color: var(--v-black-darken4);
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
        width: 100% !important;
      }
      .ag-icon.ag-icon-asc,
      .ag-icon.ag-icon-desc {
        color: var(--v-primary-darken2);
      }
      .ag-horizontal-left-spacer {
        display: table;
      }
    }
  }
}
</style>
