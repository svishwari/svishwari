<template>
  <div class="notification-wrap">
    <page-header :header-height-changes="'py-3'">
      <template slot="left">
        <breadcrumb :items="breadcrumbItems" />
      </template>
      <template #right>
        <v-btn
          data-e2e="alertFilterToggle"
          icon
          @click.native="isFilterToggled = !isFilterToggled"
        >
          <icon
            type="filter"
            :size="27"
            :color="isFilterToggled ? 'primary' : 'black'"
            :variant="isFilterToggled ? 'lighten6' : 'darken4'"
          />
          <v-badge
            v-if="finalFilterApplied > 0"
            :content="finalFilterApplied"
            color="white"
            offset-x="6"
            offset-y="4"
            light
            bottom
            overlap
            bordered
          />
        </v-btn>
        <v-btn
          data-e2e="alertConfigureToggle"
          icon
          class="ml-5"
          @click.native="toggleAlertConfigure()"
        >
          <icon type="setting-gear" :size="27" color="black" />
        </v-btn>
      </template>
    </page-header>
    <div
      class="d-flex flex-nowrap align-stretch flex-grow-1 flex-shrink-0 mw-100"
    >
      <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100">
        <page-header v-if="!isEmptyError" class="top-bar" :header-height="70">
          <template #left>
            <v-btn disabled icon color="black">
              <icon type="search" :size="20" color="black" variant="lighten3" />
            </v-btn>
          </template>

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
              data-e2e="notification-return"
              @click="goBack()"
            >
              Return to previous page
            </huxButton>
          </template>
        </page-header>
        <v-progress-linear :active="loading" :indeterminate="loading" />
        <v-row
          v-if="notificationData.length > 0 && !loading"
          class="pb-7 pl-3 white"
        >
          <hux-lazy-data-table
            :columns="columnDefs"
            :data-items="notificationData"
            sort-column="create_time"
            sort-desc
            class="big-table"
            :enable-lazy-load="enableLazyLoad"
            data-e2e="alert-table"
            view-height="calc(100vh - 230px)"
            @bottomScrollEvent="intersected"
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
                <div v-if="header.value == 'id'">
                  <a
                    data-e2e="alert-id-click"
                    @click="toggleDrawer(item[header.value])"
                    >{{ item[header.value] | Shorten | Empty("-") }}
                  </a>
                </div>

                <div v-if="header.value == 'category'">
                  {{ formatText(item[header.value]) | Empty("-") }}
                </div>

                <div v-if="header.value == 'notification_type'" class="d-flex">
                  <status
                    :status="formatText(item['notification_type'])"
                    :show-label="false"
                    class="d-flex"
                    :icon-size="item['notification_type'] === 'success' ? 21 : 18"
                  />
                  {{ formatText(item["notification_type"]) | Empty("-") }}
                </div>

                <tooltip v-if="header.value == 'description'" max-width="47%">
                  <template #label-content>
                    <span>{{ item[header.value] }}</span>
                  </template>
                  <template #hover-content>
                    {{ item[header.value] | Empty("-") }}
                  </template>
                </tooltip>

                <div v-if="header.value == 'create_time'">
                  <time-stamp :value="item['create_time']" />
                </div>
              </td>
            </template>
          </hux-lazy-data-table>
        </v-row>
        <v-row
          v-if="notificationData.length == 0 && !isEmptyError && !loading"
          class="background-empty"
        >
          <empty-page type="no-alerts" :size="50">
            <template #title>
              <div class="title-no-notification">No alerts yet</div></template
            >
            <template #subtitle>
              <div class="des-no-notification">
                Currently there are no alerts available.<br />
                Check back later or change your filters.
              </div>
            </template>
            <template #button>
              <huxButton
                button-text="Clear filters"
                variant="primary base"
                size="large"
                class="ma-2 font-weight-regular text-button"
                is-tile
                :height="'40'"
                @click="clearFilters()"
              >
                Clear filters
              </huxButton>
            </template>
          </empty-page>
        </v-row>
        <v-row
          v-if="notificationData.length == 0 && isEmptyError && !loading"
          class="d-flex justify-center align-center"
        >
          <error
            icon-type="error-on-screens"
            :icon-size="50"
            title="Alerts &amp; notifications is currently unavailable"
            subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
          >
          </error>
        </v-row>
        <alert-drawer v-model="alertDrawer" :notification-id="notificationId" />
      </div>
      <div class="ml-auto">
        <alert-filter-drawer
          ref="filters"
          v-model="isFilterToggled"
          :users="getNotificationUsers"
          @onSectionAction="alertfunction"
          @selected-filters="totalFiltersSelected"
        />
        <alert-configure-drawer
          v-model="isAlertsToggled"
          @onDrawerClose="onConfigClose"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import { formatRequestText, formatText } from "@/utils"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxLazyDataTable from "@/components/common/dataTable/HuxLazyDataTable.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon"
