<template>
  <div>
    <hux-page max-width="100%" class="home-page">
      <template #header>
        <hux-page-header
          :title="`Welcome back, ${fullName}!`"
          class="header-section"
          :header-height="110"
          :icon="demo_icon"
          :show-demo-header="showDemoHeader"
          data-e2e="welcome-banner"
        >
          <template #left>
            <p class="text-subtitle-1 font-weight-regular mb-0">
              Hux is here to help you make better, faster decisions to improve
              your customer experiences.
              <a
                class="text-decoration-none"
                href="https://resources.deloitte.com/sites/consulting/offerings/customer-marketing/advertising-marketing-commerce/Pages/Hux-by-Deloitte-Digital.aspx"
                target="_blank"
              >
                Learn More &gt;
              </a>
            </p>
          </template>
        </hux-page-header>
      </template>

      <v-row
        class="chart-card"
        :class="totalCustomers.length == 0 ? 'margin-2px-top-3px-bottom' : ''"
      >
        <v-col>
          <v-card
            class="rounded-lg box-shadow-5"
            :height="totalCustomers.length == 0 ? 280 : 367"
          >
            <v-card-title
              v-if="totalCustomers.length != 0 && !loadingTotalCustomers"
              class="pa-6"
            >
              <h3 class="text-h3 black--text text--darken-4">
                Total Hux IDs
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
                class="pt-5"
                :size="50"
              >
                <template #title>
                  <div>No data to show</div>
                </template>
                <template #subtitle>
                  <div>
                    Total customer chart will appear here once Customer data is
                    available.
                  </div>
                </template>
              </empty-page>
              <empty-page
                v-else
                type="error-on-screens"
                class="pt-5"
                :size="50"
              >
                <template #title>
                  <div>Total customer chart is currently unavailable</div>
                </template>
                <template #subtitle>
                  <div>
                    Our team is working hard to fix it. Please be patient and
                    try again soon!
                  </div>
                </template>
              </empty-page>
            </v-row>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="latest-alert-main">
        <v-col>
          <v-card
            class="rounded-lg box-shadow-5"
            data-e2e="latest-notifications"
            :height="numNotifications == 0 ? 280 : auto"
          >
            <v-card-title
              v-if="numNotifications != 0 && !loadingNotifications"
              class="pa-6"
            >
              <h3 class="text-h3 black--text text--darken-4">Latest alerts</h3>
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
              class="notifications-table px-6"
              sort-column="create_time"
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
                      {{ formatText(item[header.value]) | Empty("-") }}
                      <template #tooltip>
                        {{ formatText(item[header.value]) }}
                      </template>
                    </hux-tooltip>
                  </template>

                  <template v-if="header.value == 'notification_type'">
                    <!-- TODO: HUS-1305 update icon -->
                    <hux-status
                      :status="formatText(item['notification_type'])"
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

                  <template v-if="header.value == 'create_time'">
                    <hux-time-stamp :value="item['create_time']" />
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
                class="pt-5"
                :size="50"
              >
                <template #title>
                  <div>No data to show</div>
                </template>
                <template #subtitle>
                  <div>
                    Latest alerts table will appear here once you start getting
                    alerts.
                  </div>
                </template>
              </empty-page>
              <empty-page
                v-else
                class="pt-5"
                type="error-on-screens"
                :size="50"
              >
                <template #title>
                  <div>Latest alerts table is currently unavailable</div>
                </template>
                <template #subtitle>
                  <div>
                    Our team is working hard to fix it. Please be patient and
                    try again soon!
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
    <v-card flat class="d-flex help-section pa-7">
      <span class="d-flex align-center text-body-1">
        <icon type="kx" :size="36" class="mr-2" /> Need some help or guidance?
        &nbsp;
        <a
          href="https://resources.deloitte.com/:f:/s/GTMMarketingServices/EtcSxrQDnWVBqco8JSGIP5QBvhIO-gKp7OdlHHAEvBscOw?e=to9cdJ"
          target="_blank"
          class="text-decoration-none"
        >
          <span class="primary--text cursor-pointer">
            Click here to access demo scripts, videos, FAQs, and more.
            <icon type="new_tab_link" size="10" color="primary" class="mb-2" />
          </span>
        </a>
      </span>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import { formatText } from "@/utils"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxPage from "@/components/Page.vue"
