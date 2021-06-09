<template>
  <div class="hux-data-table">
    <div class="table-overflow" :style="{ 'margin-left': fixedWidth }">
      <v-data-table
        :headers="headers"
        :items="dataItems"
        item-key="name"
        :hide-default-footer="true"
        :fixed-header="true"
        must-sort
        :sort-by="sortColumn"
        sort-desc
        :height="height"
        :expanded.sync="expanded"
        :items-per-page="-1"
        :hide-default-header="!showHeader"
        @click:row="expandRow"
      >
        <template #item.name="{ item, isExpanded }" v-if="nested">
          <slot name="item-name" :item="item" :isExpanded="isExpanded" />
        </template>
        <template #item.data-table-expand="{ expand, isExpanded }">
          <v-icon
            @click="expand(!isExpanded)"
            small
            color="darkGrey"
            :class="{
              'rotate-expand-icon': !isExpanded,
            }"
          >
            <template>mdi-chevron-down</template>
          </v-icon>
        </template>
        <template v-for="h in headers" v-slot:[`header.${h.value}`]>
          <tooltip :key="h.value" v-if="h.tooltipValue">
            <template slot="label-content">
              {{ h.text }}
            </template>
            <template slot="hover-content">
              <span
                v-html="h.tooltipValue.replace(/(?:\r\n|\r|\n)/g, '<br />')"
              ></span>
            </template>
          </tooltip>
          <template v-if="!h.tooltipValue">
            {{ h.text }}
          </template>
        </template>
        <template #body="{ headers, items }" v-if="!nested">
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <slot name="row-item" :item="item" :headers="headers" />
            </tr>
          </tbody>
        </template>
        <template #expanded-item="{ headers, item }">
          <slot name="expanded-row" :headers="headers" :item="item" />
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
import Tooltip from "../Tooltip.vue"
export default {
  name: "HuxDataTable",
  components: { Tooltip },
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
    showHeader: {
      type: Boolean,
      required: false,
      default: true,
    },
    sortColumn: {
      type: String,
      required: false,
      default: "name",
    },
  },
  data() {
    return {
      expanded: [],
    }
  },
  computed: {
    fixedWidth() {
      const fixedHeaders = this.headers.filter((item) => item.fixed)

      return fixedHeaders.length > 0
        ? fixedHeaders
            .map(({ width }) => width)
            .map((item) => parseInt(item, 0))
            .reduce((a, b) => a + b) + "px"
        : "0px"
    },
  },
  methods: {
    expandRow(value) {
      const index = this.expanded.indexOf(value)
      if (index === -1) {
        this.expanded.push(value)
      } else {
        this.expanded.splice(index, 1)
      }
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
    ::v-deep .v-data-table__expanded__content {
      padding: 0px;
    }
  }
}
</style>
