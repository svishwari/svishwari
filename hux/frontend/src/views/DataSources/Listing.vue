<template>
  <div
    class="white"
    :class="!loading && hasDataFeeds == 0 ? 'background-base' : ' '"
  >
    <page-header v-if="selectedDataSource">
      <template #left>
        <breadcrumb :items="breadcrumbItems" />
      </template>
    </page-header>

    <v-progress-linear :active="loading" :indeterminate="loading" />

    <v-row v-if="!loading && hasDataFeeds" class="datasource-datafeeds-table">
      <hux-data-table
        sort-desc
        :columns="columns"
        :data-items="dataSourceDataFeeds"
      >
        <template #row-item="{ item }">
          <td v-for="column in columns" :key="column.value" class="text-body-1">
            <div
              v-if="column.value === 'status'"
              class="black--text text--darken-4 text-body-1"
            >
              <status
                :status="
                  item[column.value] === 'Pending'
                    ? 'Requested'
                    : item[column.value]
                "
                :show-label="true"
                class="data-feed-status d-flex"
                :icon-size="15"
              />
            </div>
            <tooltip
              v-else-if="
                column.value === 'records_processed_percentage' ||
                column.value === 'thirty_days_avg'
              "
            >
              <template #label-content>
                <span
                  class="text-body-1"
                  :class="
                    column.value === 'records_processed_percentage' &&
                    item[column.value] < 0.5
                      ? 'error--text'
                      : 'black--text text--darken-4'
                  "
                >
                  {{ item[column.value] | Percentage }}
                </span>
              </template>
              <template #hover-content>
                <span
                  class="text-body-1"
                  :class="
                    column.value === 'records_processed_percentage' &&
                    item[column.value] < 0.5
                      ? 'error--text'
                      : 'black--text text--darken-4'
                  "
                >
                  {{ item[column.value] | Percentage }}
                </span>
              </template>
            </tooltip>
            <div
              v-else-if="column.value === 'last_processed'"
              class="black--text text--darken-4 text-body-1"
            >
              <time-stamp :value="item[column.value]" />
            </div>
            <tooltip v-else-if="column.value === 'name'">
              <template #label-content>
                <span
                  class="black--text text--darken-4 text-body-1 data-feed-name"
                >
                  {{ item[column.value] }}
                </span>
              </template>
              <template #hover-content>
                <span class="black--text text--darken-4 text-body-1">
                  {{ item[column.value] }}
                </span>
              </template>
            </tooltip>
            <tooltip v-else>
              <template #label-content>
                <span class="black--text text--darken-4 text-body-1">
                  {{ item[column.value] | Numeric(false, true) }}
                </span>
              </template>
              <template #hover-content>
                <span class="black--text text--darken-4 text-body-1">
                  {{ item[column.value] | Numeric }}
                </span>
              </template>
            </tooltip>
          </td>
        </template>
      </hux-data-table>
    </v-row>
    <v-card
      v-else-if="!loading && hasDataFeeds == 0"
      class="empty-error-card mx-7"
    >
      <v-row class="data-feed-frame py-14">
        <empty-page
          v-if="!datafeedErrorState"
          type="lift-table-empty"
          :size="50"
        >
          <template #title>
            <div class="h2">No data feeds to show</div>
          </template>
          <template #subtitle>
            <div class="body-2">
              Data feeds will appear here once they have been properly ingested
              and stored in the correct data warehouse location.
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
            <div class="h2">
              {{ selectedDataSource.name }} data feed table is currently
              unavailable
            </div>
          </template>
          <template #subtitle>
            <div class="body-2">
              Our team is working hard to fix it. Please be patient and try
              again soon!
            </div>
          </template>
        </empty-page>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Status from "@/components/common/Status.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import EmptyPage from "@/components/common/EmptyPage.vue"

export default {
  name: "DataSourceListing",

  components: {
    Breadcrumb,
    PageHeader,
    HuxDataTable,
    Status,
    Tooltip,
    TimeStamp,
    EmptyPage,
  },

  data() {
    return {
      columns: [
        {
          text: "Data feed",
          value: "name",
          width: "170",
        },
        {
          text: "Status",
          value: "status",
          width: "84",
        },
        {
          text: "Records received",
          value: "records_received",
          width: "125",
        },
        {
          text: "Records processed",
          value: "records_processed",
          width: "132",
        },
        {
          text: "% of records processed",
          value: "records_processed_percentage",
          width: "150",
        },
        {
          text: "30 day avg",
          value: "thirty_days_avg",
          width: "100",
          hoverTooltip:
            "The value indicates the average % of records processed in the past 30 days",
        },
        {
          text: "Last processed",
          value: "last_processed",
          width: "120",
        },
      ],
      loading: true,
      datafeedErrorState: false,
    }
  },

  computed: {
    ...mapGetters({
      dataSource: "dataSources/single",
      dataFeeds: "dataSources/dataFeeds",
    }),

    dataSourceId() {
      return this.$route.params.id
    },

    selectedDataSource() {
      return this.dataSource(this.dataSourceId)
    },

    dataSourceDataFeeds() {
      return this.selectedDataSource ? this.dataFeeds(this.dataSourceId) : null
    },

    hasDataFeeds() {
      return this.dataSourceDataFeeds ? this.dataSourceDataFeeds.length : 0
    },

    breadcrumbItems() {
      return [
        {
          text: "Data Sources",
          disabled: false,
          href: this.$router.resolve({ name: "DataSources" }).href,
          icon: "data-source",
        },
        {
          text: this.selectedDataSource.name,
          logo: this.selectedDataSource.type,
          disabled: true,
        },
      ]
    },
  },

  async mounted() {
    this.loading = true
    try {
      if (!this.selectedDataSource) {
        await this.getDataSource(this.dataSourceId)
      }
      await this.getDataFeeds({
        id: this.selectedDataSource.id,
        type: this.selectedDataSource.type,
      })
    } catch (error) {
      this.datafeedErrorState = true
    } finally {
      this.loading = false
    }
  },

  methods: {
    ...mapActions({
      getDataFeeds: "dataSources/getDataFeeds",
      getDataSource: "dataSources/getDataSource",
    }),
  },
}
</script>
<style lang="scss" scoped>
.background-base {
  background: var(--v-black-darken4) !important;
}
.datasource-datafeeds-table {
  margin-top: 1px;
  ::v-deep .hux-data-table {
    table {
      .data-feed-name {
        @extend .text-ellipsis;
        max-width: 25ch;
      }
      .v-data-table-header {
        tr:first-child {
          th {
            padding-left: 42px;
          }
        }
      }
      tr {
        td {
          height: 60px;
        }
      }
      tbody {
        tr {
          td {
            padding-left: 42px;
          }
        }
        tr:last-child {
          td {
            border-bottom: 1px solid var(--v-black-lighten3) !important;
          }
        }
      }
    }
  }
}
.empty-error-card {
  height: 280px;
  border: 1px solid var(--v-black-lighten2);
  border-radius: 12px;
  margin-top: 72px;
}
.data-feed-frame {
  background-image: url("../../assets/images/no-lift-chart-frame.png");
  background-position: center;
}
</style>
