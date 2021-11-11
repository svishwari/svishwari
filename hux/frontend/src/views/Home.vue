<template>
  <hux-page max-width="100%">
    <template #header>
      <hux-page-header
        :title="`Welcome back, ${fullName}!`"
        :header-height="110"
        data-e2e="welcome-banner"
      >
        <template #left>
          <p class="text-subtitle-1 font-weight-regular mb-0">
            Hux is here to help you make better, faster decisions to improve
            your customer experiences.
            <a
              class="text-decoration-none"
              href="https://consulting.deloitteresources.com/offerings/customer-marketing/advertising-marketing-commerce/Pages/hux_marketing.aspx"
              target="_blank"
            >
              Learn More &gt;
            </a>
          </p>
        </template>
      </hux-page-header>
    </template>

    <v-row>
      <v-col>
        <v-card
          class="rounded-lg box-shadow-5"
          :height="totalCustomers.length == 0 ? 280 : 367"
        >
          <v-card-title v-if="totalCustomers.length != 0" class="pa-6">
            <h3 class="text-h3 black--text text--darken-4">
              Total customers
              <span class="text-body-1 black--text text--lighten-4">
                (last 9 months)
              </span>
            </h3>
          </v-card-title>

          <v-progress-linear
            v-if="loadingTotalCustomers"
            :active="loadingTotalCustomers"
            :indeterminate="loadingTotalCustomers"
          />

          <hux-total-customer-chart
            v-if="!loadingTotalCustomers && totalCustomers.length != 0"
            :customers-data="totalCustomers"
            :months-duration="9"
            data-e2e="total-customers-chart"
          />

          <v-row
            v-if="!loadingTotalCustomers && totalCustomers.length == 0"
            class="total-customers-chart-frame py-14"
          >
            <empty-page
              v-if="!totalCustomersChartErrorState"
              type="model-features-empty"
              :size="50"
            >
              <template #title>
                <div class="title-no-notification">No data to show</div>
              </template>
              <template #subtitle>
                <div class="des-no-notification">
                  Total customer chart will appear here once Customer data is
                  available.
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
                <div class="title-no-notification">
                  Total customer chart is currently unavailable
                </div>
              </template>
              <template #subtitle>
                <div class="des-no-notification">
                  Our team is working hard to fix it. Please be patient and try
                  again soon!
                </div>
              </template>
            </empty-page>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card
          class="rounded-lg box-shadow-5"
          data-e2e="latest-notifications"
          :height="numNotifications == 0 ? 280 : auto"
        >
          <v-card-title v-if="numNotifications != 0" class="pa-6">
            <h3 class="text-h3 black--text text--darken-4">
              Latest alerts
              <span
                v-if="numNotifications"
                class="text-body-1 black--text text--lighten-4"
              >
                ({{ numNotifications }})
              </span>
            </h3>
          </v-card-title>

          <v-progress-linear
            v-if="loadingNotifications"
            :active="loadingNotifications"
            :indeterminate="loadingNotifications"
          />

          <hux-data-table
            v-if="!loadingNotifications && numNotifications != 0"
            :columns="tableColumns"
            :data-items="notifications"
            class="notifications-table"
            sort-column="created"
            sort-desc
          >
            <template #row-item="{ item }">
              <td
                v-for="header in tableColumns"
                :key="header.value"
                class="text-body-1 py-4 mw-100 text-truncate"
              >
                <template v-if="header.value == 'id'">
                  <a
                    href="javascript:void(0)"
                    class="text-body-1 text-decoration-none"
                    @click="openAlertDrawer(item[header.value])"
                  >
                    {{ item[header.value] | Shorten }}
                  </a>
                </template>

                <template v-if="header.value == 'category'">
                  <hux-tooltip>
                    {{ item[header.value] }}
                    <template #tooltip> {{ item[header.value] }} </template>
                  </hux-tooltip>
                </template>

                <template v-if="header.value == 'notification_type'">
                  <!-- TODO: HUS-1305 update icon -->
                  <hux-status
                    :status="item['notification_type']"
                    :show-label="true"
                    :icon-size="20"
                  />
                </template>

                <template v-if="header.value == 'description'">
                  <hux-tooltip>
                    {{ item[header.value] }}
                    <template #tooltip> {{ item[header.value] }} </template>
                  </hux-tooltip>
                </template>

                <template v-if="header.value == 'created'">
                  <hux-time-stamp :value="item['created']" />
                </template>
              </td>
            </template>
          </hux-data-table>

          <v-row
            v-if="!loadingNotifications && numNotifications == 0"
            class="notifications-table-frame py-14"
          >
            <empty-page
              v-if="!notificationsTableErrorState"
              type="lift-table-empty"
              :size="50"
            >
              <template #title>
                <div class="title-no-notification">No data to show</div>
              </template>
              <template #subtitle>
                <div class="des-no-notification">
                  Latest alerts table will appear here once you start getting
                  alerts.
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
                <div class="title-no-notification">
                  Latest alerts table is currently unavailable
                </div>
              </template>
              <template #subtitle>
                <div class="des-no-notification">
                  Our team is working hard to fix it. Please be patient and try
                  again soon!
                </div>
              </template>
            </empty-page>
          </v-row>

          <v-card-actions v-if="numNotifications != 0" class="pa-6">
            <router-link
              :to="{ name: 'AlertsAndNotifications' }"
              class="text-body-1 text-decoration-none"
              data-e2e="all-notifications-link"
            >
              View all alerts
            </router-link>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <alert-drawer v-model="alertDrawer" :notification-id="notificationId" />
  </hux-page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxPage from "@/components/Page.vue"
