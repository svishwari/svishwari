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
      @gridReady="tableReady"
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
      if (!this.hasCheckBox) return this.columnDef

      this.columnDef[0]["headerCheckboxSelection"] = true
      this.columnDef[0]["headerCheckboxSelectionFilteredOnly"] = true
      this.columnDef[0]["checkboxSelection"] = true

      return this.columnDef
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
      } catch (err) {}
    },
    tableReady: function (params) {
      console.log("methods agReady", params)
    },
  },
  beforeMount() {
    this.gridOptions = {
      rowSelection: "multiple",
    }
    this.overlayLoadingTemplate =
      "<span class='ag-overlay-loading-center'>Please wait while your rows are loading</span>"
    this.overlayNoRowsTemplate =
      "<span style=\"padding: 10px; border: 2px solid #444; background: lightgoldenrodyellow;\">This is a custom 'no rows' overlay</span>"
  },
  mounted() {},
}
</script>

<style lang="scss" scoped></style>
