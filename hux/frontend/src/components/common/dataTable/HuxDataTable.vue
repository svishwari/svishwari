<template>
  <div class="hux-data-table">
    <div class="table-overflow" :style="{ 'margin-left': FixedWidth }">
      <v-data-table
        :headers="headers"
        :items="dataItems"
        item-key="name"
        :hide-default-footer="true"
        fixed-header
        must-sort
        :sort-by="sortColumn"
        sort-desc
        :height="height"
        :items-per-page="100"
      >
        <template v-slot:body="{ items }" v-if="!nested">
          <tbody class="data-table-body">
            <tr
              v-for="item in items"
              :key="item.id"
              class="data-table-row neroBlack--text"
            >
              <slot name="row-item" :item="item" />
            </tr>
          </tbody>
        </template>
        <template v-slot:item="{ item, expand, isExpanded }" v-if="nested">
          <tr>
            <td></td>
            <td v-for="field in Object.keys(item)" :key="field.name">
              <slot
                name="table-row"
                :field="field"
                :item="item"
                :expand="expand"
                :isExpanded="isExpanded"
              >
              </slot>
            </td>
          </tr>
        </template>
        <template v-slot:expanded-item="{ item }" v-if="nested">
          <tr v-for="(field, index) in item.child" :key="index">
            <td></td>
            <slot name="expanded-row" :field="field"></slot>
          </tr>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "HuxDataTable",
  components: {},
  props: {
    dataItems: {
      type: Array,
      default: () => [],
      required: true,
    },
    headers: {
      type: Array,
      default: () => [],
      required: true,
    },
    nested: {
      type: Boolean,
      required: false,
      default: false,
    },
    height: {
      type: Number,
      required: false,
    },
    sortColumn: {
      type: String,
      required: false,
      default: "name",
    },
  },
  data() {
    return {
      search: "",
      expanded: [],
    }
  },
  computed: {
    FixedWidth() {
      return (
        this.headers
          .filter((item) => item.fixed)
          .map(({ width }) => width)
          .map((item) => parseInt(item, 0))
          .reduce((a, b) => a + b) + "px"
      )
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-data-table {
  width: 100%;
  position: relative;
  ::v-deep .material-icons.delivered {
    color: var(--v-success-lighten1);
  }
  ::v-deep .material-icons.delivering {
    color: var(--v-success-lighten2);
  }
  ::v-deep .material-icons.alert {
    color: var(--v-error-base);
  }
  ::v-deep .rotate-icon {
    transition: 0.3s;
    -webkit-transition: 0.3s;
    -moz-transition: 0.3s;
    -ms-transition: 0.3s;
    -o-transition: 0.3s;
    -webkit-transform: rotate(90deg);
    -moz-transform: rotate(90deg);
    -o-transform: rotate(90deg);
    -ms-transform: rotate(90deg);
    transform: rotate(90deg);
  }
  ::v-deep .avatar-border {
    border-width: 2px;
    border-style: solid;
    border-radius: 50%;
    font-size: 14px;
    width: 35px;
    height: 35px;
    line-height: 22px;
    color: var(--v-neroBlack-base) !important;
    cursor: default !important;
    background: transparent !important;
  }
  .table-overflow {
    overflow-x: auto;
    overflow-y: hidden !important;
  }
  ::v-deep table {
    table-layout: fixed;

    .fixed-column {
      position: absolute;
      display: flex;
      align-items: center;
      background: var(--v-white-base) !important;
      left: 0px;
      height: 59.84px !important;
    }
    .fixed-header {
      position: absolute;
      display: flex;
      align-items: center;
      background: var(--v-white-base) !important;
      left: 0px !important;
    }
    .v-data-table-header {
      tr {
        height: 32px !important;
        th {
          height: 32px !important;
          font-size: 12px;
          font-family: inherit;
          font-style: normal;
          font-weight: 400;
          line-height: 8px;
          padding-top: 0px;
          padding-bottom: 0px;
          color: var(--v-neroBlack-base) !important;
          i {
            font-size: 16px !important;
            color: #00a3e0 !important;
          }
        }
      }
    }
    .data-table-body {
      .data-table-row {
        height: 59.84px;
        td {
          font-size: 14px !important;
        }
      }
    }
  }
}
</style>