import HuxPageHeader from "@/components/PageHeader.vue"
import HuxTimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import HuxTooltip from "@/components/common/Tooltip.vue"
import HuxStatus from "@/components/common/Status.vue"
import HuxTotalCustomerChart from "@/components/common/TotalCustomerChart/TotalCustomerChart.vue"
import AlertDrawer from "./AlertsAndNotifications/Drawer/AlertDrawer.vue"
import EmptyPage from "@/components/common/EmptyPage"

export default {
  name: "Home",

  components: {
    HuxDataTable,
    HuxPage,
    HuxPageHeader,
    HuxTimeStamp,
    HuxTooltip,
    HuxStatus,
    HuxTotalCustomerChart,
    AlertDrawer,
    EmptyPage,
  },

  data() {
    return {
      loadingTotalCustomers: false,
      loadingNotifications: false,
      tableColumns: [
        {
          text: "Alert ID",
          value: "id",
          width: "110px",
        },
        {
          text: "Category",
          value: "category",
          width: "160px",
        },
        {
          text: "Type",
          value: "notification_type",
          width: "160px",
        },
        {
          text: "Description",
          value: "description",
          width: "auto",
        },
        {
          text: "Time",
          value: "created",
          width: "180px",
        },
      ],
      alertDrawer: false,
      notificationId: null,
      totalCustomersChartErrorState: false,
      notificationsTableErrorState: false,
    }
  },

  computed: {
    ...mapGetters({
      firstName: "users/getFirstname",
      lastName: "users/getLastName",
      totalCustomers: "customers/totalCustomers",
      notifications: "notifications/list",
    }),

    fullName() {
      return `${this.firstName} ${this.lastName}`
    },

    numNotifications() {
      return this.notifications ? this.notifications.length : 0
    },
  },

  mounted() {
    this.loadTotalCustomers()
    this.loadNotifications()
  },

  methods: {
    ...mapActions({
      getTotalCustomers: "customers/getTotalCustomers",
      getAllNotifications: "notifications/getAll",
    }),

    async loadTotalCustomers() {
      this.loadingTotalCustomers = true
      try {
        await this.getTotalCustomers()
      } catch (error) {
        this.totalCustomersChartErrorState = true
      }
      this.loadingTotalCustomers = false
    },

    async loadNotifications() {
      this.loadingNotifications = true
      try {
        await this.getAllNotifications({
          batchSize: 5,
          batchNumber: 1,
        })
      } catch (error) {
        this.notificationsTableErrorState = true
      }
      this.loadingNotifications = false
    },

    openAlertDrawer(id) {
      this.alertDrawer = true
      this.notificationId = id
    },
  },
}
</script>

<style lang="scss" scoped>
.notifications-table {
  ::v-deep table {
    th {
      background: var(--v-primary-lighten2) !important;
      padding: 0px 28px !important;
      height: 32px !important;
    }
    td {
      padding: 18px 28px !important;
      height: 60px !important;
    }
  }
}

.total-customers-chart-frame {
  background-image: url("../assets/images/no-customers-chart-frame.png");
  background-position: center;
}

.notifications-table-frame {
  background-image: url("../assets/images/no-lift-chart-frame.png");
  background-position: center;
}
</style>
