<template>
  <div :class="!loading && hasDataFeeds == 0 ? 'blackdarken-4' : 'white'">
    <page-header>
      <template #left>
        <breadcrumb :items="breadcrumbItems" />
      </template>
      <template #right>
        <v-btn
          v-if="getAccess('data_source', 'update_list_of_data_sources')"
          icon
          data-e2e="filesTableFilter"
          @click.native="isFilterToggled = !isFilterToggled"
        >
          <icon
            type="filter"
            :size="27"
            :color="isFilterToggled ? 'primary' : 'black'"
            :variant="isFilterToggled ? 'lighten6' : 'darken4'"
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
      <div
        class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100"
        data-e2e="data-files-wrapper"
      >
        <v-row
          v-if="!loading && hasDataFeeds"
          class="datasource-datafeeds-details-table"
        >
          <hux-data-table
            :columns="getCols"
            :data-items="dataSourceDataFeedsDetails"
            view-height="calc(100vh - 150px)"
            sort-column="last_processed_start"
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
                      class="text-body-1 ml-n6 black--text"
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
                            color="black"
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
                          {{ item[header.value] }}
                        </span>
                      </template>
                      <template #hover-content>
                        <span class="black--text text--darken-4 text-body-1">
                          {{ item[header.value] }}
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
                  <div
                    v-else-if="
                      ['run_duration', 'sub_status'].includes(header.value)
                    "
                    class="black--text text--darken-4 text-body-1"
                  >
                    {{ item[header.value] ? item[header.value] : "-" }}
                  </div>
                  <tooltip
                    v-else-if="header.value === 'records_processed_percentage'"
                  >
                    <template #label-content>
                      <span
                        class="text-body-1"
                        :class="
                          header.value === 'records_processed_percentage' &&
                          item[header.value]['flag_indicator']
                            ? 'error--text'
                            : 'black--text text--darken-4'
                        "
                      >
                        {{ item[header.value]["value"] | Percentage }}
                      </span>
                    </template>
                    <template #hover-content>
                      <span
                        class="text-body-1"
                        :class="
                          header.value === 'records_processed_percentage' &&
                          item[header.value]['flag_indicator']
                            ? 'error--text'
                            : 'black--text text--darken-4'
                        "
                      >
                        {{ item[header.value]["value"] | Percentage }}
                      </span>
                    </template>
                  </tooltip>
                  <tooltip
                    v-else-if="header.value === 'last_processed_start'"
                    class="black--text text--darken-4 text-body-1"
                  >
                    <template #label-content>
                      <span class="text-body-1 data-feed-name">
                        {{ formatDateToLocal(item[header.value]) }}
                      </span>
                    </template>

                    <template slot="hover-content">
                      <div>
                        <div class="neroBlack--text text-body-2 mb-2">
                          Last Processed:
                        </div>
                        <div class="d-flex align-center mb-1">
                          <span class="neroBlack--text text-body-2">
                            Started:
                          </span>
                        </div>
                        <div class="neroBlack--text text-body-2 mb-2">
                          {{ formatDateToLocal(item["last_processed_start"]) }}
                        </div>
                        <div class="d-flex align-center mb-1">
                          <span class="neroBlack--text text-body-2">
                            Ended:
                          </span>
                        </div>
                        <div class="neroBlack--text text-body-2">
                          {{
                            item["last_processed_end"]
                              ? formatDateToLocal(item["last_processed_end"])
                              : "Running"
                          }}
                        </div>
                      </div>
                    </template>
                  </tooltip>
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
                      <tooltip v-if="column.value === 'status'">
                        <template #label-content>
                          <span
                            data-e2e="filesStatusTooltip"
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
                          </span>
                        </template>
                        <template #hover-content>
                          <span class="text-body-1 black--text text--darken-4">
                            {{ getTooltip(item.status, item.sub_status) }}
                          </span>
                        </template>
                      </tooltip>
                      <tooltip v-else-if="column.value === 'sub_status'">
                        <template #label-content>
                          <span class="black--text text--darken-4 text-body-1">
                            {{ item[column.value] ? item[column.value] : "-" }}
                          </span>
                        </template>
                        <template #hover-content>
                          <span class="text-body-1 black--text text--darken-4">
                            {{ getTooltip(item.status, item.sub_status) }}
                          </span>
                        </template>
                      </tooltip>
                      <tooltip
                        v-else-if="
                          column.value === 'records_processed_percentage'
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
                      <tooltip
                        v-else-if="column.value === 'last_processed_start'"
                        class="black--text text--darken-4 text-body-1"
                      >
                        <template #label-content>
                          <span class="text-body-1 data-feed-name">
                            {{ formatDateToLocal(item[column.value]) }}
                          </span>
                        </template>

                        <template slot="hover-content">
                          <div>
                            <div class="neroBlack--text text-body-2 mb-2">
                              Last Processed:
                            </div>
                            <div class="d-flex align-center mb-1">
                              <span class="neroBlack--text text-body-2">
                                Started:
                              </span>
                            </div>
                            <div class="neroBlack--text text-body-2 mb-2">
                              {{
                                formatDateToLocal(item["last_processed_start"])
                              }}
                            </div>
                            <div class="d-flex align-center mb-1">
                              <span class="neroBlack--text text-body-2">
                                Ended:
                              </span>
                            </div>
                            <div class="neroBlack--text text-body-2">
                              {{
                                item["last_processed_end"]
                                  ? formatDateToLocal(
                                      item["last_processed_end"]
                                    )
                                  : "Running"
                              }}
                            </div>
                          </div>
                        </template>
                      </tooltip>
                      <tooltip v-else-if="column.value === 'run_duration'">
                        <template #label-content>
                          <span class="black--text text--darken-4 text-body-1">
                            {{ item[column.value] ? item[column.value] : "-" }}
                          </span>
                        </template>
                        <template #hover-content>
                          <span class="text-body-1 black--text text--darken-4">
                            {{ "HH:MM:SS" }}
                          </span>
                        </template>
                      </tooltip>
                      <tooltip v-else-if="column.value === 'name'">
                        <template #label-content>
                          <span class="text-body-1 data-feed-name">
                            {{ item["filename"] }}
                          </span>
                        </template>
                        <template #hover-content>
                          <span class="black--text text--darken-4 text-body-1">
                            {{ item["filename"] }}
                            <br />
                            {{ item["unique_id"] }}
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
          <v-row class="data-feed-frame my-1 py-16">
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
                  {{ dataSourceFeedName }} data feed table is currently
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
        <data-feeds-table-filter
          v-if="getAccess('data_source', 'update_list_of_data_sources')"
          v-model="isFilterToggled"
          @onSectionAction="applyFilter"
        />
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
import { getAccess } from "../../utils"

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
      numFiltersSelected: 1,
      api_params: {
        start_date: null,
        end_date: null,
        status: [],
        type: null,
        name: null,
      },
      selected_time: "All time",
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
          width: "200",
        },
        {
          text: "Status",
          value: "status",
          width: "121",
        },
        {
          text: "Sub-status",
          value: "sub_status",
          width: "140",
        },
        {
          text: "Records received",
          value: "records_received",
          width: "170",
        },
        {
          text: "Records processed",
          value: "records_processed",
          width: "170",
        },
        {
          text: "% of records processed",
          value: "records_processed_percentage",
          width: "200",
        },
        {
          text: "Run duration",
          value: "run_duration",
          width: "135",
        },
        {
          text: `Last processed start time (${this.selected_time})`,
          value: "last_processed_start",
          width: "260",
        },
      ]
    },

    tooltipText() {
      return {
        Success: {
          Complete: "File processing complete and all jobs are success",
        },
        Canceled: {
          Canceled: "Ingestion job is canceled",
          ["Waiting / All chunks failed"]:
            "File processing complete / waiting and at least one job is canceled",
          ["Partial success"]:
            "File processing complete / waiting and at least one job is canceled with at least one record in LTD",
          ["Partial success - in progress"]:
            "File processing / job is in progress and at least one job is canceled with at least one record in LTD",
        },
        Failed: {
          ["In progress"]:
            "File processing / job is in progress and at least one job is failed",
          ["Partial success - in progress"]:
            "File processing / job is in progress and at least one job is failed with at least one record in LTD",
          ["Partial success"]:
            "File processing complete / waiting and at least one job is failed with at least one record in LTD",
          ["Waiting / All chunks failed"]:
            "File processing complete / waiting and at least one job is failed",
          Failed: "File processing failed at ingestion job",
        },
        Running: {
          ["In progress"]: "File processing / job is in progress",
          ["Partial success - in progress"]:
            "File processing started, at least one record in LTD and file processing / job is in progress",
          Waiting: "File processing startedand no active job running",
          ["Partial success - waiting"]:
            "File processing started, at least one record in LTD and no active job running",
        },
      }
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
          text: this.selectedDataSource?.name,
          disabled: false,
          href: this.$router.resolve({ name: "DataSourceListing" }).href,
          logo: this.selectedDataSource?.type,
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
      this.setDefaultData()
      if (!this.selectedDataSource) {
        this.selectedDataSource = await this.getDataSource(this.dataSourceId)
        this.api_params.type = this.selectedDataSource.type
      }
      await this.getDataFeedDetails(this.api_params)
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
    getTooltip(status, sub_status) {
      return this.tooltipText[status] && this.tooltipText[status][sub_status]
        ? this.tooltipText[status][sub_status]
        : "No hover data found for current status and sub-status"
    },
    formatDate(name, len) {
      return len ? `${formatDate(name)} (${len})` : `${formatDate(name)}`
    },

    async applyFilter(obj) {
      if (obj.selectedToday && obj.selectedYesterday) {
        const today = new Date()
        const yesterday = new Date(
          today.getFullYear(),
          today.getMonth(),
          today.getDate() - 1
        )
        this.api_params.start_date = this.$options.filters.Date(
          yesterday,
          "YYYY-MM-DD"
        )
        this.api_params.end_date = this.$options.filters.Date(
          today,
          "YYYY-MM-DD"
        )
      } else if (obj.selectedToday) {
        const today = new Date()
        this.api_params.start_date = this.$options.filters.Date(
          today,
          "YYYY-MM-DD"
        )
        this.api_params.end_date = this.$options.filters.Date(
          today,
          "YYYY-MM-DD"
        )
      } else if (obj.selectedYesterday) {
        const today = new Date()
        const yesterday = new Date(
          today.getFullYear(),
          today.getMonth(),
          today.getDate() - 1
        )
        this.api_params.start_date = this.$options.filters.Date(
          yesterday,
          "YYYY-MM-DD"
        )
        this.api_params.end_date = this.$options.filters.Date(
          yesterday,
          "YYYY-MM-DD"
        )
      }
      if (obj.selectedTimeType == "All time") {
        this.api_params.start_date = null
        this.api_params.end_date = null
      } else if (obj.selectedTimeType == "Last month") {
        let today_date = new Date()
        let getStartDate = new Date(
          today_date.getFullYear(),
          today_date.getMonth() - 2,
          today_date.getDate()
        )
        let getEndDate = new Date(
          today_date.getFullYear(),
          today_date.getMonth() - 1,
          today_date.getDate()
        )
        this.api_params.start_date = this.$options.filters.Date(
          getStartDate,
          "YYYY-MM-DD"
        )
        this.api_params.end_date = this.$options.filters.Date(
          getEndDate,
          "YYYY-MM-DD"
        )
      } else if (obj.selectedTimeType == "Last week") {
        let today_date = new Date()
        let getStartDate = new Date(
          today_date.getFullYear(),
          today_date.getMonth(),
          today_date.getDate() - 14
        )
        let getEndDate = new Date(
          today_date.getFullYear(),
          today_date.getMonth(),
          today_date.getDate() - 7
        )
        this.api_params.start_date = this.$options.filters.Date(
          getStartDate,
          "YYYY-MM-DD"
        )
        this.api_params.end_date = this.$options.filters.Date(
          getEndDate,
          "YYYY-MM-DD"
        )
      }

      if (obj.selectedStatus) {
        this.api_params.status = obj.selectedStatus
      }

      this.loading = true
      await this.getDataFeedDetails(this.api_params)
      if (obj.filterLength) {
        this.numFiltersSelected = obj.filterLength
      }
      if (obj.selectedToday && obj.selectedYesterday) {
        this.selected_time = "Today , Yesterday"
      } else if (obj.selectedToday) {
        this.selected_time = "Today"
      } else if (obj.selectedYesterday) {
        this.selected_time = "Yesterday"
      } else if (obj.selectedTimeType) {
        this.selected_time = obj.selectedTimeType
      }
      this.loading = false
    },

    setDefaultData() {
      // let today_date = new Date()
      // let getStartDate = new Date(
      //   today_date.getFullYear(),
      //   today_date.getMonth(),
      //   today_date.getDate()
      // )
      // let getEndDate = new Date(
      //   today_date.getFullYear(),
      //   today_date.getMonth(),
      //   today_date.getDate()
      // )
      // this.api_params.start_date = this.$options.filters.Date(
      //   getStartDate,
      //   "YYYY-MM-DD"
      // )
      // this.api_params.end_date = this.$options.filters.Date(
      //   getEndDate,
      //   "YYYY-MM-DD"
      // )
      this.api_params.type = this.selectedDataSource?.type
      this.api_params.name = this.dataSourceFeedName
    },

    formatDateToLocal: formatDateToLocal,
    getAccess: getAccess,
  },
}
</script>
<style lang="scss" scoped>
.datasource-datafeeds-details-table {
  margin-top: 1px;
  .hux-data-table {
    ::v-deep table {
      width: 1675px !important;
      min-width: 100% !important;
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

          .mdi-checkbox-marked-circle,
          .mdi-checkbox-blank-circle {
            background: var(--v-primary-lighten2) !important;
          }
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
