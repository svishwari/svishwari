<template>
  <div :class="!loading && hasDataFeeds == 0 ? 'blackdarken-4' : 'white'">
    <page-header v-if="selectedDataSource">
      <template #left>
        <breadcrumb :items="breadcrumbItems" />
      </template>
      <template #right>
        <v-btn icon @click.native="isFilterToggled = !isFilterToggled">
          <icon
            type="filter"
            :size="27"
            :color="numFiltersSelected > 0 ? 'primary' : 'black'"
            :variant="numFiltersSelected > 0 ? 'lighten6' : 'darken4'"
          />
          <v-badge
            v-if="numFiltersSelected > 0"
            :content="numFiltersSelected"
            color="white"
            offset-x="6"
            offset-y="4"
            light
            bottom
            overlap
            bordered
          />
        </v-btn>
      </template>
    </page-header>

    <v-progress-linear :active="loading" :indeterminate="loading" />

    <div
      class="d-flex flex-nowrap align-stretch flex-grow-1 flex-shrink-0 mw-100"
    >
      <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100">
        <v-row
          v-if="!loading && hasDataFeeds"
          class="datasource-datafeeds-details-table"
        >
          <hux-data-table
            :columns="getCols"
            :data-items="dataSourceDataFeedsDetails"
            view-height="calc(100vh - 150px)"
            sort-column="last_processed"
            sort-desc="true"
            nested
            data-e2e="data-feed-details-table"
            class="big-table"
          >
            <template #item-row="{ item, expandFunc, isExpanded }">
              <tr :class="{ 'expanded-row': isExpanded }">
                <td
                  v-for="header in getCols"
                  :key="header.value"
                  :class="{
                    'fixed-column': header.fixed,
                    'v-data-table__divider': header.fixed,
                    'primary--text': header.fixed,
                    'expanded-row': isExpanded,
                    'pl-3': header.value == 'audiences',
                  }"
                  :style="{ width: header.width }"
                >
                  <div v-if="header.value == 'name'" class="text-body-1 w-80">
                    <menu-cell
                      v-if="item.data_files && item.data_files.length > 0"
                      :value="
                        formatDate(item[header.value], item.data_files.length)
                      "
                      :data="item"
                      class="text-body-1 ml-n6"
                    >
                      <template #expand-icon>
                        <span
                          v-if="item.data_files && item.data_files.length > 0"
                          data-e2e="expand-date-group"
                          @click="expandFunc(!isExpanded)"
                        >
                          <icon
                            type="expand-arrow"
                            :size="14"
                            color="primary"
                            class="
                              cursor-pointer
                              mdi-chevron-right
                              mx-2
                              d-inline-block
                            "
                            :class="{ 'normal-icon': isExpanded }"
                          />
                        </span>
                      </template>
                    </menu-cell>
                    <tooltip v-else>
                      <template #label-content>
                        <span class="black--text text-body-1 data-feed-name">
                          {{ formatDate(item[header.value]) }}
                        </span>
                      </template>
                      <template #hover-content>
                        <span class="black--text text--darken-4 text-body-1">
                          {{ formatDate(item[header.value]) }}
                        </span>
                      </template>
                    </tooltip>
                  </div>
                  <div
                    v-else-if="header.value === 'status'"
                    class="black--text text--darken-4 text-body-1"
                  >
                    <status
                      :status="item[header.value]"
                      :show-label="true"
                      class="data-feed-status d-flex"
                      :icon-size="item[header.value] == 'Failed' ? '15' : '18'"
                    />
                  </div>
                  <tooltip
                    v-else-if="
                      header.value === 'records_processed_percentage' ||
                      header.value === 'thirty_days_avg'
                    "
                  >
                    <template #label-content>
                      <span
                        class="text-body-1"
                        :class="
                          header.value === 'records_processed_percentage' &&
                          item[header.value] < 0.5
                            ? 'error--text'
                            : 'black--text text--darken-4'
                        "
                      >
                        {{ item[header.value] | Percentage }}
                      </span>
                    </template>
                    <template #hover-content>
                      <span
                        class="text-body-1"
                        :class="
                          header.value === 'records_processed_percentage' &&
                          item[header.value] < 0.5
                            ? 'error--text'
                            : 'black--text text--darken-4'
                        "
                      >
                        {{ item[header.value] | Percentage }}
                      </span>
                    </template>
                  </tooltip>
                  <div
                    v-else-if="header.value === 'last_processed'"
                    class="black--text text--darken-4 text-body-1"
                  >
                    <!-- <time-stamp :value="item[header.value]" /> -->
                    {{ formatDateToLocal(item[header.value]) }}
                  </div>
                  <tooltip v-else>
                    <template #label-content>
                      <span class="black--text text--darken-4 text-body-1">
                        {{ item[header.value] | Numeric(false, true) }}
                      </span>
                    </template>
                    <template #hover-content>
                      <span class="black--text text--darken-4 text-body-1">
                        {{ item[header.value] | Numeric }}
                      </span>
                    </template>
                  </tooltip>
                </td>
              </tr>
            </template>
            <template #expanded-row="{ expandedHeaders, parentItem }">
              <td
                v-if="parentItem.data_files && parentItem.data_files.length > 0"
                :colspan="expandedHeaders.length"
                class="pa-0 child"
              >
                <hux-data-table
                  v-if="parentItem"
                  :columns="expandedHeaders"
                  :data-items="parentItem.data_files"
                  :show-header="false"
                  view-height="auto"
                  class="big-table"
                >
                  <template #row-item="{ item }">
                    <td
                      v-for="column in getCols"
                      :key="column.value"
                      class="text-body-1"
                      :style="{ width: column.width + 'px' }"
                    >
                      <div
                        v-if="column.value === 'status'"
                        class="black--text text--darken-4 text-body-1"
                      >
                        <status
                          :status="item[column.value]"
                          :show-label="true"
                          class="data-feed-status d-flex"
                          :icon-size="
                            item[column.value] == 'Failed' ? '15' : '18'
                          "
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
                        <!-- <time-stamp :value="item[column.value]" /> -->
                        {{ formatDateToLocal(item[column.value]) }}
                      </div>
                      <tooltip v-else-if="column.value === 'name'">
                        <template #label-content>
                          <span class="text-body-1 data-feed-name">
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
                  Data feeds will appear here once they have been properly
                  ingested and stored in the correct data warehouse location.
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
      <div class="ml-auto">
        <data-feeds-table-filter v-model="isFilterToggled" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import MenuCell from "@/components/common/huxTable/MenuCell.vue"
