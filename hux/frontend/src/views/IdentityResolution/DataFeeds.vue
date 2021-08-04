<template>
  <v-card v-if="hasData" flat class="pa-2 card-style">
    <v-card-title>
      <h5 class="text-h5 neroBlack--text">Data feeds</h5>
    </v-card-title>
    <v-card-text>
      <hux-data-table
        :headers="headers"
        :data-items="data"
        :sort-column="sortColumn"
        :sort-desc="sortDesc"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in headers"
            :key="header.value"
            class="neroBlack--text text-h6"
          >
            <tooltip v-if="header.value === 'datafeed_name'">
              <span
                class="d-inline-block mw-100 text-truncate text-decoration-none"
              >
                {{ item[header.value] }}
              </span>
              <template #tooltip>
                {{ item[header.value] }}
              </template>
            </tooltip>
            <template v-else-if="header.value === 'data_source_type'">
              <logo
                :key="item[header.value]"
                :type="item[header.value]"
                :size="26"
                class="my-3"
              />
            </template>
            <template v-else-if="header.value === 'match_rate'">
              {{ item[header.value] | Numeric(false, false, false, true) }}
            </template>
            <tooltip v-else-if="header.value === 'new_ids_generated'">
              {{ item[header.value] | Numeric(false, true) }}
              <template #tooltip>
                {{ item[header.value] | Numeric }} IDs
              </template>
            </tooltip>
            <tooltip v-else-if="header.value === 'num_records_processed'">
              {{ item[header.value] | Numeric(false, true) }}
              <template #tooltip>
                {{ item[header.value] | Numeric }} Records
              </template>
            </tooltip>
            <tooltip v-else-if="header.value === 'last_run'">
              <v-btn
                text
                class="pa-1"
                height="auto"
                color="primary"
                @click="openLastRunDrawer(item)"
              >
                {{ item[header.value] | Date("relative") }}
              </v-btn>
              <template #tooltip>{{ item[header.value] | Date }}</template>
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
  },

  data() {
    return {
      headers: [
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
  }
}
</style>