import HuxPageHeader from "@/components/PageHeader.vue"
import HuxTimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import HuxTooltip from "@/components/common/Tooltip.vue"
import HuxStatus from "@/components/common/Status.vue"
import HuxTotalCustomerChart from "@/components/common/TotalCustomerChart/TotalCustomerChart.vue"
import AlertDrawer from "./AlertsAndNotifications/Drawer/AlertDrawer.vue"
import EmptyPage from "@/components/common/EmptyPage"
import Icon from "../components/common/Icon.vue"

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
    Icon,
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
          value: "create_time",
          width: "180px",
        },
      ],
      alertDrawer: false,
      notificationId: null,
      totalCustomersChartErrorState: false,
      notificationsTableErrorState: false,
      showDemoHeader: false,
      demo_icon: "",
    }
  },

  computed: {
    ...mapGetters({
      firstName: "users/getFirstname",
      lastName: "users/getLastName",
      totalCustomers: "customers/totalCustomers",
      notifications: "notifications/latest5",
      demoConfiguration: "users/getDemoConfiguration",
    }),

    fullName() {
      return `${this.firstName} ${this.lastName}`
    },

    numNotifications() {
      return this.notifications ? this.notifications.length : 0
    },
  },
  beforeCreate() {
    this.$store.commit("notifications/RESET_ALL")
  },
  mounted() {
    this.demoConfigChangeTracker()
    this.loadTotalCustomers()
    this.loadNotifications()
  },

  methods: {
    ...mapActions({
      getTotalCustomers: "customers/getTotalCustomers",
      getAllNotifications: "notifications/getAll",
      getNotificationByID: "notifications/getById",
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

    async openAlertDrawer(notificationId) {
      this.notificationId = notificationId
      await this.getNotificationByID(notificationId)
      this.alertDrawer = !this.alertDrawer
    },
    getCurrentConfiguration() {
      this.showDemoHeader = true
      this.demo_icon = this.demoConfiguration.industry.toLowerCase()
    },
    demoConfigChangeTracker() {
      this.$root.$on("update-config-settings", () =>
        this.getCurrentConfiguration()
      )
      if (this.demoConfiguration?.demo_mode) {
        this.getCurrentConfiguration()
      } else {
        this.showDemoHeader = false
        this.demo_icon = ""
      }
    },
    formatText: formatText,
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
      &:first-child {
        border-top-left-radius: 12px !important;
      }
      &:last-child {
        border-top-right-radius: 12px !important;
      }
    }
    td {
      padding: 18px 28px !important;
      height: 60px !important;
    }
  }
}

.total-customers-chart-frame {
  background-image: url("../assets/images/no-customers-chart-frame.png");
  background-position: bottom;
  background-size: 93% 87%;
}

.notifications-table-frame {
  background-image: url("../assets/images/no-lift-chart-frame.png");
  background-position: bottom;
  background-size: 93% 87%;
}

.margin-2px-top-3px-bottom {
  margin-top: 2px;
  margin-bottom: 3px;
}
.help-section {
  background: var(--v-primary-lighten2);
  height: 96px;
  width: 100%;
}
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--v-white-base);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--v-black-lighten3);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--v-black-lighten3);
}
.header-section {
  height: 110px;
  position: fixed;
  width: 100%;
  z-index: 6 !important;
}
.chart-card {
  margin-top: 94px;
}
::v-deep .v-data-table-header__icon {
  margin-left: 4px !important;
}
::v-deep.home-page {
  min-height: calc(100vh - 166px);
  .container {
    padding-top: 45px !important;
    height: 100% !important;
    overflow: hidden !important;
  }
}
</style>
