<template>
  <div class="hux-data-table">
    <div class="table-overflow" :style="{ 'margin-left': fixedWidth }">
      <v-data-table
        :expanded.sync="expanded"
        :headers="headers"
        :hide-default-header="!showHeader"
        :height="height"
        :items="dataItems"
        :sort-by.sync="sortColumn"
        item-key="name"
        :items-per-page="-1"
        fixed-header
        hide-default-footer
        must-sort
        sort-desc
        single-select
        :disable-sort="disableSort"
      >
        <template #item="{ item, expand, isExpanded }" v-if="nested">
          <slot
            name="item-row"
            :item="item"
            :expand="expand"
            :isExpanded="isExpanded"
          ></slot>
        </template>
        <template v-for="h in headers" v-slot:[`header.${h.value}`]>
          <tooltip :key="h.value" v-if="h.tooltipValue">
            <template #label-content>
              {{ h.text }}
            </template>
            <template #hover-content>
              <span
                v-html="h.tooltipValue.replace(/(?:\r\n|\r|\n)/g, '<br />')"
              ></span>
            </template>
          </tooltip>
          <template v-if="!h.tooltipValue">
            <span v-html="h.text" :key="h.value" />
          </template>
          <Tooltip :key="h.value" v-if="h.hoverTooltip" positionTop>
            <template #label-content>
              <Icon
                type="info"
                :size="12"
                :key="h.value"
                v-if="h.hoverTooltip"
              />
            </template>
            <template #hover-content>
              {{ h.hoverTooltip }}
            </template>
          </Tooltip>
        </template>
        <template #body="{ headers, items }" v-if="!nested">
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <slot name="row-item" :item="item" :headers="headers" />
            </tr>
          </tbody>
        </template>
        <template #expanded-item="{ headers, item }">
          <slot name="expanded-row" :headers="headers" :parentItem="item" />
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
import Tooltip from "../Tooltip.vue"
import Icon from "@/components/common/Icon"
const ALL = -1
export default {
  name: "HuxDataTable",
  components: { Tooltip, Icon },
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
    disableSort: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      expanded: [],
      itemPerPage: ALL,
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
    clickRow(_, event) {
      event.expand(!event.isExpanded)
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
