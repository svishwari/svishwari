<template>
  <div class="white">
    <page-header>
      <template #left>
        <breadcrumb :items="breadcrumbItems" />
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <v-row v-if="!loading" class="datasource-datafeeds-table">
      <hux-data-table sort-desc :columns="columns" :data-items="data_feeds">
        <template #row-item="{ item }">
          <td v-for="column in columns" :key="column.value">
            <div
              v-if="column.value === 'status'"
              class="neroBlack--text text-h6"
            >
              <status
                :status="item[column.value]"
                :show-label="true"
                class="d-flex"
                :icon-size="15"
              />
            </div>
            <div
              v-else-if="
                column.value === 'records_processed_percentage' ||
                column.value === 'day_avg_30'
              "
              class="neroBlack--text text-h6"
            >
              {{ item[column.value] | Percentage }}
            </div>
            <div
              v-else-if="column.value === 'last_processed'"
              class="neroBlack--text text-h6"
            >
              <time-stamp :value="item[column.value]" />
            </div>
            <div
              v-else-if="column.value === 'name'"
              class="neroBlack--text text-h6"
            >
              {{ item[column.value] }}
            </div>
            <div v-else class="neroBlack--text text-h6">
              {{ item[column.value].toLocaleString() | Empty }}
            </div>
          </td>
        </template>
      </hux-data-table>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Status from "@/components/common/Status.vue"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"

export default {
  name: "DataSourceListing",

  components: { Breadcrumb, PageHeader, HuxDataTable, Status, TimeStamp },

  data() {
    return {
      columns: [
        {
          text: "Data feed",
          value: "name",
          width: "180",
        },
        {
          text: "Status",
          value: "status",
          width: "120",
        },
        {
          text: "Records received",
          value: "records_received",
          width: "120",
        },
        {
          text: "Records processed",
          value: "records_processed",
          width: "120",
        },
        {
          text: "% of records processed",
          value: "records_processed_percentage",
          width: "140",
        },
        {
          text: "30 day avg",
          value: "day_avg_30",
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
      data_feeds: "dataSources/data_feeds",
    }),

    selectedDataSource() {
      return this.dataSource(this.$route.params.id)
    },

    breadcrumbItems() {
      const items = [
        {
          text: "Connections",
          disabled: false,
          href: this.$router.resolve({ name: "Connections" }).href,
          icon: "connections",
        },
      ]
      if (this.selectedDataSource) {
        items.push({
          text: this.selectedDataSource.name,
          disabled: true,
          logo: this.selectedDataSource.type,
        })
      }
      return items
    },
  },

  async mounted() {
    this.loading = true
    if (!this.dataSource(this.$route.params.id)) {
      this.getAllDataSources()
    }
    await this.getDataFeeds(this.$route.params.id)
    this.loading = false
  },

  methods: {
    ...mapActions({
      getDataFeeds: "dataSources/getDataFeeds",
      getAllDataSources: "dataSources/getAll",
    }),
  },
}
</script>
<style lang="scss" scoped>
.datasource-datafeeds-table {
  margin-top: 1px;
  ::v-deep .hux-data-table {
    table {
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
            border-bottom: 1px solid var(--v-lightGrey-base) !important;
          }
        }
      }
    }
  }
}
</style>
