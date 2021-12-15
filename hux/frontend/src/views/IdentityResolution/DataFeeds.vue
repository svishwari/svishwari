<template>
  <v-card flat class="card-style">
    <v-progress-linear :active="isLoading" :indeterminate="isLoading" />
    <template v-if="!isLoading">
      <v-card-title v-if="data.length > 0" class="py-5 px-6">
        <span class="text-h3 black--text">Data feeds</span>
      </v-card-title>
      <v-card-text v-if="data.length > 0" class="px-6">
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
              class="black--text text--darken-4 text-body-1"
            >
              <tooltip v-if="col.value === 'datafeed_name'">
                <span
                  class="
                    d-inline-block
                    mw-100
                    text-truncate text-decoration-none
                  "
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

      <v-row v-else class="data-feeds-table-frame py-14">
        <empty-page v-if="!isErrorState" type="model-features-empty" :size="50">
          <template #title>
            <div class="title-no-notification">No data to show</div>
          </template>
          <template #subtitle>
            <div class="des-no-notification">
              Data feeds table will appear here after being ingested.
            </div>
          </template>
        </empty-page>
        <empty-page
          v-else
          class="title-no-notification"
          type="error-on-screens"
          :size="50"
        >
          <template #title>
            <div class="title-no-notification">
              Data feeds table is currently unavailable
            </div>
          </template>
          <template #subtitle>
            <div class="des-no-notification">
              Our team is working hard to fix it. Please be patient and try
              again soon!
            </div>
          </template>
        </empty-page>
      </v-row>
    </template>
  </v-card>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Logo from "@/components/common/Logo.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import LastRunDrawer from "./Drawers/LastRunDrawer.vue"
import EmptyPage from "@/components/common/EmptyPage"

export default {
  name: "DataFeeds",

  components: {
    HuxDataTable,
    Logo,
    Tooltip,
    LastRunDrawer,
    EmptyPage,
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
    isErrorState: {
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

.data-feeds-table-frame {
  background-image: url("../../assets/images/no-lift-chart-frame.png");
  background-position: center;
}
</style>