import AlertFilterDrawer from "./AlertFilter"
import AlertDrawer from "./Drawer/AlertDrawer"
import EmptyPage from "@/components/common/EmptyPage"
import Error from "@/components/common/screens/Error"
import AlertConfigureDrawer from "./Drawer/AlertConfigure.vue"
import Status from "@/components/common/Status.vue"

export default {
  name: "AlertsAndNotifications",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    HuxLazyDataTable,
    TimeStamp,
    Tooltip,
    Icon,
    AlertFilterDrawer,
    AlertDrawer,
    EmptyPage,
    Error,
    Status,
    AlertConfigureDrawer,
  },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Alerts & Notifications",
          disabled: true,
          icon: "bell",
        },
      ],
      alertDrawer: false,
      categoryItems: [
        { name: "Orchestration" },
        { name: "Decisioning" },
        { name: "Data management" },
      ],
      alertTypeItems: [
        { name: "Success", modelIcon: "Success" },
        { name: "Critical", modelIcon: "Critical" },
        { name: "Feedback", modelIcon: "Feedback" },
        { name: "Informational", modelIcon: "Informational" },
      ],
      columnDefs: [
        {
          text: "Alert ID",
          value: "id",
          width: "150",
        },
        {
          text: "Category",
          value: "category",
          width: "200px",
        },
        {
          text: "Type",
          value: "notification_type",
          width: "180px",
        },
        {
          text: "Brief description",
          value: "description",
          width: "auto",
        },
        {
          text: "Time",
          value: "create_time",
          width: "200px",
        },
      ],
      sortColumn: "create_time",
      sortDesc: true,
      loading: false,
      enableLazyLoad: false,
      lastBatch: 0,
      batchDetails: {},
      isFilterToggled: false,
      isAlertsToggled: false,
      isEmptyError: false,
      notificationId: null,
      numFiltersSelected: 0,
      finalFilterApplied: 1,
      getAllUsers: [],
    }
  },
  computed: {
    ...mapGetters({
      notifications: "notifications/list",
      totalNotifications: "notifications/total",
      getUserEmail: "users/getEmailAddress",
      getUserAlerts: "users/getUserAlerts",
      getUsers: "notifications/userList",
    }),

    notificationData() {
      let sortedNotificaitonList = this.notifications
      return sortedNotificaitonList.sort((a, b) => a.id - b.id)
    },
    getNotificationUsers() {
      let sortedUsers = this.getUsers
      return sortedUsers.sort(function (a, b) {
        var textA = a?.toUpperCase()
        var textB = b?.toUpperCase()
        return textA < textB ? -1 : textA > textB ? 1 : 0
      })
    },
  },

  async mounted() {
    this.loading = true
    try {
      this.setDefaultData()
      await this.getUserData()
      await this.fetchNotificationsByBatch()
      this.calculateLastBatch()
    } catch (error) {
      this.isEmptyError = true
    } finally {
      this.loading = false
    }
  },

  beforeDestroy() {
    delete this.batchDetails.notification_types
    delete this.batchDetails.category
    delete this.batchDetails.users
    this.setDefaultData()
    this.calculateLastBatch()
  },
  methods: {
    ...mapActions({
      getAllNotifications: "notifications/getAll",
      getNotificationByID: "notifications/getById",
      getUsersNoti: "notifications/getAllUsers",
    }),
    goBack() {
      this.$router.go(-1)
    },
    totalFiltersSelected(value) {
      this.numFiltersSelected = value
    },
    async toggleDrawer(notificationId) {
      this.notificationId = notificationId
      await this.getNotificationByID(notificationId)
      this.alertDrawer = !this.alertDrawer
    },
    intersected() {
      if (this.batchDetails.batch_number <= this.lastBatch) {
        this.batchDetails.isLazyLoad = true
        this.enableLazyLoad = true
        this.fetchNotificationsByBatch()
      } else {
        this.enableLazyLoad = false
      }
    },
    async fetchNotificationsByBatch() {
      await this.getAllNotifications(this.batchDetails)
      this.batchDetails.batch_number++
    },
    async getUserData() {
      await this.getUsersNoti()
    },
    calculateLastBatch() {
      this.lastBatch = Math.ceil(
        this.totalNotifications / this.batchDetails.batch_size
      )
    },
    toggleFilterDrawer() {
      this.isFilterToggled = !this.isFilterToggled
    },
    toggleAlertDrawer() {
      this.isAlertsToggled = !this.isAlertsToggled
    },
    setDefaultData() {
      let today_date = new Date()
      let getStartDate = new Date(
        today_date.getFullYear(),
        today_date.getMonth(),
        today_date.getDate() - 7
      )
      let getEndDate = new Date(
        today_date.getFullYear(),
        today_date.getMonth(),
        today_date.getDate()
      )
      this.batchDetails.start_date = this.$options.filters.Date(
        getStartDate,
        "YYYY-MM-DD"
      )
      this.batchDetails.end_date = this.$options.filters.Date(
        getEndDate,
        "YYYY-MM-DD"
      )
      this.batchDetails.batch_size = 25
      this.batchDetails.batch_number = 1
      this.batchDetails.isLazyLoad = false
    },
    async alertfunction(data) {
      this.finalFilterApplied = data.filterApplied
      this.isFilterToggled = true
      this.enableLazyLoad = false
      this.isEmptyError = false
      this.loading = true
      try {
        let today_date = new Date()
        let getEndDate = new Date(
          today_date.getFullYear(),
          today_date.getMonth(),
          today_date.getDate()
        )
        this.batchDetails.batch_size = 25
        this.batchDetails.batch_number = 1
        this.batchDetails.isLazyLoad = false
        if (data.selectedAlertType.length !== 0) {
          this.batchDetails.notification_types = formatRequestText(
            data.selectedAlertType.toString()
          )
        } else {
          delete this.batchDetails.notification_types
        }
        if (data.selectedCategory.length !== 0) {
          this.batchDetails.category = formatRequestText(
            data.selectedCategory.toString()
          )
        } else {
          delete this.batchDetails.category
        }
        if (data.selectedUsers.length !== 0) {
          this.batchDetails.users = data.selectedUsers.toString()
        } else {
          delete this.batchDetails.users
        }

        if (data.getTime === null || "") {
          this.batchDetails.start_date = ""
          this.batchDetails.end_date = ""
        } else {
          this.batchDetails.start_date = data.getTime
          this.batchDetails.end_date = this.$options.filters.Date(
            getEndDate,
            "YYYY-MM-DD"
          )
        }
        await this.fetchNotificationsByBatch()
        this.calculateLastBatch()
        this.loading = false
      } finally {
        this.isFilterToggled = true
        this.loading = false
      }
    },
    clearFilters() {
      this.$refs.filters.clearAndReload()
    },
    toggleAlertConfigure() {
      this.getAllUsers = this.getUsers
      this.isAlertsToggled = !this.isAlertsToggled
    },
    async onConfigClose() {
      await this.getUsersNoti()
      this.getAllUsers = this.getUsers
    },
    formatText: formatText,
  },
}
</script>
<style lang="scss" scoped>
.notification-wrap {
  background: var(--v-white-base);
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
      tr {
        td {
          font-size: 14px;
          height: 63px;
        }
      }
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
  .icon-border {
    cursor: default !important;
  }
}
.radio-div {
  margin-top: -11px !important;
}

