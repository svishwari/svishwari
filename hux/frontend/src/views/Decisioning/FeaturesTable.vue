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
        class="neroBlack--text text-h6"
      >
        <template v-if="col.value === 'name'">
          <tooltip>
            <template slot="label-content">
              <span class="ellipsis">
                {{ item[col.value] }}
              </span>
            </template>
            <template slot="hover-content">
              {{ item[col.value] }}
            </template>
          </tooltip>
        </template>

        <template v-if="col.value === 'feature_service'">
          {{ item[col.value] }}
        </template>

        <template v-if="col.value === 'data_source'">
          {{ item[col.value] }}
        </template>

        <template v-if="col.value === 'status'">
          <status
            :status="item[col.value]"
            :show-label="true"
            class="d-flex"
            :icon-size="17"
          />
        </template>

        <template v-if="col.value === 'popularity'">
          {{ item[col.value] }}
        </template>

        <template v-if="col.value === 'created_by'">
          <avatar :name="item[col.value]" />
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
          text: "Name of feature",
          value: "name",
          width: "285px",
        },
        {
          text: "Feature service",
          value: "feature_service",
          width: "197px",
        },
        {
          text: "Data source",
          value: "data_source",
          width: "150px",
        },
        {
          text: "Status",
          value: "status",
          width: "157px",
        },
        {
          text: "Popularity",
          value: "popularity",
          width: "150px",
          hoverTooltip:
            "Popularity of input records that are consolidated model features.",
        },
        {
          text: "Created by",
          value: "created_by",
          width: "107px",
        },
      ],

      sortColumn: "name",

      sortDesc: true,
    }
  },
}
</script>
<style lang="scss" scoped>
.hux-data-table {
  @extend .box-shadow-5;
  ::v-deep table {
    .v-data-table-header {
      tr {
        th {
          background: var(--v-aliceBlue-base);
          height: 40px !important;
        }
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
    :hover {
      .action-icon {
        display: block;
      }
    }
  }
}
</style>
