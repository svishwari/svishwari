<template>
  <div class="white">
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
          <td v-for="column in columns" :key="column.value">
            <div
              v-if="column.value === 'status'"
              class="black--text text--darken-4 text-h6"
            >
              <status
                :status="item[column.value]"
                :show-label="true"
                class="data-feed-status d-flex"
                :icon-size="15"
              />
            </div>
            <div
              v-else-if="
                column.value === 'records_processed_percentage' ||
                column.value === 'thirty_days_avg'
              "
              class="text-h6"
              :class="
                column.value === 'records_processed_percentage' &&
                item[column.value] < 0.5
                  ? 'error--text'
                  : 'black--text text--darken-4'
              "
            >
              {{ item[column.value] | Percentage }}
            </div>
            <div
              v-else-if="column.value === 'last_processed'"
              class="black--text text--darken-4 text-h6"
            >
              <time-stamp :value="item[column.value]" />
            </div>
            <tooltip v-else-if="column.value === 'name'">
              <template #label-content>
                <span class="black--text text--darken-4 text-h6 data-feed-name">
                  {{ item[column.value] }}
                </span>
              </template>
              <template #hover-content>
                <span class="black--text text--darken-4 text-h6">
                  {{ item[column.value] }}
                </span>
              </template>
            </tooltip>
            <div v-else class="black--text text--darken-4 text-h6">
              {{ item[column.value].toLocaleString() | Empty }}
            </div>
          </td>
        </template>
      </hux-data-table>
    </v-row>

    <empty-page v-if="!loading && !hasDataFeeds">
      <template #icon> mdi-alert-circle-outline </template>
      <template #title> Oops! There’s nothing here yet </template>
      <template #subtitle>
        Our team is still working hard processing your datafeeds. <br />
        Please be patient in the meantime!
      </template>
    </empty-page>
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
        },
        {
          text: "Last processed",
          value: "last_processed",
          width: "120",
        },
      ],
      loading: true,
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
      return this.dataSourceDataFeeds.length
    },

    breadcrumbItems() {
      return [
        {
          text: "Connections",
          disabled: false,
          href: this.$router.resolve({ name: "Connections" }).href,
          icon: "connections",
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
    if (!this.selectedDataSource) {
      await this.getDataSource(this.dataSourceId)
    }
    await this.getDataFeeds({
      id: this.selectedDataSource.id,
      type: this.selectedDataSource.type,
    })
    this.loading = false
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
.datasource-datafeeds-table {
  margin-top: 1px;
  ::v-deep .hux-data-table {
    table {
      .data-feed-name {
        @extend .text-ellipsis;
        max-width: 25ch;
      }
      .data-feed-status {
        span {
          span {
            font-size: 12px;
          }
        }
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
</style>
