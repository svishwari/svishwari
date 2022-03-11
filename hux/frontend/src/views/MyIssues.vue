<template>
  <div class="notification-wrap">
    <page-header :header-height-changes="'py-3'">
      <template slot="left">
        <breadcrumb :items="breadcrumbItems" data-e2e="issues-header" />
      </template>
      <template #right>
        <v-btn icon>
          <icon type="setting-issues" :size="27" color="black" />
        </v-btn>
      </template>
    </page-header>
    <div
      class="d-flex flex-nowrap align-stretch flex-grow-1 flex-shrink-0 mw-100"
    >
      <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100">
        <page-header class="top-bar mb-3" :header-height="71">
          <template #right>
            <huxButton
              variant="primary base"
              icon="keyboard-return"
              is-custom-icon
              class="ma-2 text-button no-shadow mr-0"
              size="large"
              is-tile
              :height="'40'"
              :icon-size="18"
              icon-color="white"
              icon-variant="base"
              data-e2e="issues-return"
              @click="goBack()"
            >
              Return to previous page
            </huxButton>
          </template>
        </page-header>
        <v-progress-linear :active="loading" :indeterminate="loading" />
        <div data-e2e="issue-table-wrapper">
          <v-row v-if="numIssues > 0 && !loading" class="pb-7 pl-3 white">
            <hux-data-table
              :columns="columnDefs"
              :data-items="getTickets"
              sort-column="create_time"
              sort-desc
              class="big-table"
              data-e2e="issues-table"
            >
              <template #row-item="{ item }">
                <td
                  v-for="header in columnDefs"
                  :key="header.value"
                  :class="{
                    'fixed-column': header.fixed,
                    'v-data-table__divider': header.fixed,
                    'primary--text': header.fixed,
                  }"
                  class="col-overflow text-body-1"
                  :style="{ width: header.width, left: 0 }"
                >
                  <div v-if="header.value == 'key'" data-e2e="issues-key">
                    {{ item[header.value] | Empty("-") }}
                  </div>

                  <div
                    v-if="header.value == 'status'"
                    class="d-flex align-center"
                    data-e2e="issues-status"
                  >
                    <span
                      class="circle"
                      :style="{ background: getColorStatus(item['status']) }"
                    >
                    </span>
                    <span>
                      {{ item["status"] | Empty("-") }}
                    </span>
                  </div>

                  <div
                    v-if="header.value == 'summary'"
                    position-top
                    data-e2e="issues-summary"
                  >
                    {{ item[header.value] | Empty("-") }}
                  </div>

                  <div
                    v-if="header.value == 'create_time'"
                    data-e2e="issues-time"
                  >
                    {{ item["create_time"] | Date("MM/DD/YYYY h:mm A") }}
                  </div>
                </td>
              </template>
            </hux-data-table>
          </v-row>
          <v-row
            v-else-if="numIssues == 0 && !loading && !handleErrorStateIssues"
            class="background-empty"
          >
            <empty-page type="no-alerts" :size="50">
              <template #title>
                <div class="text-h2 black-text">No issues yet</div></template
              >
              <template #subtitle>
                <div class="body-2 black-text">
                  Currently there are no issues available.<br />
                  Check back later.
                </div>
              </template>
            </empty-page>
          </v-row>
          <v-row
            v-else-if="handleErrorStateIssues && !loading"
            class="d-flex justify-center align-center error-screen"
          >
            <error
              icon-type="error-on-screens"
              :icon-size="50"
              title="Issues are currently unavailable"
              subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
            >
            </error>
          </v-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Icon from "@/components/common/Icon"
import EmptyPage from "@/components/common/EmptyPage"
import Error from "@/components/common/screens/Error"

export default {
  name: "MyIssues",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    HuxDataTable,
    Icon,
    EmptyPage,
    Error,
  },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "My issues",
          disabled: true,
          icon: "my-issues",
        },
      ],
      columnDefs: [
        {
          text: "Issue ID",
          value: "key",
          width: "250px",
          hoverTooltip:
            "This is the ID which is used to uniquely identify any issue",
          tooltipWidth: "150px",
        },
        {
          text: "Status",
          value: "status",
          width: "250px",
        },
        {
          text: "Summary",
          value: "summary",
          width: "auto",
        },
        {
          text: "Created",
          value: "create_time",
          width: "350px",
        },
      ],
      sortColumn: "create_time",
      sortDesc: true,
      loading: false,
      handleErrorStateIssues: false,
    }
  },
  computed: {
    ...mapGetters({
      getTickets: "users/getAllTickets",
    }),
    numIssues() {
      return this.getTickets && this.getTickets.length
        ? this.getTickets.length
        : 0
    },
  },

  async mounted() {
    this.loading = true
    try {
      await this.fetchtAllTickets()
    } catch (error) {
      this.handleErrorStateIssues = true
    } finally {
      this.loading = false
    }
  },
  methods: {
    ...mapActions({
      fetchtAllTickets: "users/getTickets",
    }),
    goBack() {
      this.$router.go(-1)
    },
    getColorStatus(value) {
      let color = "#1e1e1e"
      switch (value) {
        case "Done":
          color = "#43b02a"
          break
        case "In progress":
          color = "#00a3e0"
          break
        case "In review":
          color = "#a0dcff"
          break
        default:
          color = "#fec62e"
          break
      }
      return color
    },
  },
}
</script>
<style lang="scss" scoped>
.notification-wrap {
  background: white;
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  .top-bar {
    margin-top: 1px;
    .v-icon--disabled {
      color: var(--v-black-lighten3) !important;
      font-size: 24px;
    }
    .text--refresh {
      margin-right: 10px;
    }
  }
  .hux-data-table {
    margin-top: 1px;
    table {
      td {
        font-size: 14px;
        height: 63px;
      }
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
}

.col-overflow {
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

::v-deep
  .theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > tbody
  > tr:hover:not(.v-data-table__expanded__content):not(.v-data-table__empty-wrapper) {
  background: white !important;
}
::v-deep .v-data-table > .v-data-table__wrapper > table > td {
  padding-left: 32px !important;
}
.background-empty {
  height: 70vh !important;
  background-image: url("../assets/images/no-alert-frame.png");
  background-position: center;
}

::v-deep .empty-page {
  max-height: 0 !important;
  min-height: 100% !important;
  min-width: 100% !important;
}
.circle {
  border-radius: 50%;
  width: 18px;
  height: 18px;
  margin-right: 6px;
}
</style>
