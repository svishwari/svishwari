<template>
  <div class="hux-data-table">
    <div class="table-overflow" :style="{ height: viewHeight }">
      <v-data-table
        :expanded.sync="expanded"
        :headers="columns"
        :hide-default-header="!showHeader"
        :height="height"
        :items="dataItems"
        :sort-by.sync="sortColumn"
        :sort-desc.sync="sortDesc"
        item-key="name"
        :items-per-page="-1"
        fixed-header
        hide-default-footer
        must-sort
        single-select
        :disable-sort="disableSort"
      >
        <template v-if="nested" #item="{ item, expand, isExpanded }">
          <slot
            name="item-row"
            :item="item"
            :expandFunc="expand"
            :isExpanded="isExpanded"
          ></slot>
        </template>
        <template v-for="h in columns" v-slot:[`header.${h.value}`]>
          <tooltip v-if="h.tooltipValue" :key="h.id">
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
            <!-- TODO: find a better solution and remove v-html -->
            <span :key="h.value" v-html="h.text" />
          </template>
          <tooltip v-if="h.hoverTooltip" :key="h.id" position-top>
            <template #label-content>
              <icon
                v-if="h.hoverTooltip"
                :key="h.id"
                type="info"
                :size="12"
                class="ml-1"
              />
            </template>
            <template #hover-content>
              {{ h.hoverTooltip }}
            </template>
          </tooltip>
        </template>
        <template v-if="!nested" #body="{ nestedHeaders, items }">
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <slot name="row-item" :item="item" :headers="nestedHeaders" />
            </tr>
          </tbody>
        </template>
        <template #expanded-item="{ headers, item }">
          <slot
            name="expanded-row"
            :expandedHeaders="headers"
            :parentItem="item"
          />
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
    columns: {
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
    sortDesc: {
      type: Boolean,
      required: false,
      default: false,
    },
    disableSort: {
      type: Boolean,
      required: false,
      default: false,
    },
    viewHeight: {
      type: String,
      required: false,
      default: "auto",
    },
  },
  data() {
    return {
      expanded: [],
      itemPerPage: ALL,
    }
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
  ::v-deep .v-data-table__wrapper {
    overflow-y: visible;
    overflow-x: visible;
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
    color: var(--v-black-darken4) !important;
    cursor: default !important;
    background: transparent !important;
  }
  .table-overflow {
    overflow-x: auto;
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
          color: var(--v-black-darken4) !important;
          i {
            font-size: 16px !important;
            color: #00a3e0 !important;
          }
        }
      }
    }
    tr:last-child > td {
      border-bottom: thin solid rgba(0, 0, 0, 0.12);
    }
    ::v-deep .v-data-table__expanded__content {
      padding: 0px;
    }
  }
}
</style>
