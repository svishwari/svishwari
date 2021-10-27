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
        />
      </template>
    </page-header>
    <page-header class="top-bar mb-3" :header-height="71">
      <template #left>
        <v-icon medium color="black lighten-3">mdi-magnify</v-icon>
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
    <v-row v-if="!loading" class="pb-7 pl-3 white">
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
            class="col-overflow"
            :style="{ width: header.width, left: 0 }"
          >
            <div v-if="header.value == 'id'">
              <a @click="toggleProfilesDrawer(item[header.value])"
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
    <alert-drawer v-model="alertDrawer" :alert-id="alertId" />
    <v-divider v-if="enableLazyLoad" class="hr-devider"></v-divider>
    <v-progress-linear v-if="enableLazyLoad" active indeterminate />
    <observer v-if="notifications.length" @intersect="intersected"></observer>
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
import AlertDrawer from "./Drawer/AlertDrawer"
import Icon from "@/components/common/Icon"

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
    AlertDrawer,
    Icon,
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
          text: "Brief Description",
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
      batchDetails: {
        batchSize: 25,
        batchNumber: 1,
        isLazyLoad: false,
      },
      alertId: null,
    }
  },
  computed: {
    ...mapGetters({
      notifications: "notifications/list",
      totalNotifications: "notifications/total",
    }),

    notificationData() {
      let sortedNotificaitonList = this.notifications
      return sortedNotificaitonList.sort((a, b) => a.id - b.id)
    },
  },

  async mounted() {
    this.loading = true
    await this.fetchNotificationsByBatch()
    this.calculateLastBatch()
    this.loading = false
    this.enableLazyLoad = true
    if (this.notifications.length === 0) {
      this.enableLazyLoad = false
    }
  },
  methods: {
    ...mapActions({
      getAllNotifications: "notifications/getAll",
      getNotificationByID: "notifications/getById",
    }),
    goBack() {
      this.$router.go(-1)
    },
    async toggleProfilesDrawer(alertid) {
      this.alertId = alertid
      await this.getNotificationByID(alertid)
      this.alertDrawer = !this.alertDrawer
    },
    intersected() {
      if (this.batchDetails.batchNumber <= this.lastBatch) {
        this.batchDetails.isLazyLoad = true
        this.fetchNotificationsByBatch()
      } else {
        this.enableLazyLoad = false
      }
    },
    async fetchNotificationsByBatch() {
      await this.getAllNotifications(this.batchDetails)
      this.batchDetails.batchNumber++
    },
    calculateLastBatch() {
      this.lastBatch = Math.ceil(
        this.totalNotifications / this.batchDetails.batchSize
      )
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
.hr-devider {
  margin-top: -27px !important;
}
</style>
