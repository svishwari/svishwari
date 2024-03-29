<template>
  <div :class="!loading && hasDataFeeds == 0 ? 'blackdarken-4' : 'white'">
    <page-header v-if="selectedDataSource">
      <template #left>
        <breadcrumb :items="breadcrumbItems" />
      </template>
    </page-header>

    <v-progress-linear :active="loading" :indeterminate="loading" />

    <v-row
      v-if="!loading && hasDataFeeds"
      class="datasource-datafeeds-table"
      data-e2e="datasource-datafeeds-table"
    >
      <hux-lazy-data-table
        sort-desc
        :columns="columns"
        :data-items="dataSourceDataFeeds"
        :enable-lazy-load="enableLazyLoad"
        view-height="calc(100vh - 230px)"
        @bottomScrollEvent="intersected"
      >
        <template #row-item="{ item }">
          <td v-for="column in columns" :key="column.value" class="text-body-1">
            <div
              v-if="column.value === 'status'"
              class="black--text text--darken-4 text-body-1"
            >
              <status
                :status="item[column.value]"
                :show-label="true"
                class="data-feed-status d-flex"
                :icon-size="item[column.value] == 'Failed' ? 15 : 18"
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
                    item[column.value]['flag_indicator']
                      ? 'error--text'
                      : 'black--text text--darken-4'
                  "
                >
                  {{ item[column.value]["value"] | Percentage }}
                </span>
              </template>
              <template #hover-content>
                <span
                  class="text-body-1"
                  :class="
                    column.value === 'records_processed_percentage' &&
                    item[column.value]['flag_indicator']
                      ? 'error--text'
                      : 'black--text text--darken-4'
                  "
                >
                  {{ item[column.value]["value"] | Percentage }}
                </span>
              </template>
            </tooltip>

            <!-- <time-stamp :value="item[column.value]" /> -->
            <tooltip
              v-else-if="column.value === 'last_processed'"
              class="black--text text--darken-4 text-body-1"
            >
              <template #label-content>
                {{ formatDateToLocal(item[column.value]) }}
              </template>
              <template #hover-content>
                {{ formatDateToLocal(item[column.value]) }}
              </template>
            </tooltip>

            <tooltip v-else-if="column.value === 'name'">
              <template #label-content>
                <span
                  class="
                    primary--text
                    cursor-pointer
                    text-body-1
                    data-feed-name
                  "
                  @click="getDataFeedDetailsFunc(item)"
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
      </hux-lazy-data-table>
    </v-row>
    <v-card
      v-else-if="!loading && hasDataFeeds == 0"
      class="empty-error-card mx-7"
      data-e2e="datasource-datafeeds-table"
    >
      <v-row class="data-feed-frame py-13">
        <empty-page
          v-if="!datafeedErrorState"
          type="lift-table-empty"
          :size="50"
          class="pt-6"
        >
          <template #title>
            <div class="h2 mb-4">No data feeds to show</div>
          </template>
          <template #subtitle>
            <div class="body-2 pb-4">
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
import EmptyPage from "@/components/common/EmptyPage.vue"
import { formatDateToLocal } from "@/utils"
import HuxLazyDataTable from "@/components/common/dataTable/HuxLazyDataTable.vue"

export default {
  name: "DataSourceListing",

  components: {
    Breadcrumb,
    PageHeader,
    Status,
    Tooltip,
    EmptyPage,
    HuxLazyDataTable,
  },

  data() {
    return {
      columns: [
        {
          text: "Data feed",
          value: "name",
          width: "120",
        },
        {
          text: "Status",
          value: "status",
          width: "100",
        },
        {
          text: "Records received",
          value: "records_received",
          width: "110",
        },
        {
          text: "Records processed",
          value: "records_processed",
          width: "100",
        },
        {
          text: "% of records processed",
          value: "records_processed_percentage",
          width: "110",
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
      enableLazyLoad: false,
      lastBatch: 0,
      batchDetails: {
        batch_size: 25,
        batch_number: 1,
      },
    }
  },

  computed: {
    ...mapGetters({
      dataSource: "dataSources/single",
      dataFeeds: "dataSources/dataFeeds",
      getTotalrecords: "dataSources/getTotalrecords",
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
      this.batchDetails.id = this.selectedDataSource.id
      this.batchDetails.type = this.selectedDataSource.type
      await this.fetchDataSourceByBatch()
      await this.calculateLastBatch()
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
    intersected() {
      if (this.batchDetails.batch_number <= this.lastBatch) {
        this.batchDetails.isLazyLoad = true
        this.enableLazyLoad = true
        this.fetchDataSourceByBatch()
      } else {
        this.batchDetails.isLazyLoad = false
        this.enableLazyLoad = false
      }
    },
    async fetchDataSourceByBatch() {
      await this.getDataFeeds(this.batchDetails)
      this.batchDetails.batch_number++
    },
    getDataFeedDetailsFunc(item) {
      this.$router.push({
        name: "DataSourceFeedsListing",
        params: {
          id: this.selectedDataSource.id,
          name: item.name,
        },
      })
    },
    calculateLastBatch() {
      this.lastBatch = Math.ceil(
        this.getTotalrecords / this.batchDetails.batch_size
      )
    },
    formatDateToLocal: formatDateToLocal,
  },
}
</script>
<style lang="scss" scoped>
.datasource-datafeeds-table {
  margin-top: 1px;

  ::v-deep .hux-data-table {
    table {
      table-layout: initial;

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
          padding-left: 42px !important;
          height: 60px;
          white-space: nowrap;
          text-overflow: ellipsis !important;

          &:last-child {
            padding-right: 30px !important;
          }
        }
      }

      tbody {
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
  background-size: 90% 60%;
}
</style>
