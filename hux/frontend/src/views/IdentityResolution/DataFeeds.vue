<template>
  <v-card flat class="card-style">
    <v-progress-linear :active="isLoading" :indeterminate="isLoading" />
    <v-card-title class="pa-6">
      <h5 class="text-h5 black--text text--darken-4">Data feeds</h5>
    </v-card-title>
    <v-card-text class="px-6">
      <hux-data-table
        v-if="!isLoading"
        :columns="columns"
        :data-items="data"
        :sort-column="sortColumn"
        :sort-desc="sortDesc"
        empty="Be patient! The data feeds are currently not available, check back tomorrow to see if the magic is ready."
      >
        <template #row-item="{ item }">
          <td
            v-for="col in columns"
            :key="col.value"
            class="black--text text--darken-4 text-h6"
          >
            <tooltip v-if="col.value === 'datafeed_name'">
              <span
                class="d-inline-block mw-100 text-truncate text-decoration-none"
              >
                {{ item[col.value] }}
              </span>
              <template #tooltip>
                {{ item[col.value] }}
              </template>
            </tooltip>
            <template v-else-if="col.value === 'data_source_type'">
              <logo
                :key="item[col.value]"
                :type="item[col.value]"
                :size="26"
                class="my-3"
              />
            </template>
            <template v-else-if="col.value === 'match_rate'">
              {{ item[col.value] | Numeric(false, false, false, true) }}
            </template>
            <tooltip v-else-if="col.value === 'new_ids_generated'">
              {{ item[col.value] | Numeric(false, true) }}
              <template #tooltip>
                {{ item[col.value] | Numeric }} IDs
              </template>
            </tooltip>
            <tooltip v-else-if="col.value === 'num_records_processed'">
              {{ item[col.value] | Numeric(false, true) }}
              <template #tooltip>
                {{ item[col.value] | Numeric }} Records
              </template>
            </tooltip>
            <tooltip v-else-if="col.value === 'last_run'">
              <v-btn
                text
                class="pa-1"
                height="auto"
                color="primary"
                data-e2e="lastrun"
                @click="openLastRunDrawer(item)"
              >
                {{ item[col.value] | Date("relative") }}
              </v-btn>
              <template #tooltip>{{ item[col.value] | Date }}</template>
            </tooltip>
          </td>
        </template>
      </hux-data-table>
      <last-run-drawer
        v-model="toggleLastRunDrawer"
        :data-feed-id="selectedDataFeedId"
      ></last-run-drawer>
    </v-card-text>
  </v-card>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Logo from "@/components/common/Logo.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import LastRunDrawer from "./Drawers/LastRunDrawer.vue"

export default {
  name: "DataFeeds",

  components: {
    HuxDataTable,
    Logo,
    Tooltip,
    LastRunDrawer,
  },

  props: {
    data: {
      type: Array,
      required: false,
    },

    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      columns: [
        {
          text: "Data feed",
          value: "datafeed_name",
          width: "200px",
        },
        {
          text: "Data source",
          value: "data_source_type",
          width: "120px",
        },
        {
          text: "New IDs generated",
          value: "new_ids_generated",
          width: "160px",
        },
        {
          text: "No. records processed",
          value: "num_records_processed",
          width: "180px",
        },
        {
          text: "Match rate",
          value: "match_rate",
          width: "130px",
          hoverTooltip:
            "Percentage of input records that are consolidated into Hux IDs.",
        },
        {
          text: "Last run",
          value: "last_run",
          width: "160px",
        },
      ],

      sortColumn: "last_run",

      sortDesc: true,

      toggleLastRunDrawer: false,

      selectedDataFeedId: null,
    }
  },

  computed: {
    hasData() {
      return this.data && this.data.length
    },
  },

  methods: {
    openLastRunDrawer(item) {
      this.selectedDataFeedId = item.datafeed_id
      this.toggleLastRunDrawer = true
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
          background: var(--v-primary-lighten2);
          height: 40px !important;
        }
      }
    }
  }
}
</style>
