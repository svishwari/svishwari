<template>
  <div class="hux-data-table">
    <div class="table-overflow" :style="{ height: viewHeight }">
      <v-data-table
        :expanded.sync="expanded"
        :headers="columns"
        :hide-default-header="!showHeader || !hasData"
        :height="height"
        :items="dataItems"
        :sort-by.sync="sortByColumn"
        :sort-desc.sync="sortOrder"
        item-key="name"
        :items-per-page="-1"
        fixed-header
        hide-default-footer
        must-sort
        :disable-sort="disableSort"
      >
        <!-- table headers -->
        <template v-for="column in columns" #[`header.${column.value}`]>
          <tooltip v-if="column.tooltipValue" :key="column.id">
            <template #label-content>
              {{ column.text }}
            </template>
            <template #hover-content>
              <span
                v-html="
                  column.tooltipValue.replace(/(?:\r\n|\r|\n)/g, '<br />')
                "
              ></span>
            </template>
          </tooltip>
          <template v-if="!column.tooltipValue">
            <!-- TODO: find a better solution and remove v-html -->
            <span :key="column.value" v-html="column.text" />
          </template>
          <tooltip
            v-if="column.hoverTooltip"
            :key="column.id"
            :max-width="column.tooltipWidth"
            position-top
          >
            <template #label-content>
              <icon
                v-if="column.hoverTooltip"
                :key="column.id"
                type="info"
                :size="12"
                class="ml-1"
                color="primary"
                variant="base"
              />
            </template>
            <template #hover-content>
              {{ column.hoverTooltip }}
            </template>
          </tooltip>
        </template>

        <!-- table rows -->
        <template v-if="hasData && nested" #item="{ item, expand, isExpanded }">
          <slot
            name="item-row"
            :item="item"
            :expandFunc="expand"
            :isExpanded="isExpanded"
            :rowHeight="rowHeight"
          ></slot>
        </template>

        <template v-if="hasData && !nested" #body="{ nestedHeaders, items }">
          <tbody>
            <tr v-for="item in items" :key="item.id" :style="{height: rowHeight }">
              <slot name="row-item" :item="item" :headers="nestedHeaders" :rowHeight="rowHeight"/>
            </tr>
          </tbody>
        </template>

        <!-- table expanded content -->
        <template #expanded-item="{ headers, item }">
          <slot
            name="expanded-row"
            :expandedHeaders="headers"
            :parentItem="item"
          />
        </template>

        <!-- table empty slot -->
        <template #no-data>
          <v-alert color="primary lighten-1" class="empty-table ma-0">
            <v-row class="text-left black--text text--darken-1">
              <slot v-if="$slots.empty" name="empty"></slot>
              <v-col v-else class="grow">{{ empty }}</v-col>
            </v-row>
          </v-alert>
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
      type: [Boolean, String],
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
    empty: {
      type: String,
      required: false,
      default: "Nothing to show here yet.",
    },
    rowHeight: {
      type: String,
      required: false,
    }
  },
  data() {
    return {
      expanded: [],
      itemPerPage: ALL,
    }
  },
  computed: {
    hasData() {
      return this.dataItems && this.dataItems.length
    },
    sortOrder: {
      get: function () {
        return Boolean(this.sortDesc)
      },
      set: function (value) {
        this.$emit("sortDesc", value)
      },
    },
    sortByColumn: {
      get: function () {
        return this.sortColumn
      },
      set: function (value) {
        this.$emit("sortColumn", value)
      },
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
          padding-top: 0px;
          padding-bottom: 0px;
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

  ::v-deep .v-data-table__empty-wrapper {
    text-align: left;

    td {
      padding: 0 !important;
      border: 0 !important;

      .empty-table {
        border: 1px solid var(--v-black-lighten2) !important;
        padding: 20px;
      }
    }
  }
}
</style>