import Status from "@/components/common/Status.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import EmptyPage from "@/components/common/EmptyPage.vue"
import { formatDate, formatDateToLocal } from "@/utils"
import Icon from "@/components/common/Icon.vue"
import DataFeedsTableFilter from "./DataFeedsTableFilter.vue"

export default {
  name: "DataSourceFeedsListing",

  components: {
    Breadcrumb,
    PageHeader,
    HuxDataTable,
    MenuCell,
    Status,
    Tooltip,
    EmptyPage,
    Icon,
    DataFeedsTableFilter,
  },

  data() {
    return {
      loading: false,
      datafeedErrorState: false,
      isFilterToggled: false,
      numFiltersSelected: 0,
    }
  },

  computed: {
    ...mapGetters({
      dataSource: "dataSources/single",
      dataFeeds: "dataSources/dataFeeds",
      dataFeedDetails: "dataSources/dataFeedDetails",
    }),

    dataSourceId() {
      return this.$route.params.id
    },

    dataSourceFeedName() {
      return this.$route.params.name
    },

    selectedDataSource() {
      return this.dataSource(this.dataSourceId)
    },

    dataSourceDataFeedsDetails() {
      return this.dataFeedDetails
    },

    hasDataFeeds() {
      return this.dataSourceDataFeedsDetails
        ? this.dataSourceDataFeedsDetails.length
        : 0
    },

    getCols() {
      return [
        {
          text: `Files ${
            this.dataSourceDataFeedsDetails[0].data_files
              ? ""
              : `(${this.hasDataFeeds})`
          }`,
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
          width: "100",
        },
        {
          text: "30 day avg",
          value: "thirty_days_avg",
          width: "100",
          hoverTooltip:
            "The value indicates the average % of records processed in the past 30 days",
        },
        {
          text: "Last processed (Today)",
          value: "last_processed",
          width: "170",
        },
      ]
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
          disabled: false,
          href: this.$router.resolve({ name: "DataSourceListing" }).href,
          logo: this.selectedDataSource.type,
        },
        {
          text: this.dataSourceFeedName,
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
      await this.getDataFeedsDetails({
        type: this.selectedDataSource.type,
        name: this.dataSourceFeedName,
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
      getDataFeedDetails: "dataSources/getDataFeedsDetails",
    }),
    changeStatus(status) {
      switch (status) {
        case "Pending":
          return "Incomplete"

        case "Success":
          return "Complete"

        default:
          return "Failed"
      }
    },
    formatDate(name, len) {
      return len ? `${formatDate(name)} (${len})` : `${formatDate(name)}`
    },

    totalFiltersSelected(value) {
      this.numFiltersSelected = value
    },
    formatDateToLocal: formatDateToLocal,
  },
}
</script>
<style lang="scss" scoped>
.datasource-datafeeds-details-table {
  margin-top: 1px;
  .hux-data-table {
    ::v-deep table {
      .data-feed-name {
        @extend .text-ellipsis;
        max-width: 25ch;
      }
      .mdi-chevron-right {
        transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
      }
      .expanded-row {
        background-color: var(--v-primary-lighten2) !important;
      }
      .v-data-table-header {
        tr:first-child {
          th {
            padding-left: 42px;
          }
        }
      }
      tr {
        &:hover {
          background: var(--v-primary-lighten2) !important;
          box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25) !important;
        }
        height: 60px;
        td {
          font-size: 16px !important;
          line-height: 22px;
          color: var(--v-black-base);
          padding-left: 42px;
        }
      }
      .ellipsis {
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 21ch !important;
        display: inline-block;
        white-space: nowrap;
      }
      .max-26 {
        max-width: 26ch;
        width: 26ch;
      }
      .v-data-table__expanded__row {
        background: var(--v-primary-lighten2);
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
    .child {
      ::v-deep .theme--light {
        background: var(--v-primary-lighten1);
        .v-data-table__wrapper,
        .empty-table {
          box-shadow: inset 0px 10px 10px -4px var(--v-black-lighten3);
          border-bottom: thin solid rgba(0, 0, 0, 0.12);
        }
      }
      ::v-deep table {
        background: inherit;
        tbody {
          td {
            &:first-child {
              background: inherit;
            }
          }
        }
        .v-data-table__expanded__row {
          background: inherit !important;
        }
      }
      ::v-deep .child {
        .v-data-table__wrapper {
          box-shadow: none;
        }
        tbody {
          td {
            &:first-child {
              padding-left: 80px;
            }
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
.mdi-chevron-right {
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
  &.normal-icon {
    transform: rotate(90deg);
  }
}
</style>