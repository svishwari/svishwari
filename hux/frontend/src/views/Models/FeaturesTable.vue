<template>
  <hux-data-table
    :columns="columns"
    :data-items="data"
    :sort-column="sortColumn"
    :sort-desc="sortDesc"
  >
    <template #row-item="{ item }">
      <td
        v-for="col in columns"
        :key="col.value"
        class="black--text text-body-1"
      >
        <template v-if="col.value === 'name'">
          <tooltip>
            <template slot="label-content">
              <span class="ellipsis mt-1">
                {{ item[col.value] | Empty("-") }}
              </span>
            </template>
            <template slot="hover-content">
              {{ item[col.value] | Empty("-") }}
            </template>
          </tooltip>
        </template>

        <template v-else-if="col.value === 'description'" class="col-overflow">
          <tooltip>
            <template slot="label-content">
              <span class="ellipsis mt-1">
                {{ item[col.value] | Empty("-") }}
              </span>
            </template>
            <template slot="hover-content">
              {{ item[col.value] | Empty("-") }}
            </template>
          </tooltip>
        </template>
        <!-- // need after backend is updated -->

        <template v-else-if="col.value === 'feature_type'"> - </template>

        <template v-else-if="col.value === 'records_not_null'">
          {{ removeDecimal(item[col.value]) | Empty("-") }}
        </template>
        <!-- // need after backend is updated -->

        <template v-else-if="col.value === 'feature_importance'"> - </template>

        <template
          v-else-if="
            col.value === 'mean' || col.value === 'min' || col.value === 'max'
          "
        >
          {{ fixDecimalPlace(item[col.value]) | Empty("-") }}
        </template>

        <!-- // need after backend is updated -->

        <template v-else-if="col.value === 'unique_values'"> - </template>

        <template v-else-if="col.value === 'lcuv' || col.value === 'mcuv'">
          {{ item[col.value] }}
        </template>
      </td>
    </template>
  </hux-data-table>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "FeaturesTable",

  components: {
    HuxDataTable,
    Tooltip,
  },

  props: {
    data: {
      type: Array,
      required: false,
    },
  },

  data() {
    return {
      columns: [
        {
          text: "Feature name",
          value: "name",
          width: "285px",
        },
        {
          text: "Description",
          value: "description",
          width: "320px",
        },
        // need after backend is updated

        {
          text: "Feature type",
          value: "feature_type",
          width: "210px",
        },
        {
          text: "Records not null",
          value: "records_not_null",
          width: "180px",
        },
        // need after backend is updated

        {
          text: "Feature importance",
          value: "feature_importance",
          width: "180px",
        },
        {
          text: "Mean",
          value: "mean",
          width: "150px",
        },
        {
          text: "Min",
          value: "min",
          width: "150px",
        },
        {
          text: "Max",
          value: "max",
          width: "150px",
        },
        {
          text: "Unique values",
          value: "unique_values",
          width: "180px",
          hoverTooltip: "Number of unique values.",
        },
        {
          text: "LCUV",
          value: "lcuv",
          width: "210px",
          hoverTooltip: "Least common unique value.",
        },
        {
          text: "MCUV",
          value: "mcuv",
          width: "210px",
          hoverTooltip: "Most common unique value",
        },
      ],

      sortColumn: "name",

      sortDesc: true,
    }
  },
  methods: {
    fixDecimalPlace(data) {
      return Math.round(data * 10) / 10
    },
    // will remove once backend is updated
    removeDecimal(data) {
      return Math.floor(data) + "%"
    },
  },
}
</script>
<style lang="scss" scoped>
.hux-data-table {
  ::v-deep table {
    .v-data-table-header {
      tr {
        th {
          box-shadow: none !important;
          background: var(--v-primary-lighten2);
          height: 40px !important;
        }
      }
    }

    tr {
      td {
        height: 60px !important;
      }
    }

    .ellipsis {
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 28ch;
      display: inline-block;
      width: 28ch;
      white-space: nowrap;
    }

    border-radius: 12px 12px 0px 0px;
    overflow: hidden;
  }

  .col-overflow {
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }
}
</style>