.backGround-header-dropdown {
  background-color: var(--v-primary-lighten2) !important;
}
::v-deep .hux-dropdown {
  .v-btn__content {
    color: var(--v-darkBlue-base) !important;
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
  background: var(--v-white-base) !important;
}
::v-deep
  .theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > thead
  > tr:last-child
  > th {
  padding-left: 32px !important;
}
::v-deep
  .theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > tbody
  > tr:not(:last-child)
  > td:not(.v-data-table__mobile-row),
.theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > tbody
  > tr:not(:last-child)
  > th:not(.v-data-table__mobile-row) {
  padding-left: 32px !important;
}
::v-deep .v-data-table > .v-data-table__wrapper > table > tbody > tr > td,
.v-data-table > .v-data-table__wrapper > table > thead > tr > td,
.v-data-table > .v-data-table__wrapper > table > tfoot > tr > td {
  padding-left: 32px !important;
}
.hr-divider {
  margin-top: -27px !important;
}
.background-empty {
  height: 70vh !important;
  background-image: url("../../assets/images/no-alert-frame.png");
  background-position: center;
}

//to overwrite the classes

.title-no-notification {
  font-size: 24px !important;
  line-height: 34px !important;
  font-weight: 300 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}
.des-no-notification {
  font-size: 14px !important;
  line-height: 16px !important;
  font-weight: 400 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}
::v-deep .empty-page {
  max-height: 0 !important;
  min-height: 100% !important;
  min-width: 100% !important;
}
</style>
