<template>
  <div class="notification-wrap">
    <page-header :header-height-changes="'py-3'">
      <template slot="left">
        <breadcrumb :items="breadcrumbItems" />
      </template>
      <template #right>
        <icon
          type="filter"
          :size="22"
          class="cursor-pointer"
          color="black-darken4"
          @click.native="toggleFilterDrawer()"
        />
      </template>
    </page-header>
    <page-header class="top-bar mb-3" :header-height="71">
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
    <div
      class="d-flex flex-nowrap align-stretch flex-grow-1 flex-shrink-0 mw-100"
    >
      <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100">
        <v-progress-linear :active="loading" :indeterminate="loading" />
        <v-row
          v-if="notificationData.length > 0 && !loading"
          class="pb-7 pl-3 white"
        >
          <hux-data-table
            :columns="columnDefs"
            :data-items="notificationData"
            sort-column="created"
            sort-desc
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
                  <a @click="toggleDrawer(item[header.value])"
                    >{{ item[header.value] }}
                  </a>
                </div>

                <div v-if="header.value == 'category'">
                  {{ item[header.value] }}
                </div>

                <div v-if="header.value == 'notification_type'" class="d-flex">
                  <icon
                    :type="
                      item['notification_type'] === 'Success'
                        ? 'success_new'
                        : item['notification_type']
                    "
                    :size="18"
                    :color="getIconColor(item['notification_type'])"
                    :variant="getVariantColor(item['notification_type'])"
                    class="d-block mr-1"
                  />
                  {{ item["notification_type"] }}
                </div>

                <tooltip v-if="header.value == 'description'" position-top>
                  <template #label-content>
                    <span>{{ item[header.value] }}</span>
                  </template>
                  <template #hover-content>
                    <div class="text--body-1 pb-2">Description</div>
                    {{ item[header.value] }}
                  </template>
                </tooltip>

                <div v-if="header.value == 'created'">
                  <time-stamp :value="item['created']" />
                </div>
              </td>
            </template>
          </hux-data-table>
        </v-row>
        <v-row
          v-if="notificationData.length == 0 && !loading"
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
              >
                Clear filters
              </huxButton>
            </template>
          </empty-page>
        </v-row>
        <v-row
          v-if="
            notificationData.length > 0 &&
            notificationData.length <= 0 &&
            !loading
          "
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
        <v-divider v-if="enableLazyLoad" class="hr-divider"></v-divider>
        <v-progress-linear v-if="enableLazyLoad" active indeterminate />
        <observer
          v-if="notifications.length"
          @intersect="intersected"
        ></observer>
      </div>
      <div class="ml-auto mt-n3">
        <alert-filter-drawer
          v-model="isFilterToggled"
          :users="getNotificationUsers"
          @onSectionAction="alertfunction"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxDataTable from "../../components/common/dataTable/HuxDataTable.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Observer from "@/components/common/Observer"
import Icon from "@/components/common/Icon"
import AlertFilterDrawer from "./AlertFilter"
import AlertDrawer from "./Drawer/AlertDrawer"
import EmptyPage from "@/components/common/EmptyPage"
import Error from "@/components/common/screens/Error"

export default {
  name: "AlertsAndNotifications",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    HuxDataTable,
    TimeStamp,
    Tooltip,
    Observer,
    Icon,
    AlertFilterDrawer,
    AlertDrawer,
    EmptyPage,
    Error,
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
          width: "260",
        },
        {
          text: "Category",
          value: "category",
          width: "180px",
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
          value: "created",
          width: "220px",
        },
      ],
      sortColumn: "created",
      sortDesc: true,
      loading: false,
      enableLazyLoad: false,
      lastBatch: 0,
      batchDetails: {},
      isFilterToggled: false,
      notificationId: null,
    }
  },
  computed: {
    ...mapGetters({
      notifications: "notifications/list",
      totalNotifications: "notifications/total",
      getUsers: "notifications/userList",
    }),

    notificationData() {
      let sortedNotificaitonList = this.notifications
      return sortedNotificaitonList.sort((a, b) => a.id - b.id)
    },
    getNotificationUsers() {
      let sortedUsers = this.getUsers
      return sortedUsers.sort(function (a, b) {
        var textA = a["display_name"].toUpperCase()
        var textB = b["display_name"].toUpperCase()
        return textA < textB ? -1 : textA > textB ? 1 : 0
      })
    },
  },

  async mounted() {
    this.loading = true
    await this.getUserData()
    try {
      this.setDefaultData()
      await this.fetchNotificationsByBatch()
      this.calculateLastBatch()
    } finally {
      this.loading = false
      this.enableLazyLoad = true
      if (this.notifications.length === 0) {
        this.enableLazyLoad = false
      }
    }
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
    async toggleDrawer(notificationId) {
      this.notificationId = notificationId
      await this.getNotificationByID(notificationId)
      this.alertDrawer = !this.alertDrawer
    },
    intersected() {
      if (this.batchDetails.batch_number <= this.lastBatch) {
        this.batchDetails.isLazyLoad = true
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
    getIconColor(value) {
      if (value) {
        return value === "Success"
          ? "success"
          : value === "Critical"
          ? "error"
          : "primary"
      }
    },
    getVariantColor(value) {
      if (value) {
        return value === "Informational" ? "lighten6" : "base"
      }
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
      this.isFilterToggled = false
      try {
        let today_date = new Date()
        let getEndDate = new Date(
          today_date.getFullYear(),
          today_date.getMonth(),
          today_date.getDate()
        )
        this.batchDetails.batch_size = 25
        this.batchDetails.batch_number = 1
        if (data.selctedAlertType.length !== 0) {
          this.batchDetails.notification_types =
            data.selctedAlertType.toString()
        } else {
          delete this.batchDetails.notification_types
        }
        if (data.selctedCategory.length !== 0) {
          this.batchDetails.category = data.selctedCategory.toString()
        } else {
          delete this.batchDetails.category
        }
        if (data.selctedUsers.length !== 0) {
          this.batchDetails.users = data.selctedUsers.toString()
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
        this.batchDetails.isLazyLoad = false
      } finally {
        this.isFilterToggled = false
        this.loading = false
        this.enableLazyLoad = true
        if (this.notifications.length === 0) {
          this.enableLazyLoad = false
        }
      }
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
  background: white !important;
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
</style>
