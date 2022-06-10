<template>
  <hux-data-table :columns="columns" :data-items="data" :sort-column="sortColumn" :sort-desc="sortDesc">
    <template #row-item="{ item }">
      <td v-for="col in columns" :key="col.value" class="col-overflow black--text text-body-1">
        <template v-if="col.value === 'name'">
          <tooltip>
            <template slot="label-content">
              <span class="ellipsis mt-1">
                {{ item[col.value] | Empty('-') }}
              </span>
            </template>
            <template slot="hover-content">
              {{ item[col.value] | Empty('-') }}
            </template>
          </tooltip>
        </template>

        <template v-else-if="col.value === 'description'">
          <tooltip>
            <template slot="label-content">
              <span class="ellipsis mt-1">
                {{ item[col.value] | Empty('-') }}
              </span>
            </template>
            <template slot="hover-content">
              {{ item[col.value] | Empty('-') }}
            </template>
          </tooltip>
        </template>

        <!-- <template v-else-if="col.value === 'feature_type'">
          {{ item[col.value] | Empty('-') }}
        </template> -->

        <template v-else-if="col.value === 'records_not_null'">
          {{ item[col.value] | Empty('-') }}
        </template>

        <!-- <template v-else-if="col.value === 'feature_importance'">
          {{ item[col.value] | Empty('-') }}
        </template> -->

        <template v-else-if="col.value === 'mean' || 'min' || 'max'">
          {{ fixDecimalPlace(item[col.value]) }}
        </template>

        <!-- <template v-else-if="col.value === 'unique_values'">
          {{ item[col.value] | Empty('-') }}
        </template> -->

        <template v-else-if="
          col.value === 'lcuv' || 'mcuv'
        ">
          {{ item[col.value] }}
        </template>

      </td>
    </template>
  </hux-data-table>
</template>

<script>
import Avatar from "@/components/common/Avatar.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Status from "@/components/common/Status.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "FeaturesTable",

  components: {
    Avatar,
    HuxDataTable,
    Status,
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
        // {
        //   text: "Feature type",
        //   value: "feature_type",
        //   width: "210px",
        // },
        {
          text: "Records not null",
          value: "records_not_null",
          width: "150px",
        },

        // {
        //   text: "Feature importance",
        //   value: "feature_importance",
        //   width: "150px",
        // },
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
        //  {
        //   text: "Unique values",
        //   value: "unique_values",
        //   width: "150px",
        //   hoverTooltip:
        //     "Number of unique values.",
        // },
        {
          text: "LCUV",
          value: "lcuv",
          width: "210px",
          hoverTooltip:
            "Least common unique value.",
        },
        {
          text: "MCUV",
          value: "mcuv",
          width: "210px",
          hoverTooltip:
            "Most common unique value",
        },
      ],

      sortColumn: "name",

      sortDesc: true,
    }
  },
  methods: {
    fixDecimalPlace(data) {
      if (typeof (data) !== 'string' || typeof (data) !== 'boolean') {
        return Math.round(data * 10) / 10
      } else {
        return data
      }
    }
  }
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
